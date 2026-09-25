# Your workshop evidence

| [Previous: annotated solutions](solutions/README.md) | [Next: take-home companions](take-home/README.md) |
|:---|---:|

## Why it matters

Evidence links let you return to the exact revision and result. Record only public workshop data; exclude credentials, fixture values, and private screenshots.

Start with your learner repository URL, kit version, date, and route: **Codespaces primary**, local Git fallback, or file-editor fallback. To help you resume, keep only a nonsecret codespace identifier. Never share tokens, secret fixtures, or private connection details.

| Status | Meaning |
|---|---|
| Live complete | You performed the action and observed the required result in your own repository |
| Pending | The required service result has not arrived |
| Incomplete | The action failed, was unavailable, or lacks required evidence |
| Unverified | Source-level checks or local tests cannot prove this platform or human outcome |
| Not attempted | You have not started the exercise |

Record the route used separately from the result status. A fallback is not automatically complete: for example, the file-editor route cannot independently run the receipt checksum command.

## Individual live work

| Outcome | Evidence to record | Status |
|---|---|---|
| Prework | Learner repository, kit version, baseline CI run, open harmless PR | ___ |
| Codespaces readiness | Correct learner origin, permitted payer/usage, bundled guides/core checks, harmless push and stop/resume; or named fallback | ___ |
| Threat model | Three risk/control/owner rows in notes or PR description | ___ |
| Code remediation | Fix/test commit, passing CI, latest PR CodeQL result without targeted finding | ___ |
| Dependency failure (Lab 4) | Open PR/branch, manifest path and PyJWT 2.3.0, completed high-severity `dependency-review` failure and run URL | ___ |
| Secret protection (Lab 5) | Actual blocked push/commit and clean retry on the named route; redacted evidence | ___ |
| Active merge policy (Lab 6) | `workshop-main` state, `main`-only target, empty bypass list, zero approvals, exact checks, up-to-date requirement, CodeQL High-or-higher setting | ___ |
| Blocked dependency merge (Lab 6) | Same failing PR revision and proof the required failed `dependency-review` check specifically blocked merging | ___ |
| Repaired dependency PR (Lab 6) | Same branch repaired to PyJWT 2.14.0, passing required checks/CodeQL, eligible state, PR closed without merge | ___ |
| Safe application merge (Lab 6) | Safe PR merge SHA, successful `main` checks and CodeQL result for that SHA, original `py/flask-debug` alert closed/fixed or still pending | ___ |
| Release environment (Lab 7) | `workshop-demo`, own required reviewer, self-review prevention off, administrator bypass disabled, sole branch rule `main`, no secrets/credentials/variables | ___ |
| Reviewed workflow install (Lab 7) | Dedicated branch/PR, ruleset merge SHA, release workflow remained inactive until merged | ___ |
| Approved release (Lab 7) | Exact `main` release SHA, successful `guard`, `release-api-tests`, and `release-client-build` at that SHA, observed approval wait and approval | ___ |
| Receipt artifact (Lab 7) | Run URL and attempt, artifact ID/URL, `receipt.json` checksum, uploaded archive digest recorded as separate values | ___ |
| Independent receipt verification | Downloaded artifact and successful `sha256sum -c receipt.sha256` or `shasum -a 256 -c receipt.sha256`; note if route cannot verify | ___ |
| Incident response (Lab 7) | Released SHA, assigned owner, evidence still needed, chosen patch/revert/investigation action | ___ |
| Optional non-main dispatch | Non-`main` guard rejection with no receipt; optional follow-up only | ___ |
| Cleanup and lifecycle | Training fixtures not merged, pending/stale runs handled, receipt saved before expiry, safe work pushed, codespace explicitly stopped | ___ |

## References are not evidence

Examples, expected-result tables, preserved author receipts, recordings, and another learner's repository can help explain what to inspect. They do not satisfy any individual live outcome. A local test does not prove GitHub settings, Codespaces authentication, merge enforcement, environment approval, or artifact behavior.

Keep an outcome marked pending, unavailable, or unverified until you have the required evidence. An empty dependency diff or a queued check does not satisfy its checkpoint. Neither does a successful CodeQL run that still reports the finding, a receipt from another SHA, or a later deletion of a committed secret.

The optional workload-identity exercise is not another core requirement. Its OIDC references are further reading: GitHub issue authorization does not demonstrate Azure/AWS login or cloud resource access.

## Resources

[Review workflow runs](https://docs.github.com/en/actions/how-tos/monitor-workflows/using-workflow-run-logs) and [review dependency changes](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review) explain how to inspect actual results.

| [Previous: annotated solutions](solutions/README.md) | [Next: take-home companions](take-home/README.md) |
|:---|---:|
