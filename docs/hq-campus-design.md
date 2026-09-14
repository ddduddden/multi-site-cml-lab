# HQ Campus Design

## Overview

The HQ campus uses a five-device, two-tier collapsed-core design consisting of a redundant distribution/core layer, a Layer 2 access layer, and dual WAN edge routers. The internal HQ routing domain operates as OSPF Area 10, with the edge routers providing redundant paths toward the Area 0 inter-site backbone and supporting future GRE/IPsec connectivity.

The topology is designed to provide resilient Layer 2 and Layer 3 connectivity using LACP EtherChannels, HSRP, Rapid PVST+, and OSPF. Redundant physical and logical paths are included so that link, gateway, routing, and device failures can be deliberately introduced, observed, verified, and documented.

The campus design also incorporates network segmentation and is designed to support additional security controls. Dedicated VLANs separate user, voice, server, IoT, guest, wireless, and management traffic, with a dedicated native VLAN for trunking and a separate parking VLAN for unused access ports. Additional controls such as port security, DHCP snooping, Dynamic ARP Inspection, and access-control policies will be introduced during later implementation phases.

Campus services and routed infrastructure use separate hierarchical address spaces. The addressing plan uses VLSM, /31 point-to-point networks, and /32 loopbacks to provide a structure that is readable, scalable, and suitable for route summarisation.

The HQ campus forms the first stage of a larger multi-site lab. Later phases will extend the design with monitoring, real services, secure inter-site connectivity, failure testing, and network automation.

## High-Level Topology

![HQ Campus - OSPF Area 10](../diagrams/hq-campus-area10-topology.png)

## VLAN and Gateway Design

| VLAN ID | VLAN Name | Function | IPv4 Prefix | HSRP Virtual IP | `hq-d1` SVI Address | `hq-d2` SVI Address |
|---:|---|---|---|---|---|---|
| 112 | `CORP-USERS` | Corporate user endpoints | `10.10.12.0/22` | `10.10.12.1` | `10.10.12.2` | `10.10.12.3` |
| 120 | `VOICE` | IP telephony endpoints | `10.10.20.0/23` | `10.10.20.1` | `10.10.20.2` | `10.10.20.3` |
| 130 | `SERVERS` | Server and application services | `10.10.30.0/25` | `10.10.30.1` | `10.10.30.2` | `10.10.30.3` |
| 140 | `IOT-CCTV` | IoT and surveillance devices | `10.10.40.0/23` | `10.10.40.1` | `10.10.40.2` | `10.10.40.3` |
| 152 | `GUEST` | Guest network access | `10.10.52.0/22` | `10.10.52.1` | `10.10.52.2` | `10.10.52.3` |
| 160 | `FACILITIES` | Printers and facilities devices | `10.10.60.0/26` | `10.10.60.1` | `10.10.60.2` | `10.10.60.3` |
| 170 | `BYOD-WLAN` | BYOD and wireless client access | `10.10.70.0/23` | `10.10.70.1` | `10.10.70.2` | `10.10.70.3` |
| 190 | `NATIVE` | Dedicated IEEE 802.1Q native VLAN | — | — | — | — |
| 191 | `PARKING` | Unused access ports | — | — | — | — |
| 199 | `NET-MGMT` | Network infrastructure management | `10.10.99.0/26` | `10.10.99.1` | `10.10.99.2` | `10.10.99.3` |

### Addressing and VLAN Conventions

For each routed VLAN, gateway addressing follows a consistent allocation:

- First usable address — HSRP Virtual IP and client default gateway
- Second usable address — `hq-d1` SVI address
- Third usable address — `hq-d2` SVI address

VLAN 190 is reserved as the dedicated non-default native VLAN for IEEE 802.1Q trunks and does not have an SVI.

VLAN 191 is reserved for unused access ports and does not have an SVI. Unused ports assigned to this VLAN are administratively shut down.

VLAN 1 is not used for production user traffic, management, or as the configured native VLAN in this design.

## Layer 3 Addressing Design

