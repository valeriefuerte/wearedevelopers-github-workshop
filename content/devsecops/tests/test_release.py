import io
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error
from urllib.parse import urlsplit

import yaml

KIT = Path(__file__).resolve().parents[1]
WORKFLOW = yaml.load((KIT / "starter/release-simulation.yml").read_text(), Loader=yaml.BaseLoader)
GUARD = WORKFLOW["jobs"]["guard"]["steps"][0]["run"]
SHA = "a" * 40
ENV = {
    "GITHUB_REF": "refs/heads/main",
    "GITHUB_EVENT_NAME": "workflow_dispatch",
    "GITHUB_API_URL": "https://api.example.invalid",
    "GITHUB_REPOSITORY": "learner/pets",
    "GITHUB_SHA": SHA,
    "GH_TOKEN": "unit-test-placeholder",
}


class ReleaseGuardTests(unittest.TestCase):
    def setUp(self):
        self.responses = {
            "/git/ref/heads/main": {"object": {"sha": SHA}},
            "/environments/workshop-demo": {
                "can_admins_bypass": False,
                "protection_rules": [{"type": "required_reviewers", "reviewers": [{"id": 1}]}],
                "deployment_branch_policy": {
                    "protected_branches": False, "custom_branch_policies": True},
            },
            "/environments/workshop-demo/deployment-branch-policies": {
                "total_count": 1, "branch_policies": [{"name": "main", "type": "branch"}]},
        }

    def execute(self, env=None, responses=None):
        data = self.responses if responses is None else responses
        def urlopen(request, timeout):
            self.assertEqual(timeout, 30)
            path = urlsplit(request.full_url).path.removeprefix("/repos/learner/pets")
            if path not in data:
                raise urllib.error.HTTPError(request.full_url, 404, "Not found", None, io.BytesIO())
            return io.StringIO(json.dumps(data[path]))
        with patch.dict(os.environ, ENV | (env or {}), clear=True):
            with patch("urllib.request.urlopen", side_effect=urlopen):
                exec(compile(GUARD, "release-inline-guard", "exec"), {})

    def test_current_main_push_and_dispatch_pass(self):
        self.execute()
        self.execute({"GITHUB_EVENT_NAME": "push"})

    def test_non_main_and_pr_events_fail(self):
        for env in ({"GITHUB_REF": "refs/heads/exercise/release"},
                    {"GITHUB_REF": "refs/tags/main"},
                    {"GITHUB_EVENT_NAME": "pull_request"}):
            with self.subTest(env=env), self.assertRaises(SystemExit):
                self.execute(env)

    def test_stale_revision_fails(self):
        with self.assertRaisesRegex(SystemExit, "Stale revision"):
            self.execute({"GITHUB_SHA": "b" * 40})

    def test_missing_environment_or_api_failure_fails(self):
        del self.responses["/environments/workshop-demo"]
        with self.assertRaises(urllib.error.HTTPError) as raised:
            self.execute()
        raised.exception.close()

    def test_missing_or_empty_reviewers_fail(self):
        for rules in ([], [{"type": "required_reviewers", "reviewers": []}]):
            with self.subTest(rules=rules):
                self.responses["/environments/workshop-demo"]["protection_rules"] = rules
                with self.assertRaisesRegex(SystemExit, "required reviewers"):
                    self.execute()

    def test_admin_bypass_fails(self):
        self.responses["/environments/workshop-demo"]["can_admins_bypass"] = True
        with self.assertRaisesRegex(SystemExit, "administrator bypass"):
            self.execute()

    def test_unrestricted_and_protected_branch_modes_fail(self):
        for policy in (None, {}, {"protected_branches": True, "custom_branch_policies": False}):
            with self.subTest(policy=policy):
                self.responses["/environments/workshop-demo"]["deployment_branch_policy"] = policy
                with self.assertRaisesRegex(SystemExit, "selected branches"):
                    self.execute()

    def test_wildcard_tag_extra_and_missing_branch_rules_fail(self):
        for branches in (
                {"total_count": 0, "branch_policies": []},
                {"total_count": 1, "branch_policies": [{"name": "*", "type": "branch"}]},
                {"total_count": 1, "branch_policies": [{"name": "main", "type": "tag"}]},
                {"total_count": 2, "branch_policies": [{"name": "main", "type": "branch"}]}):
            with self.subTest(branches=branches):
                self.responses["/environments/workshop-demo/deployment-branch-policies"] = branches
                with self.assertRaisesRegex(SystemExit, "Only the main branch"):
                    self.execute()

    def test_same_guard_repeats_after_approval(self):
        self.assertEqual(WORKFLOW["jobs"]["release"]["steps"][0]["run"], GUARD)
        self.execute()
        self.responses["/git/ref/heads/main"]["object"]["sha"] = "b" * 40
        with self.assertRaisesRegex(SystemExit, "Stale revision"):
            self.execute()


