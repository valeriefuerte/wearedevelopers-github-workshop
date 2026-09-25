import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile

import test_helper


class PackagingTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="pets-template-package-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.repo = self.root / "template"
        self.repo.mkdir()
        files = test_helper.git(test_helper.SOURCE, "ls-files", "--cached", "--others",
                                "--exclude-standard", "-z").decode().split("\0")
        for name in sorted(set(files) - {""}):
            target = self.repo / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(test_helper.SOURCE / name, target)
        test_helper.git(self.repo, "init", "-q", "--initial-branch=main")

    def build(self, output, refresh=False):
        command = [sys.executable, str(self.repo / "content/devsecops/scripts/build-kit.py"),
                   "--output-dir", str(output)]
        if refresh:
            command.append("--refresh-manifest")
        return subprocess.run(command, cwd=self.repo, env=test_helper.ENV,
                              capture_output=True, text=True)

    def test_full_archive_is_reproducible_and_matches_inventory(self):
        first = self.build(self.root / "first", refresh=True)
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        second = self.build(self.root / "second")
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
        version = json.loads((self.repo / "template-source.json").read_text())["version"]
        name = f"pets-devsecops-workshop-template-{version}.zip"
        archive = self.root / "first" / name
        self.assertEqual(archive.read_bytes(), (self.root / "second" / name).read_bytes())
        with ZipFile(archive) as bundle:
            prefix = f"pets-devsecops-workshop-template-{version}/"
            manifest = json.loads(bundle.read(prefix + "template-source.json"))
            self.assertEqual(set(bundle.namelist()),
                             {prefix + p for p in manifest["inventory"]} | {prefix + "template-source.json"})
            for path, checksum in manifest["inventory"].items():
                self.assertEqual(hashlib.sha256(bundle.read(prefix + path)).hexdigest(), checksum, path)
            active = {p for p in manifest["inventory"] if p.startswith(".github/workflows/")}
            self.assertEqual(active, {".github/workflows/ci.yml", ".github/workflows/dependency-review.yml"})
            self.assertIn("app/server/dogshelter.db", manifest["inventory"])
            self.assertIn("content/devsecops/take-home/4-workload-identity.md", manifest["inventory"])
            for path in ("app/scripts/start-app.sh", "app/scripts/seed-database.ps1"):
                expected_executable = bool((self.repo / path).stat().st_mode & 0o111)
                actual_executable = bool((bundle.getinfo(prefix + path).external_attr >> 16) & 0o111)
                self.assertEqual(actual_executable, expected_executable)

    def test_stale_inventory_and_baseline_drift_fail_explicitly(self):
        self.assertEqual(self.build(self.root / "first", refresh=True).returncode, 0)
        (self.repo / "README.md").write_text("Changed after inventory\n")
        stale = self.build(self.root / "stale")
        self.assertNotEqual(stale.returncode, 0)
        self.assertIn("Inventory is stale", stale.stderr)
        app = self.repo / "app/server/app.py"
        app.write_text(app.read_text().replace("debug=True", "debug=False"))
        drift = self.build(self.root / "drift", refresh=True)
        self.assertNotEqual(drift.returncode, 0)
        self.assertIn("Training baseline drift", drift.stderr)

    def test_output_inside_checkout_is_rejected(self):
        result = self.build(self.repo / "output", refresh=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("outside the template checkout", result.stderr)


if __name__ == "__main__":
    unittest.main()
