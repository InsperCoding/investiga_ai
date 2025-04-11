import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def consultar_whois(lista_ips: list) -> list:
    resultados = []
    navegador = webdriver.Chrome()
    navegador.get('https://registro.br/tecnologia/ferramentas/whois?search=')
    navegador.maximize_window()

    for ip in lista_ips:
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

            resultados.append({"IP": ip, "Dono": texto_extraido})
        except Exception as e:
            resultados.append({"IP": ip, "Dono": f"Erro ao pesquisar: {str(e)}"})
    
    navegador.quit()
    return resultados
