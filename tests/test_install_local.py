import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
SKILL_NAME = "workbench-app-development"
CLIENT_PATHS = {
    "codex": Path(".codex") / "skills" / SKILL_NAME,
    "claude": Path(".claude") / "skills" / SKILL_NAME,
    "workbuddy": Path(".workbuddy") / "skills" / SKILL_NAME,
}


class InstallLocalTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.temp_root = Path(self.temp_dir.name)

    def new_home(self, name):
        home = self.temp_root / name
        home.mkdir()
        return home

    def run_installer(self, *arguments, home, project_dir=PROJECT_DIR):
        environment = os.environ.copy()
        environment["HOME"] = str(home)
        environment.pop("CODEX_HOME", None)
        return subprocess.run(
            [str(project_dir / "scripts" / "install-local.sh"), *arguments],
            cwd=project_dir,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )

    def assert_installed_clients(self, home, expected_clients):
        for client, relative_path in CLIENT_PATHS.items():
            installed = (home / relative_path).is_dir()
            self.assertEqual(
                installed,
                client in expected_clients,
                f"unexpected installation state for {client} under {home}",
            )

    def copy_project(self, name):
        project_copy = self.temp_root / name
        project_copy.mkdir()
        shutil.copytree(PROJECT_DIR / "scripts", project_copy / "scripts")
        shutil.copytree(PROJECT_DIR / "skills", project_copy / "skills")
        return project_copy

    def test_each_target_installs_only_its_client(self):
        for client in CLIENT_PATHS:
            with self.subTest(client=client):
                home = self.new_home(f"home-{client}")

                result = self.run_installer(client, home=home)

                self.assertEqual(result.returncode, 0, result.stderr)
                self.assert_installed_clients(home, {client})

    def test_all_installs_every_client(self):
        home = self.new_home("home-all")

        result = self.run_installer("all", home=home)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assert_installed_clients(home, set(CLIENT_PATHS))

    def test_help_succeeds_without_writing(self):
        home = self.new_home("home-help")

        result = self.run_installer("--help", home=home)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("codex|claude|workbuddy|all", result.stdout)
        self.assert_installed_clients(home, set())

    def test_invalid_arguments_fail_without_writing(self):
        cases = ((), ("unknown",), ("codex", "extra"))
        for index, arguments in enumerate(cases):
            with self.subTest(arguments=arguments):
                home = self.new_home(f"home-invalid-{index}")

                result = self.run_installer(*arguments, home=home)

                self.assertNotEqual(result.returncode, 0)
                self.assert_installed_clients(home, set())

    def test_validation_failure_prevents_every_write(self):
        project_copy = self.copy_project("broken-project")
        (project_copy / "skills" / SKILL_NAME / "SKILL.md").unlink()
        home = self.new_home("home-broken")

        result = self.run_installer("all", home=home, project_dir=project_copy)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing SKILL.md", result.stderr)
        self.assert_installed_clients(home, set())

    def test_installed_package_contains_shared_and_codex_files(self):
        home = self.new_home("home-complete")

        result = self.run_installer("codex", home=home)

        self.assertEqual(result.returncode, 0, result.stderr)
        destination = home / CLIENT_PATHS["codex"]
        expected_files = (
            "SKILL.md",
            "references/acceptance-scenarios.md",
            "references/command-contracts.md",
            "agents/openai.yaml",
        )
        for relative_path in expected_files:
            self.assertTrue((destination / relative_path).is_file(), relative_path)

    def test_reinstall_refreshes_changed_source_files(self):
        project_copy = self.copy_project("refresh-project")
        home = self.new_home("home-refresh")
        first_result = self.run_installer("codex", home=home, project_dir=project_copy)
        self.assertEqual(first_result.returncode, 0, first_result.stderr)

        marker = "\n<!-- refreshed installation -->\n"
        source_skill = project_copy / "skills" / SKILL_NAME / "SKILL.md"
        source_skill.write_text(source_skill.read_text(encoding="utf-8") + marker, encoding="utf-8")

        second_result = self.run_installer("codex", home=home, project_dir=project_copy)

        self.assertEqual(second_result.returncode, 0, second_result.stderr)
        installed_skill = home / CLIENT_PATHS["codex"] / "SKILL.md"
        self.assertIn(marker.strip(), installed_skill.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
