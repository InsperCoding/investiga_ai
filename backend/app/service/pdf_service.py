import fitz
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re

# Instancia o modelo com Ollama
llm = Ollama(model="mistral", temperature=0.0)

# Define o prompt para extração de IPs
prompt = PromptTemplate(
    input_variables=["chunk"],
    template = """
    You must extract all IP addresses from the following text:
    {chunk}
    
    Rules:
    1. Return ONLY the list of IP addresses.
    2. Each IP must be on a separate line.
    3. Do NOT include any explanation or formatting.
    """
)

# Cria a cadeia de execução com o modelo e o prompt
chain = LLMChain(llm=llm, prompt=prompt)

def read_pdf_text(path: str) -> str:
    """
    Lê o conteúdo textual de um PDF.
    """
    doc = fitz.open(path)
    return "".join(page.get_text() for page in doc)

def split_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 100) -> list:
    """
    Divide o texto em pedaços menores para facilitar o processamento.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(text)

def extract_valid_ips(text: str) -> list:
    """
    Extrai endereços IPv4 válidos a partir de um texto utilizando regex.
    """
    return re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text)

def extract_ips_from_pdf(pdf_path: str) -> list:
    """
    Extrai os IPs de um PDF:
      1. Lê o texto do PDF.
      2. Divide o texto em chunks.
      3. Executa a cadeia de LLM em cada chunk para extrair os IPs.
      4. Usa expressões regulares para filtrar IPs válidos.
    Retorna uma lista com todos os IPs extraídos.
    """
    text = read_pdf_text(pdf_path)
    chunks = split_text(text)
    ips = []
    for chunk in chunks:
        result = chain.run(chunk)
        ips += extract_valid_ips(result)
    return ips

def clean_ips(raw_ips: list) -> tuple:
    """
    Recebe uma lista de IPs em formato bruto e retorna três listas:
      - Lista de IPs IPv4
      - Lista de IPs IPv6
      - Lista combinada (união dos anteriores)
    """
    ipv4_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    ipv6_pattern = r'\b(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}\b'
    ipv4_list = re.findall(ipv4_pattern, "\n".join(raw_ips))
    ipv6_list = re.findall(ipv6_pattern, "\n".join(raw_ips))
    return sorted(set(ipv4_list)), sorted(set(ipv6_list)), list(set(ipv4_list + ipv6_list))
