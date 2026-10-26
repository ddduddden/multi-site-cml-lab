# Network Plan

[Portfolio](../README.md) / [Documentation](README.md) / Network Plan

## Overview

This project uses two Cisco Modeling Labs servers connected through the physical home network to create a multi-site networking and automation lab.

A Raspberry Pi 5 will provide an external Linux platform for network automation, monitoring and management services. A separate Raspberry Pi 3B+ is planned as the primary Pi-hole DNS server, with a second instance on the Pi 5 for redundancy.

## Physical Infrastructure

### Main Router

- Device: ASUS RT-BE92U
- Role: Primary home router and ISP gateway
- Provides wired connectivity to CML Server 1
- Provides wired connectivity to the Raspberry Pi 5
- Provides the primary side of the 6 GHz AiMesh wireless backhaul

### AiMesh Node

- Device: ASUS TUF Gaming BE9400
- Role: AiMesh node
- 2.4 GHz radio: Disabled
- Backhaul: 6 GHz wireless connection to the primary router
- Wired LAN ports: Up to 2.5 GbE
- Provides wired connectivity to CML Server 2

### CML Server 1

- Host type: Laptop
- CPU: Intel Core i5-9300H
- RAM: 16 GB
- Host OS: Windows 11
- Hypervisor: VMware Workstation
- Physical connection: 1 GbE to the primary router
- CML management IP address: 192.168.50.172

### CML Server 2

- CPU: AMD Ryzen 9 5900X
- RAM: 32 GB
- GPU: AMD Radeon RX 6700 XT
- Storage: 1 TB NVMe SSD
- Host OS: Windows 11
- Hypervisor: VMware Workstation
- Network adapter capability: 5 GbE
- Physical connection: 2.5 GbE to the AiMesh node

### Automation and Monitoring Server

- Device: Raspberry Pi 5
- RAM: 8 GB
- Storage: 240 GB NVMe
- Additional storage: 2 TB SSD
- Physical connection: 1 GbE to the primary router
- Planned roles:
  - Network automation using Python and Ansible
  - SNMP monitoring and alerting with LibreNMS
  - System metrics using Prometheus and Grafana
  - Centralised syslog collection
  - NTP services using Chrony
  - Secondary Pi-hole DNS with Keepalived
  - NAS services

### DNS Server

- Device: Raspberry Pi 3B+
- Role: Planned primary Pi-hole DNS server
- Physical connection: Ethernet to the home LAN (planned)
- Planned roles:
  - DNS filtering and local DNS records
  - Keepalived active peer for the shared DNS address

## Physical Connectivity

The physical network path between the two CML servers is:

CML Server 1 → ASUS RT-BE92U → 6 GHz AiMesh backhaul → ASUS TUF Gaming BE9400 → CML Server 2

CML Server 1 connects to the primary router using 1 GbE.

CML Server 2 has a 5 GbE-capable network adapter, but the physical link to the AiMesh node is limited to 2.5 GbE by the AiMesh node's 2.5 GbE LAN ports.

The Raspberry Pi 5 connects directly to the primary router using 1 GbE. The Raspberry Pi 3B+ is planned to connect by Ethernet to the same home LAN.

## CML Inter-Site Connectivity

Each CML environment will use a routed edge device connected to a CML External Connector operating in System Bridge mode.

The physical home LAN will initially provide the transit network between the two CML sites.

Layer 2 switching domains will remain inside CML. Routed interfaces will be used at the boundary between each simulated network and the physical home network.

## Redundant DNS

The planned DNS design uses Pi-hole on both Raspberry Pis, with the Pi 3B+ as primary and the Pi 5 as backup. Keepalived/VRRP will provide a shared virtual IP address for DNS clients, allowing the backup to take over if the primary becomes unavailable.

DNS service-health checking and configuration synchronisation will be configured separately from VRRP. Both devices will require individual management addresses and connectivity within the same Layer 2 network.

Testing will cover primary failure, backup takeover, DNS resolution, filtering consistency and restoration. The home router will advertise the virtual DNS address once the design has been verified.

## Network Monitoring and Time Synchronisation

The Raspberry Pi 5 will provide centralised monitoring for both CML environments. This will address a limitation identified during HQ Phase 10, where device logs, IP SLA counters and manual CLI captures were used to investigate failures without continuous external monitoring or synchronised timestamps.

### Planned Monitoring Services

| Service | Planned purpose |
|---|---|
| **LibreNMS** | SNMP polling, interface utilisation, link status, device availability and alerting |
| **Prometheus** | Collection and retention of system performance metrics |
| **Grafana** | Dashboards for network and Linux system health |
| **Node Exporter** | CPU, memory, storage and network metrics from Linux hosts |
| **Syslog-ng** | Central collection of network device syslog messages |
| **Chrony** | Common NTP time source for the lab |
| **Grafana Loki** | Later log searching and correlation alongside Grafana dashboards |

LibreNMS will be the primary network monitoring platform, using read-only SNMPv3 where supported. Initial monitoring will focus on interface state, utilisation, errors, device reachability and alerts. Prometheus and Grafana will provide a separate view of the Pi 5's Linux system metrics, with additional exporters introduced where useful.

Centralised syslog will retain events such as OSPF adjacency changes, interface failures, EtherChannel transitions and HSRP state changes. Chrony will provide a common time reference so events captured across devices can be compared more reliably.

The monitoring tools will be introduced in stages, with resource usage and data retention checked against the Pi 5's 8 GB RAM and available storage. Loki will be considered after the core monitoring services are operational.

### Monitoring Verification

Once deployed, controlled link and device failures will be repeated to check that the monitoring platform records the expected events.

Verification will include:

- SNMP polling and interface-status changes
- Device availability and alert generation
- Syslog reception and timestamp consistency
- Dashboard visibility during failures and recovery
- Retention and retrieval of historical monitoring data

This will provide better evidence of network behaviour during future resilience testing. Polling intervals and log timestamps will still need to be considered when interpreting convergence and outage measurements.

## Management

CML servers and supporting infrastructure will use predictable management IP addresses through DHCP reservations. Each Raspberry Pi will retain its own management address, separate from the shared DNS virtual IP, allowing both hosts to be accessed independently during maintenance or failover.

The Raspberry Pi 5 will provide a central management and automation platform capable of reaching both CML environments. Secure SSH access, restricted management permissions and documented credentials handling will form part of the management setup.

Configuration backups, service changes and recovery procedures will be maintained alongside the existing Git-based engineering records, providing a traceable history as the lab expands.

## Future Development

HQ V1 already implements VLANs, inter-VLAN routing, OSPF and tested alternative paths. The next expansion will introduce supporting network services and extend the lab into a multi-site environment.

Planned development includes:

- Redundant Pi-hole DNS with VRRP and synchronisation
- LibreNMS monitoring, syslog collection and NTP
- Prometheus and Grafana dashboards, with further log analysis where practical
- Branch Campus and inter-site backbone routing
- Python network automation, REST APIs and Ansible
- Continued Git-based configuration and documentation

---

[↑ Documentation](README.md) · [Lab Environment](environment.md) · [Network Plan](network-plan.md) · [Physical Topology](topology.md)
