# HQ Verification Plan

This document defines what the HQ implementation must prove before a feature is treated as verified as-built.

It is a **controlled living document**. Once a verification ID is assigned it remains permanent. Expected results and exact verification commands may be refined when the actual CML platform behaviour is confirmed.

Phases 01–05 are detailed below. Phases 06–11 contain only their agreed objective until the project reaches them.

## Project reference key

| Reference | Meaning |
|---|---|
| `HQ-VP-XX.YY` | HQ verification test — phase `XX`, test `YY` |
| `HQ-TS-NNN` | Related HQ troubleshooting record |
| `HQ-DEV-NNN` | Related HQ design deviation |

## Standard test record

Each verification test uses the same structure:

```text
Objective
Expected result
Configuration involved
Verification command(s)
Observed result
Status
Evidence
Notes / Troubleshooting
```

Each verification test uses the `Status` field to record its result.

| Status | Meaning |
|---|---|
| `Not started` | The test has not been run yet. |
| `In progress` | The test or related investigation is currently underway. |
| `Verified` | The expected behaviour has been demonstrated and recorded. |
| `Blocked` | The test cannot currently be completed because an unresolved issue, dependency, or platform limitation is preventing progress. |
| `Deviated` | The implementation intentionally differs from the design and an accepted `HQ-DEV-NNN` record exists for the test. |

There is no separate Pass/Fail field. `Blocked` means the test cannot currently be completed; it does not mean the test has permanently failed.

## Contents

| Phase | Scope | Detail |
|---:|---|---|
| 01 | Platform baseline | Detailed below |
| 02 | Layer 2 / VLAN baseline | Detailed below |
| 03 | LACP EtherChannel | Detailed below |
| 04 | Rapid PVST+ | Detailed below |
| 05 | SVIs and HSRP | Detailed below |
| 06 | Routed `/31`s and loopbacks | Objective only |
| 07 | OSPF Area 10 | Objective only |
| 08 | ECMP | Objective only |
| 09 | OSPF cost engineering | Objective only |
| 10 | Failure testing | Objective only |
| 11 | Final acceptance | Objective only |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Phase 01 — Platform Baseline

**Completed:** `20-09-2026`

**Objective:** Establish exactly what is running before assuming anything about node type, image, interface naming, interface count, licensing, or planned feature availability.

---

### HQ Device Inventory — HQ-VP-01.01

**Objective:**  
Confirm that all five intended HQ devices exist in CML with the expected hostnames and roles.

**Expected result:**  
`hq-r1`, `hq-r2`, `hq-d1`, `hq-d2`, and `hq-a1` are present and console-accessible.

**Configuration involved:**  
None.

**Verification command(s):**  
Confirm the five CML nodes and labels in the topology, then capture basic device identity from the CLI.

**Observed result:**  
All five intended HQ devices were present in the CML topology with the expected hostnames. `hq-r1` and `hq-r2` were available as IOSv edge routers; `hq-d1` and `hq-d2` as IOSvL2 multilayer distribution switches; and `hq-a1` as the IOSvL2 access switch. All five devices were booted and console-accessible.

**Status:**  
Verified

**Evidence:**  
`evidence/hq/platform-baseline/HQ-VP-01.01-base-node-topology.png`; the five `HQ-VP-01.02-*-show-version.png` console captures.

**Notes / Troubleshooting:**  
No troubleshooting record required.

---

### Image and Software Version Inventory — HQ-VP-01.02

**Objective:**  
Confirm the software image and version running on each HQ device.

**Expected result:**  
The image and software version are identified for all five devices before configuration begins.

**Configuration involved:**  
None.

**Verification command(s):**  
`show version`

**Observed result:**  
`hq-r1` and `hq-r2` were running Cisco IOSv Software Version `15.9(3)M12`, RELEASE SOFTWARE `(fc1)`. `hq-d1`, `hq-d2`, and `hq-a1` were running Cisco IOSvL2 (`vios_l2`) Experimental Version `15.2(20200924:215240)` `[sweickge-sep24-2020-l2iol-release 135]`. These were the expected image types for the planned HQ device roles.

