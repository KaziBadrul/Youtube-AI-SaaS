# V11 reproduction and recorded commands

Native ARM64 Lima2.2.1/VZ Ubuntu24.04.5 guest/runtime from V10 reused locally. No cloud or provider calls/downloads. V10 host evidence remains immutable. VM disk under `/private/tmp/s9-v10-lima`; the VM name remains `s9-v10` but this run's actual inspection/config prove 2CPUs/4GiB. Saved its original configuration as `vm-config-before.yaml`; set only cpus2/memory4GiB while stopped. No primary Docker/settings/host dependency changes. Root commands affect only the disposable VM.

```sh
LIMA_HOME=/private/tmp/s9-v10-lima /private/tmp/s9-v10-tools/bin/limactl start --tty=false s9-v10
LIMA_HOME=/private/tmp/s9-v10-lima /private/tmp/s9-v10-tools/bin/limactl copy spikes/operating-economics/v11/controller.py s9-v10:/tmp/v11-controller.py
LIMA_HOME=/private/tmp/s9-v10-lima /private/tmp/s9-v10-tools/bin/limactl copy spikes/operating-economics/v11/phase.py s9-v10:/tmp/v11-phase.py
LIMA_HOME=/private/tmp/s9-v10-lima /private/tmp/s9-v10-tools/bin/limactl copy spikes/operating-economics/v11/web.py s9-v10:/tmp/v11-web.py
LIMA_HOME=/private/tmp/s9-v10-lima /private/tmp/s9-v10-tools/bin/limactl copy spikes/operating-economics/v11/run.sh s9-v10:/tmp/v11-run.sh
LIMA_HOME=/private/tmp/s9-v10-lima /private/tmp/s9-v10-tools/bin/limactl shell s9-v10 sudo sh /tmp/v11-run.sh
```

`run.sh` preserves prior `/out` and `/work` as `/out-v10-preserved` and `/work-v10-preserved`, then starts fresh output/script directories. It cannot rerun into existing preserved output. Inputs/model/fonts remain inside ext4 with no host mount. Runtime package versions and settings unchanged; only controller's hardware assertions differ from V10. Phase/web scripts are byte-identical to V10. No repeated model/media generation or cached clip benchmark: all112scene clips encode freshly.

Results are collected after measurement through an isolated guest tar into `v11/guest`; source501hashes checked against V10's unchanged input receipt; actual VM allocation and final process inspection retained. Stop the experiment VM after collection. Verify from repository root:

```sh
python3 spikes/operating-economics/v11/verify.py
```

Classification is an explicit evidence assessment pinned to the measured summary SHA256, not a new universal percentage policy or automatically inferred from process exit0. Full media/probe/kernel/source checks must support a safe classification. Overall S9 is separately NOT_YET_PASS. Historical preservation checks tolerate only the archived live S9 index update.

**Owner stop rule:** this is the last host-sizing experiment unless it fails. Successful local qualification closes this sizing line; limitations/actual-provider tuning are documented rather than automatically triggering more sizing experiments. No next S9 work executes here.
