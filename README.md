# Multi-Site CML Home Lab

A practical Cisco Modeling Labs project focused on enterprise networking, resilience, troubleshooting, and network automation.

The lab is developed as an evolving technical portfolio, with each stage designed, implemented, verified, failure-tested, and documented — rather than treated as an isolated configuration exercise.

![HQ Campus - OSPF Area 10](diagrams/hq-campus-area10-topology.svg)

## Project Goals

- Build a realistic multi-site Cisco network using enterprise routing and switching concepts.
- Apply structured IPv4 addressing, VLSM, `/31` point-to-point networks, and `/32` loopbacks.
- Design and test Layer 2 and Layer 3 redundancy.
- Develop practical troubleshooting and failure-testing skills.
- Gain hands-on experience with Linux, Git, Python, Ansible, and Cisco APIs.
- Introduce monitoring, logging, and network automation as the project develops.
- Maintain clear design rationale, implementation evidence, and verification results for use as a technical portfolio.

## Current Architecture

The first site is the **HQ Campus**, designed as a five-device, two-tier collapsed-core topology:

- 2 × Edge Routers
- 2 × Multilayer Distribution Switches
- 1 × Access Switch

HQ operates internally as **OSPF Area 10** and is designed to connect later to an **Area 0 inter-site backbone**.

A second **Branch Campus**, planned as **OSPF Area 20**, will be introduced in a later phase and connected through the Area 0 backbone as the multi-site design develops.

Current HQ design features include:

- VLAN segmentation with VLSM addressing
- HSRP first-hop gateway redundancy
- Rapid PVST+ with HSRP/STP role alignment
- Layer 2 LACP EtherChannel
- Independent routed `/31` Distribution-to-Edge interfaces
- Four-path OSPF ECMP
- Higher-cost cross-connected OSPF paths
- `/32` loopbacks for stable routing identities
- Dedicated native, parking, and management VLANs

The full HQ design is documented in:

[`docs/hq-campus-design.md`](docs/hq-campus-design.md)

## Current Status

The HQ campus has completed Phase 10 failure testing, following ECMP and OSPF cost-engineering verification.

Phases **01–09 are verified as-built**. Phase 08 proves that the intended four-route OSPF ECMP sets are installed and usable, while Phase 09 confirms the configured cost policy, higher-cost alternate routing, and restoration to the preferred state. Phases 08 and 09 were verification-only and introduced no new configuration milestone.

Phase 10 testing is complete, with individual outcomes recorded as PASS, FAIL or INCONCLUSIVE against the original criteria. The [Test Plan](docs/implementation/hq/phase-10-test-plan.md), [Testing Methodology](docs/implementation/hq/phase-10-testing-methodology.md), [Engineering Review](docs/implementation/hq/phase-10-engineering-review.md) and [test reports and evidence](evidence/hq/failure-tests/README.md) contain the full record.

