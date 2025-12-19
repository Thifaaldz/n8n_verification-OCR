FROM n8nio/n8n:latest

USER root

# Install python3, pip, Tesseract OCR + data bahasa Inggris, dependencies
RUN apk update && apk add --no-cache \
    python3 \
    py3-pip \
    tesseract-ocr \
    tesseract-ocr-data-eng \
    bash \
    build-base \
    git \
    curl

# Set TESSDATA_PREFIX supaya pytesseract bisa menemukan data bahasa
ENV TESSDATA_PREFIX=/usr/share/tessdata

# Buat virtual environment
RUN python3 -m venv /app/venv

# Upgrade pip & install Python packages di venv
RUN /app/venv/bin/pip install --upgrade pip \
    && /app/venv/bin/pip install --no-cache-dir pillow pytesseract

# Buat folder scripts & uploads, beri permission penuh
RUN mkdir -p /app/scripts /tmp/uploads \
    && chmod -R 777 /app/scripts /tmp/uploads

# Copy script OCR dari host ke container
COPY ./scripts/ /app/scripts/

# Kembalikan user ke node
USER node
