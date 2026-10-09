[Phase 10](../README.md) / [10.06](access-uplink-failure-evidence.md)

[← Previous](HQ-VP-10.06-mode-b-po10-failure-state.md) · [↑ Phase 10 Index](../README.md) · [Test evidence](access-uplink-failure-evidence.md) · [Next →](10.06-source-final-recovery.md)

---

<details>
<summary><strong>Original retained CLI / source capture</strong></summary>

```text
HQ-VP-10.06 — Access Uplink Failure
===================================

Mode B VLAN112 traffic continuity during Po10 failure
-----------------------------------------------------

Capture date: 03-10-2026

Source: Device console capture pasted into the Phase 10 test session,
03-10-2026.

Editorial note:
Verbatim CLI supplied during the live test.

hq-a1#
hq-a1#

hq-a1#ping 10.10.12.1 source 10.10.12.4 repeat 5
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.10.12.1, timeout is 2 seconds:
Packet sent with a source address of 10.10.12.4 
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 7/7/9 ms

hq-a1#ping 10.255.10.129 source 10.10.12.4 repeat 20
Type escape sequence to abort.
Sending 20, 100-byte ICMP Echos to 10.255.10.129, timeout is 2 seconds:
Packet sent with a source address of 10.10.12.4 
!!!!!!!!!!!!!!!!!!!!
Success rate is 100 percent (20/20), round-trip min/avg/max = 8/10/13 ms

hq-a1#show ip sla statistics 101
IPSLAs Latest Operation Statistics

IPSLA operation id: 101
        Latest RTT: 9 milliseconds
Latest operation start time: 19:51:04 UTC Sat Oct 3 2026
Latest operation return code: OK
Number of successes: 302
Number of failures: 0
Operation time to live: Forever

hq-a1#show ip sla statistics 102
IPSLAs Latest Operation Statistics

IPSLA operation id: 102
        Latest RTT: 10 milliseconds
Latest operation start time: 19:51:14 UTC Sat Oct 3 2026
Latest operation return code: OK
Number of successes: 311
Number of failures: 0
Operation time to live: Forever

hq-a1#
```

</details>

---

[← Previous](HQ-VP-10.06-mode-b-po10-failure-state.md) · [↑ Phase 10 Index](../README.md) · [Test evidence](access-uplink-failure-evidence.md) · [Next →](10.06-source-final-recovery.md)
