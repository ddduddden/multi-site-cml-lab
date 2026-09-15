# HQ Campus Design

**Project:** Multi-Site Cisco CML Lab  
**Site:** HQ Campus  
**Status:** Intended design — implementation and verification in progress  
**Routing domain:** OSPF Area 10  
**Node count:** 5 network devices

> This document describes the intended HQ architecture. Platform-specific behaviour, implementation notes, commands, test evidence, and simulator limitations will be maintained separately.

---

## 1. Overview

The HQ campus uses a five-device, two-tier collapsed-core design:

- `hq-r1` — Edge Router 1
- `hq-r2` — Edge Router 2
- `hq-d1` — Distribution Switch 1
- `hq-d2` — Distribution Switch 2
- `hq-a1` — Access Switch

The internal HQ routing domain operates as **OSPF Area 10**.

The edge routers will later connect Area 10 to the **Area 0 inter-site backbone** and support future GRE/IPsec connectivity.

The design provides:

- Redundant Layer 2 access/distribution connectivity
- First-hop gateway redundancy
- Per-VLAN spanning-tree root control
- Routed Distribution-to-Edge connectivity
- OSPF equal-cost multipath
- Alternate routed paths
- VLSM addressing
- `/31` routed infrastructure interfaces
- `/32` loopbacks
- Dedicated native and parking VLANs
- A clear path toward monitoring, security, inter-site connectivity, and automation

Layer 2 multi-link connectivity uses **LACP EtherChannel**.

Layer 3 multi-link connectivity uses **independent routed interfaces with OSPF ECMP**.

These are separate design mechanisms and are documented as such.

---

## 2. High-Level Topology

The HQ campus topology is shown below.

![HQ Campus - OSPF Area 10](../diagrams/hq-campus-area10-topology.svg)

The two Distribution Switches provide the Layer 3 gateway and campus-routing functions for HQ. `hq-a1` is dual-homed to them using `Po10` and `Po20`, while `hq-d1` and `hq-d2` are interconnected by `Po30`.

Each Distribution Switch also has four routed point-to-point interfaces to its directly paired edge router for the intended OSPF ECMP design:

- `hq-d1` ↔ `hq-r1`
- `hq-d2` ↔ `hq-r2`

A further cross-connected routed interface is provided in each direction to create an alternate OSPF path:

- `hq-d1` ↔ `hq-r2`
- `hq-d2` ↔ `hq-r1`

The two edge routers will later connect HQ Area 10 to the Area 0 inter-site backbone.


---

## 3. VLAN and Gateway Design

| VLAN | Name | Function | IPv4 Prefix | HSRP Virtual IP |
|---:|---|---|---|---|
| 112 | `CORP-USERS` | Corporate users | `10.10.12.0/22` | `10.10.12.1` |
| 120 | `VOICE` | IP telephony | `10.10.20.0/23` | `10.10.20.1` |
| 130 | `SERVERS` | Server/application services | `10.10.30.0/25` | `10.10.30.1` |
| 140 | `IOT-CCTV` | IoT and surveillance | `10.10.40.0/23` | `10.10.40.1` |
| 152 | `GUEST` | Guest access | `10.10.52.0/22` | `10.10.52.1` |
| 160 | `FACILITIES` | Printers/facilities | `10.10.60.0/26` | `10.10.60.1` |
| 170 | `BYOD-WLAN` | BYOD/wireless | `10.10.70.0/23` | `10.10.70.1` |
| 190 | `NATIVE` | Dedicated native VLAN | — | — |
| 191 | `PARKING` | Unused ports | — | — |
| 199 | `NET-MGMT` | Network infrastructure management | `10.10.99.0/26` | `10.10.99.1` |

### Gateway Addressing Convention

For every routed VLAN:

- First usable address — HSRP virtual IP
- Second usable address — `hq-d1`
- Third usable address — `hq-d2`

Example for VLAN 130:

- HSRP VIP — `10.10.30.1`
- `hq-d1 Vlan130` — `10.10.30.2/25`
- `hq-d2 Vlan130` — `10.10.30.3/25`

### Reserved VLAN Policy

**VLAN 190 — `NATIVE`**

- Dedicated non-default native VLAN
- No SVI
- No intended endpoint traffic

**VLAN 191 — `PARKING`**

- Reserved for unused ports
- No SVI
- Unused ports are administratively shut down

**VLAN 1**

VLAN 1 is not used for production traffic, infrastructure management, or as the intentionally configured native VLAN.

---

## 4. Layer 3 Infrastructure Addressing

HQ infrastructure uses the `10.255.10.0/24` address space.

Point-to-point routed interfaces use `/31` prefixes. Loopback interfaces use `/32` addresses.

### Point-to-Point Routed Interfaces

