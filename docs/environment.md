# Lab Environment

## CML Server 1

- Platform: Cisco Modeling Labs
- Hypervisor: VMware Workstation
- Host OS: Windows 11
- Host CPU: Intel Core i5-9300H
- Host RAM: 16 GB
- Host storage: 512 GB NVMe SSD
- Host network adapter: 1 GbE
- Physical network link: 1 GbE
- CML VM RAM: 8.5 GB
- CML VM vCPUs: 4
- CML virtual disk: 100 GB
- VMware network mode: Bridged

## CML Server 2

- Platform: Cisco Modeling Labs
- Hypervisor: VMware Workstation
- Host OS: Windows 11
- Host CPU: AMD Ryzen 9 5900X
- Host RAM: 32 GB
- Host storage: 1 TB NVMe SSD
- Host network adapter: 5 GbE
- Physical network link: 2.5 GbE

## Automation Server

- Platform: Raspberry Pi 5
- Host OS: Raspberry Pi OS (64-bit), based on Debian GNU/Linux 13 (trixie)
- Architecture: aarch64
- RAM: 8 GB
- Primary storage: 240 GB NVMe SSD
- Additional storage: 2 TB SSD
- Physical network link: 1 GbE
- Planned roles: Network automation, Ansible control node, Python automation, SNMP trap receiver, and NAS services

## Management Connectivity

CML Server 1 is reachable from other devices on the home LAN through its bridged VMware network interface.

The CML Server 1 management IP address is assigned using DHCP with a reservation on the local router.
