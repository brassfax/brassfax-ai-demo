from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Dynamically resolve absolute path to data directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_BASE_DIR = os.path.abspath(os.path.join(BASE_DIR, "../data"))

# Initialize FastAPI app
app = FastAPI()

# Enable CORS (safe for SaaS embedding)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files for widget frontend
static_dir = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.post("/query")
async def query(request: Request):
    body = await request.json()
    client_id = body["client_id"]
    question = body["question"]

    # Build path for client vector DB
    client_vector_path = os.path.join(CHROMA_BASE_DIR, client_id)

    # Load vector store and embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectordb = Chroma(persist_directory=client_vector_path, embedding_function=embeddings)
    retriever = vectordb.as_retriever()

    # Query LLM with retrieval
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-4o", temperature=0)
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    answer = qa.invoke(question)

    return {"answer": answer['result']}  # <-- ensure only return string answer