**Status:**  
Verified

**Evidence:**  
`evidence/hq/platform-baseline/HQ-VP-01.02-hq-r1-show-version.png`; `HQ-VP-01.02-hq-r2-show-version.png`; `HQ-VP-01.02-hq-d1-show-version.png`; `HQ-VP-01.02-hq-d2-show-version.png`; `HQ-VP-01.02-hq-a1-show-version.png`.

**Notes / Troubleshooting:**  
No troubleshooting record required.

---

### Interface Inventory and Topology Fit — HQ-VP-01.03

**Objective:**  
Confirm the available interface names and counts can support the intended HQ topology.

**Expected result:**  
Each device has the required interfaces for its planned role, and the actual interface names are recorded before configuration.

**Configuration involved:**  
Physical CML links were added only after the interface inventory was verified; no production feature configuration was applied.

**Verification command(s):**  
`show ip interface brief`; compare the available interfaces with the interface allocations in the HQ Campus Design.

**Observed result:**  
`hq-r1` and `hq-r2` each had eight GigabitEthernet interfaces available (`Gi0/0`–`Gi0/7`). `hq-d1`, `hq-d2`, and `hq-a1` each had sixteen GigabitEthernet interfaces available (`Gi0/0`–`Gi3/3`). This was enough for the planned HQ topology. The 18 CML links were then added and checked against the interface allocations in the **HQ Campus Design**.

**Status:**  
Verified

**Evidence:**  
`evidence/hq/platform-baseline/HQ-VP-01.03-hq-r1-interface-inventory.png`; `HQ-VP-01.03-hq-r2-interface-inventory.png`; `HQ-VP-01.03-hq-d1-interface-inventory.png`; `HQ-VP-01.03-hq-d2-interface-inventory.png`; `HQ-VP-01.03-hq-a1-interface-inventory.png`; `HQ-VP-01.03-cabled-topology.png`.

**Notes / Troubleshooting:**  
No troubleshooting record required.

---

### Platform Capability Review — HQ-VP-01.04

**Objective:**  
Identify any known platform or image constraint that would block the planned HQ features before implementation begins.

**Expected result:**  
No unresolved capability issue blocks the planned use of Layer 2 LACP, Rapid PVST+, HSRP, OSPF, routed interfaces, or the later ECMP design.

**Configuration involved:**  
Testing was carried out on `hq-d1` (IOSvL2) and `hq-r1` (IOSv). Temporary test configuration was removed afterwards.

**Verification command(s):**  
Platform-appropriate `show` commands and context-sensitive CLI help were used to check support for the required features. Cleanup was confirmed with `show running-config` and interface-state checks.

**Observed result:**  
Testing on `hq-d1` and `hq-r1` confirmed that the IOSvL2 and IOSv images support the main features required by the HQ design, including LACP, Rapid PVST+, HSRP, routed interfaces, OSPF and ECMP. Temporary test configuration was removed afterwards and the devices were returned to their baseline state. No platform limitation was found that would prevent the planned HQ build.

**Status:**  
Verified

**Evidence:**  
`evidence/hq/platform-baseline/HQ-VP-01.04-platform-capability-review.txt`

**Notes / Troubleshooting:**  
These checks confirm platform support only. Operational protocol behaviour, failover, convergence, path selection, and summarisation will be tested during the later implementation phases. No troubleshooting record required.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Phase 02 — Layer 2 / VLAN Baseline

**Completed:** `21-09-2026`

**Objective:** Establish the VLAN database, intended access-port assignments, and parking-VLAN policy before EtherChannel/trunk implementation begins.

Native-VLAN and trunk verification belongs to Phase 03 because the production trunks are created and verified with the EtherChannels there.

---

### VLAN Database — HQ-VP-02.01

**Objective:**  
Confirm that all intended HQ VLANs exist on each switch that requires them.

**Expected result:**  
Required VLAN IDs and names match the approved HQ design on `hq-d1`, `hq-d2`, and `hq-a1`.

**Configuration involved:**  
VLAN creation and naming on the applicable switches.

**Verification command(s):**  
`show vlan brief`

