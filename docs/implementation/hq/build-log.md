# HQ Build Log

Chronological record of significant HQ implementation steps.

Detailed verification results are recorded in [`verification-plan.md`](verification-plan.md). Meaningful faults are recorded in [`troubleshooting.md`](troubleshooting.md), and accepted design differences in [`deviations.md`](deviations.md).

## Project reference key

| Reference | Meaning |
|---|---|
| `HQ-VP-XX.YY` | HQ verification test — phase `XX`, test `YY` |
| `HQ-TS-NNN` | HQ troubleshooting record |
| `HQ-DEV-NNN` | HQ accepted design deviation |

---

## Phase 01 — HQ Platform Baseline

**Completed:** `20-09-2026`

### Implemented

- Built and booted the five-node HQ CML baseline.
- Applied the intended device hostnames and baseline console configuration.
- Confirmed the intended device roles and identities.
- Recorded the running IOSv and IOSvL2 software versions.
- Verified interface names and counts against the HQ Campus Design.
- Cabled the 18 planned physical links.
- Checked IOSv and IOSvL2 support for the features required by the design.
- Removed temporary capability-test configuration and confirmed the baseline was restored.

### Verification

- `HQ-VP-01.01` — HQ Device Inventory
- `HQ-VP-01.02` — Image and Software Version Inventory
- `HQ-VP-01.03` — Interface Inventory and Topology Fit
- `HQ-VP-01.04` — Platform Capability Review

### Result

**Phase 01 verified.** No platform capability blocker was identified for the approved HQ design.

Production VLAN, EtherChannel, Rapid PVST+, HSRP, routed-link, and OSPF configuration has not yet started.

### Evidence

[`evidence/hq/platform-baseline/`](../../../evidence/hq/platform-baseline/)

### Next

**Phase 02 — Layer 2 / VLAN Baseline**
