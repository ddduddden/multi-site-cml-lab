[Portfolio](../../../../README.md) / [Evidence Map](../../README.md) / [Phase 10](../README.md) / [10.13](README.md) / Test report

# HQ-VP-10.13 — Diagonal Double Failure: hq-d1 + hq-r2

Phase 10 — Failure and Resilience Testing

**Evidence commit:** [`a8624b1`](https://github.com/ddduddden/multi-site-cml-lab/commit/a8624b176298e3b0132daedf082c2aae0c704ebd)
Evidence: [captured CLI and session records](README.md)

VLAN170 (BYOD-WLAN) setup
-------------------------
Temporary hq-a1 source: 10.10.70.4/23.

Temporary-address availability check
------------------------------------
Before assigning 10.10.70.4/23 to hq-a1:

- 10.10.70.4: 0/3 replies.
- ARP remained incomplete.

Healthy state:

- hq-d1 was HSRP Active.
- hq-a1 used Po10 as the root path.
- HSRP VIP: 5/5 replies.
- hq-r1 Loopback0: 5/5 replies.
- hq-r2 Loopback0: 5/5 replies.

The baseline gateway ping recorded min/avg/max 3/205/1007 ms. No cause is
assigned.

First failure — hq-d1
---------------------
hq-d1 was stopped.

After convergence:

- hq-d2 became HSRP Active.
- hq-a1 moved to Po20 as the root path.
- HSRP VIP: 5/5 replies.
- hq-r1 Loopback0: 5/5 replies.
- hq-r2 Loopback0: 5/5 replies.

A sourced ping was first entered on hq-d2 instead of hq-a1. IOS rejected the
source address because 10.10.70.4 belonged to hq-a1. The check was then run from
the correct device and passed.

Second failure — hq-r2
----------------------
With hq-d1 still down, hq-r2 was stopped.

hq-d2 was left with one OSPF neighbour:

- hq-r1 at 10.255.10.7.
- Interface Gi3/0.

hq-d2 route to hq-r1 Loopback0:

- Metric 101.
- Outgoing interface Gi3/0.

From hq-a1:

- HSRP VIP: 5/5 replies.
- hq-r1 Loopback0: 5/5 replies.

Reverse route on hq-r1:

- 10.10.70.0/23 via 10.255.10.6.
- Outgoing interface Gi0/4.
- Metric 101.
- Advertising router 10.255.10.132 / hq-d2.

With one OSPF path left in each direction, the route tables show the surviving
hq-d2 <-> hq-r1 cross-link was carrying the remaining campus route.

Not measured: transition packet loss when hq-r2 stopped; checks cover the
settled state.

Recovery
--------
Recovery order:

1. hq-r2 started.
2. hq-d1 started.

After hq-r2 returned, it formed four OSPF neighbours with hq-d2 while hq-d1 was
still down.

After hq-d1 returned:

- hq-d1 reclaimed HSRP Active.
- hq-d1 returned to five OSPF neighbours in Full state.
- hq-a1 returned to Po10 as the root path.
- HSRP VIP (first check): 4/5 replies.
- HSRP VIP (follow-up check): 5/5 replies.
- hq-r1 and hq-r2 Loopback0 (each): 5/5 replies.

Result
------
PASS. The settled double-failure state used the surviving hq-d2 <-> hq-r1
cross-link in both directions, and staged recovery returned the preferred
topology.

---

[◀ Evidence index](README.md) · [↑ Test evidence](README.md) · [Next record ▶](10.13-session-record.md)
