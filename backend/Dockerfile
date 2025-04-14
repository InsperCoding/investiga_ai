# Use uma imagem oficial do Python como imagem base
FROM python:3.13-slim

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar os arquivos de requisitos para o contêiner
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Instalar o Gunicorn
RUN pip install gunicorn

# Copiar o código da aplicação para o diretório de trabalho do contêiner
COPY . .

# Expor a porta em que a FastAPI será executada
EXPOSE 8010

# Comando para iniciar o servidor FastAPI com Gunicorn e Uvicorn Workers
CMD ["gunicorn", "-w", "8", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8010", "--timeout", "120"]
