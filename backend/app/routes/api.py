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
    resp_ipv4_consulta_api_ip = ip_service.consultar_api_ip(IPList(ips=ipv4))
    resp_ipv6_consulta_api_ip = ip_service.consultar_api_ip(IPList(ips=ipv6))
    # chamada do check-virustotal para cada IP
    resp_ipv4_virustotal = ip_service.checar_virustotal(IPList(ips=ipv4), "0599ef2145a358f649a363038cf91418a51934b4f95e4c0ce06a49060c3086ca")
    resp_ipv6_virustotal = ip_service.checar_virustotal(IPList(ips=ipv6), "0599ef2145a358f649a363038cf91418a51934b4f95e4c0ce06a49060c3086ca") 
    # whois
    resp_ipv4_whois = whois_service.consultar_whois(IPList(ips=ipv4))
    resp_ipv6_whois = whois_service.consultar_whois(IPList(ips=ipv6))
    resp_ipv4 = {}
    resp_ipv6 = {}
    # juntar tudo
    for ip in ipv4:
        resp_ipv4[ip] = {
            "consulta_api_ip": resp_ipv4_consulta_api_ip[ip],
            "virustotal": resp_ipv4_virustotal[ip],
            "whois": resp_ipv4_whois[ip]
        }
    for ip in ipv6:
        resp_ipv6[ip] = {
            "consulta_api_ip": resp_ipv6_consulta_api_ip[ip],
            "virustotal": resp_ipv6_virustotal[ip],
            "whois": resp_ipv6_whois[ip]
        }


    return JSONResponse(content={"ipv4": resp_ipv4, "ipv6": resp_ipv6, "total": len(combined)})
