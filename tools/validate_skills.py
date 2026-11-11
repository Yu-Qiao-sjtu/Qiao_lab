"""Validate wisp-drug skill packages.

The checker is intentionally small: frontmatter shape, in-repo prerequisites,
reference links, line count, and sample JSON. It does not execute scripts or
contact the network.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
MAX_LINES = 300


def parse_frontmatter(text: str) -> tuple[dict, list[str]]:
    errors: list[str] = []
    if not text.startswith("---\n"):
        return {}, ["missing opening frontmatter"]
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, ["missing closing frontmatter"]
    data: dict = {}
    current_list: str | None = None
    for raw in text[4:end].splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith((" ", "\t")):
            if current_list and raw.strip().startswith("- "):
                data.setdefault(current_list, []).append(raw.strip()[2:].strip().strip("\"'"))
            continue
        current_list = None
        if ":" not in raw:
            errors.append(f"frontmatter line is not a field: {raw}")
            continue
        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value == "":
            data[key] = []
            current_list = key
        elif value == "[]":
            data[key] = []
        elif value.startswith("[") and value.endswith("]"):
            data[key] = [item.strip().strip("\"'") for item in value[1:-1].split(",") if item.strip()]
        else:
            data[key] = value.strip("\"'")
    return data, errors


def linked_references(text: str) -> list[str]:
    body = text.split("\n---\n", 1)[-1]
    links: list[str] = []
    cursor = 0
    while True:
        start = body.find("](references/", cursor)
        if start < 0:
            break
        stop = body.find(")", start)
        if stop < 0:
            break
        links.append(body[start + 2 : stop].split("#", 1)[0])
        cursor = stop + 1
    return links


def validate_skill(directory: Path, skills: dict[str, dict]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    document = directory / "SKILL.md"
    if not document.is_file():
        return [f"{directory.name}: SKILL.md is missing"], warnings
    text = document.read_text(encoding="utf-8")
    frontmatter, parse_errors = parse_frontmatter(text)
    errors.extend(f"{directory.name}: {item}" for item in parse_errors)
    if len(text.splitlines()) > MAX_LINES:
        errors.append(f"{directory.name}: SKILL.md exceeds {MAX_LINES} lines")
    name = frontmatter.get("name")
    if name != directory.name:
        errors.append(f"{directory.name}: frontmatter name is {name!r}")
    if not str(frontmatter.get("description", "")).strip():
        errors.append(f"{directory.name}: description is empty")
    if not str(frontmatter.get("license", "")).strip():
        errors.append(f"{directory.name}: license is empty")
    requires = frontmatter.get("requires", [])
    loads = frontmatter.get("loads", [])
    if not isinstance(requires, list) or not isinstance(loads, list):
        errors.append(f"{directory.name}: requires and loads must be lists")
        requires, loads = [], []
    body = text.split("\n---\n", 1)[-1]
    for item in loads:
        if item not in body:
            errors.append(f"{directory.name}: loads {item} but the body never names it")
    for item in requires:
        if item == directory.name:
            errors.append(f"{directory.name}: requires itself")
        elif item not in skills:
            errors.append(f"{directory.name}: requires missing skill {item}")
    for link in linked_references(text):
        if not (directory / link).is_file():
            errors.append(f"{directory.name}: missing {link}")
    linked = set(linked_references(text))
    reference_dir = directory / "references"
    if reference_dir.is_dir():
        for path in sorted(reference_dir.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(directory).as_posix()
            if relative not in linked:
                warnings.append(f"{directory.name}: unindexed {relative}")
    scripts = directory / "scripts"
    if scripts.is_dir() and any(path.is_file() for path in scripts.rglob("*")):
        sample = directory / "samples" / "input.json"
        if not sample.is_file():
            errors.append(f"{directory.name}: scripts exist but samples/input.json is missing")
        else:
            try:
                payload = json.loads(sample.read_text(encoding="utf-8"))
            except json.JSONDecodeError as error:
                errors.append(f"{directory.name}: samples/input.json is invalid JSON: {error}")
            else:
                if not isinstance(payload, dict):
                    errors.append(f"{directory.name}: samples/input.json must be an object")
    skills[directory.name] = {"requires": [item for item in requires if isinstance(item, str)]}
    return errors, warnings


def cycles(skills: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    visiting: set[str] = set()
    visited: set[str] = set()

    def walk(name: str, trail: list[str]) -> None:
        if name in visiting:
            loop = trail[trail.index(name) :] + [name]
            errors.append("dependency cycle: " + " -> ".join(loop))
            return
        if name in visited or name not in skills:
            return
        visiting.add(name)
        for item in skills[name]["requires"]:
            walk(item, trail + [name])
        visiting.remove(name)
        visited.add(name)

    for name in sorted(skills):
        walk(name, [])
    return errors


def main() -> int:
    if not SKILLS.is_dir():
        print("PASS: 0 skill(s), 0 error(s)")
        return 0
    errors: list[str] = []
    warnings: list[str] = []
    skills: dict[str, dict] = {}
    directories = sorted(path for path in SKILLS.iterdir() if path.is_dir())
    for directory in directories:
        found, warned = validate_skill(directory, skills)
        errors.extend(found)
        warnings.extend(warned)
    errors.extend(cycles(skills))
    for warning in warnings:
        print(f"WARNING {warning}")
    for error in errors:
        print(f"ERROR {error}")
    print(f"{'FAIL' if errors else 'PASS'}: {len(skills)} skill(s), {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
