# Shelter frontend

This Astro client is part of the bundled [DevSecOps workshop](../../content/devsecops/README.md). Start with [setup](../../content/devsecops/0-setup.md) in your own copy of the workshop template, not an Astro starter or another repository.

## Why it matters

The client build checks that frontend changes compile. Security findings and policy checks answer different questions.

The core workflow runs `npm ci` and `npm run build` with Node 24 from this directory on a GitHub-hosted runner. Learners edit and use Git in Codespaces; no app install or local server is required.

The [Playwright suite](e2e-tests/README.md) remains an optional maintainer extension outside the core checks.

## Checkpoint

Inspect the `client-build` result for your PR's latest revision on GitHub. Do not treat a local editor save or an earlier green run as the current result.

## Resources

[Astro project structure](https://docs.astro.build/en/basics/project-structure/) and [Astro 6 runtime requirements](https://docs.astro.build/en/guides/upgrade-to/v6/).