**Observed result:**  
All ten approved HQ VLANs were present and active on `hq-d1`, `hq-d2`, and `hq-a1`, with VLAN IDs and names matching the approved design.

VLAN `1` remained present as the platform default but was not used for production or management access. VLAN `190` remains reserved as the native VLAN for the Phase 03 trunk implementation.

**Status:**  
Verified

**Evidence:**  
`evidence/hq/layer2-vlan-baseline/HQ-VP-02.01-hq-d1-show-vlan-brief.txt`; `HQ-VP-02.01-hq-d2-show-vlan-brief.txt`; `HQ-VP-02.01-hq-a1-show-vlan-brief.txt`.

**Notes / Troubleshooting:**  
No troubleshooting record required.

---

### Access-Port Assignments — HQ-VP-02.02

**Objective:**  
Confirm every intended HQ access port has the correct access VLAN and, where required, voice VLAN.

**Expected result:**  
Access-port and voice-VLAN assignments match the approved HQ access-switch port plan.

**Configuration involved:**  
Access-mode, access-VLAN, and voice-VLAN configuration on the intended access ports.

**Verification command(s):**  
`show vlan brief`; `show interfaces switchport`

**Observed result:**  
`hq-a1` access-port assignments matched the approved HQ port plan. All eight endpoint-facing interfaces were configured as static access ports with the correct access VLANs, and `Gi2/0` was additionally assigned voice VLAN `120` (`VOICE`).

All endpoint-facing interfaces were administratively enabled and remained operationally down because no endpoints were connected during verification.

**Status:**  
Verified

**Evidence:**  
`evidence/hq/layer2-vlan-baseline/HQ-VP-02.02-hq-a1-show-interfaces-switchport.txt`; `HQ-VP-02.03-hq-a1-parking-vlan-state.txt`.

**Notes / Troubleshooting:**  
No troubleshooting record required.

---

### Parking-VLAN Policy — HQ-VP-02.03

**Objective:**  
Confirm `hq-a1` interfaces that are not yet in service during Phase 02 are separated from production VLANs and administratively disabled.

**Expected result:**  
All `hq-a1` interfaces not yet in service are assigned to VLAN `191` (`PARKING`) and administratively shut down. Future `Po10` and `Po20` member interfaces remain parked until Phase 03.

**Configuration involved:**  
Parking-VLAN assignment and administrative shutdown of `hq-a1` interfaces not yet in service.

**Verification command(s):**  
`show vlan brief`; `show ip interface brief`; `show interfaces switchport`

**Observed result:**  
All `hq-a1` interfaces not yet in service during Phase 02 were assigned to VLAN `191` (`PARKING`) and administratively shut down.

The future `Po10` and `Po20` member interfaces remain parked until Phase 03, when they will be reconfigured for their intended EtherChannel trunk roles.

**Status:**  
Verified

**Evidence:**  
`evidence/hq/layer2-vlan-baseline/HQ-VP-02.03-hq-a1-parking-vlan-state.txt`; `HQ-VP-02.02-hq-a1-show-interfaces-switchport.txt`.

**Notes / Troubleshooting:**  
No troubleshooting record required.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Phase 03 — LACP EtherChannel

**Completed:** `22-09-2026`

**Objective:** Build and verify `Po10`, `Po20`, and `Po30`, including LACP formation, member participation, 802.1Q trunking, native-VLAN consistency, allowed-VLAN policy, and member-link resilience.

Phase 03 verifies the Layer 2 EtherChannel and trunk infrastructure before deterministic Rapid PVST+ root placement or Layer 3 gateway services are introduced.

Per-VLAN Layer 3 gateway reachability is intentionally deferred to Phase 05, after the production SVIs and HSRP gateways exist.

---

### EtherChannel Formation and LACP State — HQ-VP-03.01

**Objective:**  
Confirm that `Po10`, `Po20`, and `Po30` form successfully using LACP and contain the intended physical member interfaces.

**Expected result:**  
`Po10`, `Po20`, and `Po30` are operational LACP EtherChannels with all intended physical members bundled correctly and no unexpected suspended or standalone members.

