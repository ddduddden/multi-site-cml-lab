# Behind the Design — The Thinking Behind HQ V1

🟪 **5-MINUTE ROUTE · BEHIND THE DESIGN**

I started the Multi-Site CML Lab with a larger network in mind. The intention was never to build an isolated HQ campus and decide what to do with it afterwards. I wanted to design the foundations of a multi-site network, implement them in manageable stages and leave room for the routing, connectivity and services I planned to introduce later.

My CCNA studies had given me a foundation in the individual technologies. This project was an opportunity to make my own design decisions, understand how those technologies fitted together and test whether the network behaved as I intended.

## Designing the foundations

The first challenge was Cisco Modeling Labs Free's five-node limit. I chose two multilayer distribution switches, two edge routers and one access switch in a collapsed-core arrangement. Combining the core and distribution functions on the two switches provided campus routing and, with HSRP, gateway redundancy without needing a third switching tier.

Keeping two edge routers was a deliberate choice for the wider network. HQ would operate in OSPF Area 10, with both routers intended to become Area Border Routers towards a future Area 0 backbone, while the Branch Campus would operate in Area 20. I also planned redundant inter-site connections from the beginning, initially using GRE and later GRE over IPsec, with separate tunnel paths and failover testing. The routers therefore had a longer-term purpose beyond the routing resilience I could investigate within HQ.

The compromise was a single access switch. Its uplinks are redundant, but it remains a single point of failure for connected endpoints. With five nodes available, I considered retaining the distribution and edge pairs more useful than adding a second access switch.

## Planning the addressing before the network grows

I reserved 10.10.0.0/16 for HQ, 10.20.0.0/16 for Branch and 10.255.0.0/16 for infrastructure and transit addressing. I wanted a recognisable hierarchy from the outset, rather than having to reorganise overlapping or inconsistent networks when the backbone was introduced.

Within HQ, I used VLSM addressing instead of giving every VLAN a /24. Corporate users and guests have /22 networks for their anticipated capacity and room to grow; other functions use /23, /25 or /26 prefixes according to their needs. I also kept a relationship between VLAN IDs and subnet addresses wherever the subnet boundaries allowed. VLAN 112, for example, uses 10.10.12.0/22, while VLAN 152 uses 10.10.52.0/22. The larger /22 networks are a conscious trade-off because they also create larger Layer 2 broadcast domains.

The ten point-to-point routed connections use /31 prefixes, saving addresses without complicating the link plan. Each Layer 3 device also has a /32 loopback. I wanted stable identities for OSPF and for practical tasks such as SSH access, monitoring and troubleshooting, without tying them to the state of a particular physical interface.

I also planned the OSPF summarisation before building Area 0. When the edge routers become ABRs, my intention is to summarise HQ user, service and management networks as 10.10.0.0/16 and advertise the routed transit block as 10.255.10.0/27. The loopback addresses will remain separate /32 routes so individual devices remain identifiable and reachable. That gives the backbone a simpler routing view while retaining the detailed VLSM networks inside Area 10.

The planned Branch Campus will follow the same approach, summarising its 10.20.0.0/16 user and service networks towards Area 0 while retaining individual prefixes within Area 20.

## Giving the switching technologies clear roles

I designed three Layer 2 LACP EtherChannels for the switched campus. Po10 connects the access switch to hq-d1, Po20 connects it independently to hq-d2, and Po30 provides the direct connection between the distribution pair. LACP gives each bundle resilience against individual member-link loss, while Rapid PVST+ controls the Layer 2 forwarding topology. Several members still make one logical Port-Channel, which is an important limit on what the redundancy can protect.

I split the preferred HSRP Active roles between the distribution switches and aligned the Rapid PVST+ root placement with those gateways. Each VLAN group therefore has a more direct forwarding path towards its intended gateway, reducing unnecessary traffic across Po30 during normal operation.

