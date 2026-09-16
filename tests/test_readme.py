import unittest
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
README = PROJECT_DIR / "README.md"


class ReadmeTests(unittest.TestCase):
    def test_documents_public_commands(self):
        content = README.read_text(encoding="utf-8")
        commands = (
            "./scripts/install-local.sh codex",
            "./scripts/install-local.sh claude",
            "./scripts/install-local.sh workbuddy",
            "./scripts/install-local.sh all",
            "./scripts/validate.sh",
            "./scripts/test.sh",
        )

        for command in commands:
            with self.subTest(command=command):
                self.assertIn(command, content)

    def test_documents_client_skill_directories(self):
        content = README.read_text(encoding="utf-8")
        directories = (
            "~/.codex/skills",
            "~/.claude/skills",
            "~/.workbuddy/skills",
        )

        for directory in directories:
            with self.subTest(directory=directory):
                self.assertIn(directory, content)


if __name__ == "__main__":
    unittest.main()
