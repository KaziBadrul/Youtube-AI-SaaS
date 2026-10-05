# V10 reproduction commands and scope

Run from repository root. VM/tool disks and archives are disposable local artifacts under `/private/tmp`; no production application or cloud provisioning. Root privileges below are **inside this disposable guest only**. macOS permission escalation was required for virtualization/sysctl/local SSH/network downloads, not for a provider request.

Official sources retrieved 2026-10-05:
- https://lima-vm.io/docs/installation/
- https://lima-vm.io/docs/config/vmtype/vz/
- https://lima-vm.io/docs/examples/
- https://api.github.com/repos/lima-vm/lima/releases/latest (one public release-metadata request, not AI/provider generation)
- https://github.com/lima-vm/lima/releases/download/v2.2.1/lima-2.2.1-Darwin-arm64.tar.gz
- https://cloud-images.ubuntu.com/releases/noble/release/SHA256SUMS
- https://cloud-images.ubuntu.com/releases/noble/release/ubuntu-24.04-server-cloudimg-arm64.img

Archive SHA256 checked against GitHub release digest; guest-image digest pinned from Ubuntu checksum record in `guest.yaml`. Exact effective config and launch/setup logs retained. Lima can cache the verified image under `~/Library/Caches/lima`, but does not alter existing Docker VM settings. No additional guest-agent archive or QEMU installation required.

```sh
mkdir -p /private/tmp/s9-v10-tools
tar -xzf /private/tmp/s9-v10-lima.tar.gz -C /private/tmp/s9-v10-tools
LIMA_HOME=/private/tmp/s9-v10-lima /private/tmp/s9-v10-tools/bin/limactl start --name=s9-v10 --tty=false spikes/operating-economics/v10/guest.yaml
# Initial sandbox attempt created the instance but could not inspect boot-session ID.
# The successful approved launch used the already-created instance:
LIMA_HOME=/private/tmp/s9-v10-lima /private/tmp/s9-v10-tools/bin/limactl start --tty=false s9-v10
LIMA_HOME=/private/tmp/s9-v10-lima /private/tmp/s9-v10-tools/bin/limactl copy /private/tmp/s9-v10-inputs.tar s9-v10:/tmp/inputs.tar
LIMA_HOME=/private/tmp/s9-v10-lima /private/tmp/s9-v10-tools/bin/limactl copy spikes/operating-economics/v10/setup.sh s9-v10:/tmp/setup.sh
LIMA_HOME=/private/tmp/s9-v10-lima /private/tmp/s9-v10-tools/bin/limactl shell s9-v10 sudo sh /tmp/setup.sh
LIMA_HOME=/private/tmp/s9-v10-lima /private/tmp/s9-v10-tools/bin/limactl copy spikes/operating-economics/v10/controller.py spikes/operating-economics/v10/phase.py spikes/operating-economics/v10/web.py s9-v10:/tmp/
LIMA_HOME=/private/tmp/s9-v10-lima /private/tmp/s9-v10-tools/bin/limactl copy spikes/operating-economics/v10/run.sh s9-v10:/tmp/run.sh
LIMA_HOME=/private/tmp/s9-v10-lima /private/tmp/s9-v10-tools/bin/limactl shell s9-v10 sudo sh /tmp/run.sh
python3 spikes/operating-economics/v10/verify.py
```

Reproduction must use a new evidence directory/VM/output root; never rerun a historical writer into existing successful evidence. `prepare.py` packages only listed media, S6 renderer/fonts metadata and existing local model/font files, no credentials or primary repository configuration. `phase.py` derives from unchanged V9 with only rendering/validation split into distinct phases; V9 packet-grid correction is retained. Original scene encoding is rerun from existing stills, not reused as a falsely fresh benchmark.

`run.sh` unpacks inputs onto guest ext4 and removes only its disposable transfer duplicate. The guest has no shared host mounts. No cache dropping, swap enablement, OS service removal, overcommit/OOM suppression or reduced media validation to force a pass. Scheduled apt maintenance timers are paused only in the guest to prevent unauthorized heavy-work overlap; normal system services remain active. Probe and telemetry overhead are inside the RAM/CPU measurement. SSH diagnostic commands may also consume measured guest resources; raw timings retained.

For a fresh bundle using the recorded preparation logic:

```sh
python3 spikes/operating-economics/v10/prepare.py --bundle /private/tmp/s9-v10-new-inputs.tar --receipt /private/tmp/s9-v10-new-inputs.json
```

After the measured run, `/out` was copied through a disposable guest tar archive into `v10/guest/`; 501 guest input hashes were compared against the original receipts. Final `ps` output and `limactl list --json` confirm no orphan media/web processes and actual VM allocation. `limactl stop s9-v10` stops only this experiment guest. VM disk/software cache remain reusable; no next resource test was started.
