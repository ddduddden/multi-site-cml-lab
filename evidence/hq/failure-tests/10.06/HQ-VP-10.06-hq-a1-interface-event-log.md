[Portfolio](../../../../README.md) / [Evidence Map](../../README.md) / [Phase 10](../README.md) / [10.06](README.md) / Capture / record

# hq-a1 interface event log

<details>
<summary><strong>Original retained CLI / source capture</strong></summary>

```text
HQ-VP-10.06 — Access Uplink Failure
===================================

Hq-a1 interface event log
-------------------------

Capture date: 03-10-2026

Source: Filtered hq-a1 logging buffer captured during final recovery,
03-10-2026.

Editorial note:
Only Phase 10.06 event-window messages are retained. Earlier Phase 10.05 log
entries are omitted. The log messages themselves are verbatim.

hq-a1#show logging | include SPANTREE|EC-|LINEPROTO|LINK-
*Oct  3 19:02:21.396: %LINK-5-CHANGED: Interface GigabitEthernet1/0, changed state to administratively down
*Oct  3 19:02:21.425: %LINK-5-CHANGED: Interface GigabitEthernet1/1, changed state to administratively down
*Oct  3 19:02:21.452: %LINK-5-CHANGED: Interface Port-channel20, changed state to administratively down
*Oct  3 19:02:22.396: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet1/0, changed state to down
*Oct  3 19:02:22.427: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet1/1, changed state to down
*Oct  3 19:02:22.452: %LINEPROTO-5-UPDOWN: Line protocol on Interface Port-channel20, changed state to down
*Oct  3 19:16:01.985: %LINK-3-UPDOWN: Interface Port-channel20, changed state to down
*Oct  3 19:16:01.986: %LINK-3-UPDOWN: Interface GigabitEthernet1/0, changed state to up
*Oct  3 19:16:02.139: %LINK-3-UPDOWN: Interface GigabitEthernet1/1, changed state to up
*Oct  3 19:16:02.988: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet1/0, changed state to up
*Oct  3 19:16:03.141: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet1/1, changed state to up
*Oct  3 19:16:07.623: %LINK-3-UPDOWN: Interface Port-channel20, changed state to up
*Oct  3 19:16:08.624: %LINEPROTO-5-UPDOWN: Line protocol on Interface Port-channel20, changed state to up
*Oct  3 19:35:17.843: %LINK-5-CHANGED: Interface GigabitEthernet0/0, changed state to administratively down
*Oct  3 19:35:17.872: %LINK-5-CHANGED: Interface GigabitEthernet0/1, changed state to administratively down
*Oct  3 19:35:17.899: %LINK-5-CHANGED: Interface Port-channel10, changed state to administratively down
*Oct  3 19:35:18.844: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet0/0, changed state to down
*Oct  3 19:35:18.873: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet0/1, changed state to down
*Oct  3 19:35:18.900: %LINEPROTO-5-UPDOWN: Line protocol on Interface Port-channel10, changed state to down
*Oct  3 19:39:07.106: %LINK-3-UPDOWN: Interface Port-channel10, changed state to down
*Oct  3 19:39:07.107: %LINK-3-UPDOWN: Interface GigabitEthernet0/0, changed state to up
*Oct  3 19:39:07.260: %LINK-3-UPDOWN: Interface GigabitEthernet0/1, changed state to up
*Oct  3 19:39:08.106: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet0/0, changed state to up
*Oct  3 19:39:08.260: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet0/1, changed state to up
*Oct  3 19:39:14.328: %LINK-3-UPDOWN: Interface Port-channel10, changed state to up
*Oct  3 19:39:15.328: %LINEPROTO-5-UPDOWN: Line protocol on Interface Port-channel10, changed state to up
*Oct  3 19:43:50.703: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan112, changed state to up
*Oct  3 19:43:51.785: %LINK-3-UPDOWN: Interface Vlan112, changed state to up
*Oct  3 19:47:53.998: %LINK-5-CHANGED: Interface GigabitEthernet0/0, changed state to administratively down
*Oct  3 19:47:54.027: %LINK-5-CHANGED: Interface GigabitEthernet0/1, changed state to administratively down
*Oct  3 19:47:54.053: %LINK-5-CHANGED: Interface Port-channel10, changed state to administratively down
*Oct  3 19:47:54.999: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet0/0, changed state to down
*Oct  3 19:47:55.027: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet0/1, changed state to down
*Oct  3 19:47:55.053: %LINEPROTO-5-UPDOWN: Line protocol on Interface Port-channel10, changed state to down
*Oct  3 19:54:05.252: %LINK-3-UPDOWN: Interface Port-channel10, changed state to down
*Oct  3 19:54:05.253: %LINK-3-UPDOWN: Interface GigabitEthernet0/0, changed state to up
*Oct  3 19:54:05.403: %LINK-3-UPDOWN: Interface GigabitEthernet0/1, changed state to up
*Oct  3 19:54:06.254: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet0/0, changed state to up
*Oct  3 19:54:06.406: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet0/1, changed state to up
*Oct  3 19:54:12.136: %LINK-3-UPDOWN: Interface Port-channel10, changed state to up
*Oct  3 19:54:13.135: %LINEPROTO-5-UPDOWN: Line protocol on Interface Port-channel10, changed state to up
```

</details>

---

[◀ Previous record](HQ-VP-10.06-final-recovery-restored-baseline.md) · [↑ Test evidence](README.md) · [Next record ▶](10.06-source-po10-mode-a.md)
