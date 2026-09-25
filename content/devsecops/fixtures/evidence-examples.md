# Reading the evidence

Use these examples to understand which fields to inspect in your results. The [readiness register](../readiness.md) records what the authors observed. Record your own results in the [evidence checklist](../evidence.md).

## Why it matters

Similar green or red indicators can mean different things. Check the revision, the reporting job, and what the result actually measures.

| View | Look for | What would not prove the outcome |
|---|---|---|
| Actions CI | `api-tests` and `client-build`, success, expected SHA | An older run or a skipped job |
| CodeQL | Successful analysis of the target revision; `py/flask-debug` before and absent after fix | A successful scanner run that still reports the finding |
| PR dependency diff | `workshop-lab/dependency/requirements.txt`, PyJWT and exact version | Empty diff with a green action |
| Dependency failure | High advisory, affected version, failed `dependency-review` job | Network/API failure unrelated to an advisory |
| Blocked secret attempt | Provider/pattern, path and unpublished commit(s), rejection | A generic Git authentication failure |
| Repaired secret attempt | Clean commit/push succeeds, no fixture in submitted history | Adding a later deletion commit while earlier commits still contain it |
| Merge policy | Active own-repository rule and completed failed required `dependency-review` job listed as blocking | A draft PR, queued/missing check, or merge conflict blocking for another reason |
| Release | Own-run approval wait, successful prerequisites at the same SHA, and matching receipt/artifact | A receipt produced without the approval wait or from another SHA |

## Receipt fields

The workflow writes these fields with real values at runtime:

```text
kind: workshop-simulation-no-deployment
repository: the learner owner/repository
commit: full main SHA
ref: refs/heads/main
run: the actual Actions run URL
attempt: that run's attempt number
prerequisites: guard, release-api-tests, release-client-build
environment: workshop-demo
```

The summary adds the artifact ID/URL and uploaded archive digest after upload. `receipt.sha256` checks the receipt file itself. Neither digest is a signature or a claim of production deployment.

For a preserved author example, open [the downloaded receipt](recorded-release/receipt.json), [checksum](recorded-release/receipt.sha256), and [provenance](recorded-release/metadata.json). They came from the linked successful run after an observed approval wait and REST approval. The three-day Actions artifact may expire; these preserved files remain **historical author evidence**, never a learner's live completion.

## Recording a fallback

A facilitator may use a clearly labeled historical recording to explain a control. Include the source repository, PR and run URLs, kit version, date, route, and failure or repair state. Redact fixture values and private data. A recording can explain a control but cannot satisfy a learner's live evidence requirement. Documenting these fields does not mean a recording is included.

## Checkpoint and resources

Choose the evidence that proves the control, then record its actual state. [Workflow logs](https://docs.github.com/en/actions/how-tos/monitor-workflows/using-workflow-run-logs) explain how to inspect a run.
