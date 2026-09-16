import unittest
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
SKILL_DIR = PROJECT_DIR / "skills" / "workbench-app-development"
SKILL_FILE = SKILL_DIR / "SKILL.md"
GOTCHAS_FILE = SKILL_DIR / "references" / "arcubase-runtime-gotchas.md"
ACCEPTANCE_FILE = SKILL_DIR / "references" / "acceptance-scenarios.md"


class SkillContractTests(unittest.TestCase):
    def read_gotchas(self):
        self.assertTrue(
            GOTCHAS_FILE.is_file(),
            "SKILL.md needs a focused Arcubase runtime gotchas reference",
        )
        return GOTCHAS_FILE.read_text(encoding="utf-8")

    def test_skill_routes_datetime_and_serial_work_to_runtime_gotchas(self):
        skill = SKILL_FILE.read_text(encoding="utf-8")

        self.assertIn(
            "[Arcubase runtime gotchas](references/arcubase-runtime-gotchas.md)",
            skill,
        )

    def test_datetime_contract_requires_epoch_seconds_and_readback(self):
        gotchas = self.read_gotchas()

        self.assertIn("integer epoch seconds", gotchas)
        self.assertIn("epoch milliseconds", gotchas)
        self.assertIn("date-only and ISO strings", gotchas)
        self.assertIn("toEpochSeconds", gotchas)
        self.assertIn("read the first record back", gotchas)

    def test_serial_contract_forbids_guessing_or_silent_semantic_changes(self):
        gotchas = self.read_gotchas()

        self.assertIn("Do not guess `perdefinedFormat`", gotchas)
        self.assertIn("explicitly accepts a pure global serial", gotchas)
        self.assertIn('"length": 6', gotchas)
        self.assertIn('"reset": "no"', gotchas)

    def test_acceptance_scenario_covers_both_failures(self):
        acceptance = ACCEPTANCE_FILE.read_text(encoding="utf-8")

        self.assertIn("Datetime writes and undocumented serial formats", acceptance)
        self.assertIn("never silently changes identifier semantics", acceptance)


if __name__ == "__main__":
    unittest.main()