| Distribution Switch | Interface | Edge Router | Interface | IPv4 Prefix |
|---|---|---|---|---|
| `hq-d1` | `E2/0` | `hq-r1` | `E0/0` | `10.255.10.0/31` |
| `hq-d2` | `E2/0` | `hq-r2` | `E0/0` | `10.255.10.2/31` |
| `hq-d1` | `E3/0` | `hq-r2` | `E1/0` | `10.255.10.4/31` |
| `hq-d2` | `E3/0` | `hq-r1` | `E1/0` | `10.255.10.6/31` |
| `hq-d1` | `E2/1` | `hq-r1` | `E0/1` | `10.255.10.8/31` |
| `hq-d1` | `E2/2` | `hq-r1` | `E0/2` | `10.255.10.10/31` |
| `hq-d1` | `E2/3` | `hq-r1` | `E0/3` | `10.255.10.12/31` |
| `hq-d2` | `E2/1` | `hq-r2` | `E0/1` | `10.255.10.14/31` |
| `hq-d2` | `E2/2` | `hq-r2` | `E0/2` | `10.255.10.16/31` |
| `hq-d2` | `E2/3` | `hq-r2` | `E0/3` | `10.255.10.18/31` |

For consistency, the lower address in each `/31` is assigned to the Distribution Switch interface and the higher address to the edge-router interface.

### Loopback Addressing

| Device | Interface | IPv4 Address | Purpose |
|---|---|---|---|
| `hq-r1` | `Loopback0` | `10.255.10.129/32` | Stable identity / OSPF router ID |
| `hq-r2` | `Loopback0` | `10.255.10.130/32` | Stable identity / OSPF router ID |
| `hq-d1` | `Loopback0` | `10.255.10.131/32` | Stable identity / OSPF router ID |
| `hq-d2` | `Loopback0` | `10.255.10.132/32` | Stable identity / OSPF router ID |

Future tunnel-source addressing will be designed during the Area 0/WAN phase rather than pre-allocated here.

---

## 5. Layer 2 Design

### EtherChannel Plan

| Port-Channel | Connected Devices | Physical Port Mapping | Function | LACP Mode |
|---|---|---|---|---|
| `Po10` | `hq-a1` ↔ `hq-d1` | `hq-a1 E0/0-E0/1` ↔ `hq-d1 E0/0-E0/1` | Access-to-Distribution trunk | Active / Active |
| `Po20` | `hq-a1` ↔ `hq-d2` | `hq-a1 E1/0-E1/1` ↔ `hq-d2 E0/0-E0/1` | Access-to-Distribution trunk | Active / Active |
| `Po30` | `hq-d1` ↔ `hq-d2` | `hq-d1 E1/0-E1/3` ↔ `hq-d2 E1/0-E1/3` | Distribution interconnect trunk | Active / Active |

`Po10` and `Po20` use two member ports.

`Po30` is intended to use four member ports.

### Trunk Policy

Campus trunks use:

- VLAN 190 as the configured native VLAN
- Explicit allowed VLANs
- No production use of VLAN 1
- VLAN 191 excluded from normal trunk forwarding

Intended allowed VLAN set:

`112,120,130,140,152,160,170,190,199`

### Access Switch Port Allocation

| Port(s) | Access VLAN | Voice VLAN | Function | State |
|---|---:|---:|---|---|
| `E0/0-E0/1` | — | — | `Po10` members to `hq-d1` | Enabled |
| `E0/2-E0/3` | 191 | — | Unused / parking | Shutdown |
| `E1/0-E1/1` | — | — | `Po20` members to `hq-d2` | Enabled |
| `E1/2-E1/3` | 191 | — | Unused / parking | Shutdown |
| `E2/0` | 112 | 120 | Corporate workstation + IP phone | Enabled |
| `E2/1` | 112 | — | Corporate workstation | Enabled |
| `E2/2` | 130 | — | Server/application endpoint | Enabled |
| `E2/3` | 140 | — | IoT/CCTV endpoint | Enabled |
| `E3/0` | 152 | — | Guest endpoint | Enabled |
| `E3/1` | 160 | — | Printer/facilities endpoint | Enabled |
| `E3/2` | 170 | — | BYOD/WLAN test endpoint | Enabled |
| `E3/3` | 199 | — | Network-management endpoint | Enabled |

The access-port allocation is part of the intended design and will be adjusted only if the selected switching platform requires different port naming or availability.

---

## 6. HSRP and Rapid PVST+ Design

HSRP gateway ownership is aligned with spanning-tree root placement so the preferred Layer 2 path terminates on the Distribution Switch acting as the active default gateway.

| VLANs | `hq-d1` Role | `hq-d2` Role |
|---|---|---|
| `112,130,152,170` | HSRP Active / STP Root Primary | HSRP Standby / STP Root Secondary |
| `120,140,160,199` | HSRP Standby / STP Root Secondary | HSRP Active / STP Root Primary |

### HSRP Policy

- HSRP group numbers match VLAN IDs
- Preferred Distribution Switch priority — `110`
- Standby Distribution Switch priority — `100`
- Preemption enabled on the preferred switch
- `.1` HSRP virtual address used as the client default gateway

