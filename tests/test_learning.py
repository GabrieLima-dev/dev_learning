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

    def create_exercise_files(self, feedback: bool = False) -> tuple[str, str]:
        source = Path("src/main/java/dev/learning/Diagnostic.java")
        test = Path("src/test/java/dev/learning/DiagnosticTest.java")
        (self.root / source).parent.mkdir(parents=True, exist_ok=True)
        (self.root / test).parent.mkdir(parents=True, exist_ok=True)
        marker = "// DEV_LEARNING_FEEDBACK[LOGIC]: reveja a condição\n" if feedback else ""
        (self.root / source).write_text(
            f"package dev.learning;\n{marker}public class Diagnostic {{}}\n", encoding="utf-8"
        )
        (self.root / test).write_text(
            "package dev.learning;\nclass DiagnosticTest {}\n", encoding="utf-8"
        )
        return source.as_posix(), test.as_posix()

    def start_exercise(self, feedback: bool = False) -> None:
        source, test = self.create_exercise_files(feedback)
        self.store.teach()
        self.store.assign("Diagnostico", source, test)

    def test_initialization_is_idempotent_and_consultable(self) -> None:
        again = self.store.initialize()
        self.assertFalse(again["initialized"])
        self.assertEqual("READY", self.store.load_state()["status"])
        self.assertEqual("TEACH", self.store.continue_action()["action"])

    def test_prepare_exercise_stops_for_student(self) -> None:
        self.start_exercise()
        state = self.store.load_state()
        self.assertEqual("WAITING_FOR_STUDENT", state["status"])
        self.assertEqual("WAIT_FOR_STUDENT", self.store.continue_action()["action"])
        self.assertEqual("Diagnostico", state["exercise"]["name"])

    def test_initial_diagnostic_can_be_skipped_before_it_starts(self) -> None:
        result = self.store.skip_initial_diagnostic()
        state = self.store.load_state()

        self.assertTrue(result["skipped"])
        self.assertEqual([], result["archivedFiles"])
        self.assertIn("initial-diagnostic", state["completedLessons"])
        self.assertEqual("git-github-foundations", state["lesson"])
        self.assertEqual("READY", state["status"])
        self.assertEqual("SKIPPED", state["lastResult"]["outcome"])

    def test_skipping_active_diagnostic_archives_its_files(self) -> None:
        self.start_exercise()
        source = self.root / "src/main/java/dev/learning/Diagnostic.java"
        test = self.root / "src/test/java/dev/learning/DiagnosticTest.java"

        result = self.store.skip_initial_diagnostic()

        self.assertFalse(source.exists())
        self.assertFalse(test.exists())
        self.assertTrue(source.with_suffix(".java.skipped").is_file())
        self.assertTrue(test.with_suffix(".java.skipped").is_file())
        self.assertEqual(2, len(result["archivedFiles"]))
        self.assertIsNone(self.store.load_state()["exercise"])

    def test_only_initial_diagnostic_can_be_skipped(self) -> None:
        self.store.skip_initial_diagnostic()

        with self.assertRaisesRegex(LearningError, "somente o diagnóstico inicial"):
            self.store.skip_initial_diagnostic()

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
        self.assertEqual("git-github-foundations", state["lesson"])
        self.assertIsNone(state["exercise"])

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
