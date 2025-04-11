import requests

def consultar_api_ip(ip):
    url = f"http://ip-api.com/json/{ip}?fields=status,proxy,mobile,country,city,hosting,org,regionName"
    try:
        resp = requests.get(url)
        data = resp.json()
        if data['status'] == 'success':
            return data
        else:
            return {"error": "Não encontrado"}
    except Exception as e:
        return {"error": str(e)}

def checar_virustotal(ip, api_key):
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    headers = {"x-apikey": api_key}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        stats = data['data']['attributes']['last_analysis_stats']
        return stats
    else:
        return {"error": f"Erro na requisição: {resp.status_code}"}
