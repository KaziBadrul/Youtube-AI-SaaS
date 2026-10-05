# Disposable local architecture feasibility witnesses

These experiments test S1, S2, S3, S7 and S8 only. They are **not** an Alpha application, production schema, provider adapter or frontend foundation. Do not copy the simplified fixture schema or restoration signatures into production. No network/provider client is imported by the tests. Runtime packages are free and installed into a dedicated temporary environment.

## Reproduce

Run from the repository root with Python 3.12 and Node available:

```sh
python3 -m venv /tmp/alpha-feasibility-venv
/tmp/alpha-feasibility-venv/bin/python -m pip install -r spikes/local-feasibility/requirements.lock
/tmp/alpha-feasibility-venv/bin/python spikes/local-feasibility/s1.py
/tmp/alpha-feasibility-venv/bin/python spikes/local-feasibility/s2.py
/tmp/alpha-feasibility-venv/bin/python spikes/local-feasibility/s3.py
/tmp/alpha-feasibility-venv/bin/python spikes/local-feasibility/s7.py
/tmp/alpha-feasibility-venv/bin/python spikes/local-feasibility/s8.py
```

Execute sequentially; stop dependent gates on failure. `s3.py` must be allowed to inspect processes, signal **its own** newly created process groups and read boot/start identity. The macOS sandbox denied `ps`; the recorded successful S3 run used explicitly approved local process-inspection access. Tests use temporary directories, valid tiny silent WAVs and synthetic export bytes, not real generated media or FFmpeg. Fake provider receipts live in a separate SQLite file and intentionally do not deduplicate submissions; tests detect accidental extra calls.

S1's legacy compatibility check requires the canonical local script named in `docs/PIPELINE_INVESTIGATION.md`: `/Users/kazibadrul/Python Codes/YoutubeAI/python-scripts/make_video.py`. It AST-extracts only `seconds_to_srt`; it never imports that module or its import-time provider clients. On another workstation, provision the canonical source or adjust this explicitly documented fixture path; absence is a failed compatibility check, not a skipped PASS. Django test clients execute the real session/CSRF/HTTP boundary; Node executes the enhancement against a deterministic DOM/fetch witness. No browser-device or pixel acceptance is claimed.

Machine-readable results and source/plan hashes are written to `docs/architecture/evidence/local-feasibility/S*.json`. Rerunning replaces the final result; initial failed runs are separately retained. See the evidence index for claims, predeclared criteria, observations and limits. All run databases, key material and media are temporary; no backup keys or credentials are committed.

## Files

- `core.py`: short-transaction invariant witness, reservations, fencing, selection and durability helpers.
- `django_boundary.py`, `templates/boundary.html`, `static/boundary.js`, `static/boundary.test.js`, `s1worker.py`: isolated S1 HTTP/enhancement/fake-worker boundary.
- `fixtures.py`: local fake artifact installation.
- `publication.py`: crash checkpoints, non-idempotent fake provider, reusable bytes and atomic metadata/financial registration.
- `supervision.py`: real child-group survival, identity checking and confirmed stop.
- `backup.py`: encrypted local snapshot, independently durable non-content deletion authority, purge and reconciliation witnesses.
- `s1.py`, `s2.py`, `s3.py`, `s7.py`, `s8.py`: gate experiments and invariant assertions.
- `evidence.py`: reproducible JSON evidence writer.
- `requirements.lock`: exact free-package versions used; no frontend framework, provider SDK or alignment stack.

Local backup destination is not an off-host service. Full provider capability, narration quality, rendering and hosting/cost feasibility remain S4/S5/S6/S9. Passing these witnesses is not independent application acceptance or invitation authorization.
