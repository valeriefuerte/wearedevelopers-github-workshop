# Incident card: an advisory after release

Complete this activity yourself in Lab 7 while the release checks run. The scenario is fictional; it does not describe an actual shelter exploit.

## Scenario

A new advisory affects a dependency used by a released revision. You have the release receipt, the manifest and lockfile at that exact SHA, and an owner who can review a patch. You do not yet know whether the vulnerable behavior is reachable in this application.

## Why it matters

A new advisory may require a patch, a revert, or further investigation even though the original checks passed. Start with evidence about the released revision, not just the current branch.

## Decide

1. Name the dependency and affected range from the advisory. Compare them with the manifest and lockfile at the receipt's released SHA.
2. Assign a specific owner or responsible role. Record known facts separately from questions.
3. Identify evidence still needed: whether the affected version is present, whether the vulnerable behavior is reachable, its impact, and available fixes. Include the tests, dependency review, and scans required before another merge.
4. Choose one next action: **patch**, **revert**, or **investigation**. Explain why the evidence supports that choice and who will review the change.
5. State how the replacement revision would be validated, approved, and recorded in a new receipt. If this were a credential exposure, revocation/rotation and access review would come before source cleanup.

## Checkpoint

Record the owner, released SHA, evidence needed, chosen action, and how you would identify the replacement revision. The workshop simulates this incident-response decision; it does not execute a production rollback.

## Resources

[NIST SSDF](https://csrc.nist.gov/projects/ssdf) includes responding to vulnerabilities, and [Dependabot alerts](https://docs.github.com/en/code-security/dependabot/dependabot-alerts/about-dependabot-alerts) supplies dependency context.
