import re
from openpyxl import Workbook
from datetime import datetime, timedelta
import pdfplumber

# Função para extrair IP e horário de acesso de uma linha
def extrair_dados(linha):
    # Padrão mais flexível para capturar diferentes formatos de IPs e horários
    match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?(\d{2}:\d{2}:\d{2})', linha)
    if match:
        ip = match.group(1)
        hora_acesso = match.group(2)
        return ip, hora_acesso
    return None, None

# Função para ler o PDF com pdfplumber
def ler_pdf_com_pdfplumber(caminho_pdf):
    linhas = []
    try:
        with pdfplumber.open(caminho_pdf) as pdf:
            for pagina in pdf.pages:
                texto = pagina.extract_text()
                if texto:
                    linhas.extend(texto.splitlines())
    except Exception as e:
        print(f"Erro ao ler o PDF: {e}")
    return linhas

# Função principal para processar o PDF e gerar a planilha
def processar_pdf_para_excel(caminho_pdf, caminho_excel):
    print(f"Iniciando processamento do arquivo: {caminho_pdf}")
    
    # Ler o PDF
    linhas = ler_pdf_com_pdfplumber(caminho_pdf)
    print(f"Total de linhas extraídas do PDF: {len(linhas)}")
    
    # Criar a planilha
    wb = Workbook()
    ws = wb.active
    ws.title = "Acessos"
    ws.append(["IP", "Hora de Acesso", "Hora de Acesso -3"])
    
    # Contador para acompanhar os resultados
    contador = 0
    
    # Processar cada linha do PDF
    for linha in linhas:
        # Pular linhas vazias
        if not linha.strip():
            continue
            
        ip, hora_acesso = extrair_dados(linha)
        if ip and hora_acesso:
            contador += 1
            try:
                hora_original = datetime.strptime(hora_acesso, "%H:%M:%S")
                hora_menos_3 = (hora_original - timedelta(hours=3)).time()
                ws.append([ip, hora_acesso, hora_menos_3.strftime("%H:%M:%S")])
                print(f"Encontrado: IP: {ip}, Hora: {hora_acesso}, Hora-3: {hora_menos_3}")
            except ValueError as e:
                print(f"Erro ao processar hora {hora_acesso}: {e}")
    
    # Verificar se encontramos algum dado
    if contador == 0:
        print("Nenhum IP ou horário encontrado no PDF.")
        print("Primeiras 5 linhas do PDF para depuração:")
        for i, linha in enumerate(linhas[:5]):
            print(f"Linha {i+1}: {linha}")
    else:
        print(f"Total de registros encontrados e adicionados: {contador}")
    
    # Salvar a planilha
    try:
        wb.save(caminho_excel)
        print(f"Planilha salva com sucesso em: {caminho_excel}")
    except Exception as e:
        print(f"Erro ao salvar planilha: {e}")

# Exemplo de uso
if __name__ == "__main__":
    caminho_pdf = "ips_com_horarios.pdf"
    caminho_excel = "resultado.xlsx"
    processar_pdf_para_excel(caminho_pdf, caminho_excel)