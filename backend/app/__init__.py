from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
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

# Se o frontend rodar separado, não há necessidade de montar templates ou arquivos estáticos.
# app.mount("/static", StaticFiles(directory="static"), name="static")
# from fastapi.templating import Jinja2Templates
# templates = Jinja2Templates(directory="templates")

app.include_router(api_router)
