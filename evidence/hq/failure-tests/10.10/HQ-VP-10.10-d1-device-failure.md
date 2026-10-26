[Portfolio](../../../../README.md) / [Evidence Map](../../README.md) / [Phase 10](../README.md) / [10.10](README.md) / Test report

# HQ-VP-10.10 — hq-d1 Device Failure

Phase 10 — Failure and Resilience Testing

**Result: PASS**

**Original test plan:** [10.10 — hq-d1 device outage](../../../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1010-hq-d1-device-outage)\
**Evidence:** [Retained CLI excerpt](10.10-retained-cli-excerpt.md)\
**Evidence commit:** [a8624b1](https://github.com/ddduddden/multi-site-cml-lab/commit/a8624b176298e3b0132daedf082c2aae0c704ebd)

## Test objective

Verify that hq-d2 can maintain gateway and routed connectivity following the loss of hq-d1.

VLAN152 (GUEST) normally prefers hq-d1 for HSRP Active and STP root, so stopping that switch tests both gateway takeover and the surviving access path. Traffic was sourced from hq-a1 on VLAN152, using the temporary address 10.10.52.4/22.

## Healthy baseline

Before assigning the temporary address, I checked it from hq-d1. The ping returned 0/3 replies and ARP remained incomplete.

The initial session observations recorded:

- hq-d1 as HSRP Active for VLAN152.
- hq-a1 using Po10 as its STP root port.
- The HSRP virtual IP address (VIP) 10.10.52.1 responding to 5/5 pings.
- Both edge-router loopbacks responding to 5/5 pings.

These baseline observations were recorded during the session but were not preserved in the condensed CLI excerpt.

## Device failure

I stopped hq-d1 in CML and checked connectivity after convergence.

- hq-d2 became HSRP Active for VLAN152.
- hq-a1 selected Po20 as its STP root port.
- The gateway responded to 5/5 pings.
- Both edge-router loopbacks responded to 5/5 pings.

On hq-r1, the route to 10.10.52.0/22 had OSPF metric 101, using next hop 10.255.10.6 through Gi0/4 towards hq-d2.

This confirmed that the surviving distribution switch provided the VLAN152 gateway and a routed return path to the test source.

## Recovery

After restarting hq-d1:

- hq-a1 returned to Po10 as its STP root port.
- The first gateway check returned 4/5 replies; the immediate repeat returned 5/5.
- Both edge-router loopbacks responded to 5/5 pings.
- hq-r1's route returned to four equal-cost next hops at metric 11 towards hq-d1.

I removed the temporary VLAN152 source and returned hq-a1 to VLAN199 management. The final management gateway check returned 5/5 replies.

## Result

**PASS.** With hq-d1 stopped, hq-d2 took over the VLAN152 gateway and hq-a1 used the surviving Po20 uplink. Routing and traffic checks confirmed connectivity after convergence.

Recovery restored the preferred STP path, normal routing on hq-r1 and successful connectivity. The original baseline observations were not retained in the condensed CLI, and the final HSRP and OSPF states on hq-d1 were not separately captured.

VLAN152 exercised the HSRP and STP failover for the VLAN group that prefers hq-d1. The separate VLAN199 test cycle was not performed, and an exact convergence time could not be determined from the retained evidence.

---

[◀ Test evidence](README.md) · [Retained CLI ▶](10.10-retained-cli-excerpt.md) · [↑ Phase 10 Test Index](../README.md)