The final HQ [CML configuration milestone](lab/cml-lab-exports/hq/hq-phase-11-final-acceptance-2026-10-15.yaml) was published in [`1ee631b`](https://github.com/ddduddden/multi-site-cml-lab/commit/1ee631be011985dac4a1c6a7f97de1ff95d22c1c). A later [boot recovery capture](evidence/hq/final-acceptance/HQ-Phase-11-Boot-Recovery-CLI.md) and [operational checks](evidence/hq/final-acceptance/HQ-Phase-11-Final-Boot-Verification.txt) were retained in [`39b68a7`](https://github.com/ddduddden/multi-site-cml-lab/commit/39b68a790a3b9ed0de55071fdf7f9b004d0638b2). The [Phase 11 engineering close-out](docs/implementation/hq/phase-11-final-acceptance.md) remains in review; the public export is sanitised, and successful runtime checks followed manual intervention on `hq-a1`.

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
| 11 | Final acceptance | In progress |

Completed verification now includes:

- VLAN database and access-port policy
- LACP EtherChannel formation and member-link recovery
- 802.1Q trunk state, native VLAN consistency, and allowed-VLAN policy
- Rapid PVST+ root placement and path-failure behaviour
- SVI addressing and management reachability
- HSRP Active/Standby ownership, gateway failover, and preferred-state restoration
- HSRP/STP role alignment across the distribution layer
- Ten routed `/31` Distribution-to-Edge links with direct peer reachability before OSPF
- Four `/32` loopback identities used as explicit OSPF router IDs
- Passive-by-default OSPF Area 10 participation with point-to-point routed links
- Five `FULL` OSPF neighbours per Layer 3 device across ten unique adjacencies
- Consistent Area 10 link-state databases and learned HQ routes
- End-to-end reachability from the access-switch management network to all four routing loopbacks
- Regression confirmation that EtherChannel, Rapid PVST+, HSRP, and VLAN 199 management state remained intact
- Four-route OSPF ECMP installation with test traffic using more than one installed path
- Controlled ECMP contraction and restoration
- Lab-observed four-path OSPF installation limit with a fifth equal-cost route available
- Cost-driven direct and cross-link route selection
- Higher-cost alternate routing during complete direct-set loss
- Preferred-route restoration and final routing-state regression check

Current verification focus:

- HQ Phase 11 final acceptance and as-built close-out

Detailed implementation status and verification records are maintained in:

[`docs/implementation/hq/README.md`](docs/implementation/hq/README.md)

## Lab Environment

The project uses:

- Cisco Modeling Labs
- VMware Workstation
- Windows 11 hosts
- Raspberry Pi 5 for monitoring and future automation services
- Git and GitHub for version control and project documentation
- Physical home-network connectivity for later multi-host and multi-site integration

Environment details, including host specifications and lab setup, are documented in:

[`docs/environment.md`](docs/environment.md)

The wider lab is intended to span two CML hosts, allowing the project to grow beyond the five-device HQ topology.

## Repository Structure

```text
multi-site-cml-lab/
├── README.md
├── .gitignore
│
├── configs/
│   └── hq/
│       ├── hq-r1-running-config.txt
│       ├── hq-r2-running-config.txt
│       ├── hq-d1-running-config.txt
│       ├── hq-d2-running-config.txt
│       └── hq-a1-running-config.txt
│
├── diagrams/
│   └── hq-campus-area10-topology.svg
│
├── docs/
│   ├── environment.md
│   ├── hq-campus-design.md
│   ├── network-plan.md
│   ├── topology.md
│   └── implementation/
│       └── hq/
│           ├── README.md
│           ├── build-log.md
│           ├── verification-plan.md
│           ├── troubleshooting.md
│           ├── deviations.md
│           ├── phase-10-test-plan.md
│           ├── phase-10-testing-methodology.md
│           ├── phase-10-engineering-review.md
│           └── phase-11-final-acceptance.md
│
├── evidence/
│   └── hq/
│       ├── platform-baseline/
│       ├── layer2-vlan-baseline/
│       ├── etherchannel/
│       ├── spanning-tree/
│       ├── hsrp/
│       ├── layer3-underlay/
│       ├── ospf/
│       └── failure-tests/
│
└── lab/
    └── cml-lab-exports/
        ├── README.md
        └── hq/
            ├── hq-phase-01-platform-baseline-2026-09-20.yaml
            ├── hq-phase-05-svi-hsrp-2026-09-29.yaml
            └── hq-phase-07-ospf-area10-2026-09-30.yaml
```

Repository areas have distinct roles:

- `docs/` — design intent, environment information, implementation records, verification plans, troubleshooting, and accepted deviations.
- `evidence/` — retained CLI and test evidence supporting verification results.
- `configs/` — readable sanitised per-device running configurations at meaningful as-built milestones.
- `diagrams/` — topology and architecture visuals.
- `lab/cml-lab-exports/` — sanitised milestone CML exports used for restoration and version tracking.

## Roadmap

The project will continue through the following major stages:

1. Complete HQ final acceptance and as-built validation, including review of Phase 10 findings.
2. Introduce monitoring, SNMP, syslog, metrics, and NTP using the Raspberry Pi.
3. Build the Branch Campus as OSPF Area 20.
4. Connect HQ and Branch through the Area 0 inter-site backbone.
5. Add GRE inter-site connectivity.
6. Evolve GRE to GRE over IPsec and later dual-tunnel resilience.
7. Add Layer 2 security and ACL policy.
8. Introduce Python, Ansible, APIs, and network automation against the completed lab.

## Project Approach

The project follows an evidence-based workflow:

**Design → Implement → Verify → Break → Troubleshoot → Document → Automate**

The aim is not only to demonstrate that a configuration works, but to show why the design was chosen, how it behaves during failure, and how its operation can be verified.
