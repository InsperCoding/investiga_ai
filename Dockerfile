# Dockerfile de serviço único: FastAPI serve a API e também o frontend estático.
# Build a partir da RAIZ do projeto (contexto = investiga_ai/).
FROM python:3.13-slim

# Dependências de sistema para Chrome + ChromeDriver (usado pelo WHOIS via Selenium)
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    jq \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libxss1 \
    libappindicator1 \
    libasound2 \
    xdg-utils \
    libu2f-udev \
    libvulkan1 \
    fonts-liberation \
    ca-certificates \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable

# ChromeDriver compatível
RUN DRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json" | \
    jq -r ".channels.Stable.version") && \
    curl -sSL https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${DRIVER_VERSION}/linux64/chromedriver-linux64.zip -o /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver

WORKDIR /app

# Dependências Python do backend
COPY backend/requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Código do backend (vira a raiz /app, onde está o main.py)
COPY backend/ /app/

# Frontend estático servido pelo FastAPI (ver app/__init__.py)
COPY frontend/ /app/frontend_static/

# Cloud Run injeta $PORT (default 8080).
EXPOSE 8080

# Poucos workers: cada request pode abrir um Chrome (Selenium) — muitos estouram memória.
CMD exec gunicorn -w 2 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:${PORT:-8080} --timeout 300
