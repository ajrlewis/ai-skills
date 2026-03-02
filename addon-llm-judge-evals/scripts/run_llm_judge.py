#!/usr/bin/env python3
"""Starter template for LLM-as-judge eval runs.

Copy this file into a target project's ``scripts/evals/run_llm_judge.py`` and
adapt the backend adapter section to the project's chosen LLM integration.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class JudgeConfig:
    """Resolved judge configuration derived from args and the skill manifest."""

    backend: str
    model: str
    manifest_path: Path
    rubric_path: Path
    cases_dir: Path
    out_json: Path
    out_markdown: Path


def parse_args() -> argparse.Namespace:
    """Parse CLI args for a scaffolded judge run."""

    parser = argparse.ArgumentParser(description="Run rubric-based LLM judge evals.")
    parser.add_argument("--manifest", default="config/skill_manifest.json")
    parser.add_argument("--rubric", default="evals/judge/rubric.md")
    parser.add_argument("--cases", default="evals/judge/cases")
    parser.add_argument("--out-json", default="evals/judge/report.json")
    parser.add_argument("--out-markdown", default="REVIEW_BUNDLE/JUDGE_REPORT.md")
    parser.add_argument("--backend", default="auto")
    parser.add_argument("--model", default="")
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON object from disk."""

    return json.loads(path.read_text(encoding="utf-8"))


def resolve_backend(requested: str, manifest: dict[str, Any]) -> str:
    """Resolve the backend from explicit override and selected addons."""

    if requested != "auto":
        return requested

    addons = set(manifest.get("addons", []))
    has_langchain = "addon-langchain-llm" in addons
    has_google_adk = "addon-google-agent-dev-kit" in addons

    if has_langchain and has_google_adk:
        raise ValueError("Explicit --backend is required when multiple judge backends are installed.")
    if has_langchain:
        return "langchain"
    if has_google_adk:
        return "google-adk"
    raise ValueError("No supported judge backend was declared in config/skill_manifest.json.")


def resolve_model(explicit_model: str, backend: str, manifest: dict[str, Any]) -> str:
    """Resolve the judge model from explicit override or manifest defaults."""

    if explicit_model:
        return explicit_model

    defaults = manifest.get("defaults", {})
    if backend == "langchain":
        model = defaults.get("DEFAULT_MODEL")
    elif backend == "google-adk":
        model = defaults.get("ADK_DEFAULT_MODEL")
    else:
        raise ValueError(f"Unsupported backend: {backend}")

    if not model:
        raise ValueError(f"No default model available for backend: {backend}")
    return str(model)


def list_case_files(cases_dir: Path) -> list[str]:
    """Return stable case file names for the generated report."""

    if not cases_dir.exists():
        return []
    return sorted(
        str(path.relative_to(cases_dir))
        for path in cases_dir.rglob("*")
        if path.is_file()
    )


def build_placeholder_report(config: JudgeConfig, case_files: list[str]) -> dict[str, Any]:
    """Build a deterministic starter report until a real adapter is wired in."""

    return {
        "status": "starter-template",
        "backend": config.backend,
        "model": config.model,
        "manifest": str(config.manifest_path),
        "rubric": str(config.rubric_path),
        "cases": case_files,
        "overall_score": None,
        "pass": None,
        "notes": [
            "This bundled script is a starter template.",
            "Replace the placeholder report path with a real backend adapter in the target project.",
            "Keep backend resolution and report shapes stable when adapting this file.",
        ],
    }


def write_outputs(report: dict[str, Any], config: JudgeConfig) -> None:
    """Persist the starter report in JSON and markdown form."""

    config.out_json.parent.mkdir(parents=True, exist_ok=True)
    config.out_markdown.parent.mkdir(parents=True, exist_ok=True)

    config.out_json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    markdown = [
        "# Judge Report",
        "",
        f"- Status: {report['status']}",
        f"- Backend: {report['backend']}",
        f"- Model: {report['model']}",
        f"- Case count: {len(report['cases'])}",
        "",
        "## Notes",
    ]
    markdown.extend(f"- {note}" for note in report["notes"])
    markdown.append("")
    config.out_markdown.write_text("\n".join(markdown), encoding="utf-8")


def main() -> int:
    """Resolve config and emit a deterministic starter report."""

    args = parse_args()
    manifest_path = Path(args.manifest)
    rubric_path = Path(args.rubric)
    cases_dir = Path(args.cases)
    out_json = Path(args.out_json)
    out_markdown = Path(args.out_markdown)

    manifest = load_json(manifest_path)
    backend = resolve_backend(args.backend, manifest)
    model = resolve_model(args.model, backend, manifest)

    config = JudgeConfig(
        backend=backend,
        model=model,
        manifest_path=manifest_path,
        rubric_path=rubric_path,
        cases_dir=cases_dir,
        out_json=out_json,
        out_markdown=out_markdown,
    )

    report = build_placeholder_report(config, list_case_files(cases_dir))
    write_outputs(report, config)
    print(f"Wrote starter judge report to {config.out_json} and {config.out_markdown}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
