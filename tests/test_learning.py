from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.learning import LearningError, LearningStore


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class LearningStoreTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "curriculum").mkdir()
        shutil.copy(PROJECT_ROOT / "curriculum/java.json", self.root / "curriculum/java.json")
        self.store = LearningStore(self.root)
        self.store.initialize()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def create_exercise_files(self, feedback: bool = False) -> tuple[str, str, str]:
        lesson = self.store.current_lesson(self.store.load_state())
        assert lesson is not None
        directory = self.store.lesson_directory(lesson)
        concept = Path(
            f"src/main/java/dev/learning/{directory}/{self.store.concept_filename(lesson)}"
        )
        source = Path(f"src/main/java/dev/learning/{directory}/Diagnostic.java")
        test = Path(f"src/test/java/dev/learning/{directory}/DiagnosticTest.java")
        (self.root / source).parent.mkdir(parents=True, exist_ok=True)
        (self.root / test).parent.mkdir(parents=True, exist_ok=True)
        (self.root / concept).write_text(
            "# Diagnóstico inicial\n\n[Prática](./Diagnostic.java)\n", encoding="utf-8"
        )
        marker = "// DEV_LEARNING_FEEDBACK[LOGIC]: reveja a condição\n" if feedback else ""
        package = f"dev.learning.{directory}"
        (self.root / source).write_text(
            f"package {package};\n{marker}public class Diagnostic {{}}\n", encoding="utf-8"
        )
        (self.root / test).write_text(
            f"package {package};\nclass DiagnosticTest {{}}\n", encoding="utf-8"
        )
        return concept.as_posix(), source.as_posix(), test.as_posix()

    def start_exercise(self, feedback: bool = False) -> None:
        _, source, test = self.create_exercise_files(feedback)
        self.store.teach()
        self.store.assign("Diagnostico", source, test)

    def test_initialization_is_idempotent_and_consultable(self) -> None:
        again = self.store.initialize()
        self.assertFalse(again["initialized"])
        self.assertEqual("READY", self.store.load_state()["status"])
        self.assertEqual("TEACH", self.store.continue_action()["action"])

    def test_lesson_directories_start_with_regular_lessons(self) -> None:
        self.assertEqual(
            "lesson00_diagnostico_inicial",
            self.store.lesson_directory(self.store.lesson_by_id["initial-diagnostic"]),
        )
        self.assertEqual(
            "lesson01_intellij",
            self.store.lesson_directory(self.store.lesson_by_id["intellij-idea-foundations"]),
        )
        self.assertEqual(
            "lesson02_git",
            self.store.lesson_directory(self.store.lesson_by_id["git-github-foundations"]),
        )

    def test_prepare_exercise_stops_for_student(self) -> None:
        self.start_exercise()
        state = self.store.load_state()
        self.assertEqual("WAITING_FOR_STUDENT", state["status"])
        self.assertEqual("WAIT_FOR_STUDENT", self.store.continue_action()["action"])
        self.assertEqual("Diagnostico", state["exercise"]["name"])
        self.assertEqual(
            "src/main/java/dev/learning/lesson00_diagnostico_inicial/CONCEITO_DiagnosticoInicial.md",
            state["exercise"]["concept"],
        )

    def test_exercise_requires_concept_file_next_to_source(self) -> None:
        concept, source, test = self.create_exercise_files()
        (self.root / concept).unlink()
        self.store.teach()

        with self.assertRaisesRegex(LearningError, "CONCEITO_DiagnosticoInicial.md"):
            self.store.assign("Diagnostico", source, test)

    def test_exercise_requires_the_numbered_lesson_directory(self) -> None:
        _, source, test = self.create_exercise_files()
        invalid_source = Path("src/main/java/dev/learning/diagnostic/Diagnostic.java")
        invalid_concept = invalid_source.parent / "CONCEITO_DiagnosticoInicial.md"
        (self.root / invalid_source).parent.mkdir(parents=True)
        shutil.copy2(self.root / source, self.root / invalid_source)
        shutil.copy2(
            self.root
            / "src/main/java/dev/learning/lesson00_diagnostico_inicial/CONCEITO_DiagnosticoInicial.md",
            self.root / invalid_concept,
        )
        self.store.teach()

        with self.assertRaisesRegex(LearningError, "lesson00_diagnostico_inicial"):
            self.store.assign("Diagnostico", invalid_source.as_posix(), test)

    def test_exercise_requires_packages_that_match_their_paths(self) -> None:
        _, source, test = self.create_exercise_files()
        source_path = self.root / source
        test_path = self.root / test
        source_path.write_text("package dev.learning.other;\nclass Diagnostic {}\n", encoding="utf-8")
        self.store.teach()

        with self.assertRaisesRegex(
            LearningError, "package do source deve ser dev.learning.lesson00_diagnostico_inicial"
        ):
            self.store.assign("Diagnostico", source, test)

        source_path.write_text(
            "package dev.learning.lesson00_diagnostico_inicial;\nclass Diagnostic {}\n",
            encoding="utf-8",
        )
        test_path.write_text("package dev.learning.other;\nclass DiagnosticTest {}\n", encoding="utf-8")

        with self.assertRaisesRegex(
            LearningError, "package do teste deve ser dev.learning.lesson00_diagnostico_inicial"
        ):
            self.store.assign("Diagnostico", source, test)

    def test_active_concept_path_can_be_migrated_to_the_new_filename(self) -> None:
        self.start_exercise()
        state = self.store.load_state()
        state["exercise"]["concept"] = (
            "src/main/java/dev/learning/lesson00_diagnostico_inicial/CONCEITO.md"
        )
        (self.root / ".learning/progress.json").write_text(
            json.dumps(state), encoding="utf-8"
        )

        result = self.store.migrate_active_concept_filename()

        self.assertTrue(result["migrated"])
        self.assertEqual(
            "src/main/java/dev/learning/lesson00_diagnostico_inicial/CONCEITO_DiagnosticoInicial.md",
            result["exercise"]["concept"],
        )

    def test_initial_diagnostic_can_be_skipped_before_it_starts(self) -> None:
        result = self.store.skip_initial_diagnostic()
        state = self.store.load_state()

        self.assertTrue(result["skipped"])
        self.assertEqual([], result["archivedFiles"])
        self.assertIn("initial-diagnostic", state["completedLessons"])
        self.assertEqual("intellij-idea-foundations", state["lesson"])
        self.assertEqual("READY", state["status"])
        self.assertEqual("SKIPPED", state["lastResult"]["outcome"])

    def test_skipping_active_diagnostic_archives_its_files(self) -> None:
        self.start_exercise()
        concept = (
            self.root
            / "src/main/java/dev/learning/lesson00_diagnostico_inicial/CONCEITO_DiagnosticoInicial.md"
        )
        source = self.root / "src/main/java/dev/learning/lesson00_diagnostico_inicial/Diagnostic.java"
        test = self.root / "src/test/java/dev/learning/lesson00_diagnostico_inicial/DiagnosticTest.java"

        result = self.store.skip_initial_diagnostic()

        self.assertFalse(concept.exists())
        self.assertFalse(source.exists())
        self.assertFalse(test.exists())
        self.assertTrue(concept.with_suffix(".md.skipped").is_file())
        self.assertTrue(source.with_suffix(".java.skipped").is_file())
        self.assertTrue(test.with_suffix(".java.skipped").is_file())
        self.assertEqual(3, len(result["archivedFiles"]))
        self.assertIsNone(self.store.load_state()["exercise"])

    def test_skipping_legacy_diagnostic_also_archives_sibling_concept(self) -> None:
        self.start_exercise()
        state = self.store.load_state()
        del state["exercise"]["concept"]
        (self.root / ".learning/progress.json").write_text(
            json.dumps(state), encoding="utf-8"
        )

        result = self.store.skip_initial_diagnostic()

        archived = (
            self.root
            / "src/main/java/dev/learning/lesson00_diagnostico_inicial/CONCEITO_DiagnosticoInicial.md.skipped"
        )
        self.assertTrue(archived.is_file())
        self.assertIn(
            "src/main/java/dev/learning/lesson00_diagnostico_inicial/CONCEITO_DiagnosticoInicial.md.skipped",
            result["archivedFiles"],
        )

    def test_only_initial_diagnostic_can_be_skipped(self) -> None:
        self.store.skip_initial_diagnostic()

        with self.assertRaisesRegex(LearningError, "somente o diagnóstico inicial"):
            self.store.skip_initial_diagnostic()

    def test_reset_after_diagnostic_clears_progress_and_creates_backup(self) -> None:
        self.start_exercise()
        source = self.root / "src/main/java/dev/learning/lesson00_diagnostico_inicial/Diagnostic.java"
        test = self.root / "src/test/java/dev/learning/lesson00_diagnostico_inicial/DiagnosticTest.java"

        result = self.store.reset_after_diagnostic()
        state = self.store.load_state()

        self.assertEqual("READY", state["status"])
        self.assertEqual("intellij-idea-foundations", state["lesson"])
        self.assertEqual(["initial-diagnostic"], state["completedLessons"])
        self.assertIsNone(state["exercise"])
        self.assertTrue(source.is_file())
        self.assertTrue(test.is_file())
        backup = self.root / result["backup"]
        self.assertTrue((backup / "progress.json").is_file())
        self.assertTrue((backup / "history.md").is_file())
        self.assertTrue((backup / "session.md").is_file())
        history = (self.root / ".learning/history.md").read_text(encoding="utf-8")
        self.assertIn("RESET_AFTER_DIAGNOSTIC", history)
        self.assertNotIn("WAITING_FOR_STUDENT", history)

    def test_paths_cannot_escape_workspace_or_expected_source_root(self) -> None:
        self.store.teach()
        with self.assertRaises(LearningError):
            self.store.assign("Escape", "../outside.java", "src/test/java/Test.java")
        with self.assertRaises(LearningError):
            self.store.assign("WrongRoot", "docs/A.java", "src/test/java/Test.java")

    def test_failed_review_preserves_active_exercise(self) -> None:
        self.start_exercise()
        self.store.review_start()
        result = self.store.review_result(
            "needs-correction", tests_passed=False, analysis_passed=False, summary="loop incompleto"
        )
        state = self.store.load_state()
        self.assertFalse(result["passed"])
        self.assertEqual("WAITING_FOR_STUDENT", state["status"])
        self.assertEqual("Diagnostico", state["exercise"]["name"])
        self.assertEqual("initial-diagnostic", state["lesson"])

    def test_green_tests_are_not_sufficient_for_approval(self) -> None:
        self.start_exercise()
        self.store.review_start()
        with self.assertRaisesRegex(LearningError, "testes e análise"):
            self.store.review_result(
                "passed", tests_passed=True, analysis_passed=False, summary="contornou o conceito"
            )

    def test_feedback_marker_blocks_approval(self) -> None:
        self.start_exercise(feedback=True)
        self.store.review_start()
        with self.assertRaisesRegex(LearningError, "feedbacks temporários"):
            self.store.review_result(
                "passed", tests_passed=True, analysis_passed=True, summary="ok"
            )

    def test_approval_advances_and_diagnostic_can_skip_demonstrated_basics(self) -> None:
        self.start_exercise()
        self.store.review_start()
        result = self.store.review_result(
            "passed",
            tests_passed=True,
            analysis_passed=True,
            summary="fundamentos demonstrados",
            mastered=["variables-types", "operators"],
        )
        state = self.store.load_state()
        self.assertTrue(result["passed"])
        self.assertEqual("READY", state["status"])
        self.assertEqual("intellij-idea-foundations", state["lesson"])
        self.assertIsNone(state["exercise"])

        self.start_exercise()
        self.store.review_start()
        self.store.review_result(
            "passed",
            tests_passed=True,
            analysis_passed=True,
            summary="fundamentos do IntelliJ IDEA demonstrados",
        )
        state = self.store.load_state()
        self.assertEqual("git-github-foundations", state["lesson"])

        self.start_exercise()
        self.store.review_start()
        self.store.review_result(
            "passed",
            tests_passed=True,
            analysis_passed=True,
            summary="fundamentos de Git demonstrados",
        )
        state = self.store.load_state()
        self.assertEqual("input-output", state["lesson"])
        self.assertIsNone(state["exercise"])

    def test_diagnostic_cannot_skip_intellij_foundations(self) -> None:
        self.start_exercise()
        self.store.review_start()

        with self.assertRaisesRegex(LearningError, "não diagnosticáveis"):
            self.store.review_result(
                "passed",
                tests_passed=True,
                analysis_passed=True,
                summary="tentativa de pular a primeira aula",
                mastered=["intellij-idea-foundations"],
            )

    def test_active_git_exercise_from_previous_curriculum_is_preserved(self) -> None:
        concept, source, test = self.create_exercise_files()
        state = self.store.load_state()
        state["lesson"] = "git-github-foundations"
        state["status"] = "WAITING_FOR_STUDENT"
        state["completedLessons"] = ["initial-diagnostic"]
        state["exercise"] = {
            "name": "GitPractice",
            "concept": concept,
            "source": source,
            "test": test,
            "attempts": 0,
            "createdAt": "2026-01-01T00:00:00Z",
        }
        (self.root / ".learning/progress.json").write_text(
            json.dumps(state), encoding="utf-8"
        )

        reopened = LearningStore(self.root)
        self.assertEqual(
            "git-github-foundations", reopened.continue_action()["lesson"]["id"]
        )
        reopened.review_start()
        reopened.review_result(
            "passed",
            tests_passed=True,
            analysis_passed=True,
            summary="atividade legada concluída",
        )

        self.assertEqual("intellij-idea-foundations", reopened.load_state()["lesson"])

    def test_diagnostic_does_not_skip_a_prerequisite_gap(self) -> None:
        self.start_exercise()
        self.store.review_start()
        with self.assertRaisesRegex(LearningError, "não pode ser marcado"):
            self.store.review_result(
                "passed",
                tests_passed=True,
                analysis_passed=True,
                summary="tentativa de salto",
                mastered=["operators"],
            )

    def test_revision_preserves_main_position(self) -> None:
        self.start_exercise()
        before = self.store.load_state()
        self.store.revision_start("loops")
        with self.assertRaisesRegex(LearningError, "conclua a revisão"):
            self.store.review_start()
        ended = self.store.revision_end("conceito retomado")
        after = self.store.load_state()
        self.assertTrue(ended["mainStatePreserved"])
        for field in ("module", "lesson", "status", "exercise", "completedLessons"):
            self.assertEqual(before[field], after[field])

    def test_state_persists_across_store_instances(self) -> None:
        self.start_exercise()
        reopened = LearningStore(self.root)
        action = reopened.continue_action()
        self.assertEqual("WAIT_FOR_STUDENT", action["action"])
        self.assertEqual("Diagnostico", action["exercise"]["name"])

    def test_corrupted_state_is_rejected(self) -> None:
        state = self.store.load_state()
        state["status"] = "UNKNOWN"
        (self.root / ".learning/progress.json").write_text(
            json.dumps(state), encoding="utf-8"
        )
        with self.assertRaisesRegex(LearningError, "track ou status"):
            self.store.load_state()

    def test_state_cannot_point_to_a_non_deterministic_lesson(self) -> None:
        state = self.store.load_state()
        state["lesson"] = "operators"
        (self.root / ".learning/progress.json").write_text(
            json.dumps(state), encoding="utf-8"
        )
        with self.assertRaisesRegex(LearningError, "pré-requisitos"):
            self.store.load_state()


if __name__ == "__main__":
    unittest.main()
