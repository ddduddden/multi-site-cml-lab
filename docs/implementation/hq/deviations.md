# HQ Design Deviations

This file records **accepted differences** between the HQ design baseline and the verified implementation.

A failed test does not automatically create a deviation. Unexpected behaviour is investigated first. A verification test may be marked `Deviated` only when an accepted `HQ-DEV-NNN` record exists for that test.

Recording a deviation does not automatically rewrite `docs/hq-campus-design.md`. The design baseline is revised only when the evidence shows that the architectural intent itself should change.

## Project reference key

| Reference | Meaning |
|---|---|
| `HQ-DEV-NNN` | HQ design deviation |
| `HQ-VP-XX.YY` | Related HQ verification test |
| `HQ-TS-NNN` | Related HQ troubleshooting record |

## Entry template

```text
## HQ-DEV-NNN — Short title

Accepted:
DD-MM-YYYY

Related verification:
- HQ-VP-XX.YY

Related troubleshooting:
- HQ-TS-NNN, if applicable

Intended design:
...

Observed / accepted implementation:
...

Reason for divergence:
...

Decision taken:
...

Design baseline change required:
Yes / No

Design document action:
- None
- Update required
- Updated in <git-commit>

Evidence:
...

Status:
Accepted / Superseded
```

## Status meaning

- **Accepted** — the implementation intentionally differs from the current design baseline. Related verification tests may use the `Deviated` status.
- **Superseded** — the deviation no longer describes the current relationship between design and implementation, for example because the design baseline was formally revised or the implementation later changed.