| Device | Interface | Role / Purpose | IPv4 Address / Prefix | HSRP Virtual IP | Associated Device / Routing Notes |
|---|---|---|---|---|---|
| `hq-d1` | `Vlan112` | Corporate user gateway SVI | `10.10.12.2/22` | `10.10.12.1` | HSRP with `hq-d2` |
| `hq-d2` | `Vlan112` | Corporate user gateway SVI | `10.10.12.3/22` | `10.10.12.1` | HSRP with `hq-d1` |
| `hq-d1` | `Vlan120` | Voice gateway SVI | `10.10.20.2/23` | `10.10.20.1` | HSRP with `hq-d2` |
| `hq-d2` | `Vlan120` | Voice gateway SVI | `10.10.20.3/23` | `10.10.20.1` | HSRP with `hq-d1` |
| `hq-d1` | `Vlan130` | Server gateway SVI | `10.10.30.2/25` | `10.10.30.1` | HSRP with `hq-d2` |
| `hq-d2` | `Vlan130` | Server gateway SVI | `10.10.30.3/25` | `10.10.30.1` | HSRP with `hq-d1` |
| `hq-d1` | `Vlan140` | IoT/CCTV gateway SVI | `10.10.40.2/23` | `10.10.40.1` | HSRP with `hq-d2` |
| `hq-d2` | `Vlan140` | IoT/CCTV gateway SVI | `10.10.40.3/23` | `10.10.40.1` | HSRP with `hq-d1` |
| `hq-d1` | `Vlan152` | Guest gateway SVI | `10.10.52.2/22` | `10.10.52.1` | HSRP with `hq-d2` |
| `hq-d2` | `Vlan152` | Guest gateway SVI | `10.10.52.3/22` | `10.10.52.1` | HSRP with `hq-d1` |
| `hq-d1` | `Vlan160` | Facilities gateway SVI | `10.10.60.2/26` | `10.10.60.1` | HSRP with `hq-d2` |
| `hq-d2` | `Vlan160` | Facilities gateway SVI | `10.10.60.3/26` | `10.10.60.1` | HSRP with `hq-d1` |
| `hq-d1` | `Vlan170` | BYOD/WLAN gateway SVI | `10.10.70.2/23` | `10.10.70.1` | HSRP with `hq-d2` |
| `hq-d2` | `Vlan170` | BYOD/WLAN gateway SVI | `10.10.70.3/23` | `10.10.70.1` | HSRP with `hq-d1` |
| `hq-d1` | `Vlan199` | Network management gateway SVI | `10.10.99.2/26` | `10.10.99.1` | HSRP with `hq-d2` |
| `hq-d2` | `Vlan199` | Network management gateway SVI | `10.10.99.3/26` | `10.10.99.1` | HSRP with `hq-d1` |
| `hq-d1` | `Po101` | Routed L3 Port-channel to `hq-r1` | `10.255.10.0/31` | — | `hq-r1` / OSPF Area 10 |
| `hq-r1` | `Po101` | Routed L3 Port-channel to `hq-d1` | `10.255.10.1/31` | — | `hq-d1` / OSPF Area 10 |
| `hq-d2` | `Po201` | Routed L3 Port-channel to `hq-r2` | `10.255.10.2/31` | — | `hq-r2` / OSPF Area 10 |
| `hq-r2` | `Po201` | Routed L3 Port-channel to `hq-d2` | `10.255.10.3/31` | — | `hq-d2` / OSPF Area 10 |
| `hq-d1` | `E3/0` | Redundant Layer 3 link to `hq-r2` | `10.255.10.4/31` | — | `hq-r2 E1/0` / OSPF Area 10 |
| `hq-r2` | `E1/0` | Redundant Layer 3 link to `hq-d1` | `10.255.10.5/31` | — | `hq-d1 E3/0` / OSPF Area 10 |
| `hq-d2` | `E3/0` | Redundant Layer 3 link to `hq-r1` | `10.255.10.6/31` | — | `hq-r1 E1/0` / OSPF Area 10 |
| `hq-r1` | `E1/0` | Redundant Layer 3 link to `hq-d2` | `10.255.10.7/31` | — | `hq-d2 E3/0` / OSPF Area 10 |
| `hq-r1` | `Loopback0` | Infrastructure identity / OSPF router ID | `10.255.10.129/32` | — | OSPF router ID `10.255.10.129` |
| `hq-r2` | `Loopback0` | Infrastructure identity / OSPF router ID | `10.255.10.130/32` | — | OSPF router ID `10.255.10.130` |
| `hq-d1` | `Loopback0` | Infrastructure identity / OSPF router ID | `10.255.10.131/32` | — | OSPF router ID `10.255.10.131` |
| `hq-d2` | `Loopback0` | Infrastructure identity / OSPF router ID | `10.255.10.132/32` | — | OSPF router ID `10.255.10.132` |

