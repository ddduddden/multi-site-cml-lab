# Network Plan

## Overview

This project uses two Cisco Modeling Labs servers connected through the physical home network to create a multi-site networking and automation lab.

A Raspberry Pi 5 will provide an external Linux platform for network automation, monitoring, and management services.

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

### Automation Server

- Device: Raspberry Pi 5
- RAM: 8 GB
- Storage: 240 GB NVMe
- Additional storage: 2 TB SSD
- Physical connection: 1 GbE to the primary router
- Planned roles:
  - Network automation
  - Ansible control node
  - Python automation
  - SNMP trap receiver
  - NAS services

## Physical Connectivity

The physical network path between the two CML servers is:

CML Server 1 -> ASUS RT-BE92U -> 6 GHz AiMesh backhaul -> ASUS TUF Gaming BE9400 -> CML Server 2

CML Server 1 connects to the primary router using 1 GbE.

CML Server 2 has a 5 GbE-capable network adapter, but the physical link to the AiMesh node is limited to 2.5 GbE by the AiMesh node's 2.5 GbE LAN ports.

The Raspberry Pi 5 connects directly to the primary router using 1 GbE.

## CML Inter-Site Connectivity

Each CML environment will use a routed edge device connected to a CML External Connector operating in System Bridge mode.

The physical home LAN will initially provide the transit network between the two CML sites.

Layer 2 switching domains will remain inside CML. Routed interfaces will be used at the boundary between each simulated network and the physical home network.

## Management

CML servers and infrastructure services will use predictable management IP addresses provided through DHCP reservations.

The Raspberry Pi 5 will provide an external management and automation platform capable of reaching both CML environments.

## Future Development

The lab will progressively introduce:

- Multi-site routing
- Dynamic routing protocols
- VLANs and inter-VLAN routing
- Network monitoring
- SNMP
- Python network automation
- REST APIs
- Ansible
- Git-based configuration and documentation

