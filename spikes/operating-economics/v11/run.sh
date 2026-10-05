#!/bin/sh
set -eu
# Reuse installed native guest stack and immutable existing inputs; preserve V10 outputs.
[ ! -e /out-v10-preserved ]
mv /out /out-v10-preserved
mv /work /work-v10-preserved
mkdir /out /work
mv /tmp/v11-controller.py /work/controller.py
mv /tmp/v11-phase.py /work/phase.py
mv /tmp/v11-web.py /work/web.py
systemctl stop apt-daily.timer apt-daily-upgrade.timer
swapoff -a
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
exec /venv/bin/python /work/controller.py
