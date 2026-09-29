#!/usr/bin/env python3
"""Controlador determinístico do estado de aprendizagem do DEV_LEARNING."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


VALID_STATES = {
    "READY",
    "TEACHING",
    "WAITING_FOR_STUDENT",
    "REVIEWING",
    "NEEDS_CORRECTION",
    "PASSED",
    "COMPLETED",
}
FEEDBACK_PATTERN = re.compile(
    r"DEV_LEARNING_FEEDBACK\[(SYNTAX|LOGIC|CONCEPT|DESIGN|GOOD_PRACTICE)\]"
)


class LearningError(RuntimeError):
    """Erro de regra do fluxo de aprendizagem."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes", "sim"}:
        return True
    if normalized in {"false", "0", "no", "nao", "não"}:
        return False
    raise argparse.ArgumentTypeError("use true ou false")


class LearningStore:
    def __init__(self, root: Path | str | None = None) -> None:
        self.root = Path(root or Path(__file__).resolve().parents[1]).resolve()
        self.learning_dir = self.root / ".learning"
        self.progress_path = self.learning_dir / "progress.json"
        self.session_path = self.learning_dir / "session.md"
        self.history_path = self.learning_dir / "history.md"
        self.curriculum_path = self.root / "curriculum" / "java.json"
        self.curriculum = self._read_json(self.curriculum_path)
        self.lessons = self.curriculum.get("lessons", [])
        self.lesson_by_id = {lesson["id"]: lesson for lesson in self.lessons}
        self.module_by_id = {
            module["id"]: module for module in self.curriculum.get("modules", [])
        }
        self._validate_curriculum()

    @staticmethod
    def _read_json(path: Path) -> dict[str, Any]:
        if not path.is_file():
            raise LearningError(f"arquivo obrigatório ausente: {path}")
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise LearningError(f"JSON inválido em {path}: {error}") from error

    def _validate_curriculum(self) -> None:
        if self.curriculum.get("track") != "java" or not self.lessons:
            raise LearningError("currículo Java vazio ou inválido")
        if len(self.lesson_by_id) != len(self.lessons):
            raise LearningError("IDs de aula duplicados no currículo")

        seen: set[str] = set()
        modules = set(self.module_by_id)
        for lesson in self.lessons:
            required = {"id", "module", "title", "kind", "objective", "prerequisites"}
            missing = required.difference(lesson)
            if missing:
                raise LearningError(
                    f"aula {lesson.get('id', '?')} sem campos: {', '.join(sorted(missing))}"
                )
            if lesson["module"] not in modules:
                raise LearningError(f"módulo desconhecido em {lesson['id']}")
            for prerequisite in lesson["prerequisites"]:
                if prerequisite not in seen:
                    raise LearningError(
                        f"pré-requisito {prerequisite} deve existir antes de {lesson['id']}"
                    )
            seen.add(lesson["id"])

    def initialize(self) -> dict[str, Any]:
        if self.progress_path.exists():
            state = self.load_state()
            return {"initialized": False, "reason": "state-already-exists", "state": state}

        first = self.lessons[0]
        state = {
            "version": 1,
            "track": "java",
            "module": first["module"],
            "lesson": first["id"],
            "status": "READY",
            "exercise": None,
            "completedLessons": [],
            "requiredCheckpoint": None,
            "revision": None,
            "lastResult": None,
            "updatedAt": utc_now(),
        }
        self.learning_dir.mkdir(parents=True, exist_ok=True)
        self._write_state(state)
        self.history_path.write_text("# Histórico de aprendizagem\n", encoding="utf-8")
        self._append_history(state, "INITIALIZED", "trilha Java inicializada")
        self._write_session(
            content="trilha ainda não iniciada",
            exercise="nenhum",
            result="estado inicial criado",
            point=f"{first['title']} (`READY`)",
            next_action="continuar para apresentar o diagnóstico",
        )
        return {"initialized": True, "state": state}

    def load_state(self) -> dict[str, Any]:
        if not self.progress_path.exists():
            raise LearningError("estado ausente; execute `python3 scripts/learning.py init`")
        state = self._read_json(self.progress_path)
        self.validate_state(state)
        return state

    def validate_state(self, state: dict[str, Any] | None = None) -> None:
        state = state or self.load_state()
        required = {
            "version",
            "track",
            "module",
            "lesson",
            "status",
            "exercise",
            "completedLessons",
            "requiredCheckpoint",
            "revision",
            "lastResult",
            "updatedAt",
        }
        missing = required.difference(state)
        if missing:
            raise LearningError(f"estado sem campos: {', '.join(sorted(missing))}")
        if state["track"] != "java" or state["status"] not in VALID_STATES:
            raise LearningError("track ou status inválido")
        unknown = set(state["completedLessons"]).difference(self.lesson_by_id)
        if unknown:
            raise LearningError(f"aulas concluídas desconhecidas: {', '.join(sorted(unknown))}")
        if len(state["completedLessons"]) != len(set(state["completedLessons"])):
            raise LearningError("completedLessons contém duplicatas")

        completed = set(state["completedLessons"])
        for completed_id in completed:
            missing_prerequisites = set(
                self.lesson_by_id[completed_id]["prerequisites"]
            ).difference(completed)
            if missing_prerequisites:
                raise LearningError(
                    f"aula {completed_id} concluída sem pré-requisitos: "
                    f"{', '.join(sorted(missing_prerequisites))}"
                )

        lesson_id = state["lesson"]
        if lesson_id is None:
            if len(state["completedLessons"]) != len(self.lessons):
                raise LearningError("lesson nula antes da conclusão da trilha")
        else:
            lesson = self.lesson_by_id.get(lesson_id)
            if lesson is None or lesson["module"] != state["module"]:
                raise LearningError("lesson e module não correspondem ao currículo")
            if lesson_id in completed:
                raise LearningError("aula atual já consta como concluída")
            missing_prerequisites = set(lesson["prerequisites"]).difference(completed)
            if missing_prerequisites:
                raise LearningError(
                    f"aula atual sem pré-requisitos: {', '.join(sorted(missing_prerequisites))}"
                )
            expected = self._next_available(state["completedLessons"])
            legacy_git_in_progress = (
                expected
                and expected["id"] == "intellij-idea-foundations"
                and lesson_id == "git-github-foundations"
                and state["status"]
                in {"WAITING_FOR_STUDENT", "REVIEWING", "NEEDS_CORRECTION"}
                and state.get("exercise")
                and "initial-diagnostic" in completed
                and "intellij-idea-foundations" not in completed
            )
            if expected and expected["id"] != lesson_id and not legacy_git_in_progress:
                raise LearningError(
                    f"aula atual não é a próxima ação determinística: esperado={expected['id']}"
                )

        needs_exercise = state["status"] in {"WAITING_FOR_STUDENT", "REVIEWING"}
        if needs_exercise and not state["exercise"]:
            raise LearningError(f"estado {state['status']} exige exercício ativo")

    def current_lesson(self, state: dict[str, Any]) -> dict[str, Any] | None:
        lesson_id = state.get("lesson")
        return self.lesson_by_id.get(lesson_id) if lesson_id else None

    def lesson_directory(self, lesson: dict[str, Any]) -> str:
        """Retorna o diretório canônico que organiza os arquivos de uma aula."""
        if lesson not in self.lessons:
            raise LearningError(f"aula desconhecida: {lesson.get('id', '?')}")
        if lesson["kind"] == "diagnostic":
            return "lesson00_diagnostico_inicial"
        regular_lessons = [item for item in self.lessons if item["kind"] != "diagnostic"]
        position = regular_lessons.index(lesson) + 1
        directory_name = lesson.get(
            "directoryName", f"lesson{position:02d}_{lesson['id'].replace('-', '_')}"
        )
        return directory_name

    @staticmethod
    def concept_filename(lesson: dict[str, Any]) -> str:
        """Retorna o nome legível e estável do material conceitual da aula."""
        normalized = unicodedata.normalize("NFKD", lesson["title"])
        ascii_title = "".join(
            character for character in normalized if not unicodedata.combining(character)
        )
        words = re.findall(r"[A-Za-z0-9]+", ascii_title)
        name = "".join(word[:1].upper() + word[1:] for word in words)
        if not name:
            raise LearningError(f"título de aula inválido: {lesson['title']!r}")
        return f"CONCEITO_{name}.md"

    def continue_action(self) -> dict[str, Any]:
        state = self.load_state()
        lesson = self.current_lesson(state)
        exercise = state.get("exercise")
        actions = {
            "READY": "TRACK_COMPLETED" if lesson is None else "TEACH",
            "TEACHING": "CREATE_EXERCISE",
            "WAITING_FOR_STUDENT": "WAIT_FOR_STUDENT",
            "REVIEWING": "RESUME_REVIEW",
            "NEEDS_CORRECTION": "WAIT_FOR_STUDENT",
            "PASSED": "FINALIZE_ACTIVITY",
            "COMPLETED": "FINALIZE_ACTIVITY",
        }
        result: dict[str, Any] = {
            "action": actions[state["status"]],
            "status": state["status"],
            "module": state["module"],
            "lesson": lesson,
            "exercise": exercise,
            "revision": state.get("revision"),
        }
        if lesson:
            result["missingPrerequisites"] = [
                item
                for item in lesson["prerequisites"]
                if item not in state["completedLessons"]
            ]
        return result

    def teach(self) -> dict[str, Any]:
        state = self.load_state()
        self._ensure_no_revision(state)
        if state["status"] != "READY":
            raise LearningError(f"teach exige READY; atual={state['status']}")
        lesson = self.current_lesson(state)
        if lesson is None:
            raise LearningError("a trilha já foi concluída")
        missing = set(lesson["prerequisites"]).difference(state["completedLessons"])
        if missing:
            raise LearningError(f"pré-requisitos pendentes: {', '.join(sorted(missing))}")
        state["status"] = "TEACHING"
        self._save(state, "TEACHING", f"objetivo apresentado: {lesson['title']}")
        self._write_session(
            lesson["title"],
            "a preparar",
            "material conceitual em preparação",
            f"{lesson['title']} (`TEACHING`)",
            "criar material conceitual, starter e testes do exercício",
        )
        return {"status": state["status"], "lesson": lesson}

    def assign(self, name: str, source: str, test: str) -> dict[str, Any]:
        state = self.load_state()
        self._ensure_no_revision(state)
        if state["status"] != "TEACHING":
            raise LearningError(f"assign exige TEACHING; atual={state['status']}")
        if not name.strip():
            raise LearningError("nome do exercício não pode ser vazio")
        source_path = self._exercise_path(source, Path("src/main/java"))
        test_path = self._exercise_path(test, Path("src/test/java"))
        if not source_path.is_file() or not test_path.is_file():
            raise LearningError("source e teste devem existir antes de registrar o exercício")
        if source_path.suffix != ".java" or test_path.suffix != ".java":
            raise LearningError("source e teste devem ser arquivos .java")

        lesson = self.current_lesson(state)
        assert lesson is not None
        expected_directory = self.lesson_directory(lesson)
        if source_path.parent.name != expected_directory:
            raise LearningError(
                f"source deve ficar na pasta da aula {expected_directory}"
            )
        if test_path.parent.name != expected_directory:
            raise LearningError(
                f"teste deve ficar na pasta da aula {expected_directory}"
            )
        concept_name = self.concept_filename(lesson)
        concept_relative = (source_path.parent / concept_name).relative_to(self.root)
        concept_path = self._exercise_path(
            concept_relative.as_posix(), Path("src/main/java")
        )
        if not concept_path.is_file():
            raise LearningError(
                f"{concept_name} deve existir na mesma pasta do source"
            )

        state["exercise"] = {
            "name": name.strip(),
            "concept": concept_path.relative_to(self.root).as_posix(),
            "source": source_path.relative_to(self.root).as_posix(),
            "test": test_path.relative_to(self.root).as_posix(),
            "attempts": 0,
            "createdAt": utc_now(),
        }
        state["requiredCheckpoint"] = (
            lesson["id"] if lesson.get("kind") == "checkpoint" and lesson.get("required") else None
        )
        state["status"] = "WAITING_FOR_STUDENT"
        self._save(state, "WAITING_FOR_STUDENT", f"exercício criado: {name}")
        self._write_session(
            lesson["title"],
            name,
            "aguardando implementação",
            f"{lesson['title']} (`WAITING_FOR_STUDENT`)",
            "o aluno lê o material conceitual, realiza a prática e informa “terminei”",
        )
        return {"status": state["status"], "exercise": state["exercise"]}

    def review_start(self) -> dict[str, Any]:
        state = self.load_state()
        self._ensure_no_revision(state)
        if state["status"] == "REVIEWING":
            return {"status": "REVIEWING", "resumed": True, "exercise": state["exercise"]}
        if state["status"] not in {"WAITING_FOR_STUDENT", "NEEDS_CORRECTION"}:
            raise LearningError(
                f"review-start exige WAITING_FOR_STUDENT; atual={state['status']}"
            )
        exercise = state["exercise"]
        paths_to_check = [("source", Path("src/main/java")), ("test", Path("src/test/java"))]
        if "concept" in exercise:
            paths_to_check.insert(0, ("concept", Path("src/main/java")))
        for field, required_root in paths_to_check:
            path = self._exercise_path(exercise[field], required_root)
            if not path.is_file():
                raise LearningError(f"arquivo ativo ausente: {exercise[field]}")
        exercise["attempts"] += 1
        state["status"] = "REVIEWING"
        self._save(state, "REVIEWING", f"tentativa {exercise['attempts']} iniciada")
        return {"status": state["status"], "resumed": False, "exercise": exercise}

    def migrate_active_concept_filename(self) -> dict[str, Any]:
        """Atualiza o caminho do conceito ativo após uma convenção de nome ser alterada."""
        state = self.load_state()
        self._ensure_no_revision(state)
        exercise = state.get("exercise")
        lesson = self.current_lesson(state)
        if not exercise or lesson is None:
            raise LearningError("não há exercício ativo para migrar")

        source_path = self._exercise_path(exercise["source"], Path("src/main/java"))
        target_path = source_path.parent / self.concept_filename(lesson)
        if not target_path.is_file():
            raise LearningError(
                f"material conceitual esperado ausente: {target_path.relative_to(self.root)}"
            )
        previous = exercise.get("concept")
        exercise["concept"] = target_path.relative_to(self.root).as_posix()
        self._save(state, "CONCEPT_FILENAME_MIGRATED", f"conceito atualizado: {previous}")
        return {"exercise": exercise, "migrated": previous != exercise["concept"]}

    def migrate_active_exercise_directory(self) -> dict[str, Any]:
        """Atualiza os caminhos ativos depois que a pasta da aula foi renomeada."""
        state = self.load_state()
        self._ensure_no_revision(state)
        exercise = state.get("exercise")
        lesson = self.current_lesson(state)
        if not exercise or lesson is None:
            raise LearningError("não há exercício ativo para migrar")

        expected_directory = self.lesson_directory(lesson)
        source_path = self._exercise_path(exercise["source"], Path("src/main/java"))
        test_path = self._exercise_path(exercise["test"], Path("src/test/java"))
        target_source = source_path.parent.parent / expected_directory / source_path.name
        target_test = test_path.parent.parent / expected_directory / test_path.name
        if not target_source.is_file() or not target_test.is_file():
            raise LearningError(
                f"source e teste devem estar na pasta renomeada {expected_directory}"
            )

        exercise["source"] = target_source.relative_to(self.root).as_posix()
        exercise["test"] = target_test.relative_to(self.root).as_posix()
        concept_path = target_source.parent / self.concept_filename(lesson)
        if concept_path.is_file():
            exercise["concept"] = concept_path.relative_to(self.root).as_posix()
        self._save(
            state,
            "EXERCISE_DIRECTORY_MIGRATED",
            f"arquivos atualizados para {expected_directory}",
        )
        return {"exercise": exercise, "directory": expected_directory}

    def skip_initial_diagnostic(self) -> dict[str, Any]:
        state = self.load_state()
        self._ensure_no_revision(state)
        lesson = self.current_lesson(state)
        if lesson is None or lesson["id"] != "initial-diagnostic":
            raise LearningError("somente o diagnóstico inicial pode ser pulado")

        archived_files: list[str] = []
        exercise = state.get("exercise")
        if exercise:
            files_to_archive: list[tuple[Path, Path]] = []
            if "concept" not in exercise:
                source_path = self._exercise_path(exercise["source"], Path("src/main/java"))
                legacy_concept = source_path.parent / self.concept_filename(lesson)
                if not legacy_concept.exists():
                    legacy_concept = source_path.parent / "CONCEITO.md"
                if legacy_concept.exists():
                    archived = legacy_concept.with_suffix(f"{legacy_concept.suffix}.skipped")
                    if archived.exists():
                        raise LearningError(
                            f"arquivo de diagnóstico arquivado já existe: {archived}"
                        )
                    files_to_archive.append((legacy_concept, archived))
            for field, required_root in (
                ("concept", Path("src/main/java")),
                ("source", Path("src/main/java")),
                ("test", Path("src/test/java")),
            ):
                if field not in exercise:
                    continue
                path = self._exercise_path(exercise[field], required_root)
                if not path.exists():
                    continue
                archived = path.with_suffix(f"{path.suffix}.skipped")
                if archived.exists():
                    raise LearningError(f"arquivo de diagnóstico arquivado já existe: {archived}")
                files_to_archive.append((path, archived))

            for path, archived in files_to_archive:
                path.rename(archived)
                archived_files.append(archived.relative_to(self.root).as_posix())

        completed = list(state["completedLessons"])
        completed.append(lesson["id"])
        state["completedLessons"] = [
            item["id"] for item in self.lessons if item["id"] in set(completed)
        ]
        state["lastResult"] = {
            "lesson": lesson["id"],
            "exercise": exercise["name"] if exercise else None,
            "outcome": "SKIPPED",
            "testsPassed": False,
            "analysisPassed": False,
            "summary": "diagnóstico inicial pulado a pedido do aluno",
            "at": utc_now(),
        }
        state["status"] = "COMPLETED"
        self._append_history(state, "SKIPPED", "diagnóstico inicial pulado pelo aluno")

        next_lesson = self._next_available(state["completedLessons"])
        state["lesson"] = next_lesson["id"] if next_lesson else None
        if next_lesson:
            state["module"] = next_lesson["module"]
        state["exercise"] = None
        state["requiredCheckpoint"] = None
        state["status"] = "READY"
        self._save(state, "READY", "próxima ação liberada após pular o diagnóstico")
        point = f"{next_lesson['title']} (`READY`)" if next_lesson else "trilha concluída"
        self._write_session(
            lesson["title"],
            exercise["name"] if exercise else "não iniciado",
            "pulado a pedido do aluno",
            point,
            "continuar pela trilha completa quando quiser",
        )
        return {
            "status": state["status"],
            "skipped": True,
            "nextLesson": next_lesson,
            "archivedFiles": archived_files,
        }

    def reset_after_diagnostic(self) -> dict[str, Any]:
        state = self.load_state()
        target = self.lesson_by_id.get("intellij-idea-foundations")
        if target is None:
            raise LearningError("a aula intellij-idea-foundations não existe no currículo")

        timestamp = utc_now().replace(":", "-")
        backup_dir = self.learning_dir / "backups" / timestamp
        suffix = 2
        while backup_dir.exists():
            backup_dir = self.learning_dir / "backups" / f"{timestamp}-{suffix}"
            suffix += 1
        backup_dir.mkdir(parents=True)
        for path in (self.progress_path, self.history_path, self.session_path):
            if path.is_file():
                shutil.copy2(path, backup_dir / path.name)

        reset_state = {
            "version": state["version"],
            "track": "java",
            "module": target["module"],
            "lesson": target["id"],
            "status": "READY",
            "exercise": None,
            "completedLessons": ["initial-diagnostic"],
            "requiredCheckpoint": None,
            "revision": None,
            "lastResult": {
                "lesson": "initial-diagnostic",
                "exercise": None,
                "outcome": "COMPLETED",
                "testsPassed": True,
                "analysisPassed": True,
                "summary": "diagnóstico inicial preservado como concluído após a limpeza",
                "at": utc_now(),
            },
            "updatedAt": utc_now(),
        }
        self.validate_state(reset_state)
        self._write_state(reset_state)
        self.history_path.write_text("# Histórico de aprendizagem\n", encoding="utf-8")
        self._append_history(
            reset_state,
            "RESET_AFTER_DIAGNOSTIC",
            "histórico limpo; diagnóstico inicial mantido como concluído",
        )
        self._write_session(
            "Diagnóstico inicial",
            "nenhum",
            "concluído antes da limpeza do histórico",
            f"{target['title']} (`READY`)",
            "começar a primeira aula regular",
        )
        return {
            "status": reset_state["status"],
            "lesson": target,
            "completedLessons": reset_state["completedLessons"],
            "backup": backup_dir.relative_to(self.root).as_posix(),
        }

    def review_result(
        self,
        outcome: str,
        tests_passed: bool,
        analysis_passed: bool,
        summary: str,
        mastered: list[str] | None = None,
    ) -> dict[str, Any]:
        state = self.load_state()
        self._ensure_no_revision(state)
        if state["status"] != "REVIEWING":
            raise LearningError(f"review-result exige REVIEWING; atual={state['status']}")
        lesson = self.current_lesson(state)
        assert lesson is not None
        exercise_name = state["exercise"]["name"]
        feedback = self.feedback_markers()

        if outcome == "passed":
            if not tests_passed or not analysis_passed:
                raise LearningError("aprovação exige testes e análise aprovados")
            if feedback:
                paths = ", ".join(sorted({item["file"] for item in feedback}))
                raise LearningError(f"remova feedbacks temporários antes da aprovação: {paths}")

            completed = list(state["completedLessons"])
            if lesson["id"] not in completed:
                completed.append(lesson["id"])
            if mastered:
                self._validate_mastered(lesson, mastered, completed)
                for lesson_id in mastered:
                    if lesson_id not in completed:
                        completed.append(lesson_id)
            completed = [item["id"] for item in self.lessons if item["id"] in set(completed)]
            state["completedLessons"] = completed
            state["lastResult"] = {
                "lesson": lesson["id"],
                "exercise": exercise_name,
                "outcome": "PASSED",
                "testsPassed": True,
                "analysisPassed": True,
                "summary": summary,
                "at": utc_now(),
            }
            state["status"] = "PASSED"
            self._append_history(state, "PASSED", summary)
            state["status"] = "COMPLETED"
            self._append_history(state, "COMPLETED", f"atividade concluída: {exercise_name}")
            next_lesson = self._next_available(completed)
            state["lesson"] = next_lesson["id"] if next_lesson else None
            if next_lesson:
                state["module"] = next_lesson["module"]
            state["exercise"] = None
            state["requiredCheckpoint"] = None
            state["status"] = "READY"
            self._save(state, "READY", "próxima ação liberada")
            point = (
                f"{next_lesson['title']} (`READY`)" if next_lesson else "trilha concluída"
            )
            self._write_session(
                lesson["title"],
                exercise_name,
                f"aprovado — {summary}",
                point,
                "continuar quando quiser" if next_lesson else "consolidar o projeto final",
            )
            return {"status": "READY", "passed": True, "nextLesson": next_lesson}

        if outcome != "needs-correction":
            raise LearningError("outcome deve ser passed ou needs-correction")
        if tests_passed and analysis_passed:
            raise LearningError("resultado requer correção, mas testes e análise foram aprovados")
        state["lastResult"] = {
            "lesson": lesson["id"],
            "exercise": exercise_name,
            "outcome": "NEEDS_CORRECTION",
            "testsPassed": tests_passed,
            "analysisPassed": analysis_passed,
            "summary": summary,
            "at": utc_now(),
        }
        state["status"] = "NEEDS_CORRECTION"
        self._append_history(state, "NEEDS_CORRECTION", summary)
        state["status"] = "WAITING_FOR_STUDENT"
        self._save(state, "WAITING_FOR_STUDENT", "nova tentativa aguardada")
        self._write_session(
            lesson["title"],
            exercise_name,
            f"requer correção — {summary}",
            f"{lesson['title']} (`WAITING_FOR_STUDENT`)",
            "corrigir as pistas e informar “terminei” novamente",
        )
        return {"status": state["status"], "passed": False, "feedback": feedback}

    def revision_start(self, topic: str) -> dict[str, Any]:
        state = self.load_state()
        if state.get("revision"):
            raise LearningError("já existe uma revisão em andamento")
        snapshot = {
            key: state.get(key)
            for key in ("module", "lesson", "status", "exercise", "completedLessons")
        }
        state["revision"] = {"topic": topic.strip(), "startedAt": utc_now(), "snapshot": snapshot}
        self._save(state, "REVISION_STARTED", f"revisão sob demanda: {topic}")
        return {"revision": state["revision"], "mainStatePreserved": True}

    def revision_end(self, summary: str) -> dict[str, Any]:
        state = self.load_state()
        revision = state.get("revision")
        if not revision:
            raise LearningError("não existe revisão em andamento")
        snapshot = revision["snapshot"]
        for key, expected in snapshot.items():
            if state.get(key) != expected:
                raise LearningError(f"posição principal mudou durante a revisão: {key}")
        topic = revision["topic"]
        state["revision"] = None
        self._save(state, "REVISION_COMPLETED", f"{topic}: {summary}")
        return {"topic": topic, "summary": summary, "mainStatePreserved": True}

    def feedback_markers(self) -> list[dict[str, Any]]:
        markers: list[dict[str, Any]] = []
        source_root = self.root / "src"
        if not source_root.exists():
            return markers
        for path in sorted(source_root.rglob("*.java")):
            for line_number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            ):
                match = FEEDBACK_PATTERN.search(line)
                if match:
                    markers.append(
                        {
                            "file": path.relative_to(self.root).as_posix(),
                            "line": line_number,
                            "category": match.group(1),
                            "text": line.strip(),
                        }
                    )
        return markers

    def summary(self) -> str:
        self.load_state()
        if not self.session_path.is_file():
            raise LearningError("resumo da sessão ausente")
        return self.session_path.read_text(encoding="utf-8").strip()

    def _next_available(self, completed: list[str]) -> dict[str, Any] | None:
        completed_set = set(completed)
        for lesson in self.lessons:
            if lesson["id"] in completed_set:
                continue
            if set(lesson["prerequisites"]).issubset(completed_set):
                return lesson
        if len(completed_set) == len(self.lessons):
            return None
        blocked = [item["id"] for item in self.lessons if item["id"] not in completed_set]
        raise LearningError(f"currículo bloqueado por pré-requisitos: {', '.join(blocked)}")

    def _validate_mastered(
        self, current: dict[str, Any], mastered: list[str], completed: list[str]
    ) -> None:
        if current["kind"] != "diagnostic":
            raise LearningError("--mastered só pode ser usado no diagnóstico")
        candidates = set(mastered)
        eligible = {
            lesson["id"]
            for lesson in self.lessons
            if lesson["module"] == "fundamentals"
            and lesson["kind"] == "lesson"
            and lesson.get("diagnosticEligible", True)
        }
        invalid = candidates.difference(eligible)
        if invalid:
            raise LearningError(f"aulas não diagnosticáveis: {', '.join(sorted(invalid))}")
        available = set(completed).union(candidates)
        for lesson_id in candidates:
            missing = set(self.lesson_by_id[lesson_id]["prerequisites"]).difference(available)
            if missing:
                raise LearningError(
                    f"{lesson_id} não pode ser marcado sem: {', '.join(sorted(missing))}"
                )

    def _exercise_path(self, value: str, required_root: Path) -> Path:
        relative = Path(value)
        if relative.is_absolute() or ".." in relative.parts:
            raise LearningError("caminho absoluto ou travessia não é permitido")
        resolved = (self.root / relative).resolve()
        allowed = (self.root / required_root).resolve()
        try:
            resolved.relative_to(allowed)
        except ValueError as error:
            raise LearningError(f"caminho deve ficar em {required_root.as_posix()}") from error
        return resolved

    @staticmethod
    def _ensure_no_revision(state: dict[str, Any]) -> None:
        if state.get("revision"):
            raise LearningError("conclua a revisão sob demanda antes de alterar a trilha principal")

    def _write_state(self, state: dict[str, Any]) -> None:
        state["updatedAt"] = utc_now()
        self.learning_dir.mkdir(parents=True, exist_ok=True)
        temporary = self.progress_path.with_suffix(".json.tmp")
        temporary.write_text(
            json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        os.replace(temporary, self.progress_path)

    def _save(self, state: dict[str, Any], event: str, detail: str) -> None:
        self.validate_state(state)
        self._write_state(state)
        self._append_history(state, event, detail)

    def _append_history(self, state: dict[str, Any], event: str, detail: str) -> None:
        self.learning_dir.mkdir(parents=True, exist_ok=True)
        if not self.history_path.exists():
            self.history_path.write_text("# Histórico de aprendizagem\n", encoding="utf-8")
        timestamp = utc_now()
        block = (
            f"\n## {timestamp} — {event}\n\n"
            f"- Estado: `{state['status']}`\n"
            f"- Módulo: `{state['module']}`\n"
            f"- Aula: `{state.get('lesson') or 'TRACK_COMPLETED'}`\n"
            f"- Detalhe: {detail}\n"
        )
        with self.history_path.open("a", encoding="utf-8") as history:
            history.write(block)

    def _write_session(
        self, content: str, exercise: str, result: str, point: str, next_action: str
    ) -> None:
        self.learning_dir.mkdir(parents=True, exist_ok=True)
        self.session_path.write_text(
            "# Última sessão\n\n"
            f"- Conteúdo: {content}\n"
            f"- Exercício: {exercise}\n"
            f"- Resultado: {result}\n"
            f"- Ponto atual: {point}\n"
            f"- Próxima ação: {next_action}\n",
            encoding="utf-8",
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Estado persistente do DEV_LEARNING")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("init")
    subparsers.add_parser("status")
    subparsers.add_parser("continue")
    subparsers.add_parser("teach")
    subparsers.add_parser("review-start")
    subparsers.add_parser("skip-diagnostic")
    subparsers.add_parser("migrate-active-concept-filename")
    subparsers.add_parser("migrate-active-exercise-directory")
    subparsers.add_parser("reset-after-diagnostic")
    subparsers.add_parser("summary")
    subparsers.add_parser("feedback-list")

    assign = subparsers.add_parser("assign")
    assign.add_argument("--name", required=True)
    assign.add_argument("--source", required=True)
    assign.add_argument("--test", required=True)

    result = subparsers.add_parser("review-result")
    result.add_argument("--outcome", choices=("passed", "needs-correction"), required=True)
    result.add_argument("--tests-passed", type=parse_bool, required=True)
    result.add_argument("--analysis-passed", type=parse_bool, required=True)
    result.add_argument("--summary", required=True)
    result.add_argument("--mastered", default="")

    revision_start = subparsers.add_parser("revision-start")
    revision_start.add_argument("--topic", required=True)
    revision_end = subparsers.add_parser("revision-end")
    revision_end.add_argument("--summary", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        store = LearningStore()
        if args.command == "init":
            output: Any = store.initialize()
        elif args.command == "status":
            output = store.load_state()
        elif args.command == "continue":
            output = store.continue_action()
        elif args.command == "teach":
            output = store.teach()
        elif args.command == "assign":
            output = store.assign(args.name, args.source, args.test)
        elif args.command == "review-start":
            output = store.review_start()
        elif args.command == "skip-diagnostic":
            output = store.skip_initial_diagnostic()
        elif args.command == "migrate-active-concept-filename":
            output = store.migrate_active_concept_filename()
        elif args.command == "migrate-active-exercise-directory":
            output = store.migrate_active_exercise_directory()
        elif args.command == "reset-after-diagnostic":
            output = store.reset_after_diagnostic()
        elif args.command == "review-result":
            mastered = [item.strip() for item in args.mastered.split(",") if item.strip()]
            output = store.review_result(
                args.outcome,
                args.tests_passed,
                args.analysis_passed,
                args.summary,
                mastered,
            )
        elif args.command == "revision-start":
            output = store.revision_start(args.topic)
        elif args.command == "revision-end":
            output = store.revision_end(args.summary)
        elif args.command == "feedback-list":
            output = store.feedback_markers()
        elif args.command == "summary":
            print(store.summary())
            return 0
        else:
            raise LearningError(f"comando não implementado: {args.command}")
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0
    except LearningError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
