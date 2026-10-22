[Portfolio](../../../../README.md) / [Evidence Map](../../README.md) / [Phase 10](../README.md) / [10.11](README.md) / Test report

# HQ-VP-10.11 — hq-d2 Device Failure

Phase 10 — Failure and Resilience Testing

**Evidence commit:** [`a8624b1`](https://github.com/ddduddden/multi-site-cml-lab/commit/a8624b176298e3b0132daedf082c2aae0c704ebd)
Evidence: [Retained CLI excerpt](10.11-retained-cli-excerpt.md)

VLAN140 (IOT-CCTV) check
------------------------
Temporary hq-a1 source: 10.10.40.4/23.

Temporary-address availability check
------------------------------------
Before assigning 10.10.40.4/23 to hq-a1:

- 10.10.40.4: 0/3 replies.
- No ARP entry remained.

Healthy state:

- hq-d2 was HSRP Active.
- hq-a1 used Po20 as the root path.
- HSRP VIP: 5/5 replies.
- hq-r1 Loopback0: 5/5 replies.
- hq-r2 Loopback0: 5/5 replies.

The baseline VIP ping recorded min/avg/max 3/204/1004 ms. No cause is assigned.

Failure
-------
hq-d2 was stopped in CML.

After convergence:

- hq-d1 became HSRP Active.
- hq-a1 moved to Po10 as the root path.
- HSRP VIP: 5/5 replies.
- hq-r1 Loopback0: 5/5 replies.
- hq-r2 Loopback0: 5/5 replies.
- hq-r2 changed from four direct metric-11 routes to a metric-101 route through
  hq-d1 via 10.255.10.4 / Gi0/4.

Recovery
--------
After hq-d2 restarted:

- hq-d2 reclaimed the preferred HSRP role.
- hq-a1 returned to Po20 as the root path.
- HSRP VIP (first check): 4/5 replies.
- HSRP VIP (immediate repeat): 5/5 replies.
- hq-r1 and hq-r2 Loopback0 (each): 5/5 replies.

Result
------
PASS. With hq-d2 down, hq-d1 carried the VLAN140 gateway and access path.
The preferred HSRP/STP state returned after restart.

---

[◀ Evidence index](README.md) · [↑ Test evidence](README.md) · [Next record ▶](10.11-retained-cli-excerpt.md)