class ReleaseArtifactTests(unittest.TestCase):
    def test_prerequisites_receipt_and_checksum_are_bound_to_the_run(self):
        jobs = WORKFLOW["jobs"]
        for name in ("release-api-tests", "release-client-build"):
            with self.subTest(job=name):
                self.assertEqual(
                    "${{ github.sha }}",
                    jobs[name]["steps"][0]["with"]["ref"],
                )

        release = jobs["release"]
        self.assertEqual(
            {"guard", "release-api-tests", "release-client-build"},
            set(release["needs"]),
        )
        for name in release["needs"]:
            self.assertIn(f"needs.{name}.result == 'success'", release["if"])
        self.assertEqual("workshop-demo", release["environment"])
        self.assertEqual(GUARD, release["steps"][0]["run"])

        receipt_step = next(
            step for step in release["steps"]
            if step.get("name") == "Write simulation receipt"
        )
        with tempfile.TemporaryDirectory(prefix="pets-release-receipt-") as temporary:
            summary = Path(temporary) / "summary.md"
            env = ENV | {
                "GITHUB_SERVER_URL": "https://github.example",
                "GITHUB_RUN_ID": "456",
                "GITHUB_RUN_ATTEMPT": "2",
                "GITHUB_STEP_SUMMARY": str(summary),
            }
            original_cwd = Path.cwd()
            with patch.dict(os.environ, env, clear=True):
                try:
                    os.chdir(temporary)
                    exec(compile(receipt_step["run"], "release-receipt", "exec"), {})
                finally:
                    os.chdir(original_cwd)

            receipt_path = Path(temporary) / "receipt.json"
            receipt = json.loads(receipt_path.read_text())
            self.assertEqual("workshop-simulation-no-deployment", receipt["kind"])
            self.assertEqual(SHA, receipt["commit"])
            self.assertEqual("refs/heads/main", receipt["ref"])
            self.assertEqual(
                "https://github.example/learner/pets/actions/runs/456",
                receipt["run"],
            )
            self.assertEqual("2", receipt["attempt"])
            self.assertEqual(
                ["guard", "release-api-tests", "release-client-build"],
                receipt["prerequisites"],
            )
            self.assertEqual("workshop-demo", receipt["environment"])
            checksum = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
            self.assertEqual(
                f"{checksum}  receipt.json\n",
                (Path(temporary) / "receipt.sha256").read_text(),
            )

        artifact = next(
            step for step in release["steps"]
            if step.get("uses", "").startswith("actions/upload-artifact@")
        )
        self.assertIn("receipt.json", artifact["with"]["path"])
        self.assertIn("receipt.sha256", artifact["with"]["path"])
        self.assertEqual("3", artifact["with"]["retention-days"])
        identity = next(
            step for step in release["steps"]
            if step.get("name") == "Record artifact identity"
        )
        self.assertIn("steps.receipt.outputs.artifact-id", identity["env"]["ARTIFACT_ID"])
        self.assertIn("steps.receipt.outputs.artifact-digest", identity["env"]["ARTIFACT_DIGEST"])
        self.assertIn("receipt.json SHA-256", receipt_step["run"])
        self.assertIn("Uploaded archive digest", identity["run"])


if __name__ == "__main__":
    unittest.main()
