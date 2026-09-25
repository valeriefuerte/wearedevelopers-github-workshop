# 8. Record your live evidence

| [Previous: delivery and response](7-delivery-and-response.md) | [Next: take-home companions](take-home/README.md) |
|:---|---:|

Budget: 7 minutes, from event minute 113 through minute 120. Stop starting new troubleshooting at minute 113; do not turn a pending result into a pass to meet the schedule.

## Why it matters

Record which controls you tested yourself, what exact revision they covered, and what remains unfinished. A source example or someone else's run is not a substitute for your own result.

## Try it

1. Complete your [evidence checklist](evidence.md) using the actual results from your own repository:
   - Lab 6: active ruleset settings, dependency failure blocked by the exact required check, repaired eligibility, dependency PR closed without merging, safe merge SHA, successful `main` checks, and `py/flask-debug` alert state.
   - Lab 7: environment policy, workflow PR merge SHA, approved release SHA, run URL/attempt, successful same-SHA jobs, artifact ID, receipt checksum, archive digest, checksum verification/fallback status, and incident-response decision.
2. Keep each outcome `Pending`, `Incomplete`, `Unverified`, or `Not attempted` when the required result is absent. Record local Git, Codespaces, or file-editor route separately. The file-editor fallback cannot verify a checksum locally.
3. Compare your opening delivery sketch with the controls you configured. Identify where the process prevents, detects, reviews, merges, and approves a change.
4. Preserve safe work and run/artifact links before receipts expire. Leave the dependency and secret training fixtures unmerged. If a required result is still pending, save the resume point rather than forcing completion.
5. Open [Resume](take-home/0-resume.md) to choose the right state for any later work, then use the remaining time for questions.

## Stop the codespace safely

Save edits and review `git status --short` in the Codespaces terminal. Commit and push intended safe work to its exercise branch, then verify it on GitHub; a saved file alone is not a pushed commit. Do not publish a rejected secret fixture as a backup.

Use **Codespaces: Stop Codespace** or **Stop codespace** for this space at [github.com/codespaces](https://github.com/codespaces). Closing the tab does not stop compute. Stopped storage still counts; resume this same space for later work. Delete it only after preserving needed work and receipts. Follow [Step 0's lifecycle guidance](0-setup.md#08-stop-and-reuse-your-codespace).

## Checkpoint

Keep your own evidence record and resume point. Note any GitHub settings you have not verified, pending scans, unavailable reviewers, expired artifacts, or checksum checks you have not run. Examples, expected-result tables, and recordings remain references, not learner evidence.

## Resources

[OWASP threat modeling](https://owasp.org/www-community/Threat_Modeling) and [NIST SSDF](https://csrc.nist.gov/projects/ssdf) support the next discussion with your team. [Stopping and starting a codespace](https://docs.github.com/en/codespaces/developing-in-a-codespace/stopping-and-starting-a-codespace) explains what is preserved.

| [Previous: delivery and response](7-delivery-and-response.md) | [Next: take-home companions](take-home/README.md) |
|:---|---:|