**Configuration involved:**  
LACP `active` mode on the intended physical members and creation of `Po10`, `Po20`, and `Po30`.

**Verification command(s):**  
`show etherchannel summary`; `show lacp neighbor`

**Observed result:**  
`Po10`, `Po20`, and `Po30` formed successfully as Layer 2 LACP EtherChannels. All intended physical members were bundled in their respective Port-Channels with no suspended or standalone members. LACP neighbor output confirmed Active-mode peers on all three bundles.

**Status:**  
Verified

**Evidence:**  
`evidence/hq/etherchannel/HQ-VP-03.01-hq-a1-etherchannel-lacp-state.txt`; `HQ-VP-03.01-hq-d1-etherchannel-lacp-state.txt`; `HQ-VP-03.01-hq-d2-etherchannel-lacp-state.txt`.

**Notes / Troubleshooting:**  
No troubleshooting record required.

---

### Port-Channel Trunk Policy — HQ-VP-03.02

**Objective:**  
Confirm that all three logical Port-Channels use the approved HQ 802.1Q trunk policy and that the physical members operate consistently with their logical bundle.

**Expected result:**  
All three Port-Channels operate as 802.1Q trunks using native VLAN `190` and allowed VLANs `112,120,130,140,152,160,170,190,199`, with VLAN `191` excluded and no conflicting member configuration.

**Configuration involved:**  
Trunk configuration on `Po10`, `Po20`, and `Po30`, including the explicit native VLAN and allowed-VLAN list.

**Verification command(s):**  
`show interfaces trunk`; `show etherchannel summary`

**Observed result:**  
`Po10`, `Po20`, and `Po30` operated as 802.1Q trunks using native VLAN `190`. Each Port-Channel carried the approved allowed-VLAN list `112,120,130,140,152,160,170,190,199`, with VLAN `191` excluded.

**Status:**  
Verified

**Evidence:**  
`evidence/hq/etherchannel/HQ-VP-03.02-hq-a1-show-interfaces-trunk.txt`; `HQ-VP-03.02-hq-d1-show-interfaces-trunk.txt`; `HQ-VP-03.02-hq-d2-show-interfaces-trunk.txt`.

**Notes / Troubleshooting:**  
The effective Port-Channel and trunk behaviour was confirmed from observed IOSvL2 output. No troubleshooting record required.

---

### Operational Trunk and VLAN State — HQ-VP-03.03

**Objective:**  
Confirm that the configured Port-Channels are operational trunks and that the intended VLANs are active on the Layer 2 trunk infrastructure.

**Expected result:**  
`Po10`, `Po20`, and `Po30` report an operational trunk state with the approved VLAN set active. Final per-VLAN STP forwarding behaviour is deferred to Phase 04.

**Configuration involved:**  
No additional configuration beyond the completed Phase 03 EtherChannel and trunk configuration.

**Verification command(s):**  
`show interfaces trunk`; `show etherchannel summary`

**Observed result:**  
All three Port-Channels were operational trunks and the complete approved VLAN set was shown as allowed and active. At the time of verification, `hq-d2 Po20` showed no VLANs in the spanning-tree forwarding state; deterministic per-VLAN spanning-tree forwarding behaviour remains intentionally deferred to Phase 04.

**Status:**  
Verified

**Evidence:**  
`evidence/hq/etherchannel/HQ-VP-03.02-hq-a1-show-interfaces-trunk.txt`; `HQ-VP-03.02-hq-d1-show-interfaces-trunk.txt`; `HQ-VP-03.02-hq-d2-show-interfaces-trunk.txt`.

**Notes / Troubleshooting:**  
Per-VLAN gateway reachability remains deferred until Phase 05. No troubleshooting record required.

---

### EtherChannel Member-Link Failure and Recovery — HQ-VP-03.04

**Objective:**  
Confirm that loss of a physical EtherChannel member does not bring down the logical Port-Channel while other valid members remain available, and that the failed member rejoins correctly after recovery.

**Expected result:**  
A controlled member-link failure removes only the affected member while the Port-Channel remains operational; the restored member automatically rejoins the bundle.

