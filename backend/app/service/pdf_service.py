import os
import openai
import pandas as pd
from PyPDF2 import PdfReader
from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings

# Carregar variáveis de ambiente (.env)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# ---------------------------
# Função: Ler PDF e dividir em chunks
# ---------------------------
def load_and_split_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)
    
    return chunks


# ---------------------------
# Função: Criar vetor com embeddings OpenAI
# ---------------------------
def create_vector_store(chunks):
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(chunks, embeddings)
    return vector_store


# ---------------------------
# Função: LLM RAG com LangChain e GPT-3.5 Turbo
# ---------------------------
def query_rag(question, vector_store):
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=openai.api_key
    )
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(),
    )
    
    return qa_chain.run(question)


# ---------------------------
# Função: Transformar texto bruto em DataFrame
# ---------------------------
def texto_para_df(texto):
    dados = []
    linhas = texto.split('\n')
    
    for linha in linhas:
        partes = linha.split(' - ')
        if len(partes) == 2:
            ip = partes[0].strip()
            datetime = partes[1].strip()
            dados.append({"IP": ip, "Datetime": datetime})
    
    df = pd.DataFrame(dados)
    return df


# ---------------------------
# Função principal: Extrair IPs com timestamp do PDF
# ---------------------------
def extract_ips_from_pdf(pdf_path: str) -> pd.DataFrame:
    chunks = load_and_split_pdf(pdf_path)
    vector_store = create_vector_store(chunks)

    question_template = """
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

    resultados = []

    for chunk in chunks:
        question = question_template.replace("{chunk}", chunk)
        response = query_rag(question, vector_store)
        resultados.append(response)

    full_response = "\n".join(resultados)
    df = texto_para_df(full_response)
    return df
