# HQ Implementation

[Portfolio](../../../README.md) / [Documentation](../../README.md) / [Implementation Records](../README.md) / HQ Implementation

[HQ Evidence Map](../../../evidence/hq/README.md) — find the captures and reports for each phase.

> The HQ design document (`docs/hq-campus-design.md`) records architectural intent. This implementation area records what was actually configured, tested, observed, troubleshot, and accepted. A surprising result does not rewrite the design baseline. Any accepted difference is recorded as a design deviation first.

## Purpose

This directory is the working record for turning the HQ design into a verified as-built lab.

The five documents have distinct primary responsibilities, with deliberate cross-references between them:

| File | Primary responsibility |
|---|---|
| `README.md` | Dashboard, working rules, phase index, status rules, and reference-ID key |
| [`verification-plan.md`](verification-plan.md) | What we intend to prove and how each test will be verified |
| [`build-log.md`](build-log.md) | Chronological record of significant implementation steps |
| [`troubleshooting.md`](troubleshooting.md) | Meaningful diagnostic investigations |
| [`deviations.md`](deviations.md) | Accepted differences between design intent and as-built implementation |

Phase 10 has its own [Test Plan](phase-10-test-plan.md), [Testing Methodology](phase-10-testing-methodology.md), [Engineering Review](phase-10-engineering-review.md), and [test reports and evidence](../../../evidence/hq/failure-tests/README.md).

## Reference ID key

The reference IDs below are a project-specific indexing convention created for this lab. They are not a Cisco or industry-standard reference system.

The parts of each reference ID decode as follows:

| Code | Meaning |
|---|---|
| `HQ` | Headquarters site |
| `VP` | Verification Plan |
| `TS` | Troubleshooting |
| `DEV` | Design Deviation |
| `XX` | Phase number |
| `YY` | Test number within that phase |
| `NNN` | Sequential record number |

Examples:

| Pattern | Meaning | Example |
|---|---|---|
| `HQ-VP-XX.YY` | HQ verification test — phase `XX`, test `YY` | `HQ-VP-03.04` |
| `HQ-TS-NNN` | HQ troubleshooting record | `HQ-TS-001` |
| `HQ-DEV-NNN` | HQ accepted design deviation | `HQ-DEV-001` |

```text
HQ-VP-03.04
│  │  │  └─ Test 04
│  │  └──── Phase 03
│  └─────── Verification Plan
└────────── Headquarters
```

IDs are permanent once assigned. They are never renumbered or reused.

Typical relationship:

```text
HQ-VP-08.01
    ↓
HQ-TS-003        only if meaningful diagnosis is required
    ↓
HQ-DEV-001       only if an implementation difference is accepted
```

A failed verification test does **not** automatically create a troubleshooting record, and a troubleshooting record does **not** automatically create a deviation.

## Phase index

The phase numbers are a project-specific indexing convention. They are not a Cisco or industry-standard phase model.

