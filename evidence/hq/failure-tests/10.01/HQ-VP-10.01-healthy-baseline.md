[Portfolio](../../../../README.md) / [Evidence Map](../../README.md) / [Phase 10](../README.md) / [10.01](README.md) / Test report

# HQ-VP-10.01 — Healthy Baseline

Phase 10 — Failure and Resilience Testing

**Result: PASS**

**Original test plan:** [10.01 — Healthy baseline](../../../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1001-healthy-baseline)\
**Evidence:** [hq-a1 baseline CLI](10.01-hq-a1-baseline-cli.md)\
**Evidence commit:** [a8624b1](https://github.com/ddduddden/multi-site-cml-lab/commit/a8624b176298e3b0132daedf082c2aae0c704ebd)

## Test objective

Verify that the HQ network is operating in its intended healthy state before introducing faults, establishing a baseline for the Phase 10 failure and recovery tests.

## Healthy baseline

**Retained CLI — hq-a1**

- Po10 and Po20 operational, with both members bundled.
- STP root ports matching the design.
- VLAN199 management at 10.10.99.4/26, with gateway 10.10.99.1.
- HSRP virtual IP address (VIP) 10.10.99.1: 5/5 replies.

**Observed during the session — CLI not retained**

- Po30 operational with all four members bundled.
- No STP inconsistent ports.
- HSRP Active roles matching the design: hq-d1 for VLANs 112, 130, 152 and 170; hq-d2 for VLANs 120, 140, 160 and 199.
- Five FULL OSPF adjacencies on each Layer 3 device.
- hq-r1 Loopback0 (10.255.10.129): 5/5 replies.

The hq-r2 Loopback0 baseline ping was also performed, but its result was not retained.

## Result

**PASS.** The baseline checks confirmed the intended HQ operating state before Phase 10 failure testing. This was a healthy-state verification, not a failure or recovery test.

---

[◀ Test evidence](README.md) · [Baseline CLI ▶](10.01-hq-a1-baseline-cli.md)
