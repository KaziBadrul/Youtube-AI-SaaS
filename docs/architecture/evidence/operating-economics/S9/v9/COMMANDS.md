# V9 reproduction

All commands run from repository root. This is an isolated local spike, not application deployment. Preserve old result directories before rerunning; do not overwrite historical receipts. Dependencies/network were allowed only during disposable image build. Resource tests use `--network none`, no published ports and source mounts read-only.

## Build/runtime provenance

`Dockerfile`: `spikes/operating-economics/v9/Dockerfile`. Cached base digest: `python@sha256:392307d22300de8b5986851a12d9176dfc0fc073e65bf6523ebd7dcbeb23564e`. Recorded test image digest: `sha256:a0cca2ec982aaf614cd3a1c24f6baa7b70f8447f88f3699bb56497cf05117a50`. Exact manifests/layers in `image-inspect.json`; OS/pip versions in each environment receipt; build/download log in `image-build.log`.

```sh
docker build --platform linux/amd64 --pull=false -t s9-v9-local:bookworm spikes/operating-economics/v9
```

A future build from live Debian/PyPI may change transitive packages; recorded image identity/package freeze is authoritative for this run. No claim of byte-identical future network builds. Starting the installed Docker Desktop required GUI/tool approval. No daemon/VM CPU/RAM settings were changed.

## Inputs

Mount repo root at `/repo:ro`, derived evidence profile at `/out`, `/private/tmp/s6-render-fonts:/fonts:ro` and `/private/tmp/s9-v9-model:/model:ro`. Existing local Whisper snapshot files were dereferenced/copied into that model directory, not fetched; `local-model-receipt.json` has original source paths/bytes/hashes. Recreate only from those existing local files if necessary; do not invoke model loaders/downloads as a preparation shortcut.

Original scene images/audio/caption overlays come from S6 `fixtures/project-600/manifest.json`, read-only. ASR audio is existing S5 Call4. Backup sensitivity uses legacy images and existing S6 five-minute narration/export, not provider generation. Model weights/font binaries are not included in committed evidence.

## Profiles

Example one-CPU command, replacing mount paths with the actual repository/evidence directory:

```sh
docker run --pull never --platform linux/amd64 --network none \
  --cpus 1 --memory 2000000000 --memory-swap 2000000000 --pids-limit 256 \
  -e EXPECTED_MEMORY_BYTES=2000000000 -e 'EXPECTED_CPU_MAX=100000 100000' \
  -v '/Users/kazibadrul/Python Codes/YoutubeAISaaSFinal:/repo:ro' \
  -v '/Users/kazibadrul/Python Codes/YoutubeAISaaSFinal/docs/architecture/evidence/operating-economics/S9/v9/NEW-PROFILE:/out' \
  -v '/private/tmp/s9-v9-model:/model:ro' \
  -v '/private/tmp/s6-render-fonts:/fonts:ro' \
  s9-v9-local:bookworm python /repo/spikes/operating-economics/v9/controller.py
```

For two CPUs/4GB use `--cpus 2 --memory 4000000000 --memory-swap 4000000000`, `EXPECTED_MEMORY_BYTES=4000000000`, `EXPECTED_CPU_MAX=200000 100000`, separate output directory. Original `1cpu-2gb` used the archived pre-repair code; the current controller/phase include documented receipt/timestamp fixes. Do not overwrite the original failure to pretend it was a current-code run.

Serialized confirmation substitutes `serial_controller.py`: no maintenance overlap; reuses the first run's recorded scene clips, performs repaired mux/full validation while Django stays live, then ASR/cancellation. It is not a new complete encoding benchmark. `serial_phase.py` identifies reused-source receipts in its result.

`remux_check.py` preserves the unsuccessful explicit-duration candidate; `grid_remux.py` preserves the subsequently fully validated frame-grid repair. These refer to the original profile's derived clips. Use fresh output paths/mounts; their receipts/logs explain each historical attempt. Linux mux uses video-only `setts` with integer frame-grid PTS/DTS/duration; all original strict output thresholds stay in force.

Caption check uses `captions.py` under a separate small offline container and compares fresh output with existing S6 reference pixels using exact RGBA bytes.

## Aggregate verification only

```sh
python3 spikes/operating-economics/v9/summarize.py
```

This reads existing receipts, validates successes and failures, rejects stale overlap receipt, checks original model hashes and all pre-existing evidence, and rewrites only v9 RESULTS/invalidation-marker files. It does not rebuild containers, rerender, transcribe, rerun historical spikes or call APIs. 38 assertions verify the reported evidence; observed OOM and rejected video attempts remain failures.

Snapshot preservation: old S9 index is archived as `S9-index-before-v9.md`; other 2,034 historical files must match `preservation-before.json`. Test containers are stopped as confirmed by `container-final-states.txt`. A failing/stopped container's exit0 is not enough to claim application success: phase exits, OOM counters and full validated artifact receipts govern conclusions.
