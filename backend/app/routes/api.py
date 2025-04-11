import os
import shutil
import time
import pandas as pd
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from app.schemas.ip_list import IPList
from app.service import pdf_service, ip_service, whois_service

router = APIRouter()

# Se o backend não for servir HTML, remova a rota abaixo:
# from fastapi.templating import Jinja2Templates
# templates = Jinja2Templates(directory="templates")
#
# @router.get("/", response_class=HTMLResponse)
# async def home(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    raw_ips = pdf_service.extract_ips_from_pdf(file_path)
    ipv4, ipv6, combined = pdf_service.clean_ips(raw_ips)
    
    return JSONResponse(content={"ipv4": ipv4, "ipv6": ipv6, "total": len(combined)})

@router.post("/check-ip/")
async def check_ip_info(ip: str = Form(...)):
    data = ip_service.consultar_api_ip(ip)
    return data

@router.post("/check-virustotal/")
async def check_virustotal(ip: str = Form(...)):
    api_key = "0599ef2145a358f649a363038cf91418a51934b4f95e4c0ce06a49060c3086ca"  # Recomenda-se externalizar a chave
    resultado = ip_service.checar_virustotal(ip, api_key)
    return resultado

@router.post("/check-whois/")
async def check_whois(data: IPList):
    try:
        resultados = whois_service.consultar_whois(data.ips)
        df = pd.DataFrame(resultados)
        df.to_excel("Resultados_WHOIS.xlsx", index=False)
        return {"resultados": resultados, "mensagem": "Consulta realizada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
