#!/bin/sh
set -eu
# Inputs and outputs live on the guest's ext4 root, not a host shared filesystem.
tar -xf /tmp/inputs.tar -C /
mv /tmp/controller.py /tmp/phase.py /tmp/web.py /work/
# The transfer archive is disposable duplication, not retained project storage.
rm /tmp/inputs.tar
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
exec /venv/bin/python /work/controller.py
