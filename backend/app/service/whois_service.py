import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.schemas.ip_list import IPList

def consultar_whois(lista_ips: IPList) -> dict:
    resultados = {}

    # Configuração do navegador (sem headless para debug visual)
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")  # Descomente se quiser rodar em segundo plano

    navegador = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(navegador, 10)

    navegador.get('https://registro.br/tecnologia/ferramentas/whois?search=')

    for ip in lista_ips.ips:
        try:
            # Aguarda o campo de busca aparecer
            box = wait.until(EC.presence_of_element_located((By.ID, 'whois-field')))
            box.clear()
            box.send_keys(ip)
            box.send_keys(Keys.RETURN)

            # Aguarda o carregamento da tabela de resultado
            try:
                dono = wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="conteudo"]/div/section/div[2]/div[2]/div/div/div[1]/div/table/tbody/tr[3]/td')
                ))
                texto_extraido = dono.text.strip()
                print(f"Texto extraído: {texto_extraido}")
                if not texto_extraido:
                    texto_extraido = "Nenhuma informação encontrada"
            except Exception as e:
                print(f"[{ip}] Erro ao localizar dono: {e}")
                texto_extraido = "Nenhuma informação encontrada"

            resultados[ip] = texto_extraido
        except Exception as e:
            print(f"[{ip}] Erro ao consultar o IP: {e}")
            resultados[ip] = "Erro na consulta"

        time.sleep(1.5)  # Aguardar entre requisições para evitar bloqueios

    navegador.quit()
    return resultados
