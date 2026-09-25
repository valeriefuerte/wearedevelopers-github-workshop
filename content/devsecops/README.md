# DevSecOps: from a green build to a safer release

| [Template home](../../README.md) | [Next: setup](0-setup.md) |
|:---|---:|

You're volunteering at the dog shelter. Its Flask API and Astro website pass their functional tests. Now you need to check what happens when a change leaves the debugger enabled, introduces a vulnerable package, or includes a credential.

You'll fix code, observe dependency review reject a vulnerable package, and practice secret protection in your own public repository. Then you'll configure merge policy and run a cloud-free release simulation there. The [take-home companions](take-home/README.md) help you recover interrupted work and perform additional checks. Follow Labs 6 and 7 below for the main procedures.

> [!IMPORTANT]
> Candidate **0.2.0** bundles the application, complete workshop, and two installed core workflows. The application is not production-ready, and no live learner rehearsal is claimed. The [readiness register](readiness.md) separates source-level validation and historical evidence from pending checks on GitHub, in Codespaces, and with learners. The published `v0.1.0` release remains immutable.

## What you need

Bring a laptop with internet access. Your GitHub.com account must be able to create and administer a public learner repository, run standard GitHub-hosted Actions, configure its security settings, and use Codespaces with sufficient included usage or approved sponsorship. Use only the shelter's public sample data.

The primary route uses browser-based VS Code in **GitHub Codespaces**, where Git and Bash are already available. The learner repository is already checked out, so you do not clone it again or install the application. Your laptop needs no Python, Node.js, Docker, or Git; you also need no Azure account, Copilot subscription, second reviewer, or pasted PAT. Use the default image and smallest suitable permitted machine, normally two cores, for editing and Git.

Codespaces compute and storage have usage limits and a payer. Public repositories do not provide unlimited free Codespaces. Check access, quota, and who pays before starting. Standard Actions usage is separate. If policy, quota, or connectivity prevents the primary route, use the documented [local Git](0-setup.md#fallback-a-local-vs-code-and-git) or [file-editor fallback](0-setup.md#fallback-b-github-file-editor).

Throughout these guides, **editor** and **terminal** mean the Codespaces editor and integrated Bash terminal unless labeled as a fallback. Use GitHub.com for PRs, settings, starting Actions runs, viewing results, and approvals. Application builds, tests, scans, and the optional token proof run in Actions, not Codespaces.

Finish [Step 0](0-setup.md) before the event. Use the opening eight minutes to verify readiness.

## Agenda

These are design budgets. No representative learner rehearsal has established the timing.

| Lesson | Event minutes | Budget | Format |
|---|---:|---:|---|
| [0. Setup checkpoint](0-setup.md) | 00-08 | 8 | Verify prework |
| [1. DevOps baseline](1-devops-baseline.md) | 08-15 | 7 | Shared discussion |
| [2. Security planning](2-security-planning.md) | 15-21 | 6 | Shared planning |
| [3. Code scanning](3-code-scanning.md) | 21-38 | 17 | Individual fix and test |
| [4. Dependencies](4-dependencies.md) | 38-53 | 15 | Observe failure; leave the PR open and unrepaired |
| [5. Secrets](5-secrets.md) | 53-65 | 12 | Individual block and clean retry |
| [6. Merge policy](6-merge-policy.md) | 65-89 | 24 | Individual ruleset, blocked check, repair, safe merge |
| [7. Delivery and response](7-delivery-and-response.md) | 89-113 | 24 | Individual environment, release approval, incident decision |
| [8. Closing](8-wrap-up.md) | 113-120 | 7 | Record live evidence and questions |

The complete agenda, including setup and closing, totals exactly 120 minutes. Setup and Labs 1 through 5 occupy the first 65 minutes. Labs 6 and 7 each allow 24 minutes for learners to configure settings and work on PRs. No live learner rehearsal has verified these budgets. If Actions or CodeQL takes longer, leave results pending. Do not bypass a control or mark a pending result successful to meet the schedule.

For optional practice after the 120-minute workshop, [prove a workflow's GitHub API permissions](take-home/4-workload-identity.md): observe a denied request, then a separate narrowly authorized job and its closed training issue. The guide also points to OIDC for future cloud identity work. It does not replace any core exercise.

## Using this kit

Create your learner copy from [frye/pets-devsecops-workshop-template](https://github.com/frye/pets-devsecops-workshop-template), then open a codespace on **your copy's `main`**. The app and this guide are already in that checkout, with both core workflows installed. [Step 0](0-setup.md) verifies Actions and your own security settings before the first PR.

No companion fetch, workflow-install script, or second application clone is required. The manifest identifies the current `0.2.0` candidate; the published [v0.1.0 release](https://github.com/frye/pets-devsecops-workshop-template/releases/tag/v0.1.0) remains an immutable historical archive. A future release of this candidate must be published separately. The template UI copies the current default branch; existing learner copies do not automatically receive future updates.

Use one codespace for your learner repository. Saving changes in the editor does not commit or push them. Preserve intended work on GitHub and [stop the codespace explicitly](0-setup.md#08-stop-and-reuse-your-codespace) when finished. Closing its tab does not stop compute, and stopped storage still counts toward usage. Keep forwarded ports private; the workshop does not add app hosting.

Lesson, starter, solution, and take-home links stay within this copy. [Sources](sources.md) records the read-only source attribution. Participants work only in their learner repositories; template maintainers send changes only to this template repository.

| Your next task | Guide |
|---|---|
| Start from no setup | [Step 0](0-setup.md) |
| Return after the event or recover partial work | [Resume](take-home/0-resume.md) |
| Find exact edits and explanations | [Solutions](solutions/README.md) |
| Track personal results | [Evidence checklist](evidence.md) |
| Run the event or package the full template | [Facilitator guide](facilitator.md) |
| Diagnose a failed step | [Troubleshooting](take-home/troubleshooting.md) |
| Review pins, advisories, and limitations | [Technical sources](sources.md) |

## Why it matters

The shelter needs evidence about both functionality and risk. Each lesson identifies the control, its owner, and the result needed to proceed. Mark checks pending until their results arrive. Examples, expected-result tables, recordings, and another person's repository are references only; they do not complete your individual exercise.

## Optional primers

[GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow) explains the PR cycle. [What is DevOps?](https://learn.microsoft.com/en-us/devops/what-is-devops) introduces the delivery process. [NIST's Secure Software Development Framework](https://csrc.nist.gov/projects/ssdf) connects development to vulnerability response.

| [Template home](../../README.md) | [Next: setup](0-setup.md) |
|:---|---:|
