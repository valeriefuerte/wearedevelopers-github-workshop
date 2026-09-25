# Troubleshooting without weakening controls

| [Previous: optional workload identity](4-workload-identity.md) | [Next: annotated solutions](../solutions/README.md) |
|:---|---:|

## Why it matters

Keep each control in place while you diagnose a failure, and preserve your work. Mark an outcome incomplete if you do not have the required evidence.

## Codespaces access and recovery

Use the Codespaces editor and integrated terminal for the primary route. Keep GitHub.com open for repository settings, PRs, and Actions results. Do not install the application or create credentials to repair the editing environment.

| Symptom | Check and recovery |
|---|---|
| Codespaces is unavailable or policy-blocked | Confirm the signed-in account, learner repository ownership, and employer/organization policy. Use the approved [local Git](../0-setup.md#fallback-a-local-vs-code-and-git) or [file-editor fallback](../0-setup.md#fallback-b-github-file-editor). Do not evade policy or create duplicate spaces. |
| Quota exhausted or unexpected payer | Check **Billing and licensing > Usage** and the payer shown in the creation dialog. Use an existing allowance, approved sponsorship, or a fallback. Do not add payment details, increase budgets, or upsize the machine as the default fix. |
| Cannot resume because usage is blocked | Preserve work through [exporting changes](https://docs.github.com/en/codespaces/troubleshooting/exporting-changes-to-a-branch) where available, reviewing the files before publishing. Never export a rejected secret fixture. Do not delete the codespace before preserving needed work. |
| Startup fails or takes too long | Inspect the creation or connection error and service status, then use [creation troubleshooting](https://docs.github.com/en/codespaces/troubleshooting/troubleshooting-creation-and-deletion-of-codespaces). Record that startup is incomplete. Don't add a required devcontainer, rebuild the codespace, or choose a larger machine to mask the problem. |
| Wrong repository or automatic fork prompt | Check the existing checkout root, `git remote get-url origin`, and branch. Stop before pushing. Preserve work, stop the wrong space if it is yours, and open the intended learner copy. Do not retarget upstream or companion origins automatically. |
| Closed tab, stopped space, or expired editor session | Reopen the same named learner space at [github.com/codespaces](https://github.com/codespaces). Saving is not a push. Check the branch and `git status --short` after reconnecting before switching or fetching. |
| Bundled guide missing | Confirm the learner origin and branch, then inspect `content/devsecops` on that same repository's GitHub page. It arrived with the template. Inspect deleted or uncommitted files before recovering; do not fetch an external companion or overwrite local work. |
| Older template version | Read `content/devsecops/workshop-kit.json` in your copy. GitHub copied the default branch at creation; later template updates do not change your copy. Use the matching guide or review an intentional update in your own repo. |
| Git push/authentication fails | Keep the configured HTTPS authentication for the learner repository. Check origin, your access, and whether the Codespaces session expired; stop/reopen the existing space to refresh its configured token. If dotfiles or secrets override authentication, investigate with the owner without printing values or changing global settings as a quick fix. |
| Optional workflow-file push is rejected | Preserve the commit and inspect the rejection. Confirm the learner target and policy. Use the file-editor fallback for that reviewed change if needed; don't widen scopes, add `write-all`, or create a privileged bootstrap. Core workflows are already installed. Reconcile divergent branches deliberately; no force push. |
| Port opened or app started accidentally | Stop the process you started and leave forwarded ports private. Application hosting, dependency installation, and local tests are not part of this editing route; use the Actions jobs. |

Codespaces' developer credential and an Actions job token may both be named `GITHUB_TOKEN`. They have different scopes and lifecycles. Never print either, dump environment variables, or run the optional identity proof locally with the developer token.

Stop explicitly with **Codespaces: Stop Codespace** or the website's **Stop codespace** control. Closing the tab leaves compute running until timeout. Stopped spaces still use storage. Delete only your intended space after preserving safe work, receipts, and resume information.

## Setup and accounts

| Symptom | Check and recovery |
|---|---|
| Cannot create public repo or change settings | Confirm the signed-in account, admin access, email verification, and employer/organization policy. Managed users cannot create public repositories. Use an eligible personal account only if permitted; otherwise arrange approved observation and mark individual work incomplete. |
| Local-fallback Git authentication fails | Confirm the learner origin and your existing credential helper or VS Code browser sign-in. Use the file-editor fallback if local authentication is restricted. Never paste a PAT into code/URLs or change global work identity. |
| Author identity unknown or wrong commit email | Authentication does not set your commit author. Use the [repository-local identity steps](#commit-identity) below. Do not change global corporate settings; the helper never changes identity. |
| Optional recovery helper rejects origin | It accepts direct learner HTTPS/SSH URLs but refuses the original source, earlier companion, and public template origins, plus credentials, aliases, or mismatched destinations. Do not change remotes to bypass it. Normal setup does not need this helper. |
| Wrong branch, detached HEAD, or Git operation in progress | Finish your work on its intended branch and resolve or deliberately abort the existing operation. Then use clean `main`. The helper does not reset, stash, or change your identity. |
| Unrelated files or conflicting workflows | Review and preserve them. Compare the installed files with the bundled starters. Differing files are never silently overwritten by recovery tooling. |
| Baseline fingerprint mismatch | Review the local application change or incompatible template update. Record the path, version, and revision; do not replace the app with old source or waive the check. |
| Recovery refuses after lesson 3 | The application fingerprint changed because you fixed it. Use the resume guide and deliberate file comparison rather than forcing initial-baseline recovery. |
| Workshop files show unexpected changes | Guides are committed under `content/devsecops`. Inspect and preserve edits; do not delete or replace the folder to make the tree appear clean. |
| Starter PR already exists | Resume it and inspect its current branch/checks. For a closed/merged PR, follow [Resume](0-resume.md). |

### Commit identity

Check `git config --get user.name` and `git config --get user.email` privately in the learner-root terminal. If either is missing or the inherited email is unsuitable for public training, copy your exact noreply address from **GitHub Settings > Emails**, replace the quoted values, and run:

```bash
git config --local user.name "YOUR DISPLAY NAME"
git config --local user.email "YOUR EXACT GITHUB NOREPLY ADDRESS"
```

These settings apply only to this checkout and do not authenticate a push. Keep configured Codespaces authentication or the local fallback's existing sign-in; never print tokens or change global identity to repair this lab.

### Missing or changed core workflow

Compare `.github/workflows/ci.yml` and `dependency-review.yml` with the same copy's `content/devsecops/starter` files. If a file is missing, preserve edits and determine why before restoring only the intended file through a reviewed commit/PR.

The bundled `scripts/prepare-devsecops.sh` is optional recovery tooling, not required setup. `--check` is read-only. For a missing file it prints `WOULD COPY`; that does not prove workflows exist or remote settings are ready. `--apply` copies only missing core files when the baseline matches. It refuses conflicting content, unrelated edits, and origins that point to a source or template repository. It never bypasses GitHub policy or rewrites history.

## Checks and findings

| Symptom | Check and recovery |
|---|---|
| No CI run | Confirm `.github/workflows/ci.yml` is committed on remote `main`, Actions is permitted, and the YAML matches the kit. Use **Run workflow > main**. Do not use a non-main manual run as baseline evidence. |
| API dependency resolution fails | Read the first pip conflict; check the reviewed constraints and direct requirements. Update the snapshot through a PR when appropriate; never install the lab fixture. |
| Client build fails with Node version error | This track uses Node 24. Astro 6 requires Node >=22.12; older Pets examples using Node 20 are not the supplied workflow. Preserve `package-lock.json` and use `npm ci`. |
| Required check is missing | Confirm the workflow exists on both PR/base branches, the PR targets `main`, and exact job names are `api-tests`, `client-build`, `dependency-review`. These starters have no path filters. Rerun a real PR event; don't mark a missing check successful. |
| CodeQL is pending or failed | Inspect the analysis run, languages, and default setup settings. Avoid installing advanced setup alongside default setup. Wait/retry the failed analysis; neither silence nor a failed scanner proves the finding is gone. |
| Expected debug finding absent | Confirm the pinned original source and Python analysis. The code might already be fixed or query behavior may have changed. Report drift; do not inject a new vulnerable endpoint. |
| Default-branch alert remains after PR fix | Check the PR's latest analysis first. The default-branch alert closes after safe merge and successful default-branch analysis, not just after a PR commit. |
| Dependency job passes but package is absent | Inspect the dependency diff for `workshop-lab/dependency/requirements.txt`, PyJWT, and the exact version. Empty discovery is incomplete, not a passing fixture exercise. Keep the threshold high. |
| Dependency review says unsupported/not ready, or its API returns 403 | Confirm dependency graph is enabled in **Settings > Advanced Security** and your account is permitted to use it. Wait up to five minutes, then rerun once. If it still fails, escalate with the run URL. This is an availability or setup failure, not advisory detection; do not lower the threshold or enable a bypass. |
| Dependency repair still fails | Read the actual advisory and affected range. A newer advisory may require a kit update. Do not add allowlists or `warn-only`, and do not silently substitute an unverified version. |
| Lab 4 dependency PR was repaired before Lab 6 proved the block | Do not claim the merge-policy block. If the PR is still open/unmerged and its original failure is recorded, restore only the isolated manifest to PyJWT 2.3.0, activate the ruleset, observe a completed failed required check, then repair it in Lab 6. Never install the manifest. |
| Dependency training PR was merged by mistake | Do not install it or claim an unmerged closure. Remove the unused manifest through a separate safe PR and record the required Lab 6 outcome as incomplete. |

## Secrets

Use only the fixture documented as inactive, with a recent check of the route you plan to use. Never authenticate with it. Repository push protection can behave differently for a value already detected in that repository, so rehearse in fresh history.

For one newest unpublished Codespaces terminal commit, follow lesson 5's targeted `git add` and amend. The local Git fallback does the same. For a blocked file-editor edit, correct the uncommitted buffer and retry; no local commit exists to amend.

### More than one unpublished secret commit

1. Stop the timed exercise. In the same Codespaces terminal (or local Git fallback), read every commit/path listed in the rejection and confirm none of those commits was published or shared.
2. Save nonsecret work independently. Do not create a published backup branch containing the value.
3. Find the earliest affected commit with `git log --oneline`. Replace `EARLIEST` below with its hash:

   ```bash
   git rebase -i EARLIEST^
   ```

4. Mark every affected commit as `edit`. At each pause, remove the value, stage only the corrected file, run `git commit --amend --no-edit`, then `git rebase --continue`. Resolve conflicts carefully; a later commit can reintroduce the value.
5. Inspect all rewritten unpublished changes and push the clean branch normally. No force push is needed when the rejected branch was never published.

If the earliest commit is the root, the branch has shared history, or you are unsure whether the commits were published, stop and get help before applying this sequence. For a real exposure, revoke or rotate the credential first and follow the organization's incident process.

If the supplied fixture is not blocked, mark the result incomplete. Do not bypass, mint a real token, or claim a recording as your own live result.

## Rules and release

| Symptom | Check and recovery |
|---|---|
| Unexpected owner-review requirement | The template has neutral `CODEOWNERS`. Inspect changes in your copy, rulesets, and organization rules. Solo labs do not require owner review; do not override organization policy. |
| Passing checks but merge blocked | Inspect missing/stale checks, up-to-date requirement, unresolved reviews, and code-scanning policy. Update the branch normally and wait for the new revision. Do not bypass. |
| Release workflow guard fails | Inspect its specific error. The workflow must be on `main`; `workshop-demo` must already have a reviewer and exactly one branch-only `main` rule. API failures are blocking, not success. |
| No approval wait | Stop. Verify environment name/settings before treating the run as an approved release. |
| Required reviewer cannot be configured | Stop before installing the release workflow. Do not use a facilitator's/second person's approval or administrator bypass; record the platform or policy limitation as incomplete. |
| Waiting release is stale | Cancel it. Run current `main` and wait for its prerequisites. An old green run cannot validate a new SHA. |
| Receipt expired or upload failed | Record expiration/failure. A rerun creates a new attempt and needs its own prerequisites/approval; do not reconstruct a receipt and call it the original. |
| Receipt fields look right but checksum was not run | Do not claim independent verification. Download the actual artifact and run `sha256sum -c receipt.sha256` or `shasum -a 256 -c receipt.sha256` from Codespaces/local Git; a file-editor-only route must record this as unverified. Keep the receipt checksum distinct from the uploaded archive digest. |

## Checkpoint

For the optional job-token exercise, use [its failure and cleanup table](4-workload-identity.md#4-handle-failures-and-cleanup). Only the exact expected integration-permission denial is successful evidence. Close only the issue whose recorded URL and run marker match; cancellation can interrupt automatic cleanup. Do not grant broader permissions or replace `GITHUB_TOKEN` with a personal token to force a pass.

Record the failing step, exact error, revision, run URL, kit version, and safe next action. Exclude tokens and private data. If the issue remains unresolved, its outcome stays incomplete.

## Resources

[Codespaces authentication](https://docs.github.com/en/codespaces/troubleshooting/troubleshooting-authentication-to-a-repository), [repository access](https://docs.github.com/en/codespaces/managing-your-codespaces/managing-repository-access-for-your-codespaces), [usage and billing](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces), [required checks](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks), [blocked-push repair](https://docs.github.com/en/code-security/how-tos/secure-your-secrets/work-with-leak-prevention/push-protection-on-the-command-line), and [environment protection](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments).

| [Previous: optional workload identity](4-workload-identity.md) | [Next: annotated solutions](../solutions/README.md) |
|:---|---:|
