# HQ Campus Design

## Overview

The HQ campus uses a five-device, two-tier collapsed-core design consisting of a redundant distribution/core layer, a Layer 2 access layer, and dual WAN edge routers. The internal HQ routing domain operates as OSPF Area 10, with the edge routers providing redundant paths toward the Area 0 inter-site backbone and supporting future GRE/IPsec connectivity.

The topology is designed to provide resilient Layer 2 and Layer 3 connectivity using LACP EtherChannels, HSRP, Rapid PVST+, and OSPF. Redundant physical and logical paths are included so that link, gateway, routing, and device failures can be deliberately introduced, observed, verified, and documented.

The campus design also incorporates network segmentation and is designed to support additional security controls. Dedicated VLANs separate user, voice, server, IoT, guest, wireless, and management traffic, with a dedicated native VLAN for trunking and a separate parking VLAN for unused access ports. Additional controls such as port security, DHCP snooping, Dynamic ARP Inspection, and access-control policies will be introduced during later implementation phases.

Campus services and routed infrastructure use separate hierarchical address spaces. The addressing plan uses VLSM, /31 point-to-point networks, and /32 loopbacks to provide a structure that is readable, scalable, and suitable for route summarisation.

The HQ campus forms the first stage of a larger multi-site lab. Later phases will extend the design with monitoring, real services, secure inter-site connectivity, failure testing, and network automation.

## High-Level Topology

![HQ Campus - OSPF Area 10](../diagrams/hq-campus-area10-topology.png)
