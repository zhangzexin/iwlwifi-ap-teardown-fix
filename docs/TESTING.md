# Local test record — 2026-09-18

Environment: user-identified AX411 / driver-reported AX211, PCI 8086:7e40, subsystem 8086:40b0; iStoreOS 24.10.8; custom Linux 6.6.144; backports 6.12.96; firmware 89.d2579d43.0 ma-b0-gf4-a0-89.ucode. Single WPA2 AP.

Before the fix, internal multicast station removal reproduced assert 0x251B with both the original iwlwifi 2.4GHz AP and the experimental 5GHz configuration. Returning to the original iwlmvm reproduced it again. The previously suspected flush failure was not the cause in the captured sequence: flush and queue_remove both returned zero. Key metadata (without key material) showed the GTK still referred to the station when removal failed.

| Fixed scenario | Count | Result |
|---|---:|---|
| Diagnostic fixed module: 2.4GHz idle/load stop | 2 | Passed |
| Diagnostic fixed module: 5GHz stop under downlink traffic | 1 | Passed |
| Final module: 20/40/80MHz transitions | 3 | Passed |
| Final module: repeated VHT80 stop/start, including no connected client | 3 | Passed |
| Final module via startup script: stop/restore under upload traffic | 1 | Passed |

No new 0x251B or Microcode SW error occurred in those ten fixed scenarios. An intentional original-module teardown during rollback reproduced the old failure and is excluded from fixed results. Rollback and reactivation succeeded.

The final completed Mac Wi-Fi tests measured upload 684.50Mbps and download 585.79Mbps, 20 seconds each, with an 866.7Mbps NSS2/80MHz link. These are local observations, not guaranteed performance. Traffic-interruption tests intentionally terminated iperf connections and are not counted as completed throughput tests.

The reported module matched 9 kernel and 12 driver structure layout checks; its undefined-symbol set matched the original module. The final module contained no temporary AP_TD/AP_KEY diagnostics. Its SHA256 was `9090f28dc5e56f30ae220c3612b5e36e6df33e5bdcfc248b6ded8cf791dd9303`; the binary is not distributed here.

Not tested: full machine reboot after this fix, long-duration reliability, other platforms/firmware, multi-AP/MLO, all cipher suites, or all command-submission failure paths. The startup script's actual reload path was tested. Public evidence is this sanitized summary and source provenance; raw system logs and private build artifacts are excluded.
