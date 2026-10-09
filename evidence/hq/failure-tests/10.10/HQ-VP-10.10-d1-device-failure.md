[Phase 10](../README.md) / [10.10](d1-device-failure-evidence.md)

[← Previous](d1-device-failure-evidence.md) · [↑ Phase 10 Index](../README.md) · [Test evidence](d1-device-failure-evidence.md) · [Next →](10.10-retained-cli-excerpt.md)

---

HQ-VP-10.10 — hq-d1 Device Failure
==================================

Phase 10 — Failure and Resilience Testing

**Evidence commit:** [`a8624b1`](https://github.com/ddduddden/multi-site-cml-lab/commit/a8624b176298e3b0132daedf082c2aae0c704ebd)
Evidence: [Retained CLI excerpt](10.10-retained-cli-excerpt.md)

VLAN152 (GUEST) check
---------------------
Temporary hq-a1 source: 10.10.52.4/22.

Temporary-address availability check
------------------------------------
Before assigning 10.10.52.4/22 to hq-a1:

- 10.10.52.4: 0/3 replies.
- ARP remained incomplete.

Healthy-state observations (not retained in the condensed CLI record):

- hq-d1 was HSRP Active.
- hq-a1 used Po10 as the root path.
- HSRP VIP: 5/5 replies.
- hq-r1 Loopback0: 5/5 replies.
- hq-r2 Loopback0: 5/5 replies.

Failure
-------
hq-d1 was stopped in CML.

After convergence:

- hq-d2 became HSRP Active.
- hq-a1 moved to Po20 as the root path.
- HSRP VIP: 5/5 replies.
- hq-r1 Loopback0: 5/5 replies.
- hq-r2 Loopback0: 5/5 replies.
- hq-r1 changed from four direct metric-11 routes to a metric-101 route through
  hq-d2 via 10.255.10.6 / Gi0/4.

Recovery
--------
After hq-d1 restarted:

- hq-a1 returned to Po10 as the root path.
- HSRP VIP (first check): 4/5 replies.
- HSRP VIP (immediate repeat): 5/5 replies.
- hq-r1 and hq-r2 Loopback0 (each): 5/5 replies.
- hq-r1 returned to four metric-11 paths through hq-d1.

Not captured: hq-d1 HSRP/OSPF state after restart in this rerun.

Result
------
PASS. With hq-d1 down, hq-d2 carried the VLAN152 gateway and access path.
After hq-d1 restarted, the access path, hq-r1 routing and tested traffic
returned
to normal.

---

[← Previous](d1-device-failure-evidence.md) · [↑ Phase 10 Index](../README.md) · [Test evidence](d1-device-failure-evidence.md) · [Next →](10.10-retained-cli-excerpt.md)
