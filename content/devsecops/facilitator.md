# Facilitator guide

| [Overview](README.md) | [Readiness register](readiness.md) |
|:---|---:|

## Why it matters

Plan for up to 90 participant-owned laptops, one facilitator, and 1-2 helpers. With this staffing, learners need to complete prework. Use Codespaces as the primary route and keep learners in their own public repositories. Facilitators and helpers guide and troubleshoot; they do not configure settings, approve runs, or complete learner steps for them.

## Before announcing the event

1. Direct learners only to [frye/pets-devsecops-workshop-template](https://github.com/frye/pets-devsecops-workshop-template). Their copies already contain the app, lessons, and two core workflows.
2. Complete every mandatory [readiness gate](readiness.md). Distinguish source inspection and local tests from live GitHub results. Treat the prerelease as review material; it does not establish event readiness.
3. Confirm the published template version before the event. Update source pins only through reviewed changes in this template repository, and do not silently change its default branch during a cohort.
4. Rehearse creating an actual template copy, checking security settings, starting Codespaces, running preinstalled CI, making a harmless commit/push, and stopping and resuming the space. Test local Git and file-editor fallbacks separately. Earlier native Linux tests do not establish that Codespaces authentication works.
5. Rehearse with representative prepared learners and managed/personal laptops on the venue network. Record wall-clock editing, Actions latency, help requests, and every outcome. The equation `8 + 75 + 7 = 90` only confirms the minutes add up; rehearsal must show that the schedule fits.

## Prework and staffing

Collect learner repository, starter-PR, and CI run URLs, plus the bundled template version, through existing communications. Ask whether learners opened Codespaces, pushed a harmless change, and can stop and resume the space. Record any fallback they used. Do not collect tokens or private connection details, or require another signup.

Walk learners through **Codespaces** using the browser-based VS Code editor and integrated terminal. Keep the local Git and file-editor fallback references available for helpers rather than repeating every route. Assign the 1-2 helpers to tables or zones, prioritizing access and startup, Git problems, and the three individual exercises. At maximum capacity, a helper may cover 45-90 learners. Reconsider capacity if too few learners have completed prework.

Check power, Wi-Fi, GitHub sign-in, Actions access, and the Codespaces editor, terminal, and reconnection on representative personal and company-managed laptops. Confirm allowed quota or sponsorship before startup; do not change billing or machine size to force access. Use one codespace per learner repository on the smallest suitable machine, normally two cores. Do not require a custom devcontainer or app install. Neither a partner's run nor a facilitator's repository completes another attendee's checkpoint.

## Prepare to support Labs 6 and 7

No separate facilitator repository is required for the core merge-policy or release exercises. Each learner works in their own repository and performs their own settings changes and approvals. Before the event:

1. Review [Lab 6](6-merge-policy.md), [Lab 7](7-delivery-and-response.md), and the [resume guide](take-home/0-resume.md) so helpers can identify safe recovery states.
2. Confirm the documented ruleset has no bypass, requires zero approvals, names the three exact Actions checks, requires the branch to be up to date, omits merge queue, and selects CodeQL at High or higher.
3. Confirm the environment instructions require the learner's own account as reviewer, self-review prevention off for training, administrator bypass disabled, and exactly one branch rule (`main`) before the optional workflow is installed.
4. Remind learners that Lab 4's dependency PR must stay open and failing until Lab 6. Do not demonstrate a repaired state first or accept a queued/missing check as a block.
5. Use only the bundled [incident card](fixtures/incident-card.md) and evidence references to coach the learner's own decision. Examples, recordings, and facilitator runs can explain a control but never count as learner evidence.

## Run the room

| Event minute | Action |
|---:|---|
| 00-08 | Verify prework and resume the existing codespace; triage small remaining issues |
| 08-15 | Baseline and functional blind spots |
| 15-21 | Three-row threat model |
| 21-38 | Individual code fix/test; start scans |
| 38-53 | Callback to code results; create/observe dependency failure and leave its PR open |
| 53-65 | Individual secret-protection attempt and clean retry |
| 65-89 | Learners configure rules, prove the failed-check block, repair the fixture, and merge only safe work |
| 89-113 | Learners configure the environment, merge the reviewed workflow, approve/verify a release, and complete the incident card |
| 113-120 | Record individual evidence, identify resume state, and stop safely |

The agenda covers event minutes 0 through 120 exactly. The budgets have not been confirmed in a rehearsal, and service results may still be pending when the session ends.

After a four-minute wait, continue with an independent step and return to the result at the next scheduled check-in. This is a facilitation threshold, not a promise about Actions response time. If the Lab 4 dependency result is still pending, learners may set up the ruleset in Lab 6. They must return to the actual failed run before claiming a block or repairing the fixture. During Lab 7, learners can complete the incident card while release checks run. They must observe all three successful prerequisites and the environment approval wait before approving.

At minute 113, stop starting new troubleshooting or edits and begin closing. Mark queued, unavailable, or unverified outcomes as pending or incomplete. Even learners familiar with the tools may need more time; let them resume later rather than rush. Never bypass secret protection, required checks, code-scanning policy, or approval to finish on time.

At closing, have learners save and push intended safe work and explicitly stop their own codespace. Closing a tab does not stop compute; stopped storage still counts. Keep forwarded ports private. Preserve needed work and evidence before deletion, and reopen the same space for take-home.

## Optional identity practice

During lesson 1's existing seven minutes, identify the job's GitHub App installation identity and read-only scope alongside the CI commands. Point to [the self-service workload-identity lab](take-home/4-workload-identity.md) for later practice. Offer its two-job permission exercise as optional take-home or a separately scheduled follow-along. Do not add another required outcome to the 120-minute core or displace the secret, merge-policy, or release exercises.

Learners copy the bundled optional workflow in Codespaces and install it through a reviewed PR. Its jobs execute only in Actions. Do not run the proof with the developer `GITHUB_TOKEN` or print either credential. OIDC remains reading only; no cloud account, PAT, or new app is required.

## Maintain and publish this template

Work only in a checkout of `frye/pets-devsecops-workshop-template`. From its root:

```bash
python3 -m unittest discover -s content/devsecops/tests -v
python3 content/devsecops/scripts/validate-kit.py
bash -n content/devsecops/scripts/prepare-devsecops.sh
actionlint .github/workflows/ci.yml .github/workflows/dependency-review.yml content/devsecops/starter/ci.yml content/devsecops/starter/dependency-review.yml content/devsecops/starter/release-simulation.yml content/devsecops/starter/token-permissions.yml
python3 content/devsecops/scripts/build-kit.py --refresh-manifest --output-dir /path/to/template-output
python3 content/devsecops/scripts/build-kit.py --output-dir /path/to/second-output
```

Use an isolated validation environment with Flask dependencies and PyYAML. Tests use the bundled baseline and independent-history temporary repositories, not the original source's Git objects. These are author tools, not learner prerequisites.

For the author test suite on Windows, select the Git Bash executable explicitly before invoking Python. This avoids Python selecting the unrelated Windows Subsystem for Linux launcher:

```bash
export WORKSHOP_BASH="$(cygpath -w "$BASH")"
```

Run that command in Git Bash only. The learner's helper invocation already runs in their chosen Bash terminal.

The builder verifies baseline fingerprints, source metadata, and payload inventories, then creates a deterministic ZIP of the complete template and a SHA-256 sidecar. Refresh manifests only after reviewing changes. The builder does not download or approve a different application baseline. Compare two archive hashes, and keep output outside the checkout.

Publish the whole repository layout, including `app/`, bundled `content/devsecops`, and exactly the two active core workflows. Keep optional starters inactive. Use an unused immutable version in this repository; do not modify previous companion releases.

All maintainer commits, PRs, releases, and setting changes target this template only. Source repositories in `template-source.json` are read-only inputs. Update those inputs through a reviewed PR here, record their provenance, and repeat the exercise checks. Never push to the original Pets or earlier companion repository.

## Checkpoint

The application and complete lessons ship together, and bundled paths work without another fetch. The readiness register separates automated checks from checks with a fresh copy, learners, and Codespaces. Preserve that distinction in event invitations.

## Resources

[GitHub template repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template), [Git archive](https://git-scm.com/docs/git-archive), and [Actions usage](https://docs.github.com/en/billing/concepts/product-billing/github-actions).

[Codespaces creation](https://docs.github.com/en/codespaces/developing-in-a-codespace/creating-a-codespace-for-a-repository), [billing](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces), and [stop/start](https://docs.github.com/en/codespaces/developing-in-a-codespace/stopping-and-starting-a-codespace) support the primary route.
