# Use imagem base do Python
FROM python:3.13-slim

# Instalar dependências do sistema para Chrome + ChromeDriver
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
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

# Instalar Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable

# Instalar ChromeDriver compatível
RUN CHROME_VERSION=$(google-chrome-stable --version | awk '{print $3}' | cut -d '.' -f 1) && \
    DRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json" | \
    jq -r ".channels.Stable.version") && \
    curl -sSL https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${DRIVER_VERSION}/linux64/chromedriver-linux64.zip -o /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver

# Criar diretório de trabalho
WORKDIR /app

# Copiar os arquivos de requisitos e instalar dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Instalar Gunicorn
RUN pip install gunicorn

# Copiar o código da aplicação
COPY . .

# Expor a porta
EXPOSE 8010

# Rodar a aplicação com Gunicorn e Uvicorn Worker
CMD ["gunicorn", "-w", "8", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8010", "--timeout", "120"]