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
    
    df_ips = pdf_service.extract_ips_from_pdf(file_path)
    resp_ip_consulta_api_ip = ip_service.consultar_api_ip(IPList(ips=df_ips["IP"].tolist()))
    # chamada do check-virustotal para cada IP
    resp_ip_virustotal = ip_service.checar_virustotal(IPList(ips=df_ips["IP"].tolist()), "0599ef2145a358f649a363038cf91418a51934b4f95e4c0ce06a49060c3086ca")
    # whois
    resp_ip_whois = whois_service.consultar_whois(IPList(ips=df_ips["IP"].tolist()))

    resp_ip = {}
    # juntar tudo
    for ip in df_ips["IP"].tolist():
        resp_ip[ip] = {
            "consulta_api_ip": resp_ip_consulta_api_ip[ip],
            "virustotal": resp_ip_virustotal[ip],
            "whois": resp_ip_whois[ip]
        }


    return JSONResponse(content={"ip": resp_ip})