**Configuration involved:**  
Controlled administrative failure and restoration of selected physical EtherChannel members.

**Verification command(s):**  
`show etherchannel summary`

**Observed result:**  
A single physical member was administratively removed and restored on each of `Po10`, `Po20`, and `Po30`. In every test the affected member left the bundle while the logical Port-Channel remained operational using the surviving members. After restoration, each member automatically rejoined its EtherChannel. During `Po30` recovery, the restored member briefly entered LACP hot-standby state before returning to the bundled state.

**Status:**  
Verified

**Evidence:**  
`evidence/hq/etherchannel/HQ-VP-03.04-member-link-failure-recovery.txt`

**Notes / Troubleshooting:**  
No troubleshooting record required. Complete Port-Channel, device, and combined failure scenarios remain within Phase 10.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Phase 04 — Rapid PVST+

**Completed:** `24-09-2026`

**Objective:**  
Verify Rapid PVST+ mode, deterministic root placement, forwarding paths, alternate-path behaviour, and recovery after controlled EtherChannel failures.

---

### Rapid PVST+ Mode and Root Placement — HQ-VP-04.01

**Objective:**  
Confirm that Rapid PVST+ is operating across the HQ switching topology and that the intended root-primary and root-secondary placement is established for each participating VLAN.

**Expected result:**  
Rapid PVST+ is active, with `hq-d1` root for VLANs `112,130,152,170,190` and `hq-d2` root for VLANs `120,140,160,199`. The other multilayer distribution switch holds the secondary role for each group.

**Configuration involved:**  
Rapid PVST+ mode and the approved root-primary/root-secondary assignments on `hq-d1` and `hq-d2`.

**Verification command(s):**  
`show spanning-tree summary`; `show spanning-tree root`; `show spanning-tree bridge`; representative `show spanning-tree vlan <vlan-id>` checks.

**Observed result:**  
`show spanning-tree summary` confirmed Rapid PVST+ mode on all three HQ switches. Root placement matched the approved design: `hq-d1` was root for VLANs `112,130,152,170,190`, while `hq-d2` was root for VLANs `120,140,160,199`. Root switches used base priority `24576`, secondaries `28672`, and `hq-a1` retained the default `32768`. `hq-a1` used `Po10` toward the `hq-d1` group and `Po20` toward the `hq-d2` group.

**Status:**  
Verified

**Evidence:**  
`evidence/hq/spanning-tree/HQ-VP-04.01-hq-a1-spanning-tree-state.txt`; `HQ-VP-04.01-hq-d1-spanning-tree-state.txt`; `HQ-VP-04.01-hq-d2-spanning-tree-state.txt`.

**Notes / Troubleshooting:**  
VLAN `1` remains locally present on the multilayer distribution switches because unused ports remain assigned to it. It is not carried on the production trunks and is outside the Phase 04 root-placement policy.

An early VLAN `112` capture showed a transient root-state mismatch immediately after the STP changes. The condition cleared without configuration changes and the final topology matched the design.

No troubleshooting record required.

---

### Access-Layer Forwarding and Alternate Paths — HQ-VP-04.02

**Objective:**  
Confirm that Rapid PVST+ produces the expected forwarding paths and places the redundant EtherChannel into the alternate state.

**Expected result:**  
`hq-a1` uses the preferred path toward the correct root bridge for each VLAN group, while the other EtherChannel remains available as the alternate path.

**Configuration involved:**  
No additional configuration beyond the completed Rapid PVST+ root-placement policy.

**Verification command(s):**  
`show spanning-tree vlan <vlan-id>` on `hq-a1`, `hq-d1`, and `hq-d2`.

**Observed result:**  
Representative VLANs confirmed the expected forwarding paths. VLAN `112` used `Po10` toward `hq-d1`, while VLAN `120` used `Po20` toward `hq-d2`, with the opposite Port-Channel held as the alternate path. The resulting topology was loop-free and matched the intended design.

**Status:**  
Verified

**Evidence:**  
`evidence/hq/spanning-tree/HQ-VP-04.02-representative-vlan-forwarding-state.txt`

