import requests

def consultar_api_ip(ip: str) -> dict:
    """
    Consulta a API do ip-api.com para obter informações sobre o IP informado.
    Retorna os dados se o status da resposta for 'success', ou uma mensagem de erro caso contrário.
    """
    url = f"http://ip-api.com/json/{ip}?fields=status,proxy,mobile,country,city,hosting,org,regionName"
    try:
        resp = requests.get(url)
        data = resp.json()
        if data.get("status") == "success":
            return data
        else:
            return {"error": "Não encontrado"}
    except Exception as e:
        return {"error": str(e)}

def checar_virustotal(ip: str, api_key: str) -> dict:
    """
    Consulta a API do VirusTotal para o endereço IP informado.
    Retorna as estatísticas de análise se a requisição for bem-sucedida, ou uma mensagem de erro caso contrário.
    """
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    headers = {"x-apikey": api_key}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
        return stats
    else:
        return {"error": f"Erro na requisição: {resp.status_code}"}
