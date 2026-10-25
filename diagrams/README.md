# Network Diagrams

[Portfolio](../README.md) / Network Diagrams

| Diagram | Supporting document |
|---|---|
| [High-level HQ campus topology](#high-level-topology) | [HQ Campus Design](../docs/hq-campus-design.md) |
| [Detailed HQ campus topology and VLANs](#detailed-topology) | [HQ Campus Design](../docs/hq-campus-design.md) |
| [Physical network topology](#physical-network-topology) | [Physical Topology](../docs/topology.md) · [Network Plan](../docs/network-plan.md) |

## High-level topology

The five-device HQ campus, the OSPF Area 10 routed connections and the EtherChannel layout.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="hq-campus-area10-topology-dark.svg">
  <img src="hq-campus-area10-topology.svg" alt="HQ campus high-level topology with two routers, two distribution switches and one access switch">
</picture>

[Open high-level SVG at full size](hq-campus-area10-topology.svg) · [Dark version](hq-campus-area10-topology-dark.svg) · **[Continue to detailed topology ↓](#detailed-topology)**

---

## Detailed topology

Interface and /31 addressing, VLAN allocations, gateway roles, STP root-port selection and management connections. Open the full-size SVG to read the smaller labels.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="hq-campus-area10-topology-detailed-dark.svg">
  <img src="hq-campus-area10-topology-detailed.svg" alt="Detailed HQ topology showing routed interfaces, VLANs, HSRP, STP root ports and management connectivity">
</picture>

[Open detailed SVG at full size](hq-campus-area10-topology-detailed.svg) · [Dark version](hq-campus-area10-topology-detailed-dark.svg) · [↑ High-level topology](#high-level-topology)

---

## Physical network topology

The physical home-lab connections between the FTTP gateway, two CML hosts, Raspberry Pi 5 and AiMesh backhaul. Service roles labelled as planned are not yet deployed.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="physical-network-topology-dark.svg">
  <img src="physical-network-topology.svg" alt="Physical network topology showing the FTTP connection, ASUS router and AiMesh node, two CML hosts and Raspberry Pi 5">
</picture>

[Open physical SVG at full size](physical-network-topology.svg) · [Dark version](physical-network-topology-dark.svg) · [Physical connections and notes](../docs/topology.md) · [↑ High-level topology](#high-level-topology)

---

[↑ Portfolio](../README.md) · [HQ Evidence Map](../evidence/hq/README.md)
