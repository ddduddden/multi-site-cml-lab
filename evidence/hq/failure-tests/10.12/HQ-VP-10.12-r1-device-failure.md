[Phase 10](../README.md) / [10.12](r1-device-failure-evidence.md)

[← Previous](r1-device-failure-evidence.md) · [↑ Phase 10 Index](../README.md) · [Test evidence](r1-device-failure-evidence.md) · [Next →](10.12-retained-cli-excerpt.md)

---

# [←](../10.11/HQ-VP-10.11-d2-device-failure.md "Previous VP") HQ-VP-10.12 — hq-r1 Device Failure [→](../10.13/HQ-VP-10.13-diagonal-double-failure.md "Next VP")

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
INCONCLUSIVE. `hq-r2` remained reachable while `hq-r1` was stopped, and
`hq-d1` kept its OSPF neighbour to `hq-r2` over the cross-link. These
surviving-path checks passed. Normal connectivity returned after restoration.

However, the tested traffic was not confirmed to use `hq-r1` before the
failure, so live-flow failover through `hq-r2` was not demonstrated.

---

[← Previous](r1-device-failure-evidence.md) · [↑ Phase 10 Index](../README.md) · [Test evidence](r1-device-failure-evidence.md) · [Next →](10.12-retained-cli-excerpt.md)
