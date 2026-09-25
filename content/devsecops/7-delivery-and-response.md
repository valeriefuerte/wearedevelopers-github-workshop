# 7. Approve a simulated release and plan a response

| [Previous: merge policy](6-merge-policy.md) | [Next: closing](8-wrap-up.md) |
|:---|---:|

Budget: 24 minutes. Configure the release environment, install the workflow through a reviewed PR, approve a passing simulation, and record your own evidence. It deploys no application and needs no cloud account.

Work only in your own learner repository. Edit files and use Git in Codespaces. Configure the environment, manage PRs, and give approvals on GitHub.com; Actions runs the simulation. If a platform result is delayed, complete the incident-card activity while it runs. Do not approve a failed or stale revision.

## Why it matters

When you approve a release, you approve a particular revision based on its evidence. The receipt lets the shelter identify that revision if a later advisory appears.

## 1. Configure the environment before installing the workflow

1. Complete Lab 6, and verify your safe application change is on your learner repository's `main`. If the safe PR is already merged, use [Resume](take-home/0-resume.md) to check its exact main result; do not recreate the old finding.
2. On GitHub.com, open your repository's **Settings > Environments > New environment** and name it exactly `workshop-demo`.
3. Enable **Required reviewers**, add your own account, and save the protection rule.
4. Leave **Prevent self-review** off for solo practice. You can approve your own simulated release; this is a training accommodation, not production separation of duties.
5. Disable **Allow administrators to bypass configured protection rules**. Do not use a bypass if a run is blocked.
6. Under **Deployment branches and tags**, select **Selected branches and tags**. Add exactly one **Branch** rule named `main`. Do not add a tag rule, wildcard, or **Protected branches only**.
7. Reopen the environment and verify the reviewer, disabled administrator bypass, selected-branch mode, and sole `main` rule. Add no environment secrets, cloud credentials, or variables.

Public repositories support required reviewers on GitHub Free. If your account or organization policy prevents you from setting yourself as reviewer or applying this exact branch policy, stop before installing the workflow. Record the limitation and mark the outcome incomplete. Do not ask a facilitator to configure or approve on your behalf.

## 2. Review and install the release workflow through a PR

1. In the learner-root Codespaces terminal, preserve any work, update your own `main`, and create a dedicated branch:

   ```bash
   git status --short
   git fetch origin
   git switch main
   git merge --ff-only origin/main
   git switch -c exercise/release-simulation
   ```

   If this branch already exists, inspect and resume it instead of overwriting its changes.
2. Review the bundled [`starter/release-simulation.yml`](starter/release-simulation.yml) in the editor. The distributed template has exactly two preinstalled workflows; keep this optional starter inactive until this reviewed PR. Copy it only if the destination does not exist:

   ```bash
   test ! -e .github/workflows/release-simulation.yml &&
   cp content/devsecops/starter/release-simulation.yml .github/workflows/release-simulation.yml
   ```

3. Inspect the supplied controls before committing:

   | Control | What the workflow enforces |
   |---|---|
   | Trigger and guard | `main` push or manual dispatch; other refs/events fail |
   | Environment | Existing `workshop-demo`, required reviewer, administrator bypass disabled, exactly one branch-only `main` rule |
   | Revision | Each release prerequisite checks out this run's exact `github.sha` |
   | Prerequisites | `guard`, `release-api-tests`, and `release-client-build` must all succeed; failed, skipped, or cancelled jobs cannot release |
   | Approval | `release` waits for `workshop-demo`; it rechecks current `main` and policy after approval |
   | Permissions | `contents: read`; no cloud identity, PR-target trigger, or persisted checkout credential |
   | Receipt | Records run attempt, commit, prerequisites, receipt checksum, artifact identity and archive digest; retention is three days |

4. Review the diff, commit, push, and open a PR against your own `main`:

   ```bash
   git add -- .github/workflows/release-simulation.yml
   git diff --cached
   git commit -m "Add reviewed cloud-free release simulation"
   git push -u origin exercise/release-simulation
   ```

   Name the PR **Add the reviewed release simulation**. Do not edit the default branch directly.
5. Wait for Lab 6's required PR checks and CodeQL policy to pass on the workflow PR's latest revision. The release workflow itself does not run on PR events and is not a new required PR check. Merge the reviewed PR using the normal `workshop-main` ruleset, without bypassing it. Record the merge SHA.

