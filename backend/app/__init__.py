import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes import router as api_router

app = FastAPI(
    title="Investiga AI API",
    description="API do projeto Investiga AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajuste conforme sua política
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas da API (devem ser registradas antes do mount estático em "/").
app.include_router(api_router)

# Serviço único: o próprio FastAPI serve o frontend estático.
# Procura a pasta do frontend em ordem: env var, layout do container, layout de dev local.
_here = os.path.dirname(__file__)
_frontend_candidates = [
    os.getenv("FRONTEND_DIR"),
    os.path.join(_here, "..", "frontend_static"),   # container (COPY frontend/ -> /app/frontend_static)
    os.path.join(_here, "..", "..", "frontend"),     # dev local (../../frontend)
]
for _dir in _frontend_candidates:
    if _dir and os.path.isdir(_dir):
        app.mount("/", StaticFiles(directory=_dir, html=True), name="frontend")
        break
