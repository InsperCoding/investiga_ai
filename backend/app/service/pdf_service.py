import os
import openai
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar chave da API do OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")


# Função para ler o PDF e dividir em chunks
def load_and_split_pdf(pdf_path):
    # Ler o PDF
    reader = PdfReader(pdf_path)
    text = ""
    
    for page in reader.pages:
        text += page.extract_text()
    
    # Dividir o texto em chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)
    
    return chunks

def create_vector_store(chunks):
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(chunks, embeddings)
    return vector_store

from langchain.llms import OpenAI  # Certifique-se de importar a classe OpenAI
from langchain.chains import RetrievalQA

def query_rag(question, vector_store):
    # Usando OpenAI LLM com a chave da API
    llm = OpenAI(model_name="text-davinci-003", temperature=0, openai_api_key=openai.api_key)
    
    # Criar a cadeia de perguntas e respostas com o retriever
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # Ou outro tipo dependendo do seu caso
        retriever=vector_store.as_retriever(),
    )
    
    # Obter a resposta
    response = qa_chain.run(question)
    
    return response

import pandas as pd

def texto_para_df(texto):
    # Criando uma lista de dicionários, onde cada dicionário é uma linha do DataFrame
    dados = []
    
    # Dividir o texto em linhas
    linhas = texto.split('\n')
    
    for linha in linhas:
        # Separar o texto antes de " - " como IP e o restante como datetime
        partes = linha.split(' - ')
        if len(partes) == 2:
            ip = partes[0]
            datetime = partes[1]
            dados.append({"IP": ip, "Datetime": datetime})
    
    # Criar o DataFrame a partir da lista de dicionários
    df = pd.DataFrame(dados)
    return df

def extract_ips_from_pdf(pdf_path: str) -> list:
    """
    Extrai os IPs de um PDF:
      1. Lê o texto do PDF.
      2. Divide o texto em chunks.
      3. Executa a cadeia de LLM em cada chunk para extrair os IPs.
      4. Usa expressões regulares para filtrar IPs válidos.
    Retorna uma lista com todos os IPs extraídos.
    """
    chunks = load_and_split_pdf(pdf_path)
    vector_store = create_vector_store(chunks)

    question = """
        You are an expert in analyzing raw logs and unstructured text. Your task is to extract **all IP addresses (IPv4 and IPv6)** and the **exact timestamp** associated with each IP.

        Instructions:
        1. From the text below, find all valid IPv4 and IPv6 addresses.
        2. For each IP address, find the **full date and time** (timestamp) that appears **closest and most directly associated** with that IP.
        3. Return only the IP address and its timestamp in this exact format: `IP_ADDRESS - TIMESTAMP`
        4. Check if the IP address has a timestamp associated with it. If not, do not include it in the results.
        5. If multiple timestamps are present near the same IP, choose the most **complete and specific one** (e.g., including date + time + timezone if possible).
        6. Each result must be on a **separate line**.
        7. Do NOT include any explanation, markdown, bullet points, or extra formatting.


        Text:
        {chunk}
    """
    response = query_rag(question, vector_store)

    df = texto_para_df(response)

    return df