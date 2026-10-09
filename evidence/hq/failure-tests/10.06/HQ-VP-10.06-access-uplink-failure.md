[Phase 10](../README.md) / [10.06](access-uplink-failure-evidence.md)

[← Previous](HQ-VP-10.06-mode-b-vlan112-setup-baseline.md) · [↑ Phase 10 Index](../README.md) · [Test evidence](access-uplink-failure-evidence.md) · [Next →](HQ-VP-10.06-final-recovery-restored-baseline.md)

---

HQ-VP-10.06 — Access Uplink Failure
===================================

Phase 10 — Failure and Resilience Testing

**Evidence commit:** [`a8624b1`](https://github.com/ddduddden/multi-site-cml-lab/commit/a8624b176298e3b0132daedf082c2aae0c704ebd)
Evidence: [captured CLI and source files](access-uplink-failure-evidence.md)

Po20 failure — VLAN199 (NET-MGMT)
--------------------------------
With hq-a1 Po20 shut:

- VLAN199 moved from Po20 to Po10.
- STP root-path cost changed from 3 to 6.
- hq-d2 stayed HSRP Active.

Reachability after convergence:

- HSRP VIP 10.10.99.1: 5/5 replies.
- hq-r2 Loopback0: 20/20 replies.

Po10 failure — VLAN112 (CORP-USERS)
-----------------------------------
Before assigning 10.10.12.4/22 to hq-a1:

- 10.10.12.4: 0/3 replies.
- ARP remained incomplete.

With Po10 shut:

- VLAN112 moved from Po10 to Po20.
- STP root-path cost changed from 3 to 6.
- hq-d1 stayed HSRP Active.

Reachability after convergence:

- HSRP VIP: 5/5 replies.
- hq-r1 Loopback0: 20/20 replies.
- Both IP SLA probes recorded zero failures during the measured failure window.

Not measured: packet loss during the later Po10 restoration.

Cleanup
-------
hq-a1 was returned to VLAN199 management with gateway 10.10.99.1.

Result
------
PASS. Either access uplink could be removed and the other Layer-2 path carried
the tested traffic while the intended HSRP gateway stayed Active.

---

[← Previous](HQ-VP-10.06-mode-b-vlan112-setup-baseline.md) · [↑ Phase 10 Index](../README.md) · [Test evidence](access-uplink-failure-evidence.md) · [Next →](HQ-VP-10.06-final-recovery-restored-baseline.md)
