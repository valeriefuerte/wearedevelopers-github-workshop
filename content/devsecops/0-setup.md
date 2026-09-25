# 0. Open your self-contained workshop

| [Previous: overview](README.md) | [Next: baseline](1-devops-baseline.md) |
|:---|---:|

## Why it matters

Your template copy already contains the application, lessons, and two core workflows. Before the event, check your access and repository security settings. You do not need to assemble files from another repository. Use the opening eight minutes to verify readiness.

The flow is **use the workshop template -> open your copy in Codespaces -> verify checks and security settings -> open the starter PR**. There is no companion fetch, archive extraction, second clone, or workflow-install command.

Unless labeled otherwise, **editor** means browser-based VS Code in Codespaces and **terminal** means its integrated Bash terminal. Run Git commands from your learner root, in order, stopping at any error. Use GitHub.com for PRs, settings, Actions results, and approvals.

## 0.1 Check your account and Codespaces access

1. Sign in at [GitHub.com](https://github.com) with an account that can own or administer a public repository and use Actions.
2. Follow your employer's public-training policy. Enterprise Managed Users cannot create public repositories; use a personal account only if permitted. If needed, use [signup](https://github.com/signup), verify an email you control, and configure two-factor authentication. Do not use an email already verified for a managed user.
3. Check that Codespaces is available and confirm the payer displayed during creation. Check your remaining compute and storage allowance or approved sponsorship. Public repositories do not provide unlimited free Codespaces. Codespaces usage is separate from Actions.
4. Do not add payment details, increase budgets, widen credentials, or evade policy to continue. Use the [local Git](#fallback-a-local-vs-code-and-git) or [file-editor fallback](#fallback-b-github-file-editor) if needed.

You need no laptop runtime, Azure account, Copilot subscription, or pasted PAT. If no route is permitted, arrange approved observation and leave individual outcomes incomplete.

## 0.2 Create your copy from this template

1. Open [frye/pets-devsecops-workshop-template](https://github.com/frye/pets-devsecops-workshop-template). This is the only learner template for this version.
2. Select **Use this template > Create a new repository**. Do not open a codespace on the template owner's repository.
3. Choose your account as **Owner**, name the repository `pets-devsecops` (or another unused name), select **Public**, and leave **Include all branches** off.
4. Select **Create repository from template**. Confirm the URL names your learner account, the default branch is `main`, and **Settings** and **Actions** are accessible.
5. Confirm these files are present on `main`:

   ```text
   app/server/app.py
   app/client/package-lock.json
   content/devsecops/0-setup.md
   .github/workflows/ci.yml
   .github/workflows/dependency-review.yml
   ```

GitHub copies the template's current default-branch files and starts independent history. The bundled [manifest](workshop-kit.json) identifies this version; old releases are retained for reference. Do not copy the original source repository, fetch the earlier companion, or merge their histories into your learner copy.

## 0.3 Open your codespace

1. In **your learner repository**, select `main`, then **Code > Codespaces**.
2. Confirm who pays. Use the default image and smallest suitable permitted machine, normally two cores. Use **New with options** only if you need to inspect those choices.
3. Select **Create codespace on main**. If you already have a space for this copy, reopen it.
4. Wait for initialization and select **Terminal > New Terminal**. Inspect the checkout Codespaces already created:

   ```bash
   repo_root=$(git rev-parse --show-toplevel) && cd "$repo_root"
   pwd
   git remote get-url origin
   git branch --show-current
   git status --short
   ```

5. Confirm the root is under `/workspaces`, origin is your learner repository, the branch is `main`, and the tree has no unrelated edits. Open `content/devsecops/README.md` in the editor.

Do not clone again, add a required devcontainer, rebuild the image, install dependencies, or start the app. Tests, builds, and scans run in Actions. Keep forwarded ports private. If you see a prompt to fork or an unexpected origin, stop and open the correct learner copy.

All guides and starters are in `content/devsecops` in your checkout. Later copy commands use paths relative to the learner root. Saving a file does not commit or push it.

## 0.4 Verify the preinstalled checks

1. On your learner repository's **Actions** page, enable workflows if prompted and policy permits.
2. Open **CI** and inspect any run for `main`. If template creation did not start one, choose **Run workflow > main**. Do not assume the template owner's run is your result.
3. Confirm the exact jobs `api-tests` and `client-build` succeed, and record your run URL.
4. If a file is missing or differs from the bundled starter, follow [troubleshooting](take-home/troubleshooting.md). Do not blindly reinstall files or disable checks to obtain green results.

The two active workflows are already on `main` before any exercise branch. `dependency-review` is PR-triggered and is checked in 0.6. `release-simulation.yml` and `token-permissions.yml` remain optional files under `content/devsecops/starter`; do not install them during prework.

## 0.5 Verify security in your learner repository

A template copies files. Verify security settings, secrets, environments, rulesets, and reviewer lists in your own repository because they may differ from the template. Organization defaults may already enable some settings.

1. Open **Settings > Advanced Security** and confirm **Dependency graph** is enabled.
2. Under **CodeQL analysis**, choose **Set up > Default**, confirm Python is detected, review other languages, and enable it. Do not combine default and advanced setup.
3. Confirm **Secret scanning** and repository **Push protection** are enabled. Do not test a fixture or real credential during prework.
4. Wait for successful CodeQL analysis. In **Security and quality > Code scanning**, locate **Flask app is run in debug mode**, rule `py/flask-debug`, at `app/server/app.py`.
5. Record the analysis and alert links. Leave the intentional finding for lesson 3.

Missing, failed, or pending analysis is not a ready baseline. Report the run and bundled version; do not add a vulnerable endpoint to force detection. The [readiness register](readiness.md) distinguishes this template's results from historical source-kit evidence.

## 0.6 Create the working PR

1. In the same codespace, check your commit identity privately:

   ```bash
   git config --get user.name
   git config --get user.email
   ```

   If the identity is missing or unsuitable, use [repository-local identity recovery](take-home/troubleshooting.md#commit-identity). Keep the configured Codespaces authentication. Never print or replace its developer token, or paste a PAT. That credential differs from an Actions job token.
2. Confirm a clean `main`, then create your working branch:

   ```bash
   git status --short
   git branch --show-current
   git switch -c exercise/shelter-change
   ```

3. In the editor, create and save `workshop-notes.md`:

   ```markdown
   # Workshop notes

   Goal: improve the shelter's delivery process.
   ```

4. Commit and push only that file:

   ```bash
   git add -- workshop-notes.md
   git commit -m "Start the shelter workshop"
   git push -u origin exercise/shelter-change
   ```

5. On GitHub.com, open **Prepare the shelter for a safer release** with base `main` and compare `exercise/shelter-change`, both in **your learner repository**. Do not open a PR against the template, original source, or old companion.
6. Wait for `api-tests`, `client-build`, and `dependency-review` to pass and confirm CodeQL operates. Leave the PR open and unmerged.

If the branch or PR already exists, use [Resume](take-home/0-resume.md) rather than creating a duplicate or discarding work.

## 0.7 Checkpoint: ready for Step 1

| Check | Your evidence |
|---|---|
| Own public copy | Correct URL, accessible settings, permitted account/usage |
| Bundled baseline | App, guides, and both core workflows on your `main` |
| Editing route | Own codespace opens and harmless push succeeds, or named fallback |
| Functional/security baseline | Passing CI, successful CodeQL with intended debug finding, graph and secret protection enabled |
| Working PR | Open own-repository PR with passing core checks |

Send your repository URL, PR URL, CI run URL, and bundled version through the event readiness channel. State whether you used Codespaces or a fallback. Never share tokens or private connection details, or present another repository's result as your own.

## 0.8 Stop and reuse your codespace

Reuse one codespace throughout the workshop. Saved checkout files persist when you stop, restart, or rebuild it. Deleting the codespace removes unpushed work. Save and push intended safe changes before leaving; never publish a rejected fixture as a backup.

Select **Codespaces: Stop Codespace** in the Command Palette or **Stop codespace** at [github.com/codespaces](https://github.com/codespaces). Closing the browser tab does not stop compute. Stopped storage still counts. Reopen the same space for take-home work and delete it only after preserving needed work and receipts.

If usage blocks resuming, consult [exporting changes](https://docs.github.com/en/codespaces/troubleshooting/exporting-changes-to-a-branch) and inspect what will be published before exporting.

## Fallback A: local VS Code and Git

Use an existing editor, Bash-compatible terminal, and authenticated Git if Codespaces is unavailable. Only this route needs a clone:

```bash
git clone https://github.com/YOUR-OWNER/pets-devsecops.git
cd pets-devsecops
```

Substitute your learner repository's owner and name, then open the bundled guide and continue at 0.4. There is no companion fetch or workflow-install step. Later Git commands are the same. You do not need Python, Node.js, or Docker on your laptop. Codespaces lifecycle guidance does not apply to this local clone.

## Fallback B: GitHub file editor

Use GitHub.com's editor if neither Codespaces nor local Git is available. Your template copy already contains everything:

1. Complete 0.4 and 0.5 on GitHub.
2. On your copy's `main`, select **Add file > Create new file**, create the same `workshop-notes.md`, and choose **Create a new branch for this commit and start a pull request**, named `exercise/shelter-change`.
3. Complete the same PR and readiness checks. For later edits, select the intended branch and use the local `content/devsecops` starter/fixture files in that copy.

The file editor has no terminal. Its secret lesson blocks a commit and repairs an uncommitted edit; it does not prove terminal history repair. Use lesson 5's labeled fallback.

## Resources

[Create from a template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template), [create a codespace](https://docs.github.com/en/codespaces/developing-in-a-codespace/creating-a-codespace-for-a-repository), [Codespaces authentication](https://docs.github.com/en/codespaces/troubleshooting/troubleshooting-authentication-to-a-repository), [usage](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces), and [stop/resume](https://docs.github.com/en/codespaces/developing-in-a-codespace/stopping-and-starting-a-codespace).

| [Previous: overview](README.md) | [Next: baseline](1-devops-baseline.md) |
|:---|---:|
