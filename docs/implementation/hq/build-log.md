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

---

## Phase 03 — LACP EtherChannel

**Completed:** `22-09-2026`

### Implemented

- Built `Po10` between `hq-a1` and `hq-d1` using two LACP member links.
- Built `Po20` between `hq-a1` and `hq-d2` using two LACP member links.
- Built `Po30` between `hq-d1` and `hq-d2` using four LACP member links.
- Configured all three Port-Channels as 802.1Q trunks with native VLAN `190`.
- Applied the approved allowed-VLAN list `112,120,130,140,152,160,170,190,199`.
- Reconfigured the former Phase 02 parked `Po10` and `Po20` member interfaces for their production EtherChannel roles.

### Verification

- `HQ-VP-03.01` — EtherChannel Formation and LACP State
- `HQ-VP-03.02` — Port-Channel Trunk Policy
- `HQ-VP-03.03` — Operational Trunk and VLAN State
- `HQ-VP-03.04` — EtherChannel Member-Link Failure and Recovery

### Result

**Phase 03 verified.** `Po10`, `Po20`, and `Po30` formed successfully with all intended LACP members bundled. The approved trunk policy was operational across all three Port-Channels, and each bundle remained operational during a controlled single-member failure and recovered correctly after restoration.

Deterministic Rapid PVST+ root placement and forwarding behaviour remain for Phase 04.

### Evidence

[`evidence/hq/etherchannel/`](../../../evidence/hq/etherchannel/)

### Next

**Phase 04 — Rapid PVST+**

---

## Phase 04 — Rapid PVST+

**Completed:** `24-09-2026`

### Implemented

- Enabled Rapid PVST+ on `hq-a1`, `hq-d1`, and `hq-d2`.
- Configured `hq-d1` as root primary for VLANs `112,130,152,170,190`.
- Configured `hq-d2` as root primary for VLANs `120,140,160,199`.
- Configured each multilayer distribution switch as root secondary for the other's VLAN group.
- Configured deterministic `hq-d1` root placement for native VLAN `190`.
- Preserved the existing Phase 03 EtherChannel and trunk configuration.
- Applied Root Guard on the distribution-to-access Port-Channels (`hq-d1 Po10` and `hq-d2 Po20`) to protect the intended distribution-layer STP root placement from a superior BPDU arriving from the access layer.
- Corrected the VLAN `152` name on `hq-a1` to `GUEST` after a minor naming issue was identified during evidence review. No functional behaviour was affected.

### Verification

- `HQ-VP-04.01` — Rapid PVST+ Mode and Root Placement
- `HQ-VP-04.02` — Access-Layer Forwarding and Alternate Paths
- `HQ-VP-04.03` — STP Path Failure and Recovery

### Result

**Phase 04 verified.** Rapid PVST+ operated across all three HQ switches and matched the approved root-placement design. Representative VLAN checks confirmed the expected forwarding paths, and controlled failures of `Po10` and `Po20` proved alternate-path recovery in both directions.

SVI addressing and HSRP gateway redundancy remain for Phase 05.

### Evidence

[`evidence/hq/spanning-tree/`](../../../evidence/hq/spanning-tree/)

### Next

**Phase 05 — SVIs and HSRP**


---

## Phase 05 — SVIs and HSRP

**Completed:** `27-09-2026`

### Implemented

- Configured the approved SVIs and HSRP gateways on `hq-d1` and `hq-d2`, using `.2` / `.3` physical addresses and `.1` virtual gateways.
- Applied HSRP group numbers matching each routed VLAN, priority `110` on the preferred peer and `100` on the standby peer, with preemption retained only on the preferred peer.
- Aligned HSRP ownership with the Phase 04 Rapid PVST+ root placement.
- Configured `hq-a1 Vlan199` as `10.10.99.4/26` with default gateway `10.10.99.1`, and used a temporary `Vlan112` SVI for gateway testing.
- Configured VTP `transparent` on all three switches so VLAN definitions were locally represented in the exported CML configuration.
- Corrected unintended HSRP group `0` configuration on `hq-d2`.
- Verified failover and recovery for representative VLANs `112` and `199`, then removed the temporary `hq-a1 Vlan112` SVI.
- Restored recent unsaved configuration after an unexpected VMware/CML interruption before verification continued; no fault was identified with the Phase 05 SVI or HSRP design.
- Updated the operating workflow so significant configuration milestones are written to startup configuration, followed by a CML configuration fetch and retained versioned YAML exports.

### Verification

- `HQ-VP-05.01` — SVI Addressing and Layer 3 Baseline
- `HQ-VP-05.02` — HSRP Configuration and Normal Operating State
- `HQ-VP-05.03` — HSRP/STP Alignment and Gateway Reachability
- `HQ-VP-05.04` — HSRP Gateway Failover
- `HQ-VP-05.05` — HSRP Preemption and Preferred-State Restoration

### Result

**Phase 05 verified.** The approved SVI addressing, normal HSRP ownership, STP/HSRP alignment and gateway reachability were demonstrated. Controlled failure of the preferred SVI for representative VLANs `112` and `199` transferred gateway ownership to the peer, and restoration returned each VLAN to its planned preferred Active peer. The temporary `hq-a1 Vlan112` test SVI was removed after testing.

During final review, redundant preemption statements were removed from the non-preferred priority-`100` peers so the as-built HSRP configuration matched the approved design. Final normal-state captures confirmed the intended preferred-only preemption policy and unchanged Active/Standby ownership; the completed failover tests were not repeated.

Routed `/31` Distribution-to-Edge links and loopbacks remain for Phase 06.

### Evidence

[`evidence/hq/hsrp/`](../../../evidence/hq/hsrp/)

### Next

**Phase 06 — Routed `/31`s and Loopbacks**