I also used a dedicated, non-default native VLAN, a separate parking VLAN for unused ports and a distinct management VLAN. Unused access ports are shut down. These choices are part of the switching and management security baseline, not a claim that VLAN separation alone is a complete security policy.

## Engineering the routed paths

I changed one important choice during the design. My original proposal used Layer 3 EtherChannels between the distribution and edge devices. The CML images had limitations around routed Port-Channels, and I wanted to investigate how OSPF handled independent routed paths. I therefore used four parallel /31 links between each preferred distribution–edge pair, allowing separate OSPF adjacencies and equal-cost next hops. LACP would remain responsible for Layer 2 member resilience, while OSPF would select between the independent routed paths.

I added diagonal routed links to the opposite edge routers and gave the direct and cross-connected interfaces deliberate OSPF costs of 10 and 100 respectively. I wanted predictable preferred paths without removing higher-cost alternatives. Because OSPF uses the total cost to a destination, the routing design had to consider complete paths, not just the numbers on individual interfaces.

I selected point-to-point OSPF network types, fixed router IDs and passive-by-default operation, allowing neighbour relationships only over the intended routed interfaces. The future Area 0 and VPN design will need to follow the same principle of controlled routing. In particular, reachability to GRE tunnel endpoints must come from the underlying transport network, independently of the routes carried inside the tunnels, avoiding recursive routing.

## Building a design I could verify

I divided HQ into phases so I could verify each part before depending on it in the next stage. VLANs and EtherChannels came before spanning tree and HSRP, then routed links, OSPF, ECMP and cost engineering. That made it easier to identify what a change had affected instead of troubleshooting the whole network at once.

I chose Git and GitHub for version control and traceability. Configuration milestones, CML exports, verification records and engineering decisions can be tied to a particular state of the project. Branches, commits and pull requests give me a reviewable change history, so I can revisit earlier configurations and explain why the network developed as it did.

I retained the detailed test evidence deliberately. The CLI captures and reports let someone follow what changed, which paths were selected and how I reached each conclusion. To make that material easier to explore, I also built interactive topology diagrams and guided walkthroughs of selected test runs. These show the network behaviour visually and link back to the original reports and captures in GitHub. The website provides an accessible way into the project; GitHub remains the source of truth.

The later resilience tests checked how those decisions worked together. Alternate OSPF paths were selected and preferred routes returned after restoration. [Complete Po30 loss](../evidence/hq/failure-tests/10.07/HQ-VP-10.07-po30-progressive-failure.md) showed that member-link redundancy did not provide a second logical inter-distribution connection; Root Guard protected the intended spanning-tree boundary but could not replace that missing path. [Layer 2 isolation](../evidence/hq/failure-tests/10.08/HQ-VP-10.08-d2-layer2-isolation.md) also showed why an apparently healthy HSRP and OSPF state did not guarantee a usable return path. Those findings inform the next design revision without changing the original intent retrospectively.

## Building towards the wider network

HQ V1 establishes the first routing area and the switching and gateway baseline for the next stages. I plan to extend it into a hybrid physical–virtual lab, with the Raspberry Pi 5 serving as the lab's NTP server alongside monitoring and centralised logging. The Raspberry Pi 5 and Pi 3B+ will also support redundant DNS, while Docker containers are planned to generate more realistic traffic for future verification. Using a common time source will help me match device events, logs and test results when investigating outages.

The planned Branch Campus and Area 0 backbone can then be introduced alongside redundant inter-site connectivity, building on the addressing and routing policies already defined. Wider security controls and automation will follow as the network develops.

What I value most about HQ V1 is the process of making those choices, documenting the compromises and testing the results. The finished configuration shows what I built; the design decisions and evidence explain why.

---

[↑ Portfolio](../README.md) · [HQ Campus Design](hq-campus-design.md) · [HQ Evidence Map](../evidence/hq/README.md)

[![Choose Another Route ↗](https://img.shields.io/badge/CHOOSE%20ANOTHER%20ROUTE%20%E2%86%97-C2185B?style=flat-square)](../README.md#explore-the-hq-project)
