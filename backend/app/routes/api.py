import os
import shutil
import time
import pandas as pd
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from app.schemas.ip_list import IPList
from app.service import pdf_service, ip_service, whois_service

router = APIRouter()

from fastapi.responses import FileResponse

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
@router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
<<<<<<< HEAD
    raw_ips = pdf_service.extract_ips_from_pdf(file_path)
    ipv4, ipv6, combined = pdf_service.clean_ips(raw_ips)
    resp_ipv4_consulta_api_ip = ip_service.consultar_api_ip(IPList(ips=ipv4))
    resp_ipv6_consulta_api_ip = ip_service.consultar_api_ip(IPList(ips=ipv6))
    resp_ipv4_virustotal = ip_service.checar_virustotal(IPList(ips=ipv4), "0599ef2145a358f649a363038cf91418a51934b4f95e4c0ce06a49060c3086ca")
    resp_ipv6_virustotal = ip_service.checar_virustotal(IPList(ips=ipv6), "0599ef2145a358f649a363038cf91418a51934b4f95e4c0ce06a49060c3086ca")
    resp_ipv4_whois = whois_service.consultar_whois(IPList(ips=ipv4))
    resp_ipv6_whois = whois_service.consultar_whois(IPList(ips=ipv6))

    excel = {
        'ip': [], 
        'whois': [], 
        'ip_api_org': [], 
        'ip_api_mobile': [], 
        'ip_api_proxy': [], 
        'ip_api_hosting': [], 
        'ip_api_city': [], 
        'ip_api_regionName': [], 
        'ip_api_country': [],
        'blacklist': [],
    }

    for ip in ipv4:
        excel['ip'].append(ip)
        excel['whois'].append(resp_ipv4_whois[ip])
        excel['ip_api_org'].append(resp_ipv4_consulta_api_ip[ip]['org'])
        excel['ip_api_mobile'].append(resp_ipv4_consulta_api_ip[ip]['mobile'])
        excel['ip_api_proxy'].append(resp_ipv4_consulta_api_ip[ip]['proxy'])
        excel['ip_api_hosting'].append(resp_ipv4_consulta_api_ip[ip]['hosting'])
        excel['ip_api_city'].append(resp_ipv4_consulta_api_ip[ip]['city'])
        excel['ip_api_regionName'].append(resp_ipv4_consulta_api_ip[ip]['regionName'])
        excel['ip_api_country'].append(resp_ipv4_consulta_api_ip[ip]['country'])
        excel['blacklist'].append(resp_ipv4_virustotal[ip]['malicious'] + resp_ipv4_virustotal[ip]['suspicious'])

    for ip in ipv6:
        excel['ip'].append(ip)
        excel['whois'].append(resp_ipv6_whois[ip])
        excel['ip_api_org'].append(resp_ipv6_consulta_api_ip[ip]['org'])
        excel['ip_api_mobile'].append(resp_ipv6_consulta_api_ip[ip]['mobile'])
        excel['ip_api_proxy'].append(resp_ipv6_consulta_api_ip[ip]['proxy'])
        excel['ip_api_hosting'].append(resp_ipv6_consulta_api_ip[ip]['hosting'])
        excel['ip_api_city'].append(resp_ipv6_consulta_api_ip[ip]['city'])
        excel['ip_api_regionName'].append(resp_ipv6_consulta_api_ip[ip]['regionName'])
        excel['ip_api_country'].append(resp_ipv6_consulta_api_ip[ip]['country'])
        excel['blacklist'].append(resp_ipv6_virustotal[ip]['malicious'] + resp_ipv6_virustotal[ip]['suspicious'])
=======
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
>>>>>>> 73ea0e9cfe13bde09b1eff000e8c955ac9378f24

    df = pd.DataFrame(excel)
    excel_path = os.path.join(UPLOAD_FOLDER, "resultado.xlsx")
    df.to_excel(excel_path, index=False)

<<<<<<< HEAD
    return FileResponse(
        path=excel_path,
        filename="resultado.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
=======
    return JSONResponse(content={"ip": resp_ip})
>>>>>>> 73ea0e9cfe13bde09b1eff000e8c955ac9378f24
