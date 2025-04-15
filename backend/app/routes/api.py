from datetime import timedelta, datetime
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

    excel = {
        'ip': [], 
        "horario": [],
        "horario -3": [],
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

    df_ips = pdf_service.extract_ips_from_pdf(file_path)
    resp_ip_consulta_api_ip = ip_service.consultar_api_ip(IPList(ips=df_ips["IP"].tolist()))
    # chamada do check-virustotal para cada IP
    resp_ip_virustotal = ip_service.checar_virustotal(IPList(ips=df_ips["IP"].tolist()), "0599ef2145a358f649a363038cf91418a51934b4f95e4c0ce06a49060c3086ca")
    # whois
    resp_ip_whois = whois_service.consultar_whois(IPList(ips=df_ips["IP"].tolist()))


    for ip in df_ips["IP"].tolist():
        data_str = df_ips[df_ips["IP"] == ip]["Datetime"].values[0]

        excel['ip'].append(ip)
        excel["horario"].append(datetime.strptime(data_str.replace(" UTC", ""), "%Y-%m-%d %H:%M:%S"))
        excel["horario -3"].append(datetime.strptime(data_str.replace(" UTC", ""), "%Y-%m-%d %H:%M:%S") - timedelta(hours=3))
        excel['whois'].append(resp_ip_whois[ip])
        excel['ip_api_org'].append(resp_ip_consulta_api_ip[ip]['org'])
        excel['ip_api_mobile'].append(resp_ip_consulta_api_ip[ip]['mobile'])
        excel['ip_api_proxy'].append(resp_ip_consulta_api_ip[ip]['proxy'])
        excel['ip_api_hosting'].append(resp_ip_consulta_api_ip[ip]['hosting'])
        excel['ip_api_city'].append(resp_ip_consulta_api_ip[ip]['city'])
        excel['ip_api_regionName'].append(resp_ip_consulta_api_ip[ip]['regionName'])
        excel['ip_api_country'].append(resp_ip_consulta_api_ip[ip]['country'])
        excel['blacklist'].append(resp_ip_virustotal[ip]['malicious'] + resp_ip_virustotal[ip]['suspicious'])

    df = pd.DataFrame(excel)
    excel_path = os.path.join(UPLOAD_FOLDER, "resultado.xlsx")
    df.to_excel(excel_path, index=False)

    return FileResponse(
        path=excel_path,
        filename="resultado.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
