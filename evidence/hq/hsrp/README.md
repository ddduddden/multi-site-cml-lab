# Phase 05 — SVIs and HSRP

[Portfolio](../../../README.md) / [Evidence Map](../README.md) / Phase 05 — SVIs and HSRP

The table links each verification record to its retained captures and the checks recorded in the verification plan.

| Test | Check | Recorded status | Verification plan |
|---|---|---|---|
| [HQ-VP-05.01](#hq-vp-0501) | SVI Addressing and Layer 3 Baseline | Verified | [Test record](../../../docs/implementation/hq/verification-plan.md#svi-addressing-and-layer-3-baseline--hq-vp-0501) |
| [HQ-VP-05.02](#hq-vp-0502) | HSRP Configuration and Normal Operating State | Verified | [Test record](../../../docs/implementation/hq/verification-plan.md#hsrp-configuration-and-normal-operating-state--hq-vp-0502) |
| [HQ-VP-05.03](#hq-vp-0503) | HSRP/STP Alignment and Gateway Reachability | Verified | [Test record](../../../docs/implementation/hq/verification-plan.md#hsrpstp-alignment-and-gateway-reachability--hq-vp-0503) |
| [HQ-VP-05.04](#hq-vp-0504) | HSRP Gateway Failover | Verified | [Test record](../../../docs/implementation/hq/verification-plan.md#hsrp-gateway-failover--hq-vp-0504) |
| [HQ-VP-05.05](#hq-vp-0505) | HSRP Preemption and Preferred-State Restoration | Verified | [Test record](../../../docs/implementation/hq/verification-plan.md#hsrp-preemption-and-preferred-state-restoration--hq-vp-0505) |

Open a test below to find its device captures. The raw files are kept unchanged. Use your browser’s Back button to return here after viewing a TXT or PNG file.

## HQ-VP-05.01

SVI Addressing and Layer 3 Baseline

| Capture | File |
|---|---|
| hq-d1 — SVI addressing | [View capture](HQ-VP-05.01-hq-d1-svi-addressing.txt) |
| hq-d2 — SVI addressing | [View capture](HQ-VP-05.01-hq-d2-svi-addressing.txt) |
| hq-a1 — management SVI | [View capture](HQ-VP-05.01-hq-a1-management-svi.txt) |

[Verification record](../../../docs/implementation/hq/verification-plan.md#svi-addressing-and-layer-3-baseline--hq-vp-0501) · [↑ Test index](#phase-05--svis-and-hsrp)

## HQ-VP-05.02

HSRP Configuration and Normal Operating State

| Capture | File |
|---|---|
| hq-d1 — HSRP normal state | [View capture](HQ-VP-05.02-hq-d1-hsrp-normal-state.txt) |
| hq-d2 — HSRP normal state | [View capture](HQ-VP-05.02-hq-d2-hsrp-normal-state.txt) |

[Verification record](../../../docs/implementation/hq/verification-plan.md#hsrp-configuration-and-normal-operating-state--hq-vp-0502) · [↑ Test index](#phase-05--svis-and-hsrp)

## HQ-VP-05.03

HSRP/STP Alignment and Gateway Reachability

| Capture | File |
|---|---|
| hq-a1 — gateway reachability | [View capture](HQ-VP-05.03-hq-a1-gateway-reachability.txt) |
| hq-d1 — HSRP normal state | [View capture](HQ-VP-05.02-hq-d1-hsrp-normal-state.txt) |
| hq-d2 — HSRP normal state | [View capture](HQ-VP-05.02-hq-d2-hsrp-normal-state.txt) |
| hq-a1 — spanning tree state | [View capture](../spanning-tree/HQ-VP-04.01-hq-a1-spanning-tree-state.txt) |

[Verification record](../../../docs/implementation/hq/verification-plan.md#hsrpstp-alignment-and-gateway-reachability--hq-vp-0503) · [↑ Test index](#phase-05--svis-and-hsrp)

## HQ-VP-05.04

HSRP Gateway Failover

| Capture | File |
|---|---|
| hsrp failover vlan112 | [View capture](HQ-VP-05.04-hsrp-failover-vlan112.txt) |
| hsrp failover vlan199 | [View capture](HQ-VP-05.04-hsrp-failover-vlan199.txt) |

[Verification record](../../../docs/implementation/hq/verification-plan.md#hsrp-gateway-failover--hq-vp-0504) · [↑ Test index](#phase-05--svis-and-hsrp)

## HQ-VP-05.05

HSRP Preemption and Preferred-State Restoration

| Capture | File |
|---|---|
| hsrp preemption recovery vlan112 | [View capture](HQ-VP-05.05-hsrp-preemption-recovery-vlan112.txt) |
| hsrp preemption recovery vlan199 | [View capture](HQ-VP-05.05-hsrp-preemption-recovery-vlan199.txt) |
| hq-a1 — final STP alignment | [View capture](HQ-VP-05.05-hq-a1-final-stp-alignment.txt) |
| hq-a1 — management SVI | [View capture](HQ-VP-05.01-hq-a1-management-svi.txt) |

[Verification record](../../../docs/implementation/hq/verification-plan.md#hsrp-preemption-and-preferred-state-restoration--hq-vp-0505) · [↑ Test index](#phase-05--svis-and-hsrp)

---

[◀ Phase 04](../spanning-tree/README.md) · [↑ Evidence Map](../README.md) · [Phase 06 ▶](../layer3-underlay/README.md)
