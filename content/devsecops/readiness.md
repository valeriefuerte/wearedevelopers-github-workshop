# Template readiness

## Why it matters

Bundled files remove installation steps. Verify each learner's account access, repository security settings, and Codespaces setup separately in a fresh copy.

Candidate version 0.2.0 is being prepared in **frye/pets-devsecops-workshop-template**; no 0.2.0 GitHub release or learner rehearsal is claimed. The published `v0.1.0` remains immutable. Participants copy only this repository. The original app and previous companion are read-only provenance, recorded in [the source manifest](../../template-source.json).

## This template's checks

The app and complete workshop are bundled. Exactly two root workflows, `ci.yml` and `dependency-review.yml`, match the bundled starters. The release and job-token starters remain inactive. Neutral CODEOWNERS has no inherited reviewer, and the intentional debug-startup finding is preserved.

The local suite checks template inventory, repository-relative guide links, independent Git history, and missing or mismatched installed workflows. It also covers safe recovery, the startup fix and test, release guards, token errors and cleanup, and the required learner steps in Labs 4, 6, and 7. These source checks do not prove GitHub settings, environment approval, artifact behavior, or learner timing. [Template validation evidence](fixtures/template-validation.json) lists the executed v0.2.0 source-level checks and pending live checks separately from the historical v0.1.0 GitHub observations. Pending values are not successes.

The published v0.1.0 state had an [initial CI run](https://github.com/frye/pets-devsecops-workshop-template/actions/runs/35960087578) with passing API tests and client build. Its [harmless PR](https://github.com/frye/pets-devsecops-workshop-template/pull/1) reported all three core checks after dependency graph became ready. The initial review attempt failed on availability, not an advisory; the cause of that transient state was not established. These URLs are historical v0.1.0 evidence, not checks for candidate 0.2.0. No failing result was bypassed.

[The v0.1.0 CodeQL baseline analysis](https://github.com/frye/pets-devsecops-workshop-template/actions/runs/35960102321) succeeded and reported [the intended debug finding](https://github.com/frye/pets-devsecops-workshop-template/security/code-scanning/1) at `app/server/app.py:83`. The finding stays open so learners can fix it in their copies. These are observations in the template itself, not a freshly generated learner copy or candidate 0.2.0 CI result.

No second live learner repository is created by this implementation. Tests inside this template repository and disposable local copies cannot prove the complete GitHub **Use this template** experience. That remains a separate human/authorized validation step.

## Historical source-kit evidence

The bundled [secret provenance](fixtures/secret-validation.md), [recorded release receipt](fixtures/recorded-release/metadata.json), and [job-token evidence](fixtures/token-permissions-evidence.json) identify earlier author runs in `frye/pets-devsecops-rehearsal`. Those runs support the source exercise design; they were not performed in this template or by a new participant.

The underlying application has known dependency alerts. Successful functional tests or dependency review of a harmless PR do not clear the existing backlog or make this sample suitable for production.

## Remaining manual checks

| Check | Evidence still needed |
|---|---|
| Fresh GitHub template copy | Own public repository created through the new template, all bundled files present, core checks operating on the initial/main and starter-PR revisions |
| Repository security | Dependency graph, CodeQL default setup, secret scanning, and push protection verified in that new copy; settings are not assumed inherited |
| Codespaces | Actual creation with known payer/usage, existing checkout, harmless push, secret block/repair, stop/resume and persistence |
| Independent learner completion | A learner follows core Labs 6 and 7 and the recovery instructions from fresh, partial, and resumed states without hidden setup or someone else doing the work |
| Ruleset and release capability | An authorized learner repository confirms CodeQL merge-protection availability, exact ruleset enforcement, environment approval wait, artifact upload, and receipt checksum |
| File-editor fallback | Actual blocked commit and clean retry, distinct from terminal history repair |
| Pacing and venue | Representative learners, planned staffing/network, and a measured 120-minute duration without bypasses; current per-lab times are design budgets only |
| Event-date review | Template version, dependency advisories, action pins, and inactive fixture behavior rechecked |

The earlier authoring environment lacked Codespaces OAuth scope and an authenticated browser page handle. No additional authentication or billing changes have been made to force that check. [The inherited access record](fixtures/codespaces-rehearsal.json) provides historical context; it is not a new access test.

## Checkpoint

Publish the template as a prerelease with observed results and pending manual checks labeled accurately. Do not borrow a recorded run, successful source lookup, or local Linux test as a participant's completed result.

## Resources

[Template behavior](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template), [Codespaces](https://docs.github.com/en/codespaces/developing-in-a-codespace/creating-a-codespace-for-a-repository), and [CodeQL setup](https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/configure-code-scanning/configure-code-scanning).