### Layer 3 Addressing Conventions

The master addressing schedule defines the IPv4 addresses assigned to all routed HQ interfaces.

For routed VLANs, the first usable address is reserved as the HSRP Virtual IP, the second usable address is assigned to `hq-d1`, and the third usable address is assigned to `hq-d2`.

Point-to-point routed infrastructure links use /31 prefixes. The lower address is assigned to the distribution switch and the higher address to the edge router.

Loopback0 provides a stable Layer 3 identity for each routing device and is explicitly used as the OSPF router ID.

Physical interfaces participating in Layer 3 EtherChannels are not individually addressed. The IPv4 address is assigned to the logical Port-channel interface.

VLANs 190 and 191 are intentionally absent from this schedule because they do not have Layer 3 SVIs.

## Layer 2 EtherChannel and Trunk Design

HQ uses three four-link LACP EtherChannels for resilient Layer 2 connectivity between the Access and Distribution Switches. LACP operates in active mode at both ends of each bundle.

| Port-channel | Connected Switches | Physical Port Mapping | Function | LACP Mode | Native VLAN | Allowed VLANs |
|---|---|---|---|---|---:|---|
| `Po10` | `hq-a1` ↔ `hq-d1` | `hq-a1 E0/0-E0/3` ↔ `hq-d1 E0/0-E0/3` | Access-to-distribution trunk | Active / Active | 190 | `112,120,130,140,152,160,170,199` |
| `Po20` | `hq-a1` ↔ `hq-d2` | `hq-a1 E1/0-E1/3` ↔ `hq-d2 E0/0-E0/3` | Access-to-distribution trunk | Active / Active | 190 | `112,120,130,140,152,160,170,199` |
| `Po30` | `hq-d1` ↔ `hq-d2` | `hq-d1 E1/0-E1/3` ↔ `hq-d2 E1/0-E1/3` | Distribution interconnect trunk | Active / Active | 190 | `112,120,130,140,152,160,170,199` |

### Trunk Policy

- VLAN 190 is the dedicated unused native VLAN.
- VLAN 191 is reserved for unused access ports and is not carried across campus trunks.
- Only required production and management VLANs are explicitly permitted.
- Active/Active LACP provides a consistent negotiation policy across all HQ EtherChannels.

---

## Layer 3 EtherChannel Design

Two routed LACP EtherChannels provide resilient Layer 3 connectivity between the Distribution Switches and their directly connected Edge Routers.

| Port-channel | Distribution Switch | Interface Range | Edge Router | Interface Range | Function | LACP Mode | IPv4 Network | OSPF Area |
|---|---|---|---|---|---|---|---|---:|
| `Po101` | `hq-d1` | `E2/0-E2/3` | `hq-r1` | `E0/0-E0/3` | Routed distribution-to-edge uplink | Active / Active | `10.255.10.0/31` | 10 |
| `Po201` | `hq-d2` | `E2/0-E2/3` | `hq-r2` | `E0/0-E0/3` | Routed distribution-to-edge uplink | Active / Active | `10.255.10.2/31` | 10 |

### Port-channel Addressing

| Port-channel | Distribution Switch | Edge Router |
|---|---|---|
| `Po101` | `hq-d1 Po101` — `10.255.10.0/31` | `hq-r1 Po101` — `10.255.10.1/31` |
| `Po201` | `hq-d2 Po201` — `10.255.10.2/31` | `hq-r2 Po201` — `10.255.10.3/31` |

---

## Redundant Layer 3 Link Design

Two additional routed point-to-point links connect each Distribution Switch to the opposite Edge Router. These links provide additional OSPF paths and allow routing reconvergence to be tested independently from EtherChannel link redundancy.

| Distribution Switch | Interface | Edge Router | Interface | Function | IPv4 Network | OSPF Area |
|---|---|---|---|---|---|---:|
| `hq-d1` | `E3/0` | `hq-r2` | `E1/0` | Redundant Layer 3 link | `10.255.10.4/31` | 10 |
| `hq-d2` | `E3/0` | `hq-r1` | `E1/0` | Redundant Layer 3 link | `10.255.10.6/31` | 10 |

### Link Addressing