**Notes / Troubleshooting:**  
VLANs `112` and `120` were used as representative examples for the two root-placement groups. The blocked path was located at `hq-a1`; during Phase 03, before deterministic root placement was configured, `hq-d2 Po20` showed no VLANs in the spanning-tree forwarding state.

No troubleshooting record required.

---

### STP Path Failure and Recovery — HQ-VP-04.03

**Objective:**  
Confirm that Rapid PVST+ uses the alternate EtherChannel when a preferred path fails and returns to the normal forwarding path after recovery.

**Expected result:**  
Loss of either EtherChannel causes the alternate path to become active for the affected VLAN group. Restoring the EtherChannel returns the topology to its normal state.

**Configuration involved:**  
Controlled shutdown and restoration of `Po10` with VLAN `112`, and `Po20` with VLAN `120`, to verify failover in both directions.

**Verification command(s):**  
`show spanning-tree vlan <vlan-id>`; `show interfaces trunk`; `show etherchannel summary`

**Observed result:**  
Failure of `Po10` for VLAN `112` and `Po20` for VLAN `120` caused the alternate Port-Channel to become the forwarding path while the root bridge remained unchanged. In both tests, the root-path cost increased from `3` to `6` during failure and returned to `3` after recovery.

**Status:**  
Verified

**Evidence:**  
`evidence/hq/spanning-tree/HQ-VP-04.03-path-failure-recovery.txt`

**Notes / Troubleshooting:**  
The logical Port-Channels were shut down so the tests exercised complete EtherChannel failure rather than repeating the member-link resilience already verified in Phase 03.

Whole-switch and combined Layer 2/Layer 3 failures remain in Phase 10.

No troubleshooting record required.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Phase 05 — SVIs and HSRP

**Objective:** Build and verify the HQ routed VLAN interfaces and first-hop gateway redundancy, including SVI addressing, HSRP operating state, STP/HSRP alignment, gateway reachability, failover, and recovery to the preferred state.

`hq-a1` uses VLAN `199` for in-band management, with address `10.10.99.4/26` and default gateway `10.10.99.1`.

---

### SVI Addressing and Layer 3 Baseline — HQ-VP-05.01

**Objective:**  
Confirm the production SVI addressing on `hq-d1` and `hq-d2`, establish the VLAN 199 management SVI on `hq-a1`, and verify that only the intended VLANs provide Layer 3 interfaces.

**Expected result:**  
All eight routed VLANs use the approved `.1` VIP / `.2 hq-d1` / `.3 hq-d2` convention and subnet masks. `hq-a1` uses `10.10.99.4/26` on VLAN `199` with default gateway `10.10.99.1`. VLANs `190` and `191` have no Layer 3 interfaces.

**Configuration involved:**  
SVI addressing on `hq-d1` and `hq-d2`, plus the VLAN 199 management SVI and default-gateway configuration on `hq-a1`.

**Verification command(s):**  
`show ip interface brief`; `show running-config | section ^interface Vlan`; `show running-config | include ^ip default-gateway` on `hq-a1`.

**Observed result:**  
All eight SVIs on `hq-d1` and `hq-d2` were up/up with the approved addresses and masks. Neither switch had a VLAN `190` or `191` SVI. Following temporary-SVI removal, `hq-a1` retained only `Vlan199`, up/up at `10.10.99.4/26`, with default gateway `10.10.99.1`.

**Status:**  
Verified

**Evidence:**  
`evidence/hq/hsrp/HQ-VP-05.01-hq-d1-svi-addressing.txt`; `HQ-VP-05.01-hq-d2-svi-addressing.txt`; `HQ-VP-05.01-hq-a1-management-svi.txt`.

**Notes / Troubleshooting:**  
The final baseline was captured on `27-09-2026`. Temporary `hq-a1 Vlan112` removal is also referenced by `HQ-VP-05.05`.

---

### HSRP Configuration and Normal Operating State — HQ-VP-05.02

**Objective:**  
Confirm that every routed VLAN has the intended HSRP group, virtual IP, priority, preemption policy, and Active/Standby ownership.

