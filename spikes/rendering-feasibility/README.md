# Disposable S6 rendering feasibility

This directory is isolated experiment code, not a production application foundation.
Evidence lives in `docs/architecture/evidence/rendering-feasibility/S6/`.
No providers or AI models are used. Fonts are outside the repository under
`/private/tmp/s6-render-fonts`, with source/license/hash/version in evidence.

Commands from repository root:

```sh
python3 spikes/rendering-feasibility/inspect_environment.py
python3 -m venv /private/tmp/s6-render-venv
/private/tmp/s6-render-venv/bin/python -m pip install --only-binary=:all: Pillow==12.0.0 numpy==2.2.6 psutil==7.0.0 fonttools==4.60.1 uharfbuzz==0.51.0 freetype-py==2.5.1
python3 spikes/rendering-feasibility/setup_fonts.py
/private/tmp/s6-render-venv/bin/python spikes/rendering-feasibility/s6.py languages
/private/tmp/s6-render-venv/bin/python spikes/rendering-feasibility/s6.py benchmark --duration 180
/private/tmp/s6-render-venv/bin/python spikes/rendering-feasibility/s6.py benchmark --duration 300
/private/tmp/alpha-feasibility-venv/bin/python spikes/rendering-feasibility/web_boundary.py
/private/tmp/s6-render-venv/bin/python spikes/rendering-feasibility/s6.py control
/private/tmp/s6-render-venv/bin/python spikes/rendering-feasibility/failures.py
/private/tmp/s6-render-venv/bin/python spikes/rendering-feasibility/real_narration_control.py
/private/tmp/s6-render-venv/bin/python spikes/rendering-feasibility/inspect_controls.py
/private/tmp/s6-render-venv/bin/python spikes/rendering-feasibility/inspect_captions.py
/private/tmp/s6-render-venv/bin/python spikes/rendering-feasibility/lifecycle.py test
/private/tmp/s6-render-venv/bin/python spikes/rendering-feasibility/final_evidence.py
```

The web witness reuses the existing S1 temporary Django 5.2.17 environment;
it launches the 600-second render separately and samples HTTP test-client
latency while it runs. It requires process-inspection permissions, as does
the lifecycle witness. Package/font setup requires explicit network access;
no production environment changes. Setup is not an instruction to download
AI models. Downloaded font hashes must match the retained provenance before
reproducing prior results.

Visual inspection of decoded multilingual and English frames must precede
marking shaping PASS in `multilingual-results.json`. Final aggregation refuses
pending shaping evidence. Read the S6 report for actual findings and limits.
Use a fresh isolated evidence copy for independent reproduction; commands
may regenerate fixtures/current result files. Historical first-run data and
all original S5 audio must remain preserved. All subprocesses use argv lists;
caption text is shaped into pixels rather than inserted into FFmpeg filters.
