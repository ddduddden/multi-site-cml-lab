[Portfolio](../../../../README.md) / [Evidence Map](../../README.md) / [Phase 10](../README.md) / [10.13](README.md) / Test report

# HQ-VP-10.13 — Diagonal Double Failure: hq-d1 + hq-r2

Phase 10 — Failure and Resilience Testing

**Result: PASS**

**Original test plan:** [HQ-VP-10.13 — Diagonal double-device failure](../../../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1013-diagonal-double-device-failure)\
**Evidence:** [Session record](10.13-session-record.md)\
**Evidence commit:** [a8624b1](https://github.com/ddduddden/multi-site-cml-lab/commit/a8624b176298e3b0132daedf082c2aae0c704ebd)

## Test objective

Verify connectivity through the surviving diagonal pair, hq-d2 and hq-r1, after the sequential loss of hq-d1 and hq-r2.

Traffic was sourced from hq-a1 on VLAN170 (BYOD-WLAN), using the temporary address 10.10.70.4/23.

## Healthy baseline

Before assigning the temporary address, I checked its availability from hq-d1. The ping returned 0/3 replies and ARP remained incomplete.

The healthy baseline confirmed:

- hq-d1 was HSRP Active for VLAN170.
- hq-a1 used Po10 as its STP root port.
- The HSRP virtual IP address (VIP) 10.10.70.1 responded to 5/5 pings.
- Both edge-router loopbacks responded to 5/5 pings.

The baseline gateway ping recorded min/avg/max 3/205/1007 ms. No cause was established.

## First failure — hq-d1

I stopped hq-d1 in CML.

After convergence:

- hq-d2 became HSRP Active for VLAN170.
- hq-a1 selected Po20 as its STP root port.
- The gateway and both edge-router loopbacks returned **5/5 replies**.

## Second failure — hq-r2

With hq-d1 still stopped, I stopped hq-r2.

hq-d2 retained one FULL OSPF adjacency to hq-r1, using Gi3/0 and neighbour address 10.255.10.7.

Its route to hq-r1 Loopback0 had metric **101** through Gi3/0.

Traffic from hq-a1 remained successful:

- VLAN170 gateway: **5/5 replies**.
- hq-r1 Loopback0: **5/5 replies**.

The reverse route on hq-r1 confirmed:

- **Destination:** 10.10.70.0/23
- **Next hop:** 10.255.10.6
- **Outgoing interface:** Gi0/4
- **OSPF metric:** 101
- **Advertising router:** 10.255.10.132 (hq-d2)

The advertising-router ID identified hq-d2 as the origin of the VLAN170 route. Together, the forward and reverse routing evidence supported the hq-d2 ↔ hq-r1 cross-link as the only remaining routed path.

These checks covered the settled double-failure state. Packet loss during the transition was not measured.

## Recovery

I restored the devices in reverse order of failure, starting hq-r2 before hq-d1.

With hq-d1 still down, hq-r2 restored its four OSPF adjacencies to hq-d2.

After hq-d1 returned:

- hq-d1 reclaimed HSRP Active for VLAN170.
- All five OSPF adjacencies on hq-d1 returned to FULL.
- hq-a1 returned to Po10 as its STP root port.
- The first gateway check returned **4/5 replies**; the repeat returned **5/5**.
- Both edge-router loopbacks responded to **5/5** pings.

I removed the temporary VLAN170 source and returned hq-a1 to its original VLAN199 management gateway.

## Result

**PASS.** The settled double-failure state retained connectivity through the surviving hq-d2–hq-r1 cross-link, with routing evidence supporting the path in both directions.

Staged recovery restored the preferred HSRP, STP and OSPF state. The initial 4/5 recovery result remains recorded, and no claim is made about packet loss or convergence time during the transitions.

---

[◀ Test evidence](README.md) · [Session record ▶](10.13-session-record.md)
