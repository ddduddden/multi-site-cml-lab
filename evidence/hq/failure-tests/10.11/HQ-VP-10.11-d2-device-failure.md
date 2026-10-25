[Portfolio](../../../../README.md) / [Evidence Map](../../README.md) / [Phase 10](../README.md) / [10.11](README.md) / Test report

# HQ-VP-10.11 — hq-d2 Device Failure

Phase 10 — Failure and Resilience Testing

**Result: PASS**

**Original test plan:** [HQ-VP-10.11 — hq-d2 device outage](../../../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1011-hq-d2-device-outage)\
**Evidence:** [Retained CLI excerpt](10.11-retained-cli-excerpt.md)\
**Evidence commit:** [a8624b1](https://github.com/ddduddden/multi-site-cml-lab/commit/a8624b176298e3b0132daedf082c2aae0c704ebd)

## Test objective

Verify that hq-d1 can maintain gateway and routed connectivity when hq-d2 fails completely. VLAN140 (IOT-CCTV) was selected because it normally prefers hq-d2 for HSRP Active and STP root.

## Healthy baseline

Before assigning the temporary address 10.10.40.4/23 to hq-a1, I checked its availability from hq-d2. The ping returned 0/3 replies and no ARP entry was present.

The healthy baseline confirmed:

- hq-d2 was HSRP Active and hq-d1 Standby.
- hq-a1 used Po20 as its STP root port, with Po10 as the alternate.
- The HSRP virtual IP address (VIP) 10.10.40.1 responded to 5/5 pings.
- Both edge-router loopbacks responded to 5/5 pings.

The baseline VIP check recorded a maximum response time of 1004 ms. No cause was established.

## Device failure

I stopped hq-d2 in CML and checked the network after convergence.

With the preferred distribution switch unavailable:

- hq-d1 became HSRP Active for VLAN140.
- hq-a1 selected Po10 as its STP root port.
- The virtual gateway responded to 5/5 pings.
- Both edge-router loopbacks remained reachable, each returning 5/5 replies.

The routing evidence also confirmed an alternate return path. On hq-r2, the route to 10.10.40.0/23 used OSPF metric 101, with next hop 10.255.10.4 through Gi0/4 towards hq-d1.

This showed that the surviving distribution switch was providing both the VLAN gateway and a routed path back towards the test source.

## Recovery

After restarting hq-d2, the preferred roles returned:

- hq-d2 reclaimed HSRP Active for VLAN140.
- hq-a1 returned to Po20 as its STP root port.
- The first VIP check returned 4/5 replies; an immediate repeat returned 5/5.
- Both edge-router loopbacks responded to 5/5 pings.

I removed the temporary VLAN140 test configuration and returned hq-a1 to VLAN199 management with gateway 10.10.99.1. The first management gateway check returned 4/5 replies; an immediate repeat returned 5/5.

## Result

**PASS.** When hq-d2 was stopped, hq-d1 took over the VLAN140 gateway and hq-a1 used its surviving Po10 uplink. The recorded routing and traffic checks confirmed connectivity through the remaining distribution switch.

After recovery, the preferred HSRP and STP roles returned. The initial 4/5 gateway check is retained rather than presenting recovery as loss-free.

VLAN140 prefers hq-d2, so the one device stop/start cycle exercised both HSRP and STP failover. The separate planned VLAN112 cycle was not run. The results confirm settled-state connectivity, but the exact convergence time and whether the transition was loss-free could not be determined from the retained evidence.

---

[◀ Test evidence](README.md) · [Retained CLI ▶](10.11-retained-cli-excerpt.md)
