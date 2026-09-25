# 6. Enforce a merge policy in your repository

| [Previous: secrets](5-secrets.md) | [Next: delivery and response](7-delivery-and-response.md) |
|:---|---:|

Budget: 24 minutes. Configure the ruleset in your own learner repository. The facilitator and helpers guide and troubleshoot; they do not configure or bypass controls for you.

Use your existing Codespaces editor and terminal for Git and file changes. Use GitHub.com to configure settings, inspect PRs, and record Actions and CodeQL results. The local Git and file-editor fallbacks use the same learner repository and policy requirements.

## Why it matters

A failed check provides feedback. An active ruleset can require that check to pass before merging. A successful CodeQL analysis confirms the scanner ran; the ruleset also sets the finding severity that must be resolved.

## 1. Confirm the two separate PRs

1. Open your learner repository on GitHub. Confirm the safe application PR and dependency-training PR are separate, both target your own `main`, and neither contains the other's files:
   - The safe PR contains the startup fix and regression test, not the dependency or secret fixture.
   - The dependency PR is `exercise/dependency-policy` and contains only `workshop-lab/dependency/requirements.txt` with the still-failing `PyJWT==2.3.0` fixture.
2. If the dependency PR is closed or the PR or branch is missing, use [Resume](take-home/0-resume.md) to recreate an isolated failing fixture PR from your current `main`. Never merge the lab manifest.
3. Check the latest safe-PR revision for the exact `api-tests`, `client-build`, and `dependency-review` jobs and its CodeQL analysis. If anything is queued or pending, keep its status pending. Configure the ruleset while you wait, then return to the results. Do not assume an older green revision covers the latest commit.

## 2. Create and verify the ruleset

1. On your learner repository, open **Settings > Rules > Rulesets > New ruleset > New branch ruleset**.
2. Name it `workshop-main`, set **Enforcement status** to **Active**, and leave the bypass list empty.
3. Under **Target branches**, add only the inclusion pattern `main`.
4. Enable **Require a pull request before merging** and set required approvals to **0**. Leave code-owner review and last-push approval off. Do not require a second person.
5. Enable **Require status checks to pass** and add these exact GitHub Actions job names:

   ```text
   api-tests
   client-build
   dependency-review
   ```

   Select **GitHub Actions** as the expected source where the UI allows it.
6. Require the branch to be up to date before merging. Do not enable merge queue: these workflows do not have a `merge_group` trigger.
7. Enable **Require code scanning results**, select **CodeQL**, and require **High or higher** findings to be resolved. If the UI also offers a general alert severity, select **Errors**. Do not require code-owner review.
8. Save and reopen the ruleset. Verify it is active, targets only `main`, has no bypass actors, requires zero approvals, contains the exact checks above, and includes the CodeQL threshold.

If a status check is missing from the selector, confirm the starter workflow exists on both branches and wait for or rerun its real PR workflow. Do not guess a check name or remove a requirement to merge. If your account or organization policy makes CodeQL merge protection unavailable, stop and record that requirement as unavailable or incomplete. Do not claim it is enforced or weaken another rule.

Code-scanning merge protection primarily evaluates findings introduced in a PR. Documented limitations apply to existing findings outside the PR diff and some cases involving Dependabot or default setup. The intended `py/flask-debug` alert can remain open until the safe fix merges.

## 3. Prove the failing dependency check blocks a merge

1. Open the Lab 4 dependency-training PR. Confirm it is not a draft, has no unrelated merge conflict, and the latest `dependency-review` job completed with the high-severity PyJWT advisory for the visible 2.3.0 manifest.
2. Confirm GitHub's merge control is blocked specifically by the required failed `dependency-review` check. A missing, queued, cancelled, or unrelated failing check does not prove the intended policy result. Do not click Merge.
3. Record the active ruleset, PR revision, advisory, failed run URL, and the specific blocked-check reason.

If the result is pending, leave the PR unchanged and return when Actions completes. Do not label the merge blocked by dependency review until the actual failed job is visible.

## 4. Repair the fixture on the same branch

1. In the Codespaces terminal, inspect your state and switch to the existing Lab 4 branch. Do not create a replacement branch or overwrite unrelated work:

   ```bash
   git status --short
   git switch exercise/dependency-policy
   ```

2. In the editor, change the one line in `workshop-lab/dependency/requirements.txt` to the content of the bundled repair fixture:

   ```text
   PyJWT==2.14.0
   ```

   Never install this manifest in Codespaces, on your laptop, or in CI.
3. Review, commit, and push the repair to the same branch:

   ```bash
   git add -- workshop-lab/dependency/requirements.txt
   git diff --cached -- workshop-lab/dependency/requirements.txt
   git commit -m "Repair isolated dependency policy fixture"
   git push
   ```

4. If `main` advanced, update the branch normally and inspect the new PR checks. Wait for all three required checks and the CodeQL result on the repaired PR revision. Confirm the checks pass and the merge control shows the PR is eligible.
5. Close the dependency-training PR **without merging it**. Record the passing repair run and eligible state before closing. Keep the branch unmerged; deletion is optional after preserving the evidence.

If any required check or CodeQL result is still pending, leave the PR open and mark the result pending. Do not call it eligible or close it as if the repair passed.

## 5. Merge only safe application work

1. Return to the safe application PR. Confirm the changed files contain no dependency-training directory and no secret fixture. Ensure its latest revision is up to date with `main` and has passing required checks plus an acceptable CodeQL result.
2. Use GitHub's normal merge control. Do not bypass the ruleset. Record the safe merge commit SHA.
3. On `main`, verify the `api-tests` and `client-build` results and the CodeQL analysis for that exact merge SHA. `dependency-review` is PR-triggered; do not expect it to run on `main`.
4. In **Security and quality > Code scanning**, confirm the original `py/flask-debug` alert is closed/fixed after default-branch analysis. A green PR check alone does not prove that the alert closed.

If a result is pending or a policy capability is unavailable, preserve the PR and record the actual state. Never bypass checks or mark an incomplete result as successful to stay on schedule.

## Checkpoint

Record the active ruleset settings and the failed required check that blocked merging. For the repaired dependency PR, record its eligible state and closure without merging. Also record the safe application merge SHA, successful `main` checks, and the original alert's status. Use the [evidence checklist](evidence.md). Expected examples and other learners' runs are references, not evidence for your repository.

When Codespaces is unavailable, use the documented [local Git](0-setup.md#fallback-a-local-vs-code-and-git) or [file-editor fallback](0-setup.md#fallback-b-github-file-editor). GitHub settings, merge enforcement, and actual check results still have to be verified in your own repository.

## Resources

[Create branch rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository), [code-scanning merge protection](https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/manage-your-configuration/set-merge-protection), and [code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners).

| [Previous: secrets](5-secrets.md) | [Next: delivery and response](7-delivery-and-response.md) |
|:---|---:|