The [local Git](0-setup.md#fallback-a-local-vs-code-and-git) and [file-editor](0-setup.md#fallback-b-github-file-editor) routes use the same dedicated branch and PR. Configure the environment first on either route. The file-editor route does not provide an independent checksum command.

## 3. Inspect, approve, and verify the exact release

1. In **Actions > Release simulation**, open the run for the workflow PR's exact merge SHA. If the push run did not start, use **Run workflow > main** and record the exact current `main` SHA selected. Never substitute a run from another revision.
2. Verify `guard`, `release-api-tests`, and `release-client-build` all succeeded for the same run commit SHA. In each test job, inspect the checkout log and confirm the ref is that exact SHA.
3. While Actions runs, complete the [incident card](fixtures/incident-card.md) as your own exercise: assign an owner, name the evidence needed from the advisory and released revision, and choose **patch**, **revert**, or **investigation**. Record the decision and remaining evidence in your notes and [evidence checklist](evidence.md).
4. Observe the `release` job waiting for approval in `workshop-demo` **before** approving it. If a prerequisite fails, is pending, is skipped, or is cancelled, do not approve. If the release job does not wait, stop and diagnose the environment rather than treating the run as approved.
5. After confirming all three prerequisites succeeded on the exact SHA and the configured review request is for that revision, select **Review deployments**, choose `workshop-demo`, inspect the revision, add an approval comment, and select **Approve and deploy**. The UI wording does not mean an application is deployed.
6. Open the completed run summary and record the full commit SHA, run URL and attempt, artifact ID and URL, SHA-256 checksum for `receipt.json`, and the uploaded archive digest. The receipt checksum and archive digest are different values: `receipt.sha256` verifies `receipt.json`; the artifact digest identifies the uploaded ZIP archive.
7. Download the small receipt artifact before its three-day expiration. Confirm `receipt.json` has kind `workshop-simulation-no-deployment`, the same `main` SHA, run URL/attempt, environment, and prerequisite job names.

For Codespaces and local Git users, independently verify `receipt.sha256`:

1. In the learner-root terminal, create a folder outside the repository for the exact run ID:

   ```bash
   mkdir -p ../pets-devsecops-receipts/RUN_ID
   ```

2. For Codespaces, use **File > Add Folder to Workspace** to show that folder alongside the learner repo. Upload the downloaded ZIP there as `receipt.zip`; do not put the artifact in the application checkout. For local Git, save the ZIP to the same outside-repository folder.
3. Extract and verify the artifact:

   ```bash
   cd ../pets-devsecops-receipts/RUN_ID
   unzip receipt.zip
   sha256sum -c receipt.sha256
   ```

   On macOS, use `shasum -a 256 -c receipt.sha256`. Confirm the output says `receipt.json: OK`. Return the terminal to the learner root before further Git commands.
4. A file-editor-only learner may inspect the downloaded fields but cannot independently run this checksum command. Record that limitation as unverified/incomplete; do not use an expected checksum as a substitute.

## 4. Handle failures without bypassing

| Result | Action |
|---|---|
| Guard fails on environment policy or API error | Fix the stated setting/access issue, then run current `main` again. A missing response never means approval exists. |
| API test or client build fails | Diagnose it in a new PR, get required checks passing, and merge the repair. Do not approve a release from the failed run. |
| A prerequisite is pending, skipped, or cancelled | Leave release unapproved. Wait or rerun the full workflow when ready; do not treat a missing result as success. |
| Release job belongs to an older SHA | Cancel it and run current `main`. The post-approval guard also rejects stale revisions. |
| Approval cannot be given by the solo owner | Check reviewer membership and self-review prevention. If policy still prevents it, leave the lab incomplete; do not bypass the environment. |
| Upload fails or artifact expires before verification | Record the failure/expiration. A rerun has its own attempt, prerequisites, approval, and receipt; do not reconstruct the old receipt. |

## Optional follow-up: reject a non-`main` dispatch

Only after the required release and evidence steps are complete, dispatch the unchanged workflow from a non-`main` branch that contains it. Confirm the guard rejects the run and no receipt is produced. This is optional follow-up, not required core evidence; never weaken the branch guard to create this result.

## Checkpoint

Record the environment policy, reviewed workflow PR, and merge SHA. For one approved current-`main` run, record the successful prerequisites at that SHA, the approval wait you observed, the run and attempt, and the artifact identity. Include the receipt checksum and archive digest as separate values, your independent checksum result or explicit fallback status, and your incident-response decision. Never treat a stale run, sample receipt, recording, or another repository's result as your evidence.

## Resources

[Manage environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments), [review deployments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/review-deployments), and [workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax).

| [Previous: merge policy](6-merge-policy.md) | [Next: closing](8-wrap-up.md) |
|:---|---:|
