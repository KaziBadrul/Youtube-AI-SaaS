# S9 v9 local Linux resource envelope

Authorized by owner: test 1 vCPU/2 GB and 2 vCPU/4 GB using local Linux. Use strict decimal 2,000,000,000 / 4,000,000,000 bytes; report GiB conversion separately. This is more restrictive than 2/4 GiB application cgroups, but does not account for the external VM kernel.

Existing Docker Desktop 29.8.1, cached Python 3.12 Debian Bookworm image is linux/amd64 on Apple Silicon. Emulated Linux timings do not predict native VM latency. Shared Linux VM kernel/daemon RAM sits outside container accounting: this is application-cgroup validation, not a full VPS RAM certification.

Before installation: disposable image needs FFmpeg/libgomp from Debian repositories and Django/Gunicorn/numpy/Pillow/psutil/HarfBuzz/FreeType/fontTools/cryptography/faster-whisper from PyPI. Candidate pinned versions in Dockerfile; approximate download footprint a few hundred MB. Actual package versions/build image identity and sizes captured afterward. No production environment change, paid API, paid benchmark or model download. Existing Whisper base weights (~145 MB), local fonts, S5 WAVs and S6 fixture images/audio/caption PNGs reused read-only.

Run both envelopes serially, container network disabled, no external ports, read-only repository/model/font mounts, disposable output only. CPU quotas 100000/100000 and 200000/100000; memory limits 2000000000 and 4000000000, memory-swap equal memory (no swap). Record kernel/cgroup proof before trusting labels. No OOM protection bypass. Capture memory.current/peak/events, cpu.stat/throttling, process RSS, disk use, versions and wall time.

Within each envelope: minimal private Django/Gunicorn + SQLite WAL status boundary remains running while controlled worker renders existing representative ten-minute S6 fixture, transcribes existing Call4 with local cached Whisper base, and constructs/encrypts/restores a full-sized five-project backup sensitivity. Test sequential phases plus explicit backup/render-overlap stress, bounded cancellation/process cessation, output probe/decode, SQLite integrity, previous export/source preservation. Failures remain failures; do not silently weaken fixture/runtime to pass. Sample web requests during phases, without inventing product latency acceptance thresholds.

No token/preflight experiment. No production implementation, TASKS.md, deployment, accounts, purchase, hosting selection, final credits or allowances. S9 overall may remain NOT_YET_PASS even if these local tests succeed.
