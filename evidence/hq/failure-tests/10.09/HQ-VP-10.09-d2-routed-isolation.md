[Phase 10](../README.md) / [10.09](d2-routed-isolation-evidence.md)

[← Previous](d2-routed-isolation-evidence.md) · [↑ Phase 10 Index](../README.md) · [Test evidence](d2-routed-isolation-evidence.md) · [Next →](10.09-session-record.md)

---

HQ-VP-10.09 — hq-d2 Routed Isolation
====================================

Phase 10 — Failure and Resilience Testing

**Evidence commit:** [`a8624b1`](https://github.com/ddduddden/multi-site-cml-lab/commit/a8624b176298e3b0132daedf082c2aae0c704ebd)
Evidence: [captured CLI and session records](d2-routed-isolation-evidence.md)

Failure
-------
All five routed hq-d2 uplinks were shut. Po20 and Po30 were left up.

What happened
-------------
hq-d2:

- Lost all OSPF neighbours.
- Lost routes to both edge-router loopbacks.
- Stayed HSRP Active for VLAN199 (NET-MGMT).
- Kept Po20 and Po30 up.

From hq-a1:

- HSRP VIP 10.10.99.1: 5/5 replies.
- Edge-router loopback checks returned ICMP unreachable.

The gateway was still reachable, but hq-d2 no longer had a routed path to the
remote destinations.

hq-d1 stayed HSRP Standby and could still reach both edge loopbacks.

Recovery
--------
After all five routed links returned:

- hq-d2 returned to five OSPF neighbours in Full state.
- hq-d2 was still HSRP Active.
- hq-a1 could again reach the VIP and both edge loopbacks.

Result
------
DESIGN LIMITATION CONFIRMED. hq-d2 stayed HSRP Active after losing all routed
upstream connectivity because no HSRP uplink tracking is configured. The local
gateway still answered, but remote routed traffic failed.

Design note: with the current HSRP priority split of 110/100, tracking would
need a decrement greater than 10 so hq-d2 falls below hq-d1. hq-d1 would also
need preempt enabled for that priority change to trigger takeover.

---

[← Previous](d2-routed-isolation-evidence.md) · [↑ Phase 10 Index](../README.md) · [Test evidence](d2-routed-isolation-evidence.md) · [Next →](10.09-session-record.md)
