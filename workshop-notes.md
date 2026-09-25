# Workshop notes

Goal: improve the shelter's delivery process.

Pipeline Workflow:
Change -> PR -> Checks -> Merge

1. Change: Developer modifies code in a feature branch.
2. PR: A Pull Request is opened against the base branch.
3. Checks: Automated CI jobs run (e.g., api-tests, client-build, CodeQL).
4. Merge: Changes are merged into main once all checks pass.

Does the API expose vulnerable dependencies or unhandled injection vectors? and Does the app handle unauthenticated access to sensitive endpoints?

## Checkpoint: CI Baseline & Security Scope

- **Baseline Run:** `api-tests`, `client-build`, and `dependency-review` completed successfully with green status.
- **Token Permissions:** `GITHUB_TOKEN` is scoped to minimal permissions (`contents: read`). This allows `actions/checkout` to pull repository code for testing without granting unnecessary write access to source files or issues.
- **Blind Spots:**
  1. API functional assertions passed at this revision; however, startup configuration and runtime startup behavior were not tested.
  2. Potential vulnerabilities in third-party dependencies or unhandled authentication logic are not covered by functional unit tests and require static security analysis (SAST / CodeQL).

  # 2. Plan the shelter's security checks

| Asset and risk | Control to complete | Owner to assign | Acceptance result |
|---|---|---|---|
| API process: direct startup enables a debugger | Safe default plus regression test | ___ | `debug=False` asserted and targeted CodeQL finding removed |
| Dependency change: introduces a vulnerable package | ___ | Maintainer | High-severity introduction fails review; repaired version passes |
| Repository history: contains a credential | Repository push protection and exposure response | ___ | Verified nonfunctional fixture blocked; clean retry succeeds |
