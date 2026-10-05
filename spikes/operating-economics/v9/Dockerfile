FROM python:3.12-slim-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg libgomp1 && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir Django==5.2.17 gunicorn==23.0.0 numpy==2.2.6 Pillow==12.0.0 psutil==7.2.2 uharfbuzz==0.52.0 freetype-py==2.5.1 fonttools==4.61.1 cryptography==46.0.3 faster-whisper==1.2.1
RUN ffmpeg -version > /runtime-ffmpeg.txt && python -m pip freeze > /runtime-python.txt
ENV HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
WORKDIR /work
