# 0. Resume without losing your work

| [Previous: take-home index](README.md) | [Next: Lab 6 merge policy](../6-merge-policy.md) |
|:---|---:|

## Why it matters

Your repository may have changed since the event. Check its current state before adding rules or trying to recreate an exercise.

## Reopen the same codespace

1. At [github.com/codespaces](https://github.com/codespaces), find the space for **your learner repository** and reopen it. Check access, payer, and remaining usage; do not change spending settings to resume. Do not create a new space merely because the old one is stopped.
2. Wait for initialization and open **Terminal > New Terminal**. Inspect the existing checkout:

   ```bash
   repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root"
   pwd
   git remote get-url origin
   git branch --show-current
   git status --short
   test -f content/devsecops/workshop-kit.json
   ```

3. Confirm the root is under `/workspaces` and origin names your learner repository. Saved files persist when you stop, restart, or rebuild the codespace. A replacement space starts with the committed template files; unpushed work stays in the old space.
4. Confirm `content/devsecops/workshop-kit.json` and the two root workflows exist in your copy. If any are missing, check the branch and file deletion history, then follow [troubleshooting](troubleshooting.md). Do not fetch an external kit or overwrite your application. Record your bundled version before considering a reviewed update.

If quota prevents resuming, follow [the recovery guide](troubleshooting.md#codespaces-access-and-recovery) and preserve work before using a fallback. Do not delete a space to resolve an authentication or quota error.

## Inspect your state

1. Confirm you own the public learner repository and can administer it. Check both core files on remote `main`: `.github/workflows/ci.yml` and `.github/workflows/dependency-review.yml`.
2. Open your working PR and dependency-training PR, if they exist. Record their branch names, state, latest commit, and checks. Inspect the actual file contents as well as old run links.
3. Confirm CodeQL default setup, dependency graph, secret scanning, and repository push protection are enabled. Check the current kit's [readiness register](../readiness.md) for any unresolved exercise blocker.
4. Before a branch switch in the Codespaces terminal, inspect `git status --short`. Commit your work to its intended branch or preserve it separately; these labs never reset or stash it for you.

| State | Safe next action |
|---|---|
| Labs 0 through 7 complete | Verify the safe merge SHA and its `main` results, the dependency PR is closed without merging, and the release receipt belongs to the approved current-`main` run. Save evidence and stop safely. |
| Labs 0 through 5 complete; dependency PR open and failing | Leave it unrepaired and open. Continue at [Lab 6](../6-merge-policy.md) to configure the ruleset, prove the required-check block, and only then repair it. |
| Code fix submitted, results pending or failed | Inspect the latest revision and finish [Lab 3](../3-code-scanning.md). Do not count an older green revision. Keep pending CodeQL/Actions results pending. |
| Dependency PR missing or closed; branch gone | Recreate the isolated `exercise/dependency-policy` branch from current `main` and follow [Lab 4](../4-dependencies.md) to observe the real failure. Never merge or install the lab manifest. |
| Dependency fixture repaired before proving the ruleset block | Do not claim the block. If the initial failure was observed and the PR remains unmerged, restore only the isolated manifest to PyJWT 2.3.0, observe the actual required-check failure with the active ruleset, then repair it in Lab 6. |
| Dependency PR accidentally merged | Stop. Do not install the manifest. Remove the unused fixture with a separate safe PR and mark the required unmerged-closure outcome incomplete. |
| Safe application PR still open | Reopen it if possible and confirm the latest fix/test, checks, and CodeQL result. Continue at Lab 6; do not merge before the ruleset is active. |
| Safe application PR already merged | Verify `debug=False`, the regression test, merge SHA, `main` checks, and alert status. If it was merged before the ruleset, do not claim a ruleset-enforced safe merge. A harmless notes-only PR through the active ruleset can provide recovery evidence, but label it as a recovery PR and keep the original merge state accurate. Never restore debug mode. |
| Fresh template copy | Complete [Step 0](../0-setup.md), then Labs 1 through 5. Lab 4 must leave an observed failing dependency PR open for Lab 6. Record unavailable or pending outcomes as such. |
| App files intentionally changed since setup | Do not rerun the strict helper or overwrite them. Compare workflows manually with this kit, validate compatibility, and preserve the changes. |

The preinstalled workflows do not need an installer. Optional recovery tooling checks the initial application's fingerprints and may reject a copy you have already fixed. Compare files and review later changes yourself.

## Resume release work

| State | Safe next action |
|---|---|
| `workshop-demo` configured; release workflow not installed | Verify that you are the required reviewer, bypass is disabled, and the only branch rule is `main`. Then follow Lab 7's reviewed-PR procedure. If a required setting cannot be configured, stop before workflow installation and mark the outcome incomplete. |
| Release workflow branch or PR already exists | Inspect the exact diff and latest checks. Resume that branch/PR; do not overwrite it or write directly to `main`. |
| Workflow PR merged; release run pending or absent | Wait for the run for that exact merge SHA. If the push run did not start, dispatch the unchanged workflow from current `main` and record that SHA. |
| Release prerequisite failed, queued, skipped, or cancelled | Do not approve. Wait or rerun the full workflow on current `main`; missing/pending results are not successful. |
| Release run is stale | Cancel it and start a current-`main` run. The post-approval guard must still reject any stale revision. |
| Receipt expired or checksum not verified | Do not reconstruct the old artifact or claim verification. Run the current workflow again if permitted, observe a new approval wait, and record its new run attempt and receipt. |
| Required reviewer cannot be configured | Stop before installing the workflow. Do not use a facilitator/second person's approval or administrator bypass; record the limitation as incomplete. |

## Refresh a branch safely

A required workflow must exist in the branch you use. In the same codespace, update your local `main` from your learner origin before starting new take-home branches. For an existing working PR, the commands below merge the updated `main` into its branch.

The fast-forward command refuses to update a divergent local `main`. Substitute your actual working branch if it differs from `exercise/shelter-change`. If the working branch is gone or its PR was already merged, stop after the fast-forward of `main`. Skip the last two lines and use the new-branch sequence below:

```bash
git status --short
git fetch origin
git switch main
git merge --ff-only origin/main
git switch exercise/shelter-change
git merge main
```

Start only with a clean working tree. If the fast-forward or merge fails, stop and inspect the conflict; do not force it. These commands use the learner's own origin, never companion or upstream history.

To recreate the working PR after updating `main`, create a new branch with `git switch -c exercise/shelter-resume`, edit `workshop-notes.md` in the Codespaces editor with a harmless resume note, and save:

```bash
git add -- workshop-notes.md
git diff --cached -- workshop-notes.md
git commit -m "Resume the shelter workshop"
git push -u origin exercise/shelter-resume
```

Open the new PR on GitHub against your own `main`. Apply only missing code/test edits, using this branch name in later instructions. Never restore the unsafe debug setting just to recreate prework.

For the file-editor fallback, create new branches from current remote `main` and use **Update branch** for an existing PR when available. Resolve conflicts deliberately. The local Git fallback uses the same terminal commands without Codespaces lifecycle assumptions.

## Checkpoint

You have an open safe PR, working core checks on its current revision, and a separate unmerged dependency exercise. Mark any missing live outcome incomplete. You can still learn about later controls as long as their own prerequisites pass.

When pausing, verify that safe commits are pushed, then explicitly stop this codespace. Closing the tab does not stop it. Delete the codespace only after preserving needed work and evidence.

## Resources

[GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow) and [keeping a pull request up to date](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/keeping-your-pull-request-in-sync-with-the-base-branch).

| [Previous: take-home index](README.md) | [Next: Lab 6 merge policy](../6-merge-policy.md) |
|:---|---:|
