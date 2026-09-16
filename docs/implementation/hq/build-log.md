# HQ Build Log

This is the chronological record of deliberate HQ implementation activity.

The build log tells the build story in order. It remains the chronology even when something goes wrong; detailed diagnosis is moved to `troubleshooting.md` and linked back here.

A typo or an immediately corrected command does not need its own build-log event unless it materially affected the implementation.

## Project reference key

| Reference | Meaning |
|---|---|
| `HQ-VP-XX.YY` | Related HQ verification test |
| `HQ-TS-NNN` | Related HQ troubleshooting record |
| `HQ-DEV-NNN` | Related HQ design deviation |

## Entry template

```text
## DD-MM-YYYY — Short description

Implemented:
...

Related verification:
- HQ-VP-XX.YY

Result:
...

Troubleshooting:
- HQ-TS-NNN, if applicable

Deviation:
- HQ-DEV-NNN, if applicable

Config snapshot:
- configs/hq/<device>.cfg @ <git-commit>, once configs exist

Evidence:
- Path or reference, if applicable

Next:
...
```

### Traceability rule

Once `configs/hq/` exists, any build-log entry that depends on a specific device state should cite both:

1. The config filename.
2. The Git commit hash representing that state.

A filename by itself is not enough because the config will continue changing through later phases.
