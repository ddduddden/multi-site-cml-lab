[Phase 10](../README.md) / [10.14](final-restoration-evidence.md)

[← Previous](final-restoration-evidence.md) · [↑ Phase 10 Index](../README.md) · [Test evidence](final-restoration-evidence.md) · [Next →](10.14-config-excerpts.md)

---

HQ-VP-10.14 — Final Restoration
===============================

Phase 10 — Failure and Resilience Testing

**Evidence commit:** [`a8624b1`](https://github.com/ddduddden/multi-site-cml-lab/commit/a8624b176298e3b0132daedf082c2aae0c704ebd)
Evidence: [captured CLI and session records](final-restoration-evidence.md)

Final baseline
--------------
All temporary failure conditions were removed and the HQ network was returned
to its normal operating state.

Final checks showed:

- Po10 and Po20 were up with both members bundled.
- Po30 was up with all four members bundled.
- STP showed no inconsistent ports.
- The intended STP root and HSRP Active/Standby split was restored.
- hq-d1, hq-d2, hq-r1 and hq-r2 each had five OSPF neighbours in Full state.
- No IP SLA test operations remained on hq-a1.

Final reachability from hq-a1:

- VLAN199 (NET-MGMT) gateway 10.10.99.1: 5/5 replies.
- hq-r1 Loopback0: 5/5 replies.
- hq-r2 Loopback0: 5/5 replies.

VLAN120 (VOICE) final coverage
------------------------------
A temporary VLAN120 source was used for the last routed-VLAN check.
Not retained: a pre-assignment availability check for 10.10.20.4.

- HSRP VIP 10.10.20.1: 5/5 replies.
- hq-r1 Loopback0: 5/5 replies.
- hq-r2 Loopback0: 5/5 replies.

The gateway ping recorded min/avg/max 3/205/1009 ms. No cause was proved.

The temporary VLAN120 configuration was then removed.

During this check, the temporary address was briefly entered on hq-d1 instead
of hq-a1. The mistake was spotted straight away and hq-d1 Vlan120 was restored
to 10.10.20.2/23 with its normal HSRP state. The incorrect default-gateway line
was also removed.

Cleanup and configuration checks
--------------------------------
hq-a1 finished with:

- VLAN199 at 10.10.99.4/26.
- Default gateway 10.10.99.1.
- No temporary source SVI.
- No IP SLA test configuration.

The final running/startup comparison is retained for hq-a1:

- hq-a1: `logging buffered 65536 informational` remained from Phase 10.

The session notes record the hq-d1 comparison result, but its CLI output was not
retained: only IOSv banner differences remained, with no VLAN120 or
default-gateway test residue present.

Not retained: final post-change running/startup comparisons for hq-d2, hq-r1 and
hq-r2.

The close-out record reports no failure-test interface shutdowns or temporary
addressing left in the forwarding design. Management-only changes, including
SSH access controls, management host routes and the hq-r1 Gi0/5 external
management connection, are outside the public HQ design configs and were
not treated as failure-test residue.

Result
------
PASS. The forwarding and redundancy state returned to baseline and temporary
failure-test configuration was removed. The remaining hq-a1 logging change and
the three uncaptured final running/startup comparisons are recorded above.

---

[← Previous](final-restoration-evidence.md) · [↑ Phase 10 Index](../README.md) · [Test evidence](final-restoration-evidence.md) · [Next →](10.14-config-excerpts.md)
