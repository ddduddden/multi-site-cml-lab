<h1 align="center">Multi-Site CML Home Lab</h1>

<p align="center"><strong>Network Design · Implementation · Verification · Failure Testing · Troubleshooting</strong></p>

<table align="center">
  <tr>
    <td align="center" width="128">
      <a href="https://www.credly.com/badges/877c5523-1160-4fca-9dfb-0efba8a15a60/public_url"><img src="https://images.credly.com/images/683783d8-eaac-4c37-a14d-11bd8a36321d/twitter_thumb_201604_ccna_600.png" alt="Official Cisco CCNA badge" width="112"></a>
    </td>
    <td align="center">
      <strong>Dominic Dudden</strong><br>
      <strong>Cisco Certified Network Associate (CCNA)</strong><br>
      <a href="https://www.credly.com/badges/877c5523-1160-4fca-9dfb-0efba8a15a60/public_url">Verify certification on Credly</a>
    </td>
  </tr>
</table>


<a href="diagrams/README.md#high-level-topology">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="diagrams/hq-campus-area10-topology-dark.svg">
    <img src="diagrams/hq-campus-area10-topology.svg" alt="HQ Campus — OSPF Area 10 high-level topology. Click to explore both diagrams.">
  </picture>
</a>

[View the topology full size and explore the detailed VLAN diagram](diagrams/README.md#high-level-topology)

## Project Approach

I'm developing this as a practical network engineering portfolio, following a structured engineering process rather than treating each configuration as an isolated exercise.

Each phase is supported by implementation records, verification results and retained evidence. Git and GitHub provide version control and traceability, allowing the network's development, configuration changes and engineering decisions to be followed and reviewed through the relevant commits.

**Design → Implement → Verify → Failure Test → Troubleshoot → Document**

## Explore the HQ Project

The documentation follows the HQ network from its original design through implementation, verification, failure testing and final acceptance. Each stage links to the supporting engineering records and evidence.

<table align="center">
<tbody><tr>
<td colspan="2" align="center">
<h3>Explore the HQ Project</h3>
<sub><b>FOUR ROUTES &nbsp;·&nbsp; ONE ENGINEERING STORY</b></sub>
<br><br>
<code>Design</code> → <code>Implementation</code> → <code>Verification</code> → <code>Failure Testing</code>
<br>
</td>
</tr></tbody>
<tbody><tr>
<td width="50%" valign="top">
<br>
🟩 &nbsp;<b>01</b> &nbsp;·&nbsp; 2 MINUTES
<br><br>
<b>The HQ overview</b>
<br>
The network design and technologies<br>at a glance.
<br><br><br>
<a href="#hq-campus-overview"><img src="https://img.shields.io/badge/START%20HERE%20%E2%86%97-238636?style=flat-square" alt="START HERE ↗"></a>
<br><br>
</td>
<td width="50%" valign="top">
<br>
🟪 &nbsp;<b>02</b> &nbsp;·&nbsp; 5 MINUTES
<br><br>
<b>Behind the design</b>
<br>
The engineering decisions behind HQ V1,<br>from the initial design to future expansion.
<br><br>
<a href="docs/hq-behind-the-design.md"><img src="https://img.shields.io/badge/FOLLOW%20THE%20THINKING%20%E2%86%97-8250df?style=flat-square" alt="FOLLOW THE THINKING ↗"></a>
<br><br>
</td>
</tr></tbody>
<tbody><tr>
<td width="50%" valign="top">
<br>
🟧 &nbsp;<b>03</b> &nbsp;·&nbsp; 10 MINUTES
<br><br>
<b>Follow the evidence</b>
<br>
From test planning and verification<br>through failure testing to the<br>results and what they revealed.
<br><br>
<a href="evidence/hq/README.md"><img src="https://img.shields.io/badge/INVESTIGATE%20%E2%86%97-bf6700?style=flat-square" alt="INVESTIGATE ↗"></a>
<br><br>
</td>
<td width="50%" valign="top">
<br>
🟦 &nbsp;<b>04</b> &nbsp;·&nbsp; INTERACTIVE
<br><br>
<b>Explore the network</b>
<br>
Explore the topology, routed paths<br>and selected failure scenarios.
<br><br><br>
<a href="https://dominicdudden.co.uk"><img src="https://img.shields.io/badge/EXPLORE%20THE%20INTERACTIVE%20PORTFOLIO%20%E2%86%97-0969da?style=flat-square" alt="EXPLORE THE INTERACTIVE PORTFOLIO ↗"></a>
<br><br>
</td>
</tr></tbody>
<tbody><tr>
<td colspan="2" align="center">
<br>
<b>Complete engineering documentation</b>
<br>
<sub>Design &nbsp;·&nbsp; Build Log &nbsp;·&nbsp; Verification &nbsp;·&nbsp; Evidence &nbsp;·&nbsp; Troubleshooting</sub>
<br><br>
<a href="#engineering-documents">↓ Browse the full document index below ↓</a>
<br><br>
</td>
</tr></tbody>
</table>

### Engineering Documents

| Document | What you'll find |
|---|---|
| [HQ Campus Design](docs/hq-campus-design.md) | Network architecture, addressing, routing design and engineering decisions |
| [Behind the Design — The Thinking Behind HQ V1](docs/hq-behind-the-design.md) | Five-minute narrative explaining the decisions and original multi-site planning |
| [HQ Implementation](docs/implementation/hq/README.md) | Phased implementation, progress and navigation to engineering records |
| [Build Log](docs/implementation/hq/build-log.md) | Configuration milestones, implementation notes and Git commit history |
| [Verification Plan](docs/implementation/hq/verification-plan.md) | Test procedures, results and supporting evidence |
| [HQ Evidence Map](evidence/hq/README.md) | Evidence for every phase, with links back to the verification records |
| [Failure Testing](evidence/hq/failure-tests/README.md) | Phase 10 test reports, observations and supporting evidence |
| [Engineering Review](docs/implementation/hq/phase-10-engineering-review.md) | Investigations, unexpected findings and design limitations |
| [Troubleshooting](docs/implementation/hq/troubleshooting.md) | Technical problems, investigations and corrective actions |
| [Final Acceptance](docs/implementation/hq/phase-11-final-acceptance.md) | Operational verification and final engineering close-out |

## HQ Campus Overview

🟩 **2-MINUTE ROUTE · HQ OVERVIEW**

The HQ campus forms the foundation of a planned multi-site enterprise network, built around a five-device, two-tier collapsed-core topology consisting of two edge routers (`hq-r1`, `hq-r2`), two Multilayer Distribution Switches (`hq-d1`, `hq-d2`) and one access switch (`hq-a1`). HQ operates in OSPF Area 10, with its routing and addressing architecture designed from the outset to support a future Branch Campus in Area 20, connected through an Area 0 backbone.

Built in Cisco Modeling Labs using VMware Workstation on Windows 11, HQ operates within the CML Free five-node limit. The wider home lab includes a second CML-capable computer, physical network infrastructure and Raspberry Pis planned for supporting services. Both CML hosts will eventually support separate campuses connected through the home network.

[View the lab environment and hardware](docs/environment.md)

### Network Design and Technologies

| Area | Implementation |
|---|---|
| Campus switching | VLAN segmentation, 802.1Q trunking, LACP EtherChannels and Rapid PVST+ |
| IP addressing & subnet design | Hierarchical, site-based VLSM addressing, with a consistent VLAN-to-subnet convention, capacity-based allocations and a planned inter-area summarisation strategy |
| First-hop redundancy | HSRP with preferred Active/Standby distribution roles and spanning-tree alignment |
| OSPF routing & path engineering | Four-path ECMP, deliberate OSPF cost design, preferred forwarding paths and higher-cost alternate routes for failure conditions |
| Network management | Dedicated management addressing, SSH access restrictions and retained configuration records |
| Resilience & fault testing | Controlled link, EtherChannel and device failures, including traffic verification, recovery testing and investigation of unexpected behaviour |

The addressing hierarchy reserves `10.10.0.0/16` for HQ, `10.20.0.0/16` for Branch and `10.255.0.0/16` for infrastructure. Inter-area summarisation is planned for the future backbone, while individual `/32` loopbacks are used as OSPF router IDs and will remain advertised separately.

LACP provides redundancy within Layer 2 EtherChannels, while OSPF uses independent routed interfaces and deliberate cost engineering to control Layer 3 path selection.

I developed HQ through eleven documented phases, progressing from VLANs and campus switching to gateway redundancy, OSPF routing, ECMP and deliberate cost engineering. Each stage has supporting verification records, with Phase 10 bringing the separate technologies together for controlled resilience testing.

The tests demonstrated working alternative routes and access paths, while also exposing limitations in the inter-distribution connection, HSRP upstream tracking and Layer 2 isolation behaviour. The resulting findings are retained alongside the original evidence. Phase 11 configuration and operational checks are documented, with final acceptance still under review.

## Implementation Progress

The HQ campus is organised into eleven documented phases, progressing from the initial platform configuration through routing, resilience testing and final acceptance.

| Phases | Scope | Status |
|---|---|---|
| 01–04 | Platform baseline, VLANs, EtherChannel and Rapid PVST+ | **Verified** |
| 05–07 | SVIs, HSRP, routed infrastructure and OSPF Area 10 | **Verified** |
| 08–09 | ECMP and OSPF cost engineering | **Verified** |
| 10 | Failure and resilience testing | **Completed with findings** |
| 11 | Final acceptance and close-out | **In progress** |

Phase 11 includes the final sanitised CML export and device configurations. During subsequent boot testing, `hq-a1` required a manual management SVI reset before operational checks succeeded. The cause remains unresolved, and final acceptance is still under review.

Engineering records: [Build Log](docs/implementation/hq/build-log.md) · [Verification Plan](docs/implementation/hq/verification-plan.md) · [Phase 11 Final Acceptance](docs/implementation/hq/phase-11-final-acceptance.md)

## Failure Testing and Engineering Findings

With the HQ network built and verified, Phase 10 put the redundancy design to the test. I deliberately introduced routed-link, EtherChannel and device failures to see how traffic was affected, which alternative paths were used and whether the network recovered as intended.

Some of the most valuable results came from the tests that didn't behave as expected.

During one test, I fully isolated `hq-d2` at Layer 2 while leaving its routed uplinks operational. Its VLAN interfaces remained up in IOSvL2, rather than going down as normally expected on Cisco Catalyst switches. OSPF continued advertising the affected subnet, and `hq-r2` selected `hq-d2` for return traffic despite there being no working Layer 2 path back to the source.

The interfaces and routing information appeared healthy, but traffic was still failing. Working out why meant examining the routing and forwarding decisions rather than relying on protocol status alone.

Other tests demonstrated where the redundancy design worked as intended and where its limitations became apparent, including successful alternate routing, unexpected EtherChannel behaviour and `hq-d2` remaining HSRP Active after losing its upstream routes because tracking had not been configured.

Not every test passed, and some results remain inconclusive, so I've retained the original test criteria, troubleshooting records and supporting evidence for review. The testing also highlighted where the design worked as intended, what still needs investigating and the improvements I'd consider for the next revision.

Explore: [Failure Test Results](evidence/hq/failure-tests/README.md) · [Engineering Review](docs/implementation/hq/phase-10-engineering-review.md)

[![Choose Another Route ↗](https://img.shields.io/badge/CHOOSE%20ANOTHER%20ROUTE%20%E2%86%97-C2185B?style=flat-square)](#explore-the-hq-project)

## Repository Guide

The repository separates design documents, implementation records, verification evidence and configuration milestones so each stage of the project can be reviewed independently.

| Location | Contents |
|---|---|
| [`docs/`](docs/README.md) | Network design, environment and planning documents |
| [`docs/implementation/hq/`](docs/implementation/hq/README.md) | Build, verification, troubleshooting and engineering records |
| [`evidence/hq/`](evidence/hq/README.md) | Retained CLI output, test records and supporting evidence |
| [`configs/hq/`](configs/hq/README.md) | Sanitised device configurations |
| [`diagrams/`](diagrams/README.md) | HQ network topology |
| [`lab/cml-lab-exports/`](lab/cml-lab-exports/README.md) | Sanitised CML restoration milestones and export guidance |

## Future Development

With the HQ campus established, the next stages will introduce supporting network services before expanding into a multi-site environment.

### Next — Monitoring, DNS and Branch Campus

Deploy LibreNMS, Grafana, Prometheus and Loki on the Raspberry Pi 5, alongside SNMP, syslog and NTP. Introduce redundant Pi-hole DNS using Keepalived/VRRP, with the Raspberry Pi 3B+ as primary and the Pi 5 as backup. Synchronisation, failover and recovery will be tested.

Build the Branch Campus in OSPF Area 20 and connect it to HQ through the planned Area 0 backbone.

### Later — Connectivity, Security and Automation

Develop GRE and GRE/IPsec connectivity with dual-tunnel resilience testing, followed by documented ACL and security policies. Introduce Python, Ansible and Cisco APIs for configuration management and repeatable network verification.
