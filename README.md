# Pets DevSecOps workshop template

**[Start the workshop](content/devsecops/0-setup.md)** | [Lessons and agenda](content/devsecops/README.md) | [Take-home labs](content/devsecops/take-home/README.md)

Create your own public repository for the shelter application from this template. It includes the complete workshop and its core checks.

1. Select **Use this template > Create a new repository** on [frye/pets-devsecops-workshop-template](https://github.com/frye/pets-devsecops-workshop-template). Choose your account, a public repository, and the default branch only.
2. In **your new copy**, select **Code > Codespaces > Create codespace on main**. Check Codespaces access, payer, and usage first.
3. Open `content/devsecops/0-setup.md` in the existing checkout. Verify Actions and your repository's security settings, then create the starter PR.

No companion fetch, second clone, or workflow-install step is needed. The app is in `app/`, the lessons are in `content/devsecops/`, and `.github/workflows` contains exactly the two core workflows. Builds and tests run in Actions; Codespaces provides the editor and Git terminal.

## Why it matters

The shelter's functional tests cannot answer every security question. You'll fix a code-scanning finding, review a dependency change, and practice secret protection. Then you'll configure merge policy and approve a cloud-free release simulation in your own repository.

The complete agenda is exactly 120 minutes: eight minutes for setup, 57 for Labs 1 through 5, 48 for learner-run Labs 6 and 7, and seven for closing. These are planned budgets that have not been confirmed in a rehearsal. If platform results are delayed or unavailable, record them as pending or incomplete. The repository includes recovery guides and optional material on job tokens and OIDC. The guides also cover local Git and GitHub file-editor fallbacks. You need no cloud account or personal token.

> [!IMPORTANT]
> This is a training prerelease, not a production-ready application. The debug-startup finding is intentional exercise input; existing dependency alerts are not claimed resolved. Do not run or expose the app as a public service. Automated tests do not replace a fresh template-copy check, a live Codespaces check, or a human pacing rehearsal; see [readiness](content/devsecops/readiness.md).

## Checkpoint

Your learner copy has the app, bundled guides, `ci.yml`, and `dependency-review.yml` before you create an exercise branch. Still verify dependency graph, CodeQL default setup, secret scanning, and push protection in that copy; repository settings are not assumed to transfer.

## Maintainers and sources

Make changes to this template only in **frye/pets-devsecops-workshop-template**. Participants make lesson changes and PRs in their own copies. Do not send workshop PRs to the original Pets project or the earlier companion.

The [source manifest](template-source.json) records the pinned application and workshop sources, whose licenses and attribution are retained. Use these sources only to trace where the template came from, not to set up your learner repository. [Maintainer instructions](content/devsecops/facilitator.md#maintain-and-publish-this-template) cover validation and packaging.

## Resources

[Creating from a template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template), [Codespaces creation](https://docs.github.com/en/codespaces/developing-in-a-codespace/creating-a-codespace-for-a-repository), and [LICENSE](LICENSE).