**Expected result:**  
All eight HSRP groups use the approved virtual IPs and VLAN-matching group numbers. Each preferred peer is Active at priority `110`, with the standby peer at priority `100`. Preemption is enabled on the preferred peer only.

**Configuration involved:**  
HSRP configuration on the eight routed VLAN SVIs on `hq-d1` and `hq-d2`.

**Verification command(s):**  
`show running-config | section ^interface Vlan`; `show standby brief`

**Observed result:**  
Final captures confirmed the approved virtual IPs and group numbers, priority `110` on each preferred peer, priority `100` on the standby peer, and preemption only on the preferred peer. `hq-d1` was Active for VLANs `112,130,152,170`; `hq-d2` was Active for VLANs `120,140,160,199`.

**Status:**  
Verified

**Evidence:**  
`evidence/hq/hsrp/HQ-VP-05.02-hq-d1-hsrp-normal-state.txt`; `HQ-VP-05.02-hq-d2-hsrp-normal-state.txt`.

**Notes / Troubleshooting:**  
An unintended HSRP group `0` on `hq-d2` and redundant preemption on the non-preferred peers were removed before the final state was recaptured. No troubleshooting or deviation record required.

---

### HSRP/STP Alignment and Gateway Reachability — HQ-VP-05.03

**Objective:**  
Confirm that HSRP Active ownership matches the Rapid PVST+ root-primary placement and that the virtual gateways are reachable through the access-layer topology.

**Expected result:**  
The HSRP Active peer is also the Rapid PVST+ root switch for each routed VLAN. For representative VLANs `112` and `199`, `hq-a1` can reach the virtual gateway and both distribution-switch SVI addresses.

**Configuration involved:**  
HSRP and Rapid PVST+ on `hq-d1` and `hq-d2`, with gateway testing from `hq-a1` using its permanent `Vlan199` management SVI and temporary `Vlan112` SVI (`10.10.12.4/22`).

**Verification command(s):**  
`show ip interface brief`; `ping` from `hq-a1`. HSRP state is cross-referenced to `HQ-VP-05.02`; STP root placement and access-layer root ports to `HQ-VP-04.01`.

**Observed result:**  
HSRP Active ownership matched the recorded STP root placement. All six gateway targets returned `5/5`. The Phase 04 evidence shows `hq-a1` using root port `Po10` for VLAN `112` and `Po20` for VLAN `199`.

**Status:**  
Verified

**Evidence:**  
`evidence/hq/hsrp/HQ-VP-05.03-hq-a1-gateway-reachability.txt`; `HQ-VP-05.02-hq-d1-hsrp-normal-state.txt`; `HQ-VP-05.02-hq-d2-hsrp-normal-state.txt`; `evidence/hq/spanning-tree/HQ-VP-04.01-hq-a1-spanning-tree-state.txt`.

**Notes / Troubleshooting:**  
STP state comes from the earlier Phase 04 capture, rather than a simultaneous ping capture. The temporary `Vlan112` SVI remained through failover testing; final removal is recorded in `HQ-VP-05.05`.

---

### HSRP Gateway Failover — HQ-VP-05.04

**Objective:**  
Confirm that gateway service recovers through the Standby peer when the preferred Active SVI becomes unavailable.

**Expected result:**  
The Standby peer becomes Active, retains the same virtual IP and provides gateway reachability after convergence. Tests cover VLAN `112` with `hq-d1` unavailable and VLAN `199` with `hq-d2` unavailable.

**Configuration involved:**  
Controlled shutdown of `hq-d1 Vlan112` and, separately, `hq-d2 Vlan199`, with gateway testing from `hq-a1`.

**Verification command(s):**  
`show standby brief`; `ping` from `hq-a1`; `show ip interface brief` on `hq-d2` to confirm the VLAN `199` shutdown state.

**Observed result:**  
Shutting down `hq-d1 Vlan112` caused `hq-d2` to become Active for group `112`; a post-failover ping returned `5/5`. Shutting down `hq-d2 Vlan199` caused `hq-d1` to become Active for group `199`; both post-failover pings returned `5/5`. The virtual IPs remained unchanged.

