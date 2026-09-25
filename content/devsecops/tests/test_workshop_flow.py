import json
from pathlib import Path
import re
import unittest

KIT = Path(__file__).resolve().parents[1]
ROOT = KIT.parents[1]


def content(path):
    return (KIT / path).read_text()


class WorkshopFlowTests(unittest.TestCase):
    def test_agenda_is_contiguous_and_totals_120_minutes(self):
        agenda = content("README.md")
        rows = re.findall(
            r"^\| \[(\d)\. [^|]+\]\([^)]+\) \| (\d{2,3})-(\d{2,3}) \| (\d+) \|",
            agenda,
            re.MULTILINE,
        )
        self.assertEqual(list(range(9)), [int(row[0]) for row in rows])
        minute = 0
        for _, start, end, budget in rows:
            self.assertEqual(minute, int(start))
            self.assertEqual(int(budget), int(end) - int(start))
            minute = int(end)
        self.assertEqual(120, minute)
        self.assertIn("Budget: 24 minutes", content("6-merge-policy.md"))
        self.assertIn("Budget: 24 minutes", content("7-delivery-and-response.md"))

    def test_lab_4_leaves_the_observed_failure_open_for_lab_6(self):
        lab4 = content("4-dependencies.md")
        lab6 = content("6-merge-policy.md")
        self.assertIn("PyJWT==2.3.0", lab4)
        self.assertNotIn("PyJWT==2.14.0", lab4)
        self.assertIn("Leave the dependency-training PR open and failing for Lab 6", lab4)
        self.assertIn("Do not repair the fixture in Lab 4", lab4)
        self.assertIn("exercise/dependency-policy", lab4)
        self.assertIn("exercise/dependency-policy", lab6)
        self.assertIn("PyJWT==2.14.0", lab6)

    def test_lab_6_enforces_the_exact_solo_merge_policy(self):
        lab6 = content("6-merge-policy.md")
        for required in (
            "`workshop-main`",
            "Enforcement status** to **Active",
            "leave the bypass list empty",
            "add only the inclusion pattern `main`",
            "required approvals to **0**",
            "code-owner review and last-push approval off",
            "`api-tests`",
            "`client-build`",
            "`dependency-review`",
            "up to date before merging",
            "Do not enable merge queue",
            "**High or higher**",
            "Close the dependency-training PR **without merging it**",
            "Merge only safe application work",
            "safe merge commit SHA",
            "`py/flask-debug` alert is closed/fixed",
        ):
            with self.subTest(required=required):
                self.assertIn(required, lab6)
        self.assertIn("A missing, queued, cancelled, or unrelated failing check does not prove", lab6)
        self.assertIn("blocked specifically by the required failed `dependency-review` check", lab6)

    def test_lab_7_configures_environment_then_installs_through_reviewed_pr(self):
        lab7 = content("7-delivery-and-response.md")
        self.assertLess(
            lab7.index("## 1. Configure the environment before installing"),
            lab7.index("## 2. Review and install the release workflow through a PR"),
        )
        for required in (
            "add your own account",
            "Leave **Prevent self-review** off",
            "not production separation of duties",
            "Disable **Allow administrators to bypass configured protection rules**",
            "exactly one **Branch** rule named `main`",
            "Add no environment secrets, cloud credentials, or variables",
            "exercise/release-simulation",
            "open a PR against your own `main`",
            "normal `workshop-main` ruleset",
            "`guard`, `release-api-tests`, and `release-client-build`",
            "waiting for approval",
            "**before** approving it",
            "run URL and attempt",
            "artifact ID and URL",
            "checksum for `receipt.json`",
            "uploaded archive digest",
            "sha256sum -c receipt.sha256",
            "Optional follow-up: reject a non-`main` dispatch",
            "assign an owner",
            "**patch**, **revert**, or **investigation**",
        ):
            with self.subTest(required=required):
                self.assertIn(required, lab7)
        self.assertIn("receipt checksum and archive digest are different values", lab7)
        self.assertIn("do not approve", lab7.lower())

    def test_core_labs_are_learner_work_not_facilitator_repository_steps(self):
        for path in ("6-merge-policy.md", "7-delivery-and-response.md"):
            text = content(path).lower()
            self.assertIn("your own learner repository", text)
            for obsolete in (
                "presenter demonstrates",
                "inspect the presenter's repository",
                "participants do not need an environment",
                "individual configuration belongs to take-home",
                "watching the demonstration",
            ):
                with self.subTest(path=path, obsolete=obsolete):
                    self.assertNotIn(obsolete, text)

    def test_evidence_and_closing_capture_individual_live_outcomes(self):
        evidence = content("evidence.md")
        wrap_up = content("8-wrap-up.md")
        self.assertIn("## Individual live work", evidence)
        self.assertIn("Blocked dependency merge (Lab 6)", evidence)
        self.assertIn("Approved release (Lab 7)", evidence)
        self.assertIn("Examples, expected-result tables, preserved author receipts, recordings", evidence)
        self.assertIn("your own repository", wrap_up)
        self.assertIn("actual results", wrap_up)
        self.assertIn("Pending", wrap_up)
        self.assertNotIn("demonstrations you watched", wrap_up.lower())

    def test_incident_card_requires_owner_evidence_and_action(self):
        card = content("fixtures/incident-card.md")
        self.assertIn("Assign a specific owner", card)
        self.assertIn("Identify evidence still needed", card)
        for action in ("**patch**", "**revert**", "**investigation**"):
            with self.subTest(action=action):
                self.assertIn(action, card)
        self.assertIn("replacement revision", card)

    def test_distributed_template_keeps_only_two_core_workflows_active(self):
        active = ROOT / ".github/workflows"
        self.assertEqual(
            {"ci.yml", "dependency-review.yml"},
            {path.name for path in active.iterdir()},
        )
        self.assertTrue((KIT / "starter/release-simulation.yml").is_file())
        self.assertFalse((active / "release-simulation.yml").exists())
        manifest = json.loads((KIT / "workshop-kit.json").read_text())
        self.assertEqual(["ci.yml", "dependency-review.yml"], manifest["core_workflows"])
        self.assertIn("release-simulation.yml", manifest["optional_workflows"])

    def test_candidate_version_and_readiness_remain_honest(self):
        kit = json.loads((KIT / "workshop-kit.json").read_text())
        template = json.loads((ROOT / "template-source.json").read_text())
        validation = json.loads((KIT / "fixtures/template-validation.json").read_text())
        readiness = content("readiness.md").lower()
        self.assertEqual("0.2.0", kit["version"])
        self.assertEqual(kit["version"], template["version"])
        self.assertEqual(kit["version"], validation["template_version"])
        self.assertIn("passed", validation["status"])
        self.assertFalse(validation["local_checks"]["codespaces_run"])
        self.assertIn("pending", validation["candidate_live_gates"]["template_main_ci"])
        self.assertIn("unverified", validation["candidate_live_gates"]["learner_timing"])
        self.assertIn(
            "unverified",
            validation["candidate_live_gates"]["learner_ruleset_release_artifact"],
        )
        self.assertIn("no 0.2.0 github release or learner rehearsal is claimed", readiness)
        self.assertIn("not a freshly generated learner copy or candidate 0.2.0 ci result", readiness)


if __name__ == "__main__":
    unittest.main()
