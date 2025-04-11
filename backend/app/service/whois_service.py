import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from app.schemas.ip_list import IPList

def consultar_whois(lista_ips: IPList) -> list:
    resultados = {}

    # Configuração do modo headless
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Use "--headless" se tiver problema com "--headless=new"
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-dev-shm-usage")

    navegador = webdriver.Chrome(options=chrome_options)
    navegador.get('https://registro.br/tecnologia/ferramentas/whois?search=')

    for ip in lista_ips.ips:
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

            resultados[ip] = texto_extraido
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao consultar o IP {ip}: {e}")

    navegador.quit()
    return resultados
