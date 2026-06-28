# Dockerfile de serviço único: FastAPI serve a API e também o frontend estático.
# Build a partir da RAIZ do projeto (contexto = investiga_ai/).
# Sem Chrome/Selenium: o WHOIS agora usa RDAP (HTTP/JSON), então a imagem é leve.
FROM python:3.13-slim

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

# A maioria dos hosts (Render, Cloud Run, etc.) injeta $PORT (default 8080).
EXPOSE 8080

CMD exec gunicorn -w 2 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:${PORT:-8080} --timeout 300
