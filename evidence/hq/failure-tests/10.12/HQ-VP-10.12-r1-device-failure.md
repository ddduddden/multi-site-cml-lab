[Phase 10](../README.md) / [10.12](r1-device-failure-evidence.md)

[← Previous](r1-device-failure-evidence.md) · [↑ Phase 10 Index](../README.md) · [Test evidence](r1-device-failure-evidence.md) · [Next →](10.12-retained-cli-excerpt.md)

---

HQ-VP-10.12 — hq-r1 Device Failure
==================================

Phase 10 — Failure and Resilience Testing

**Evidence commit:** [`a8624b1`](https://github.com/ddduddden/multi-site-cml-lab/commit/a8624b176298e3b0132daedf082c2aae0c704ebd)
Evidence: [Retained CLI excerpt](10.12-retained-cli-excerpt.md)

Before failure
--------------
From hq-a1 VLAN199 (NET-MGMT):

- hq-r1 Loopback0: 5/5 replies.
- hq-r2 Loopback0: 5/5 replies.

Failure
-------
hq-r1 was stopped in CML.

After convergence:

- hq-r1 Loopback0: 0/5 replies.
- hq-r2 Loopback0: 5/5 replies.
- hq-d1 kept its hq-r2 cross-link OSPF neighbour.
- hq-d2 kept its four direct hq-r2 OSPF neighbours.

Scope: surviving VLAN199 traffic to hq-r2 did not depend on hq-r1;
live-flow failover away from hq-r1 was not tested.

Recovery
--------
Two early checks to hq-r1 still failed:

- hq-r1 Loopback0 (each early check): 0/5 replies.

Once hq-r1 had finished booting and OSPF had converged:

- hq-r1 Loopback0: 5/5 replies.
- hq-r1 Loopback0 (immediate repeat): 5/5 replies.
- hq-r2 Loopback0: 5/5 replies.
- hq-r1 returned to five OSPF neighbours in Full state.

Result
------
PASS. Stopping hq-r1 made its Loopback0 interface unreachable, while hq-r2
remained reachable and hq-d1 kept its surviving OSPF neighbour to hq-r2 over
the cross-link.

After hq-r1 restarted, hq-r1 rebuilt its five OSPF neighbours and normal
connectivity returned.

---

[← Previous](r1-device-failure-evidence.md) · [↑ Phase 10 Index](../README.md) · [Test evidence](r1-device-failure-evidence.md) · [Next →](10.12-retained-cli-excerpt.md)
