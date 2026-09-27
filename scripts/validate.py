#!/usr/bin/env python3
"""Valida estrutura, currículo, estado, skills e testes locais da V1."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from learning import LearningError, LearningStore


ROOT = Path(__file__).resolve().parents[1]


def check(name: str, operation) -> bool:
    try:
        operation()
        print(f"PASS  {name}")
        return True
    except Exception as error:  # relatório único de validação
        print(f"FAIL  {name}: {error}")
        return False


def require_paths() -> None:
    required = [
        "AGENTS.md",
        "README.md",
        "pom.xml",
        "mvnw",
        "mvnw.cmd",
        ".mvn/wrapper/maven-wrapper.properties",
        ".learning/progress.json",
        ".learning/session.md",
        ".learning/history.md",
        "curriculum/java.json",
        "docs/architecture.md",
        "docs/roadmap.md",
        "docs/traceability.md",
        ".agents/skills/java-learning/SKILL.md",
        ".agents/skills/java-learning/references/teach-and-assign.md",
        ".agents/skills/java-learning/references/review.md",
        ".agents/skills/java-learning/references/revision.md",
    ]
    missing = [item for item in required if not (ROOT / item).is_file()]
    if missing:
        raise AssertionError(f"ausentes: {', '.join(missing)}")


def validate_skill() -> None:
    path = ROOT / ".agents/skills/java-learning/SKILL.md"
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        raise AssertionError("frontmatter ausente")
    if "name: java-learning" not in content or "description:" not in content:
        raise AssertionError("name/description inválidos")
    for reference in ("teach-and-assign.md", "review.md", "revision.md"):
        if f"references/{reference}" not in content:
            raise AssertionError(f"referência não roteada: {reference}")


def validate_intents() -> None:
    path = ROOT / "evals/intents.jsonl"
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        case = json.loads(line)
        if case.get("skill") != "java-learning" or not case.get("prompt"):
            raise AssertionError(f"caso inválido na linha {number}")


def run_unit_tests() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError((result.stdout + result.stderr).strip())


def run_java_tests() -> None:
    wrapper = ROOT / ("mvnw.cmd" if os.name == "nt" else "mvnw")
    result = subprocess.run(
        [str(wrapper), "test", "-q"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError((result.stdout + result.stderr).strip())


def main() -> int:
    checks = [
        check("estrutura", require_paths),
        check("pom.xml", lambda: ET.parse(ROOT / "pom.xml")),
        check("currículo e estado", lambda: LearningStore(ROOT).validate_state()),
        check("skill java-learning", validate_skill),
        check("evals de intenção", validate_intents),
        check("testes do controlador", run_unit_tests),
        check("Maven + JUnit", run_java_tests),
    ]
    passed = sum(checks)
    failed = len(checks) - passed
    print(f"SUMMARY: PASS={passed} FAIL={failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