**Status:**  
Verified

**Evidence:**  
`evidence/hq/hsrp/HQ-VP-05.04-hsrp-failover-vlan112.txt`; `HQ-VP-05.04-hsrp-failover-vlan199.txt`.

**Notes / Troubleshooting:**  
The VLAN `199` sequence includes an early capture taken before convergence; later evidence confirms `hq-d2 Vlan199` down and `hq-d1` Active. The tests were completed before redundant non-preferred preemption was removed; that cleanup does not change the recorded failover results. Final HSRP state is recorded in `HQ-VP-05.02`. Whole-device and combined STP/HSRP failures remain within Phase 10.

---

### HSRP Preemption and Preferred-State Restoration — HQ-VP-05.05

**Objective:**  
Confirm that restoration of the preferred gateway returns HSRP ownership to the intended peer and that temporary access-switch test configuration is removed.

**Expected result:**  
Preemption restores the planned Active/Standby ownership and HSRP/STP alignment. `hq-a1` retains its permanent `Vlan199` management SVI, with the temporary `Vlan112` SVI removed.

**Configuration involved:**  
Restoration of `hq-d1 Vlan112` and `hq-d2 Vlan199`, followed by removal of the temporary `hq-a1 Vlan112` SVI.

**Verification command(s):**  
`show standby brief`; `show ip interface brief`; `show spanning-tree root`; `ping` from `hq-a1`.

**Observed result:**  
VLAN `112` returned to `hq-d1` Active / `hq-d2` Standby, and VLAN `199` returned to `hq-d2` Active / `hq-d1` Standby. Recovery pings returned `4/5`, then `5/5` in both tests. All eight groups returned to planned ownership, the final STP root-port split matched the design, the temporary `Vlan112` SVI was removed, and `Vlan199` remained up/up at `10.10.99.4/26`.

**Status:**  
Verified

**Evidence:**  
`evidence/hq/hsrp/HQ-VP-05.05-hsrp-preemption-recovery-vlan112.txt`; `HQ-VP-05.05-hsrp-preemption-recovery-vlan199.txt`; `HQ-VP-05.05-hq-a1-final-stp-alignment.txt`; `HQ-VP-05.01-hq-a1-management-svi.txt`.

**Notes / Troubleshooting:**  
One earlier VLAN `112` recovery ping could not be reliably linked to the final test run, so it was excluded from the evidence. The bridge MAC addresses differed from the Phase 04 capture after the CML environment was restored. CML assigns MAC addresses automatically, and recreated or wiped nodes can receive new addresses; however, the configured STP priorities and intended `Po10`/`Po20` roles were unchanged, so the planned root and forwarding design remained the same. Final as-built preemption policy is recorded in `HQ-VP-05.02`.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Phase 06 — Routed `/31`s and Loopbacks

**Objective:** Build and verify all routed point-to-point interfaces and loopback identities before dynamic routing is enabled.

_No individual verification IDs assigned yet._

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Phase 07 — OSPF Area 10

**Objective:** Verify router IDs, passive-interface policy, intended adjacencies, Area 10 route advertisement, and routing reachability.

_No individual verification IDs assigned yet._

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Phase 08 — ECMP

**Objective:** Prove that the intended equal-cost OSPF paths are actually installed and usable; do not infer ECMP merely from topology.

_No individual verification IDs assigned yet._

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Phase 09 — OSPF Cost Engineering

**Objective:** Prove that preferred direct paths and higher-cost cross-connected alternatives are selected according to the approved design and become usable during the intended failures.

_No individual verification IDs assigned yet._

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Phase 10 — Failure Testing

**Objective:** Execute the agreed failure matrix for member links, Port-Channels, routed interfaces, multilayer distribution switches, edge routers, and routing recovery.

_No individual verification IDs assigned yet._

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Phase 11 — Final Acceptance

**Objective:** Confirm that all required implementation records, verification outcomes, troubleshooting records, deviations, configs, and evidence support describing HQ as verified as-built.

_No individual verification IDs assigned yet._
