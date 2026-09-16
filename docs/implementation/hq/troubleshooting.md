# HQ Troubleshooting

This file records **meaningful diagnostic investigations**.

It is not a diary of every mistake. The build log remains the chronology; a build-log or verification entry links here only when the observed behaviour requires real investigation.

## Project reference key

| Reference | Meaning |
|---|---|
| `HQ-TS-NNN` | HQ troubleshooting record |
| `HQ-VP-XX.YY` | Related HQ verification test |
| `HQ-DEV-NNN` | Related HQ design deviation |

## When to create a troubleshooting record

**Normally does not need an `HQ-TS-NNN` record:**
- A mistyped command that is corrected immediately.
- A wrong interface selected and immediately corrected.
- A forgotten `no shutdown` noticed immediately.
- A minor syntax correction with no meaningful effect on the build.

**Normally does justify an `HQ-TS-NNN` record:**
- A protocol fails to establish even though the configuration appears correct.
- Failover or reconvergence differs from the expected behaviour.
- A platform or image behaves differently from the documented assumption.
- A routing decision cannot initially be explained.
- A feature limitation requires investigation before implementation can continue.

## Entry template

```text
## HQ-TS-NNN — Short title

Opened:
DD-MM-YYYY

Related verification:
- HQ-VP-XX.YY

Related build-log entry:
- DD-MM-YYYY — description

Symptom:
...

Expected behaviour:
...

Scope / impact:
...

Investigation:
1. ...
2. ...
3. ...

Root cause:
...

Correction:
...

Re-verification:
...

Evidence:
...

Related deviation:
- HQ-DEV-NNN, only if an accepted design deviation results

Status:
Open / Resolved
```

## Cross-reference rule

Resolving a troubleshooting record does not automatically mean the related verification test is `Verified`.

After the correction, the verification test must be run or re-run and its own `Observed result`, `Status`, and evidence updated.
