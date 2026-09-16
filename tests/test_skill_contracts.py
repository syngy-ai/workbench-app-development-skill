import unittest
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
SKILL_DIR = PROJECT_DIR / "skills" / "workbench-app-development"
SKILL_FILE = SKILL_DIR / "SKILL.md"
GOTCHAS_FILE = SKILL_DIR / "references" / "arcubase-runtime-gotchas.md"
LOCAL_VALIDATION_FILE = SKILL_DIR / "references" / "local-validation.md"
OCTOPUS_CLIENT_FILE = SKILL_DIR / "references" / "octopus-client.md"
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

    def test_skill_requires_local_real_environment_acceptance_before_build(self):
        skill = SKILL_FILE.read_text(encoding="utf-8")

        self.assertIn(
            "[local validation contract](references/local-validation.md)",
            skill,
        )
        local_validation = skill.index("local validation contract")
        production_build = skill.index("production build")
        remote_project = skill.index("remote Workbench project")
        self.assertLess(local_validation, production_build)
        self.assertLess(local_validation, remote_project)

    def test_local_validation_contract_has_real_data_and_human_gate(self):
        self.assertTrue(
            LOCAL_VALIDATION_FILE.is_file(),
            "local validation needs a focused contract reference",
        )
        contract = LOCAL_VALIDATION_FILE.read_text(encoding="utf-8")

        self.assertIn("WORKBENCH_REQUIRED_TEAM_ID=<teamId>", contract)
        self.assertIn("npm run dev", contract)
        self.assertIn("real backend rows", contract)
        self.assertIn("explicitly approves publishing", contract)
        self.assertIn("does not waive this checkpoint", contract)
        self.assertIn("explicitly waives interactive local acceptance", contract)

    def test_local_arcubase_codegen_uses_current_supported_flags(self):
        contract = LOCAL_VALIDATION_FILE.read_text(encoding="utf-8")

        self.assertIn("--app-id <appId>", contract)
        self.assertIn("--team-id <teamId>", contract)
        self.assertIn("Do not pass `--web-url`", contract)

    def test_acceptance_scenario_covers_local_gate_and_write_safety(self):
        acceptance = ACCEPTANCE_FILE.read_text(encoding="utf-8")

        self.assertIn("Local real-data acceptance before publish", acceptance)
        self.assertIn(
            "stops before the production build and remote project creation",
            acceptance,
        )
        self.assertIn("does not mutate real records without authorization", acceptance)

    def test_skill_routes_host_user_api_requirements_to_octopus(self):
        skill = SKILL_FILE.read_text(encoding="utf-8")

        self.assertIn(
            "[Octopus client contract](references/octopus-client.md)",
            skill,
        )
        self.assertIn("users, teams, members, organization", skill)

    def test_octopus_contract_selects_package_facade_and_data_boundary(self):
        self.assertTrue(
            OCTOPUS_CLIENT_FILE.is_file(),
            "Host user API work needs a focused Octopus client reference",
        )
        contract = OCTOPUS_CLIENT_FILE.read_text(encoding="utf-8")

        self.assertIn("--features=octopus", contract)
        self.assertIn("@syngy/octopus-client", contract)
        self.assertIn("createSyngyClients().octopus.api", contract)
        self.assertIn("v1TeamsOrganizationMembersSearchCreate", contract)
        self.assertIn("current installed type declarations", contract)
        self.assertIn("must use the `arcubase` feature", contract)
        self.assertIn("never its generic Arcubase proxy methods", contract)

    def test_acceptance_scenario_covers_octopus_host_api_selection(self):
        acceptance = ACCEPTANCE_FILE.read_text(encoding="utf-8")

        self.assertIn("Host directory plus persisted business data", acceptance)
        self.assertIn("selects both `octopus` and `arcubase`", acceptance)
        self.assertIn("refuses the generic Arcubase proxy shortcut", acceptance)


if __name__ == "__main__":
    unittest.main()