| Link | Distribution Switch | Edge Router |
|---|---|---|
| `hq-d1` ↔ `hq-r2` | `hq-d1 E3/0` — `10.255.10.4/31` | `hq-r2 E1/0` — `10.255.10.5/31` |
| `hq-d2` ↔ `hq-r1` | `hq-d2 E3/0` — `10.255.10.6/31` | `hq-r1 E1/0` — `10.255.10.7/31` |

These links initially operate as additional valid OSPF paths. Preferred and alternate routing behaviour will be introduced later through deliberate OSPF cost manipulation.

---

## Loopback Interface Design

Loopback interfaces provide stable Layer 3 identities that are independent of individual physical links.

| Device | Interface | IPv4 Address | Function | OSPF Area |
|---|---|---|---|---:|
| `hq-r1` | `Loopback0` | `10.255.10.129/32` | Device identity, OSPF router ID, in-band management | 10 |
| `hq-r2` | `Loopback0` | `10.255.10.130/32` | Device identity, OSPF router ID, in-band management | 10 |
| `hq-d1` | `Loopback0` | `10.255.10.131/32` | Device identity, OSPF router ID, in-band management | 10 |
| `hq-d2` | `Loopback0` | `10.255.10.132/32` | Device identity, OSPF router ID, in-band management | 10 |
| `hq-r1` | `Loopback1` | TBD | Future GRE/IPsec tunnel source | TBD |
| `hq-r2` | `Loopback1` | TBD | Future GRE/IPsec tunnel source | TBD |

### Design Notes

- Loopback0 addresses are advertised into OSPF Area 10 and explicitly used as OSPF router IDs.
- Loopback0 also provides a stable in-band address for future monitoring, automation and troubleshooting.
- Loopback1 is reserved for future GRE/IPsec tunnel sourcing and will be addressed during the Area 0/WAN design.
- True out-of-band management will be designed separately later.

---

## HQ Access Port Design

`hq-a1` provides endpoint access for the HQ campus. Ports are grouped by function to simplify cabling, troubleshooting and future changes.

| Port Range | Access VLAN | Voice VLAN | Mode | Function | Administrative State |
|---|---:|---:|---|---|---|
| `E2/0-E2/1` | 112 | 120 | Access | Corporate workstation + IP phone | Enabled |
| `E2/2-E2/3` | 112 | — | Access | Corporate workstation | Enabled |
| `E3/0-E3/1` | 130 | — | Access | Server/application endpoint | Enabled |
| `E3/2-E3/3` | 140 | — | Access | IoT/CCTV endpoint | Enabled |
| `E4/0-E4/1` | 152 | — | Access | Guest endpoint | Enabled |
| `E4/2-E4/3` | 160 | — | Access | Printer/facilities endpoint | Enabled |
| `E5/0-E5/1` | 170 | — | Access | BYOD/WLAN test endpoint | Enabled |
| `E5/2-E5/3` | 199 | — | Access | Network-management endpoint | Enabled |
| `E6/0-E7/3` | 191 | — | Access | Parking / unused | **Shutdown** |

### Reserved VLANs

| VLAN | Name | Function |
|---:|---|---|
| 190 | `NATIVE` | Dedicated non-default native VLAN for Layer 2 trunks |
| 191 | `PARKING` | Unused access ports; administratively shut |

### Design Notes

- Endpoint-facing ports use static access mode to prevent unintended trunk negotiation and restrict each port to its assigned access VLAN.
- VLANs 112 and 120 demonstrate a workstation connected through an IP phone using separate data and voice VLANs.
- VLAN 199 provides in-band network management.
- Unused interfaces are placed in VLAN 191 and administratively shut down.

---

## HSRP and Rapid PVST+ Role Design

HSRP gateway ownership is aligned with Rapid PVST+ root placement so the preferred Layer 2 forwarding path terminates on the Distribution Switch acting as the active default gateway.

Preferred roles are divided across both Distribution Switches so both participate in normal forwarding while retaining redundancy.

| VLAN | Function | HSRP Active / STP Root Primary | HSRP Standby / STP Root Secondary |
|---:|---|---|---|
| 112 | Corporate Users | `hq-d1` | `hq-d2` |
| 120 | Voice | `hq-d2` | `hq-d1` |
| 130 | Servers | `hq-d1` | `hq-d2` |
| 140 | IoT/CCTV | `hq-d2` | `hq-d1` |
| 152 | Guest | `hq-d1` | `hq-d2` |
| 160 | Facilities | `hq-d2` | `hq-d1` |
| 170 | BYOD/WLAN | `hq-d1` | `hq-d2` |
| 199 | Network Management | `hq-d2` | `hq-d1` |

