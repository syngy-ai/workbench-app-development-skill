#!/usr/bin/env python3
import re
import sys
from pathlib import Path


NAME_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
REQUIRED_REFERENCES = (
    "references/acceptance-scenarios.md",
    "references/arcubase-runtime-gotchas.md",
    "references/command-contracts.md",
    "references/local-validation.md",
    "references/octopus-client.md",
)
OPENAI_INTERFACE_KEYS = (
    "display_name",
    "short_description",
    "default_prompt",
)


class ValidationError(Exception):
    pass


def read_text(path):
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ValidationError(f"cannot read {path}: {exc}") from exc


def parse_frontmatter(skill_file):
    lines = read_text(skill_file).splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValidationError("SKILL.md must start with YAML frontmatter")

    try:
        closing_index = next(
            index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"
        )
    except StopIteration as exc:
        raise ValidationError("SKILL.md frontmatter is not closed") from exc

    return lines[1:closing_index]


def scalar_value(frontmatter, key):
    prefix = f"{key}:"
    values = [line[len(prefix) :].strip() for line in frontmatter if line.startswith(prefix)]
    if len(values) != 1 or not values[0]:
        raise ValidationError(f"SKILL.md requires one non-empty {key} field")

    value = values[0]
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1].strip()
    if not value:
        raise ValidationError(f"SKILL.md requires one non-empty {key} field")
    return value


def validate_openai_metadata(skill_dir):
    metadata_file = skill_dir / "agents" / "openai.yaml"
    if not metadata_file.exists():
        return

    content = read_text(metadata_file)
    if not re.search(r"^interface\s*:\s*$", content, re.MULTILINE):
        raise ValidationError("agents/openai.yaml requires an interface mapping")
    for key in OPENAI_INTERFACE_KEYS:
        if not re.search(rf"^\s+{re.escape(key)}\s*:\s*\S", content, re.MULTILINE):
            raise ValidationError(f"agents/openai.yaml requires {key}")


def validate_skill(skill_dir):
    if not skill_dir.is_dir():
        raise ValidationError(f"skill directory does not exist: {skill_dir}")

    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        raise ValidationError("missing SKILL.md")

    frontmatter = parse_frontmatter(skill_file)
    name = scalar_value(frontmatter, "name")
    description = scalar_value(frontmatter, "description")

    if len(name) > 64 or not NAME_PATTERN.fullmatch(name):
        raise ValidationError("name must use lowercase letters, numbers, and single hyphens")
    if name != skill_dir.name:
        raise ValidationError(f"name {name!r} must match directory {skill_dir.name!r}")
    if len(description) > 1024:
        raise ValidationError("description must be at most 1024 characters")

    for relative_path in REQUIRED_REFERENCES:
        if not (skill_dir / relative_path).is_file():
            raise ValidationError(f"missing required file: {relative_path}")

    validate_openai_metadata(skill_dir)


def main(argv):
    if len(argv) != 2:
        print("Usage: validate_skill.py SKILL_DIRECTORY", file=sys.stderr)
        return 2

    skill_dir = Path(argv[1]).expanduser().resolve()
    try:
        validate_skill(skill_dir)
    except ValidationError as exc:
        print(f"Validation error: {exc}", file=sys.stderr)
        return 1

    print(f"Skill is valid: {skill_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
