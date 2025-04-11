import requests
from app.schemas.ip_list import IPList


def consultar_api_ip(ips: IPList) -> dict:
    """
    Consulta a API do ip-api.com para obter informações sobre o IP informado.
    Retorna os dados se o status da resposta for 'success', ou uma mensagem de erro caso contrário.
    """
    resposta = {}

    for ip in ips.ips:
        url = f"http://ip-api.com/json/{ip}?fields=status,proxy,mobile,country,city,hosting,org,regionName"
        try:
            resp = requests.get(url)
            data = resp.json()
            if data.get("status") == "success":
                resposta[ip] = {
                    "country": data.get("country"),
                    "city": data.get("city"),
                    "regionName": data.get("regionName"),
                    "proxy": data.get("proxy"),
                    "mobile": data.get("mobile"),
                    "hosting": data.get("hosting"),
                    "org": data.get("org")
                }
        except Exception as e:
            print(f"Erro ao consultar IP {ip}: {e}")
            
    return resposta

def checar_virustotal(ip: IPList, api_key: str) -> dict:
    """
    Consulta a API do VirusTotal para o endereço IP informado.
    Retorna as estatísticas de análise se a requisição for bem-sucedida, ou uma mensagem de erro caso contrário.
    """
    resposta = {}
    for ip in ip.ips:
        url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
        headers = {"x-apikey": api_key}
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
            resposta[ip] = stats
        else:
            print(f"Erro ao consultar VirusTotal para o IP {ip}: {resp.status_code} - {resp.text}")
    return resposta

def whois(ip: IPList):
    response = requests.get(f"https://registro.br/v2/ajax/whois/?qr={ip}&recaptchaResponse=", headers={"x-xsrf-token": "D8A03071793BC75FEC61098D78FB65ACEBAAE488"})
    print(response.json()["IPNetwork"]["Owner"])