### HSRP Policy

- HSRP group numbers match their VLAN IDs.
- The preferred Distribution Switch uses HSRP priority `110`.
- The standby Distribution Switch uses priority `100`.
- Preemption is enabled on the preferred Distribution Switch so the intended active role is restored after recovery.
- The `.1` HSRP virtual address remains the default gateway for each routed VLAN.

### Rapid PVST+ Policy

- HQ uses Rapid PVST+.
- HSRP Active is aligned with STP Root Primary.
- HSRP Standby is aligned with STP Root Secondary.
- Root placement uses the Rapid PVST+ primary/secondary root mechanism rather than manually assigned bridge-priority values.
- Migration from Rapid PVST+ to MSTP is reserved for a later design exercise.

---

## OSPF Area 10 Design

HQ uses OSPF Area 10 as its internal routing domain.

Loopback0 addresses provide explicit OSPF router IDs, while OSPF adjacency formation is limited to the routed connections between the Distribution Switches and Edge Routers.

### OSPF Interface Policy

OSPF uses a passive-by-default policy.

User/service SVIs and Loopback0 interfaces are advertised into Area 10 without attempting to form OSPF neighbour relationships. Adjacency formation is explicitly enabled only on routed Distribution-to-Edge links.

This approach:

- prevents unnecessary OSPF hello traffic on endpoint-facing networks;
- reduces the opportunity for unintended OSPF neighbours;
- scales more safely because newly added interfaces remain passive unless explicitly enabled for adjacency formation.

### OSPF Adjacency Links

| Distribution Switch | Interface | Edge Router | Interface | Network Type | Area |
|---|---|---|---|---|---:|
| `hq-d1` | `Po101` | `hq-r1` | `Po101` | Point-to-point | 10 |
| `hq-d2` | `Po201` | `hq-r2` | `Po201` | Point-to-point | 10 |
| `hq-d1` | `E3/0` | `hq-r2` | `E1/0` | Point-to-point | 10 |
| `hq-d2` | `E3/0` | `hq-r1` | `E1/0` | Point-to-point | 10 |

Point-to-point network type matches the two-device topology of these routed links and avoids unnecessary DR/BDR election within HQ.

### OSPF Path Engineering

The initial deployment will first establish and document normal OSPF behaviour using baseline/default costs.

After the baseline has been verified:

- `hq-d1 → Po101 → hq-r1` will become the preferred routed path from `hq-d1`.
- `hq-d2 → Po201 → hq-r2` will become the preferred routed path from `hq-d2`.
- The Redundant Layer 3 Links will remain available at a higher OSPF cost.
- Failure of a preferred path will be used to demonstrate OSPF reconvergence through the alternate path.

Links will only be described as preferred or backup after the intended cost policy has been implemented and verified.

---

## Design Rationale

| Design Decision | Rationale |
|---|---|
| Two-tier collapsed core | Provides realistic campus redundancy within the five-device HQ design |
| Four-member LACP EtherChannels | Demonstrates aggregation, member-link resilience and EtherChannel failure behaviour |
| Active/Active LACP | Provides a consistent EtherChannel negotiation policy |
| Redundant Layer 3 links | Separates routing reconvergence testing from EtherChannel member-link failure |
| `/31` routed links | Efficient addressing for point-to-point infrastructure |
| `/32` loopbacks | Stable device identities and explicit OSPF router IDs |
| VLSM | Sizes subnets according to function and expected scale |
| Dedicated native VLAN | Keeps native traffic separate from production VLANs |
| Parking VLAN | Provides controlled treatment of unused access interfaces |
| HSRP/STP alignment | Aligns the preferred Layer 2 path with the active default gateway |
| Split HSRP/STP ownership | Uses both Distribution Switches during normal operation while preserving redundancy |
| Passive-by-default OSPF | Improves adjacency control, scalability and operational safety |
| OSPF point-to-point links | Matches the two-device routed topology without unnecessary DR/BDR election |

---

## Implementation Status

This document describes the **intended HQ design**.

The design will be updated to an as-built state after CML implementation, verification and failure testing.

Layer 3 LACP support on the selected IOL router image must be proven during implementation, and links will not be labelled as preferred or backup until OSPF path behaviour has been configured and verified.
