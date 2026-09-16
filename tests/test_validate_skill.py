import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
SOURCE_SKILL_DIR = PROJECT_DIR / "skills" / "workbench-app-development"
VALIDATOR = PROJECT_DIR / "scripts" / "validate_skill.py"


class ValidateSkillTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.skill_dir = Path(self.temp_dir.name) / "workbench-app-development"
        shutil.copytree(SOURCE_SKILL_DIR, self.skill_dir)

    def run_validator(self):
        return subprocess.run(
            [sys.executable, str(VALIDATOR), str(self.skill_dir)],
            capture_output=True,
            text=True,
            check=False,
        )

    def replace_skill_line(self, prefix, replacement):
        skill_file = self.skill_dir / "SKILL.md"
        lines = skill_file.read_text(encoding="utf-8").splitlines()
        updated = [replacement if line.startswith(prefix) else line for line in lines]
        skill_file.write_text("\n".join(updated) + "\n", encoding="utf-8")

    def test_valid_skill_passes(self):
        result = self.run_validator()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Skill is valid", result.stdout)

    def test_name_must_match_parent_directory(self):
        self.replace_skill_line("name:", "name: different-skill")

        result = self.run_validator()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must match directory", result.stderr)

    def test_description_is_required(self):
        self.replace_skill_line("description:", "description:")

        result = self.run_validator()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("description", result.stderr)

    def test_required_reference_must_exist(self):
        (self.skill_dir / "references" / "command-contracts.md").unlink()

        result = self.run_validator()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("references/command-contracts.md", result.stderr)

    def test_runtime_gotchas_reference_must_exist(self):
        (self.skill_dir / "references" / "arcubase-runtime-gotchas.md").unlink()

        result = self.run_validator()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("references/arcubase-runtime-gotchas.md", result.stderr)

    def test_optional_openai_metadata_is_checked_when_present(self):
        metadata_file = self.skill_dir / "agents" / "openai.yaml"
        lines = metadata_file.read_text(encoding="utf-8").splitlines()
        metadata_file.write_text(
            "\n".join(line for line in lines if "default_prompt:" not in line) + "\n",
            encoding="utf-8",
        )

        result = self.run_validator()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("default_prompt", result.stderr)


if __name__ == "__main__":
    unittest.main()
