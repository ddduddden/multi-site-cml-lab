# HQ Verification Plan

This document defines what the HQ implementation must prove before a feature is treated as verified as-built.

It is a **controlled living document**. Once a verification ID is assigned it remains permanent. Expected results and exact verification commands may be refined when the actual CML platform behaviour is confirmed.

Only phases 01 and 02 are detailed initially. Phases 03–11 contain only their agreed objective until the project reaches them.

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
| 03 | LACP EtherChannel | Objective only |
| 04 | Rapid PVST+ | Objective only |
| 05 | SVIs and HSRP | Objective only |
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
Pending

**Status:**  
Not started

**Evidence:**  
—

**Notes / Troubleshooting:**  
—

---

### Access-Port Assignments — HQ-VP-02.02

**Objective:**  
Confirm every intended HQ access port has the correct access VLAN and, where required, voice VLAN.

**Expected result:**  
Access-port and voice-VLAN assignments match the approved HQ access-switch port plan.

**Configuration involved:**  
Access-mode, access-VLAN, and voice-VLAN configuration on the intended access ports.

**Verification command(s):**  
Verify switchport mode, access-VLAN assignment, and voice-VLAN assignment where applicable using the platform-appropriate switchport display command.

**Observed result:**  
Pending

**Status:**  
Not started

**Evidence:**  
—

**Notes / Troubleshooting:**  
—

---

### Parking-VLAN Policy — HQ-VP-02.03

**Objective:**  
Confirm unused `hq-a1` access ports are separated from production VLANs and administratively disabled as designed.

**Expected result:**  
The unused `hq-a1` access ports designated for parking are assigned to VLAN `191` (`PARKING`) and administratively shut down.

**Configuration involved:**  
Parking-VLAN assignment and administrative shutdown of the intended unused `hq-a1` access ports.

**Verification command(s):**  
Verify VLAN membership and administrative state using platform-appropriate interface/VLAN display commands.

**Observed result:**  
Pending

**Status:**  
Not started

**Evidence:**  
—

**Notes / Troubleshooting:**  
—

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Phase 03 — LACP EtherChannel

**Objective:** Build and verify Po10, Po20, and Po30, including member state, 802.1Q trunking, native-VLAN consistency, allowed-VLAN forwarding, and member-link failure behaviour.

_No individual verification IDs assigned yet._

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Phase 04 — Rapid PVST+

**Objective:** Verify intended root placement, forwarding/blocking state, and spanning-tree behaviour during defined failures.

_No individual verification IDs assigned yet._

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Phase 05 — SVIs and HSRP

**Objective:** Verify SVI addressing, HSRP active/standby roles, preemption, gateway reachability, and failover.

_No individual verification IDs assigned yet._

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
