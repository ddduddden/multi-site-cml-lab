[Portfolio](../../../../README.md) / [Evidence Map](../../README.md) / [Phase 10](../README.md) / [10.14](README.md) / Test report

# HQ-VP-10.14 — Final Restoration

Phase 10 — Failure and Resilience Testing

**Result: PASS**

**Original test plan:** [10.14 — Final restoration and hygiene](../../../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1014-final-restoration-and-hygiene)\
**Evidence:** [Session record](10.14-session-record.md)\
**Original evidence commit:** [a8624b1](https://github.com/ddduddden/multi-site-cml-lab/commit/a8624b176298e3b0132daedf082c2aae0c704ebd)\
**Follow-up evidence (12 October 2026):** [Configuration reconciliation](10.14-config-excerpts.md#configuration-reconciliation--12-october-2026)

## Test objective

Confirm that failure testing left the HQ network in its intended operating state, with temporary configurations removed and the final device configurations reconciled.

## Final operational state

The checks on 6 October 2026 confirmed:

- Po10 and Po20 operational with both members bundled.
- Po30 operational with all four members bundled.
- No STP inconsistent ports.
- The intended STP root and HSRP Active/Standby roles restored.
- Five FULL OSPF adjacencies on each Layer 3 device.
- No remaining IP SLA test operations on hq-a1.

From hq-a1 on VLAN199 (10.10.99.4), the gateway and both edge-router loopbacks each responded to 5/5 pings.

## Final VLAN120 check

A temporary VLAN120 (VOICE) source, 10.10.20.4/23, was used for a final routed-VLAN connectivity check.

The gateway 10.10.20.1 and both edge-router loopbacks returned 5/5 replies. The gateway ping recorded min/avg/max 3/205/1009 ms, with no established cause for the higher response time.

A pre-assignment availability check for 10.10.20.4 was not retained.

The temporary VLAN120 configuration was initially entered on hq-d1 instead of hq-a1. This was corrected: hq-d1 Vlan120 was restored to 10.10.20.2/23, its intended HSRP Standby state was confirmed in the session record, and the incorrect default-gateway setting was removed.

The temporary VLAN120 configuration was removed from hq-a1 after testing.

## Configuration close-out

At the end of the 6 October 2026 session, hq-a1 had returned to:

- VLAN199 management address 10.10.99.4/26.
- Default gateway 10.10.99.1.
- No temporary test SVI or IP SLA operations.

The 6 October configuration checks identified an outstanding buffered-logging change on hq-a1. I restored the original settings and saved the configuration during the 12 October follow-up.

I also completed the remaining configuration checks across all five devices. The follow-up confirmed that:

- hq-a1 had its intended EtherChannel, STP and management state, with no remaining IP SLA operations.
- The running/startup comparisons showed no unexplained failure-test configuration differences.

The remaining VTY timeout differences were the known CML configuration-fetch artefact, shown in the [retained configuration comparisons](10.14-config-excerpts.md). Management-only SSH access controls, management host routes and the hq-r1 Gi0/5 external management connection were not treated as forwarding-test residue.

A fresh private CML export was retained after cleanup.

## Result

**PASS.** The 6 October session confirmed restored forwarding, redundancy and connectivity. The 12 October follow-up completed the configuration close-out.

I kept the 6 and 12 October checks separate so it's clear what was completed during each session.

---

[◀ Test evidence](README.md) · [Session record ▶](10.14-session-record.md) · [Configuration captures](10.14-config-excerpts.md) · [↑ Phase 10 Test Index](../README.md)
