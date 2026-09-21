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

---

## Phase 02 — Layer 2 / VLAN Baseline

**Completed:** `21-09-2026`

### Implemented

- Created and named the approved HQ VLAN database on `hq-d1`, `hq-d2`, and `hq-a1`.
- Configured the intended `hq-a1` endpoint-facing access ports, including voice VLAN `120` on `Gi2/0`.
- Assigned all `hq-a1` interfaces not yet in service to VLAN `191` (`PARKING`) and administratively shut them down, including the future `Po10` and `Po20` members until Phase 03.
- Left VLAN `1` present as the platform default with no production or management access ports assigned.

### Verification

- `HQ-VP-02.01` — VLAN Database
- `HQ-VP-02.02` — Access-Port Assignments
- `HQ-VP-02.03` — Parking-VLAN Policy

### Result

**Phase 02 verified.** The approved VLAN database, access-port assignments, voice-VLAN assignment, and parking-VLAN policy were demonstrated and recorded.

EtherChannel/trunking and later Layer 2 and Layer 3 features remain for subsequent phases.

### Evidence

[`evidence/hq/layer2-vlan-baseline/`](../../../evidence/hq/layer2-vlan-baseline/)

### Next

**Phase 03 — LACP EtherChannel**
