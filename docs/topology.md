# Physical Network Topology

This diagram represents the current physical infrastructure supporting the multi-site Cisco Modeling Labs environment.

```text
                                              INTERNET
                                                 |
                                                 |
                                                ISP
                                                 |
                                            Fibre / FTTP
                                                 |
                                                 |
                                                ONT
                                                 |
                                             Ethernet WAN
                                                 |
                                                 |
                                          ASUS RT-BE92U
                                    Primary Router / Gateway
                    _____________________________|_____________________________
                   |                             |                             |
                   |                             |                             |
                 1 GbE                        1 GbE                    6 GHz Wi-Fi 7
                   |                             |                      IEEE 802.11be
                   |                             |                 AiMesh Wireless Backhaul
                   |                             |                             |
                   |                             |                             |
            CML SERVER 1                 RASPBERRY PI 5                ASUS TUF BE9400
            Laptop                       Automation Server              AiMesh Node
            Intel Core i5-9300H          8 GB RAM                             |
            16 GB RAM                    240 GB NVMe                          |
            Windows 11                   2 TB SSD                             | 2.5 GbE
            VMware Workstation           Network automation                   |
            Cisco Modeling Labs          Ansible / Python                     |
            Management IP:               SNMP trap receiver             CML SERVER 2
            192.168.50.172               NAS services                   Desktop
                                                                        AMD Ryzen 9 5900X
                                                                        32 GB RAM
                                                                        1 TB NVMe SSD
                                                                        Windows 11
                                                                        VMware Workstation
                                                                        Cisco Modeling Labs
                                                                        5 GbE-capable NIC

```

## Connectivity Notes

- The ISP connection is delivered using fibre-to-the-premises (FTTP).
- The fibre connection terminates at the ONT.
- The ONT connects to the ASUS RT-BE92U through the WAN interface.
- CML Server 1 connects directly to the primary router using 1 GbE.
- The Raspberry Pi 5 connects directly to the primary router using 1 GbE.
- The ASUS RT-BE92U and ASUS TUF Gaming BE9400 use a 6 GHz Wi-Fi 7 (IEEE 802.11be) AiMesh wireless backhaul.
- The 2.4 GHz radio on the AiMesh node is disabled.
- CML Server 2 connects to the AiMesh node using a 2.5 GbE link.
- CML Server 2 has a 5 GbE-capable network adapter, with the physical link limited by the AiMesh node's 2.5 GbE LAN interface.
