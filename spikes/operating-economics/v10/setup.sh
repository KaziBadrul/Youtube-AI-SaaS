#!/bin/sh
set -eu
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-install-recommends ffmpeg python3-venv libgomp1
python3 -m venv /venv
/venv/bin/pip install --only-binary=:all: Django==5.2.17 gunicorn==23.0.0 numpy==2.2.6 Pillow==12.0.0 psutil==7.2.2 uharfbuzz==0.52.0 freetype-py==2.5.1 fonttools==4.61.1 cryptography==46.0.3 faster-whisper==1.2.1 ctranslate2==4.8.2
mkdir -p /out /work
# Scheduled package installation is memory-heavy maintenance too: paused only in this disposable VM.
systemctl stop apt-daily.timer apt-daily-upgrade.timer
swapoff -a
