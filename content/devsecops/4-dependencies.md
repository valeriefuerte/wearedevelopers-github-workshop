# 4. Observe a vulnerable dependency change

| [Previous: code scanning](3-code-scanning.md) | [Next: secrets](5-secrets.md) |
|:---|---:|

Budget: 15 minutes. A volunteer proposes a package change. Your review should catch a known vulnerability before it reaches `main`.

## Why it matters

Dependency review evaluates packages a PR introduces. Dependabot alerts monitor dependencies already present, and version-update PRs help keep them current. You still need to test each update.

> [!WARNING]
> This exercise uses an unused manifest. Never install its packages or merge its PR. The files in this kit are inert `.txt` handouts; only your isolated exercise branch gets a real `requirements.txt`.

## Try it

1. Return briefly to your safe application PR and record its current results. Inspect `.github/dependabot.yml`: it covers npm in `/app/client`. Pip and Actions configuration are not part of this lab.
2. In the Codespaces terminal, confirm previous work is committed and the tree is clean, then update your learner `main` and create the isolated branch:

   ```bash
   git status --short
   git fetch origin
   git switch main
   git merge --ff-only origin/main
   git switch -c exercise/dependency-policy
   ```

   If that branch already exists, inspect it and resume it instead of overwriting it. If `main` cannot fast-forward cleanly, stop and follow [Resume](take-home/0-resume.md).
3. Copy the bundled workshop's inert before fixture into the unused lab directory:

   ```bash
   test ! -e workshop-lab/dependency/requirements.txt &&
   mkdir -p workshop-lab/dependency &&
   cp content/devsecops/fixtures/dependency-before.txt workshop-lab/dependency/requirements.txt
   ```

   Open **`workshop-lab/dependency/requirements.txt`** in the Codespaces editor and confirm it contains exactly:

   ```text
   PyJWT==2.3.0
   ```

4. Review, commit, and push only this manifest:

   ```bash
   git add -- workshop-lab/dependency/requirements.txt
   git diff --cached -- workshop-lab/dependency/requirements.txt
   git commit -m "Add isolated dependency policy training fixture"
   git push -u origin exercise/dependency-policy
   ```

   On GitHub.com, open a PR against your own `main` titled **Training only: prove dependency policy; do not merge**. Confirm it is separate from your safe application PR. The workflow on `main` reports the `dependency-review` job; neither CI job reads the lab directory.
5. Wait for the initial dependency-review result. Inspect the PR dependency diff and confirm it lists the lab manifest, PyJWT, and version 2.3.0. Open the failed `dependency-review` job and record the high-severity advisory and run URL.
6. **Do not repair the fixture in Lab 4.** Leave the dependency-training PR open and failing for Lab 6. Do not change the branch to a repaired version, close the PR, or merge it here.

If the result is pending at minute 53, move to the secret exercise and return at the start of Lab 6. A queued or missing check does not show that dependency review detected the vulnerability. Wait for a completed failure that identifies the advisory before continuing the dependency exercise. If it never arrives, record the outcome as pending or incomplete.

The [local Git fallback](0-setup.md#fallback-a-local-vs-code-and-git) uses the same commands. For the [file-editor fallback](0-setup.md#fallback-b-github-file-editor), create `exercise/dependency-policy` from your `main`, add the same manifest, open the PR, and leave it open after observing the failure.

## Read the advisory

[GHSA-ffqj-6fqr-9h24](https://github.com/advisories/GHSA-ffqj-6fqr-9h24) is high severity and affects PyJWT `>=1.5.0,<2.4.0`; the lab's 2.3.0 version is in that range. The first patch for this advisory was 2.4.0, but later advisories may change which version is appropriate. Lab 6 contains the reviewed repair procedure. Recheck the advisory before each event; no version is guaranteed to remain vulnerability-free. [Technical sources](sources.md) record the original lookup.

The starter fails on **high** or **critical** severity across runtime, development, and unknown scopes. A green job with an empty dependency diff does not prove it detected the fixture. If the manifest is absent or the service returns an availability error, record that discovery failed. Do not lower the threshold or install the fixture to force a result.

## Checkpoint

Your evidence has the actual manifest path and version, a completed high-severity failed run, and a link to the open dependency-training PR. The PR must remain unrepaired and unmerged until Lab 6. Do not claim a failure-and-repair cycle before both states are observed.

## Resources

[Dependency review](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review) and [Dependabot quickstart](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/dependabot-quickstart) explain the separate controls. [Supported dependency ecosystems](https://docs.github.com/en/code-security/reference/supply-chain-security/dependency-graph-supported-package-ecosystems) describes manifest support.

| [Previous: code scanning](3-code-scanning.md) | [Next: secrets](5-secrets.md) |
|:---|---:|