### Rapid PVST+ Policy

- Rapid PVST+ is the intended HQ spanning-tree mode
- HSRP Active aligns with STP Root Primary
- HSRP Standby aligns with STP Root Secondary
- Root-primary/root-secondary configuration is preferred over arbitrary manually selected priorities
- MST remains a later design exercise

---

## 7. OSPF Area 10 and ECMP Design

HQ uses **OSPF Area 10**.

`Loopback0` provides the explicit OSPF router ID for each Layer 3 device.

OSPF uses a **passive-by-default** policy:

- User/service SVIs are advertised but do not form OSPF neighbour relationships
- Loopback0 is advertised but passive
- Only routed Distribution-to-Edge interfaces form OSPF adjacencies

The routed Ethernet interfaces are intended to use the OSPF point-to-point network type.

### Direct Equal-Cost Paths

The four routed interfaces between `hq-d1` and `hq-r1` form one intended equal-cost path set:

- `hq-d1 E2/0` ↔ `hq-r1 E0/0`
- `hq-d1 E2/1` ↔ `hq-r1 E0/1`
- `hq-d1 E2/2` ↔ `hq-r1 E0/2`
- `hq-d1 E2/3` ↔ `hq-r1 E0/3`

The four routed interfaces between `hq-d2` and `hq-r2` form the second intended equal-cost path set:

- `hq-d2 E2/0` ↔ `hq-r2 E0/0`
- `hq-d2 E2/1` ↔ `hq-r2 E0/1`
- `hq-d2 E2/2` ↔ `hq-r2 E0/2`
- `hq-d2 E2/3` ↔ `hq-r2 E0/3`

### Alternate Routed Paths

The cross-connected paths are:

- `hq-d1 E3/0` ↔ `hq-r2 E1/0`
- `hq-d2 E3/0` ↔ `hq-r1 E1/0`

These interfaces are intended to use deliberately higher OSPF costs so that they act as alternate paths.

They will only be described as backup paths after the full routing behaviour has been implemented and verified.

### ECMP Design Note

OSPF ECMP retains each routed interface as an independent Layer 3 path.

It does not create a logical Port-Channel.

The implementation phase will verify:

- Four equal-cost routes are actually installed where intended
- Forwarding uses the available paths as expected
- Route selection changes correctly when interfaces fail
- The higher-cost cross-connected paths become active when required

---

## 8. Design Rationale

| Design Decision | Rationale |
|---|---|
| Two-tier collapsed core | Provides meaningful campus redundancy within the five-device HQ design |
| Single access switch | Preserves the five-device HQ limit |
| LACP at Layer 2 | Demonstrates logical link aggregation and member-link resilience |
| OSPF ECMP at Layer 3 | Demonstrates multipath routing across independent routed interfaces |
| Cross-connected routed paths | Enables path-cost and routing-reconvergence testing |
| `/31` routed interfaces | Efficient addressing for two-endpoint routed infrastructure |
| `/32` loopbacks | Stable device identities and explicit OSPF router IDs |
| VLSM | Sizes networks by function rather than assigning every VLAN a `/24` |
| Dedicated native VLAN | Keeps trunk native traffic separate from production user VLANs |
| Parking VLAN | Keeps unused access ports separate from production VLANs |
| HSRP/STP alignment | Aligns the preferred Layer 2 path with the active gateway |
| Split HSRP/STP ownership | Allows both Distribution Switches to participate in normal forwarding |
| Passive-by-default OSPF | Limits neighbour formation to intentional routed interfaces |
| Separate implementation evidence | Keeps design intent separate from platform-specific behaviour and proof |

---

## 9. Current Design Status

The following are **design decisions**:

- Five-device HQ topology
- OSPF Area 10
- VLAN and VLSM plan
- HSRP addressing convention
- LACP EtherChannels at Layer 2
- Routed Distribution-to-Edge interfaces
- Four-path OSPF ECMP intent
- Higher-cost cross-connected routed paths
- HSRP/STP role alignment
- `/31` point-to-point addressing
- `/32` loopbacks

The following require implementation evidence before they are considered **as-built**:

- Final platform/image selection
- Exact interface availability and naming
- EtherChannel formation
- Trunk VLAN state
- HSRP failover
- Rapid PVST+ root/blocking behaviour
- OSPF adjacency formation
- Four installed equal-cost routes
- ECMP forwarding behaviour
- Alternate-path failover
- Failure/reconvergence behaviour

Implementation detail and evidence will be maintained separately as the build progresses.

---

## 10. Next Design Phase

After the HQ baseline is implemented and verified, the project will progress toward:

- Monitoring and logging
- Layer 2 security controls
- ACL policy
- Area 0 backbone design
- Branch/Area 20
- GRE
- GRE over IPsec
- Dual-tunnel resilience
- WAN failover / wider ECMP testing
- Python and Ansible automation

The HQ design should remain stable unless implementation evidence identifies a genuine platform or architectural constraint.
