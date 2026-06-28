import requests
from app.schemas.ip_list import IPList

# RDAP é o sucessor moderno do WHOIS: protocolo HTTP/JSON, sem chave e sem navegador.
# rdap.org é um "bootstrap" que redireciona automaticamente para o RIR correto
# (LACNIC para IPs do Brasil, ARIN/RIPE/APNIC para os demais).
RDAP_URL = "https://rdap.org/ip/{ip}"
TIMEOUT = 15
TENTATIVAS = 2


def _extrair_nome_vcard(entity: dict):
    """Extrai o nome (campo 'fn') do vCard de uma entidade RDAP, se existir."""
    vcard = entity.get("vcardArray")
    if not vcard or len(vcard) < 2:
        return None
    # vcard[1] é uma lista de campos no formato [nome, params, tipo, valor]
    for campo in vcard[1]:
        if len(campo) >= 4 and campo[0] == "fn" and campo[3]:
            return campo[3]
    return None


def _extrair_owner(data: dict) -> str:
    """Determina o 'dono' do IP a partir da resposta RDAP."""
    entities = data.get("entities", []) or []

    # 1) Preferir a entidade responsável, na ordem de papéis mais úteis.
    for papel_alvo in ("registrant", "administrative", "technical", "abuse"):
        for ent in entities:
            if papel_alvo in (ent.get("roles") or []):
                nome = _extrair_nome_vcard(ent)
                if nome:
                    return nome

    # 2) Qualquer entidade que tenha um nome.
    for ent in entities:
        nome = _extrair_nome_vcard(ent)
        if nome:
            return nome

    # 3) Fallback: nome/handle da própria rede.
    return data.get("name") or data.get("handle") or "Nenhuma informação encontrada"


def consultar_whois(lista_ips: IPList) -> dict:
    """
    Consulta o proprietário (owner) de cada IP via RDAP — protocolo padrão, sem navegador.
    Mantém a mesma assinatura/retorno da versão anterior: {ip: nome_do_responsavel}.
    """
    resultados = {}
    headers = {"Accept": "application/rdap+json"}

    for ip in lista_ips.ips:
        resultados[ip] = "Erro na consulta"
        for tentativa in range(1, TENTATIVAS + 1):
            try:
                resp = requests.get(RDAP_URL.format(ip=ip), headers=headers, timeout=TIMEOUT)
                if resp.status_code == 200:
                    resultados[ip] = _extrair_owner(resp.json())
                else:
                    print(f"[{ip}] RDAP retornou status {resp.status_code}")
                    resultados[ip] = "Nenhuma informação encontrada"
                break  # sucesso ou resposta definitiva: não tenta de novo
            except Exception as e:
                print(f"[{ip}] Tentativa {tentativa}/{TENTATIVAS} falhou: {e}")

    return resultados
