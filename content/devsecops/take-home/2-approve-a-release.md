# 2. Release recovery and extended validation

| [Previous: merge policy](1-enforce-merge-policy.md) | [Next: dependency maintenance](3-maintain-dependencies.md) |
|:---|---:|

Follow [core Lab 7](../7-delivery-and-response.md) for the release procedure, including workflow installation and approval. Use this page to resume incomplete work or run the optional non-`main` check.

## Why it matters

Use a release receipt that identifies the exact current `main` revision, its own run attempt, the approval wait you observed, and the artifact actually uploaded.

## Resume safely

1. Read [Resume](0-resume.md), then verify the environment and workflow state in your own repository before using an old run link.
2. If `workshop-demo` is configured but the workflow is not on `main`, verify the exact environment settings before creating or resuming `exercise/release-simulation`. Install only the bundled starter through a reviewed PR.
3. If the workflow PR is still open, inspect its diff and latest checks. Do not write directly to `main`; merge only through the active Lab 6 ruleset.
4. If the workflow is already merged, record its merge SHA and inspect a run for that exact current `main` SHA. Do not approve a run for an older commit.
5. If a run is stale, cancel it and dispatch the unchanged workflow from current `main`. A manual run has its own prerequisites, approval wait, run attempt, and receipt.
6. If any prerequisite is failed, pending, skipped, or cancelled, do not approve. If no environment approval wait appears, stop and diagnose the policy before continuing.
7. If your account or organization prevents you from configuring the required reviewer, exact single `main` branch rule, or disabled administrator bypass, stop before installing the workflow. Record the outcome as incomplete. Do not ask another person to configure it or use a bypass.
8. If an artifact expired or upload failed, record that fact. A new run creates a different attempt and receipt; do not reconstruct or relabel the old artifact.

## Extended validation

After the required core evidence is recorded, the non-`main` dispatch check is optional: dispatch the unchanged workflow from a non-`main` branch that contains it, confirm the guard rejects the run, and verify no receipt was produced. Never edit the branch guard or use this check to replace the approved `main` run.

For Codespaces or local Git, follow Lab 7 to download the artifact outside the application checkout and run `sha256sum -c receipt.sha256` or `shasum -a 256 -c receipt.sha256`. This verifies `receipt.json`; it is not the uploaded archive digest. A file-editor-only route cannot independently run the verification command and should say so.

## Checkpoint

Record the exact SHA, run URL and attempt, and three successful prerequisites at that SHA. Include the approval wait you observed and the approval itself. Keep the artifact ID, receipt checksum, separate archive digest, and independent checksum status with that record. Another repository's receipt, an expected-result example, and a recording are not your evidence.

## Resources

[Manage environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments), [review deployments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/review-deployments), and [workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax).

| [Previous: merge policy](1-enforce-merge-policy.md) | [Next: dependency maintenance](3-maintain-dependencies.md) |
|:---|---:|
