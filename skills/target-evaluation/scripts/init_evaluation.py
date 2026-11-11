"""Create a target-evaluation workspace from an input JSON file.

The script copies the normalized input and writes the initial progress file.
It does not fetch literature or invent scientific findings.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def slug(value: str) -> str:
    lowered = value.strip().lower()
    cleaned = re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")
    return cleaned or "untitled"


def load_input(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise SystemExit(f"input is not valid JSON: {error}") from error
    if not isinstance(payload, dict):
        raise SystemExit("input JSON must be an object")
    target = payload.get("target")
    indication = payload.get("indication")
    if not isinstance(target, str) or not target.strip():
        raise SystemExit("input.target must be a non-empty string")
    if not isinstance(indication, str) or not indication.strip():
        raise SystemExit("input.indication must be a non-empty string")
    modality = payload.get("modality", "")
    context = payload.get("additional_context", "")
    if not isinstance(modality, str) or not isinstance(context, str):
        raise SystemExit("modality and additional_context must be strings when present")
    return {
        "target": target.strip(),
        "indication": indication.strip(),
        "modality": modality.strip(),
        "additional_context": context.strip(),
    }


def default_workdir(payload: dict) -> Path:
    name = f"target-evaluation-{slug(payload['target'])}-{slug(payload['indication'])}"
    return Path("do_not_commit") / name


def write_workspace(payload: dict, workdir: Path, force: bool) -> None:
    progress_path = workdir / "progress.json"
    evidence = [
        workdir / "identity.json",
        workdir / "genetic.json",
        workdir / "mechanism.json",
        workdir / "tractability.json",
        workdir / "safety_competition.json",
        workdir / "target_evaluation.json",
        workdir / "target_evaluation_report.md",
    ]
    if progress_path.exists() and not force:
        raise SystemExit(f"{progress_path} already exists; rerun with --force to replace the input and progress files")
    if force and any(path.exists() for path in evidence):
        raise SystemExit("refusing --force after evidence files exist")
    workdir.mkdir(parents=True, exist_ok=True)
    (workdir / "input.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    progress = {"phase": "identity", "completed": []}
    progress_path.write_text(
        json.dumps(progress, indent=2) + "\n",
        encoding="utf-8",
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--workdir", type=Path)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    payload = load_input(args.input)
    workdir = args.workdir or default_workdir(payload)
    write_workspace(payload, workdir, args.force)
    print(workdir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
