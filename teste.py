# pdf_ip_extractor.py

import fitz  # PyMuPDF
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import re

# 1. Ler Pdf
def read_pdf_text(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# 2. Dividir o texto
def split_text(text, chunk_size=1000, chunk_overlap=100):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return text_splitter.split_text(text)

# 3. LLM setup
llm = Ollama(model="mistral", temperature=0.0)

# 4. Prompt
prompt = PromptTemplate(
    input_variables=["chunk"],
    template="""
        You must extract all IP addresses from the following text:

        {chunk}

        Rules:
        1. Return ONLY the list of IP addresses.
        2. Each IP must be on a separate line.
        3. Do NOT include any explanation, label, bullet point, or formatting—just raw IP addresses.
        4. Do NOT return anything other than the IPs. No intros, no summaries.
    """
)

chain = LLMChain(llm=llm, prompt=prompt)

# 5. Função auxiliar para IPs válidos
def extract_valid_ips(text):
    return re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text)

# 6. Extração principal por PDF
def extract_ips_from_pdf(pdf_path):
    text = read_pdf_text(pdf_path)
    chunks = split_text(text)
    ips = []
    for chunk in chunks:
        result = chain.run(chunk)
        ips += extract_valid_ips(result)
    return "\n".join(ips)

# 7. Regex IPv6
def extract_ipv6(text):
    ipv6_pattern = r'\b(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}\b'
    return re.findall(ipv6_pattern, text)

# 8. Processa todos os PDFs de uma pasta
def process_pdf_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            print(f"📄 Processando: {filename}")

            raw_text = extract_ips_from_pdf(pdf_path)

            # IPv4 & IPv6
            ipv4_list = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', raw_text)
            ipv6_list = extract_ipv6(raw_text)

            unique_ips = sorted(set(ipv4_list + ipv6_list))

            # Salvar IPs
            base_name = os.path.splitext(filename)[0]
            txt_filename = os.path.join(folder_path, f"{base_name}_ips.txt")

            with open(txt_filename, "w") as f:
                for ip in unique_ips:
                    f.write(f"{ip}\n")

            print(f"✅ IPs salvos em: {txt_filename}\n")

# 9. Executar
if __name__ == "__main__":
    pasta_pdf = "pdfs"  # <-- Altere aqui com o nome da pasta onde estão seus PDFs
    process_pdf_folder(pasta_pdf)
