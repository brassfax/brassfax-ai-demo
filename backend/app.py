# brassfax-ai/backend/app.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import os

app = FastAPI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHROMA_BASE_DIR = "../data"

class QueryRequest(BaseModel):
    client_id: str
    question: str

@app.post("/query")
async def query_ai(request: QueryRequest):
    try:
        client_vector_path = os.path.join(CHROMA_BASE_DIR, request.client_id)
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        vectordb = Chroma(persist_directory=client_vector_path, embedding_function=embeddings)

        retriever = vectordb.as_retriever()
        llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
        qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

        result = qa.run(request.question)
        return {"answer": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
