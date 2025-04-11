from fastapi import FastAPI, UploadFile, File, HTTPException, Request, Form
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
import shutil
import os
from app.pdf_processor import extract_ips_from_pdf, clean_ips
from app.ip_checker import consultar_api_ip, checar_virustotal
from typing import List
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware  
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Inicializa o app
app = FastAPI()

# CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Diretórios corrigidos com base na sua estrutura de pastas
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Modelo de entrada
class IPList(BaseModel):
    ips: List[str]

# Função auxiliar
def consultar_whois(lista_ips):
    resultados = []
    navegador = webdriver.Chrome()
    navegador.get('https://registro.br/tecnologia/ferramentas/whois?search=')
    navegador.maximize_window()

    for ip in lista_ips:
        try:
            box = navegador.find_element(By.ID, 'whois-field')
            box.click()
            box.clear()
            time.sleep(1)
            box.send_keys(ip)
            time.sleep(2)
            box.send_keys(Keys.RETURN)
            time.sleep(3)

            try:
                dono = navegador.find_element(By.CLASS_NAME, 'cell-owner')
                texto_extraido = dono.text.strip()
                if not texto_extraido:
                    texto_extraido = "Nenhuma informação encontrada"
            except Exception:
                texto_extraido = "Nenhuma informação encontrada"

            resultados.append({"IP": ip, "Dono": texto_extraido})

        except Exception as e:
            resultados.append({"IP": ip, "Dono": f"Erro ao pesquisar: {str(e)}"})

    navegador.quit()
    return resultados

# Pasta de uploads
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Upload e extração de IPs do PDF
@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    raw_ips = extract_ips_from_pdf(file_path)
    ipv4, ipv6, combined = clean_ips(raw_ips)

    return JSONResponse(content={"ipv4": ipv4, "ipv6": ipv6, "total": len(combined)})

# Consulta API de IP
@app.post("/check-ip/")
def check_ip_info(ip: str):
    data = consultar_api_ip(ip)
    return data

# Consulta VirusTotal
@app.post("/check-virustotal")
def check_virustotal(ip: str):
    api_key = "0599ef2145a358f649a363038cf91418a51934b4f95e4c0ce06a49060c3086ca"
    resultado = checar_virustotal(ip, api_key)
    return resultado

# Consulta WHOIS com Selenium
@app.post("/check-whois/")
def check_whois(data: IPList):
    try:
        resultados = consultar_whois(data.ips)
        df = pd.DataFrame(resultados)
        df.to_excel("Resultados_WHOIS.xlsx", index=False)
        return {"resultados": resultados, "mensagem": "Consulta realizada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
