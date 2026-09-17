# Source verification and integration boundary

The patch baseline, file hashes and upstream archive reference are in `SOURCE.json`.
The modified upstream files are GPL-2.0 OR BSD-3-Clause; this distribution selects GPL-2.0-only and preserves attribution in `NOTICE`.

Run this read-only source check against your extracted matching backports tree:

```sh
python3 verify_patch.py /path/to/backports-6.12.96
```

The verifier hashes the relevant input files, copies only those files into a temporary directory, checks patch application, then applies the patch there. It does not modify your source tree or install anything. For the teardown fix, the patched hashes are also compared against the recorded fixed sources.

A kernel version string alone is not sufficient for module compatibility. The local test used a custom 6.6.144 kernel, matching configuration, symbol exports and compatibility headers. This repository does not reproduce the entire private system build or distribute its binaries. Integrate the patch into an appropriately configured distribution/kernel build and validate ABI, dependencies and recovery before deployment. Do not force-load an incompatible module.

No firmware, kernel modules, device backups, raw logs, passwords, private keys or automatic installer are part of this publication.
