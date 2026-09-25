import importlib.util
import json
import shutil
import subprocess
import unittest

import test_helper

SPEC = importlib.util.spec_from_file_location(
    "template_validator", test_helper.KIT / "scripts/validate-kit.py")
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class TemplateTests(unittest.TestCase):
    def setUp(self):
        self.fixture = test_helper.HelperTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.repo = self.fixture.repo
        self.kit = self.repo / "content/devsecops"
        shutil.copytree(test_helper.KIT, self.kit,
                        ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"))
        workflow_dir = self.repo / ".github/workflows"
        workflow_dir.mkdir(parents=True)
        for name in ("ci.yml", "dependency-review.yml"):
            shutil.copyfile(self.kit / "starter" / name, workflow_dir / name)
        for name in ("LICENSE", "template-source.json", ".github/CODEOWNERS"):
            shutil.copyfile(test_helper.SOURCE / name, self.repo / name)
        test_helper.git(self.repo, "add", ".")
        test_helper.git(self.repo, "commit", "-qm", "Independent template copy")

    def test_complete_independent_history_copy(self):
        VALIDATOR.validate_installed_files(self.repo, self.kit)
        original_object = subprocess.run(
            ["git", "-C", str(self.repo), "cat-file", "-e", test_helper.MANIFEST["source_commit"]],
            env=test_helper.ENV, capture_output=True)
        self.assertNotEqual(original_object.returncode, 0)
        before = test_helper.snapshot(self.repo)
        self.fixture.run_helper("--check")
        self.fixture.run_helper("--apply")
        self.assertEqual(before, test_helper.snapshot(self.repo))
        self.assertTrue((self.kit / "take-home/4-workload-identity.md").is_file())

    def test_missing_required_workflow_fails(self):
        (self.repo / ".github/workflows/ci.yml").unlink()
        with self.assertRaisesRegex(ValueError, "Exactly two"):
            VALIDATOR.validate_installed_files(self.repo, self.kit)

    def test_different_workflow_fails(self):
        (self.repo / ".github/workflows/ci.yml").write_text("name: Not the tested CI\n")
        with self.assertRaisesRegex(ValueError, "differs"):
            VALIDATOR.validate_installed_files(self.repo, self.kit)

    def test_optional_workflow_not_active(self):
        shutil.copyfile(self.kit / "starter/release-simulation.yml",
                        self.repo / ".github/workflows/release-simulation.yml")
        with self.assertRaisesRegex(ValueError, "Exactly two"):
            VALIDATOR.validate_installed_files(self.repo, self.kit)

    def test_linked_workflow_fails(self):
        path = self.repo / ".github/workflows/ci.yml"
        path.unlink()
        path.symlink_to(self.kit / "starter/ci.yml")
        with self.assertRaisesRegex(ValueError, "Invalid installed"):
            VALIDATOR.validate_installed_files(self.repo, self.kit)

    def test_missing_application_fails(self):
        (self.repo / "app/server/app.py").unlink()
        with self.assertRaisesRegex(ValueError, "Missing template"):
            VALIDATOR.validate_installed_files(self.repo, self.kit)

    def test_inherited_owner_fails(self):
        (self.repo / ".github/CODEOWNERS").write_text("* @original-maintainer\n")
        with self.assertRaisesRegex(ValueError, "inherit"):
            VALIDATOR.validate_installed_files(self.repo, self.kit)

    def test_recovery_refuses_source_and_template_origins(self):
        for origin in ("frye/pets-devsecops-workshop", "frye/pets-devsecops-workshop-template"):
            with self.subTest(origin=origin):
                test_helper.git(self.repo, "remote", "set-url", "origin", "https://github.com/" + origin)
                self.fixture.run_helper(ok=False)

    def test_empty_fingerprints_refuse_recovery(self):
        (self.kit / "baseline.sha256").write_text("")
        result = subprocess.run(
            [test_helper.BASH, (self.kit / "scripts/prepare-devsecops.sh").as_posix(),
             "--repo", self.repo.as_posix(), "--check"],
            env=test_helper.ENV, capture_output=True)
        self.assertNotEqual(result.returncode, 0)

    def test_crlf_manifest_accepts_baseline_but_not_drift(self):
        fingerprints = self.kit / "baseline.sha256"
        fingerprints.write_bytes(fingerprints.read_bytes().replace(b"\r\n", b"\n")
                                 .replace(b"\n", b"\r\n"))
        test_helper.git(self.repo, "add", ".")
        test_helper.git(self.repo, "commit", "--allow-empty", "-qm", "CRLF manifest")
        command = [test_helper.BASH, (self.kit / "scripts/prepare-devsecops.sh").as_posix(),
                   "--repo", self.repo.as_posix(), "--check"]
        before = test_helper.snapshot(self.repo)
        result = subprocess.run(command, env=test_helper.ENV, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(before, test_helper.snapshot(self.repo))
        app = self.repo / "app/server/app.py"
        app.write_bytes(app.read_bytes() + b"\n")
        self.assertNotEqual(subprocess.run(command, env=test_helper.ENV, capture_output=True).returncode, 0)


if __name__ == "__main__":
    unittest.main()