| Phase | Scope | Objective |
|---:|---|---|
| 01 | [Platform baseline](build-log.md#phase-01--hq-platform-baseline) | Confirm the actual CML nodes, images, interfaces, and platform assumptions before configuration |
| 02 | [Layer 2 / VLAN baseline](build-log.md#phase-02--layer-2--vlan-baseline) | Establish the VLAN database, access-port assignments, and parking-VLAN policy |
| 03 | [LACP EtherChannel](build-log.md#phase-03--lacp-etherchannel) | Build and verify Po10, Po20, and Po30, including trunking and member-link behaviour |
| 04 | [Rapid PVST+](build-log.md#phase-04--rapid-pvst) | Verify root placement, port state, and spanning-tree failure behaviour |
| 05 | [SVIs and HSRP](build-log.md#phase-05--svis-and-hsrp) | Verify SVI addressing, HSRP roles, preemption, and gateway failover |
| 06 | [Routed `/31` underlay](build-log.md#phase-06--routed-31-underlay) | Build and verify the ten routed point-to-point links before dynamic routing |
| 07 | [Loopbacks and OSPF Area 10](build-log.md#phase-07--loopbacks-and-ospf-area-10) | Add stable loopback identities and verify the Area 10 routing domain |
| 08 | [ECMP](build-log.md#phase-08--ecmp) | Prove the intended equal-cost routes are actually installed and usable |
| 09 | [OSPF cost engineering](build-log.md#phase-09--ospf-cost-engineering) | Prove preferred and higher-cost alternate path selection behaves as designed |
| 10 | [Failure testing](build-log.md#phase-10--failure-and-resilience-testing) | Exercise defined device, interface, Port-Channel, and routing failures and recovery |
| 11 | [Final acceptance](build-log.md#phase-11--final-configuration-milestone) | Confirm the evidence required to describe HQ as verified as-built |

Phases 01–09 are detailed in `verification-plan.md`. Phases 06 and 07 were built and verified in one combined build window, and Phases 08 and 09 were verified in one combined test window; each phase keeps separate test IDs, phase status, and build-log entries. Phase 10 has a standalone test plan and recorded outcomes; Phase 11 has a [narrative engineering close-out](phase-11-final-acceptance.md), with acceptance still in review.

## Working rules

- **Design intent stays separate from implementation reality.** `hq-campus-design.md` is not edited merely because the lab behaves unexpectedly.
- **The verification plan is a controlled living document.** Assigned test IDs remain permanent; expected results and exact verification commands may be refined when platform behaviour is confirmed.
- **The build log is chronological.** Significant implementation steps are recorded as the build progresses.
- **Troubleshooting records are selective.** A typo or immediately corrected command does not get a `HQ-TS-NNN` record. Meaningful diagnosis does.
- **Deviations are accepted differences.** A test may be marked `Deviated` only when an accepted `HQ-DEV-NNN` record exists for that test.
- **Evidence and configs are created only when real content exists.** No empty scaffolding.
- **Cross-references are explicit.** Build-log, verification, troubleshooting, deviation, config, evidence, and Git references should point to one another where relevant.

## Test status values

Each verification test uses the `Status` field to record its result.

| Status | Meaning |
|---|---|
| `Not started` | The test has not been run yet. |
| `In progress` | The test or related investigation is currently underway. |
| `Verified` | The expected behaviour has been demonstrated and recorded. |
| `Blocked` | The test cannot currently be completed because an unresolved issue, dependency, or platform limitation is preventing progress. |
| `Deviated` | The implementation intentionally differs from the design and an accepted `HQ-DEV-NNN` record exists for the test. |

`Blocked` does not mean the test has permanently failed. It means progress is currently prevented until the blocking issue is resolved or an accepted deviation is recorded.

## Phase status roll-up

Phase status is derived mechanically from the test statuses in `verification-plan.md`.

Evaluate these rules from top to bottom; first match wins:

1. If **any** test is `Blocked` → phase is **Blocked**.
2. If **all** tests are `Not started` → phase is **Not started**.
3. If **all** tests are complete (`Verified` or `Deviated`) and at least one is `Deviated` → phase is **Deviated**.
4. If **all** tests are `Verified` → phase is **Verified**.
5. Otherwise → phase is **In progress**.

A phase does not show as `Deviated` just because one test in it has an accepted deviation — every test in the phase has to be resolved first.

| Phase | Scope | Status |
|---:|---|---|
| 01 | Platform baseline | **Verified** |
| 02 | Layer 2 / VLAN baseline | **Verified** |
| 03 | LACP EtherChannel | **Verified** |
| 04 | Rapid PVST+ | **Verified** |
| 05 | SVIs and HSRP | **Verified** |
| 06 | Routed `/31` underlay | **Verified** |
| 07 | Loopbacks and OSPF Area 10 | **Verified** |
| 08 | ECMP | **Verified** |
| 09 | OSPF cost engineering | **Verified** |
| 10 | Failure testing | **Completed** |
| 11 | [Final acceptance](phase-11-final-acceptance.md) | In progress |

Phase 10 uses PASS, FAIL and INCONCLUSIVE for individual test outcomes. **Completed** means the planned execution and final reconciliation have finished; it does not mean every test passed. See the [Phase 10 results](../../../evidence/hq/failure-tests/README.md).

## Evidence folders

Evidence folders are created only when genuine artifacts exist.

| Phase | Folder |
|---:|---|
| 01 | [evidence/hq/platform-baseline/](../../../evidence/hq/platform-baseline/README.md) |
| 02 | [evidence/hq/layer2-vlan-baseline/](../../../evidence/hq/layer2-vlan-baseline/README.md) |
| 03 | [evidence/hq/etherchannel/](../../../evidence/hq/etherchannel/README.md) |
| 04 | [evidence/hq/spanning-tree/](../../../evidence/hq/spanning-tree/README.md) |
| 05 | [evidence/hq/hsrp/](../../../evidence/hq/hsrp/README.md) |
| 06 | [evidence/hq/layer3-underlay/](../../../evidence/hq/layer3-underlay/README.md) |
| 07–09 | [evidence/hq/ospf/](../../../evidence/hq/ospf/README.md) |
| 10 | [evidence/hq/failure-tests/](../../../evidence/hq/failure-tests/README.md) |
| 11 | [evidence/hq/final-acceptance/](../../../evidence/hq/final-acceptance/README.md) |

Smaller evidence sets can use files directly inside the relevant phase folder:

```text
evidence/hq/platform-baseline/HQ-VP-01.04-platform-capability-review.txt
```

Where one verification test produces several related artifacts, a dedicated verification-ID subfolder can be used:

```text
evidence/hq/etherchannel/HQ-VP-03.04-member-link-failure/
```

## Configs and Git traceability

[HQ Device Configurations](../../../configs/hq/README.md) · [CML Lab Exports](../../../lab/cml-lab-exports/README.md)

`configs/hq/` contains the readable sanitised as-built device configurations from the latest milestone (currently the sanitised Phase 11 milestone):

```text
configs/hq/
├── hq-r1-running-config.txt
├── hq-r2-running-config.txt
├── hq-d1-running-config.txt
├── hq-d2-running-config.txt
└── hq-a1-running-config.txt
```

Relevant build-log and verification entries record the config filename and the Git commit hash representing the retained milestone state. Phases 01–05 predate `configs/hq/`, so their phase-level completion commits provide the historical Git traceability instead.

Per-device files in `configs/hq/` are the readable as-built configuration reference. Selected CML YAML files under `lab/cml-lab-exports/` are milestone lab-restoration artifacts; they complement the per-device configs and do not replace them.

## What counts as as-built

A feature is not treated as verified as-built merely because it appears in the design or because its commands were entered.

```text
Configured
    ↓
Verified
    ↓
Failure-tested where appropriate
    ↓
Evidence recorded
    ↓
Faults resolved or explicitly documented
    ↓
Accepted as-built
```

## Before committing an implementation record

Check that:

- Design intent remains in `hq-campus-design.md`.
- Implementation reality is recorded in this subtree.
- All assigned IDs are permanent and correctly cross-referenced.
- Each verification test uses the `Status` field to record its result.
- Meaningful faults use `HQ-TS-NNN`, not routine typing mistakes.
- `Deviated` is backed by an accepted `HQ-DEV-NNN`, and every test in the phase is resolved before the phase itself reads as `Deviated`.
- Phase 10 documentation links to the executed tests; Phase 11 links to its final operational captures and narrative engineering close-out. Acceptance is still pending.
- Config/evidence directories contain real content rather than placeholders.

---

[← HQ Campus Design](../../hq-campus-design.md) · [↑ Phase index](#phase-index) · [HQ Build Log →](build-log.md)
