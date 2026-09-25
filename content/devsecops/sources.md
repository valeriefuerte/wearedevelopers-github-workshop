# Technical sources and maintenance

## Why it matters

Action tags, package advisories, and product interfaces change. Record what was checked for each kit version so maintainers can review future updates.

## Source and runtime baseline

The original Pets source inspected locally and through the GitHub API is [d2437a6f3dbb1fe4bd5e97790ccc12c42cbfc03a](https://github.com/github-samples/pets-workshop/tree/d2437a6f3dbb1fe4bd5e97790ccc12c42cbfc03a). The live upstream `main` still matched it during the 2026-09-22 UTC check. Template copies have independent Git history; compatibility uses [file fingerprints](baseline.sha256), also recorded in [the manifest](workshop-kit.json).

The learner entry point is [frye/pets-devsecops-workshop-template](https://github.com/frye/pets-devsecops-workshop-template). It contains the pinned application and the workshop derived from [companion v0.1.2](https://github.com/frye/pets-devsecops-workshop/tree/ea050921bb902668d3e4fad5556548981c16cb91). Those links are attribution only: do not use either source for participant setup or send changes there. [template-source.json](../../template-source.json) records the inputs and deliberate overlays.

Standard `ubuntu-24.04` runners use Python 3.14 and Node 24. [Astro 6's upgrade guide](https://docs.astro.build/en/guides/upgrade-to/v6/) requires Node >=22.12. Other Pets workshop tracks are not included in this template; follow the bundled DevSecOps guide.

The Python constraints were resolved with pip for the existing three direct requirements. Linux's `greenlet` version was verified against PyPI. Both functional workflows use the same constraint block. This snapshot pins versions and can be updated, but does not lock package hashes. [Take-home maintenance](take-home/3-maintain-dependencies.md) explains direct pins and how to refresh the snapshot.

## Verified action pins

These release tags resolved to the following commit objects through the owners' GitHub API on 2026-09-22 UTC. Their `action.yml` files declare Node 24. Full commit pins are used in all starter workflows.

| Action release | Verified commit |
|---|---|
| [actions/checkout v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1) | `3d3c42e5aac5ba805825da76410c181273ba90b1` |
| [actions/setup-node v7.0.0](https://github.com/actions/setup-node/releases/tag/v7.0.0) | `820762786026740c76f36085b0efc47a31fe5020` |
| [actions/setup-python v7.0.0](https://github.com/actions/setup-python/releases/tag/v7.0.0) | `5fda3b95a4ea91299a34e894583c3862153e4b97` |
| [actions/dependency-review-action v5.0.0](https://github.com/actions/dependency-review-action/releases/tag/v5.0.0) | `a1d282b36b6f3519aa1f3fc636f609c47dddb294` |
| [actions/upload-artifact v7.0.1](https://github.com/actions/upload-artifact/releases/tag/v7.0.1) | `043fb46d1a93c77aae656e7c1c64a875d1fc6a0a` |

Maintainers can resolve a candidate tag with `gh api repos/OWNER/ACTION/git/ref/tags/TAG`. If it references an annotated tag object, resolve that object's commit too. Read the release notes and action inputs before updating. A commit pin makes the action reference immutable; it does not prove the action is safe.

## Exercise sources

| Exercise | Primary evidence |
|---|---|
| Code | [CodeQL `py/flask-debug`](https://codeql.github.com/codeql-query-help/python/py-flask-debug/): security severity 7.5, included in the default Python suite |
| Dependency before | [GHSA-ffqj-6fqr-9h24](https://github.com/advisories/GHSA-ffqj-6fqr-9h24): high, PyJWT `>=1.5.0,<2.4.0` |
| Later PyJWT advisory | [GHSA-752w-5fwx-jx9f](https://github.com/advisories/GHSA-752w-5fwx-jx9f): high, `<=2.11.0`, first patch 2.12.0 |
| Dependency after | [PyPI PyJWT 2.14.0](https://pypi.org/project/PyJWT/2.14.0/); GitHub Advisory API lookup for `PyJWT@2.14.0` returned an empty list on 2026-09-22 |
| Secret fixture | Official [GitHub Skills step at 77045e0](https://github.com/skills/introduction-to-secret-scanning/blob/77045e069f9deda2beba27990d65899c4ee4b221/.github/steps/3-enable-push-protection.md) explicitly labels its training value inactive |
| Push repair | [CLI repair](https://docs.github.com/en/code-security/how-tos/secure-your-secrets/work-with-leak-prevention/push-protection-on-the-command-line) and [web repair](https://docs.github.com/en/code-security/how-tos/secure-your-secrets/work-with-leak-prevention/push-protection-in-the-github-ui) |
| Environment | [Deployment protections](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments) and [environment REST API](https://docs.github.com/en/rest/deployments/environments) |
| Job-token identity | [GITHUB_TOKEN](https://docs.github.com/en/actions/concepts/security/github_token): distinct per-job installation token, repository scope and effective lifetime; [authentication tutorial](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token): job-level `issues: write` example |
| Cloud identity guidance only | [OIDC overview](https://docs.github.com/en/actions/concepts/security/openid-connect), [claims/trust reference](https://docs.github.com/en/actions/reference/security/oidc), [Azure](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-azure), and [AWS](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws) |

For the earlier companion v0.1.1, these identity sources were read on 2026-09-22 UTC. The OIDC reference explicitly distinguishes ID-bearing immutable subjects for new GitHub.com repositories after July 15, 2026. Provider trust must match the actual subject and audience; older name-only examples are not universal templates. The optional issue workflow requests no ID token and contains no provider login or new external action pin.

During authoring, the advisory API reported a later high-severity issue for PyJWT 2.10.1, so that candidate was rejected. Recheck the shipped repair before each event. An advisory lookup does not prove GitHub discovered the exercise manifest. Workflow evidence is recorded separately.

Do not infer a safe secret fixture from search-result prose. This kit uses only the attributed, delimiter-masked GitHub Skills value and never authenticates with it. The course's bypass activity and initial disable-protection activity are deliberately excluded. See [fixture provenance and route status](fixtures/secret-validation.md).

## Codespaces primary-route sources

The v0.1.2 route was checked against these official pages on 2026-09-22. Documentation review establishes the intended behavior, not a completed live Codespaces walkthrough; the authoring access limitation is recorded in [readiness](readiness.md).

| Topic | Source and relevant fact |
|---|---|
| Creation and payer | [Create a codespace for a repository](https://docs.github.com/en/codespaces/developing-in-a-codespace/creating-a-codespace-for-a-repository): create on the learner's selected branch and read the payer shown in the dialog |
| Editor and Git | [Source control](https://docs.github.com/en/codespaces/developing-in-a-codespace/using-source-control-in-your-codespace): use the existing checkout, terminal or VS Code editor, configured HTTPS authentication, then commit/push |
| Default image and persistence | [Deep dive](https://docs.github.com/en/codespaces/about-codespaces/deep-dive): the repository is already cloned under `/workspaces`; its saved files and siblings persist across stop/start and rebuild |
| Authentication | [Troubleshooting repository authentication](https://docs.github.com/en/codespaces/troubleshooting/troubleshooting-authentication-to-a-repository): keep configured repository-scoped authentication; do not overwrite its developer token |
| Repository access | [Manage access](https://docs.github.com/en/codespaces/managing-your-codespaces/managing-repository-access-for-your-codespaces): default access is scoped; this kit does not add custom grants or a required devcontainer |
| Security | [Security in Codespaces](https://docs.github.com/en/codespaces/reference/security-in-github-codespaces): credential and port boundaries; keep forwarded ports private and never print developer secrets |
| Usage | [Codespaces billing](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces): included personal quotas or approved sponsorship, separate compute/storage, and no unlimited free usage just because a repo is public |
| Stop/resume | [Stop and start](https://docs.github.com/en/codespaces/developing-in-a-codespace/stopping-and-starting-a-codespace): closing a browser tab is not stopping; stopped storage still counts |

Each learner's copy contains the complete materials. No companion fetch, local tag, or external Git history is needed. Template copies have independent history. Validation uses bundled files and checksums because the source commits do not need to exist in their `.git` directories.

## Attribution

Pets source remains under its [original license](SOURCE-LICENSE). The reused inactive fixture is covered by [GitHub Skills' license](fixtures/SKILLS-LICENSE). Other lesson text is written for this workshop; linked documentation is not copied into the package.

## Checkpoint

Before changing a pin or fixture, update the evidence and rerun local and authorized live checks. Publish a new version only in the template repository. Never retag an existing release or present a source lookup as an executed control.
