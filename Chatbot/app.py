# """
# LangChain Q&A System for Text Files
# Folder ki saari .txt files load karta hai aur sawaal jawab karta hai
# """

# from langchain_community.document_loaders import DirectoryLoader, TextLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings
# import os
# from dotenv import load_dotenv
# from openai import OpenAI
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel

# load_dotenv()

# client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")

# # Configuration
# FOLDER_PATH = "txt_dataset"

# # PROMPT = """
# # You are a coding assistant. I have provided you with my .ts (TypeScript) files and their content.

# # IMPORTANT INSTRUCTIONS:
# # 1. Always refer to the provided file contents when answering my questions
# # 2. Give answers ONLY in code format - no explanations, no text descriptions
# # 3. Base your responses strictly on the existing code structure and patterns in my files
# # 4. When I ask a question, respond with code that directly addresses it
# # 5. Do not provide unnecessary information or explanations
# # 6. Keep responses focused and code-only

# # When responding:
# # - Write code that fits naturally with my existing files
# # - Follow the same coding style and patterns I use
# # - Only output executable/usable code
# # - No markdown formatting unless it's actual code
# # - No conversational responses

# # Format: Just give me the code I need, nothing else.
# # """

# PROMPT = """
# You are a coding and conversational assistant.  
# I will provide you with TypeScript (.ts), HTML, or related code files — or sometimes general questions or conversations.

# INSTRUCTIONS:
# 1. Always understand the question or request before responding.  
# 2. If I provide code files, base your response strictly on their existing structure, logic, and naming conventions.  
# 3. When the question requires code — give complete, functional, and production-ready code.  
# 4. Always provide both .ts and .html parts if relevant.  
# 5. Explain your answer clearly after the code — what it does, how it works, and why you used that approach.  
# 6. If my message is conversational (like "hi", "how are you", etc.), respond naturally in a human-like tone.  
# 7. Never ignore context or give incomplete code.  
# 8. Always follow my project's style, syntax, and structure.  
# 9. Keep your answer clean, readable, and ready to use.  

# When responding:
# - Write code that fits naturally with my existing project files.  
# - Follow the same naming conventions, formatting, and structure I use.  
# - Output complete, working code (no placeholders or incomplete snippets).  
# - Use markdown formatting only for actual code blocks.  
# - After the code, give a short, clear explanation (unless I ask for "code only").  
# - Avoid unnecessary text or unrelated suggestions.  

# Goal:
# Provide accurate, contextual, and usable solutions — both technical and conversational — in a professional and natural way.
# """

# # PROMPT = """
# # You are a coding and conversational assistant specialized in Angular development.  

# # PROJECT CONTEXT:
# # - The project is built using Angular (version 19+) with custom-built Angular Material wrapper components (e.g., lib-button, lib-text-field, lib-date-picker, etc.).
# # - These wrappers completely replace direct usage of Angular Material components (like mat-button, mat-form-field, etc.).
# # - You must never use or suggest direct Material UI or Angular Material syntax (mat-*, Material UI, MUI, @mui/material, etc.).
# # - Always use the existing project library components and follow the custom naming conventions.
# # - Assume that all UI components and services already exist within the library (e.g., toast service, throttling service, etc.).

# # INSTRUCTIONS:
# # 1. Always analyze my question or provided files carefully before responding.
# # 2. When I ask for code, provide complete, working TypeScript and HTML code.
# # 3. Use only the custom library components from my Angular project — never Material UI or third-party code.
# # 4. Match the code style, syntax, and architecture already used in my project.
# # 5. If I ask a conceptual or conversational question, respond naturally and professionally.
# # 6. When giving code, use markdown formatting for clarity.
# # 7. Always provide a short, clear explanation after the code — unless I specifically say “code only.”
# # 8. Keep all responses aligned with my Angular setup, not any React, Vue, or MUI framework.

# # When responding:
# #  - Write code that fits naturally with my existing project files.  
# #  - Follow the same naming conventions, formatting, and structure I use.
# #  - Output complete, working code (no placeholders or incomplete snippets).
# #  - Use markdown formatting only for actual code blocks.
# #  - After the code, give a short, clear explanation (unless I ask for "code only").
# #  - Avoid unnecessary text or unrelated suggestions.

# # GOAL:
# # Ensure all generated code perfectly fits into my Angular project and uses my custom UI library components instead of Material UI or any external UI framework.
# # """


# def load_documents(folder_path):
#     """Folder se saari .txt files load karta hai"""
#     loader = DirectoryLoader(
#         folder_path,
#         glob="**/*.txt",
#         loader_cls=TextLoader,
#         show_progress=True
#     )
    
#     documents = loader.load()
#     print(f"✅ Loaded {len(documents)} documents")
#     return documents

# def split_documents(documents):
#     """Documents ko chhote chunks mein split karta hai"""
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1000, 
#         chunk_overlap=200, 
#         length_function=len
#     )
#     chunks = text_splitter.split_documents(documents)
#     print(f"✅ Created {len(chunks)} chunks")
#     return chunks

# def create_vectorstore(chunks):
#     """FAISS vector store banata hai"""
#     embeddings = OpenAIEmbeddings()
#     vectorstore = FAISS.from_documents(chunks, embeddings)
#     print("✅ Vector store created successfully")
#     return vectorstore

# def search_similar_documents(vectorstore, query, k=3):
#     results = vectorstore.similarity_search_with_score(query, k=k)
#     return results

# def get_llm_response(question, similar_results):
#     # Similar documents ka content extract karo
#     context = "\n\n---\n\n".join([doc.page_content for doc, score in similar_results])
    
#     response = client.chat.completions.create(
#         model="deepseek-chat",
#         messages=[
#             {"role": "system", "content": PROMPT},
#             {"role": "user", "content": f"Context from files:\n{context}\n\nQuestion: {question}"},
#         ],
#         stream=False
#     )

#     content = response.choices[0].message.content
#     return content

# def main(question):
#     documents = load_documents(FOLDER_PATH)
    
#     if not documents:
#         print("❌ No documents found! Check your folder path.")
#         return
    
#     chunks = split_documents(documents)
#     vectorstore = create_vectorstore(chunks)
#     similar_results = search_similar_documents(vectorstore, question, k=5)
    
#     print(f"\n📄 Found {len(similar_results)} similar documents\n")
    
#     # LLM se response lo
#     llm_response = get_llm_response(question, similar_results)
    
#     print("🤖 Response:\n")
#     print(llm_response)
    

# # FastAPI setup
# app = FastAPI()

# class QuestionRequest(BaseModel):
#     question: str

# vectorstore_cache = None

# @app.on_event("startup")
# async def startup_event():
#     global vectorstore_cache
#     documents = load_documents(FOLDER_PATH)
#     if documents:
#         chunks = split_documents(documents)
#         vectorstore_cache = create_vectorstore(chunks)
#         print("✅ Vectorstore loaded on startup")

# @app.post("/ask")
# async def ask_question(request: QuestionRequest):
#     global vectorstore_cache
    
#     if vectorstore_cache is None:
#         raise HTTPException(status_code=500, detail="Vectorstore not initialized")
    
#     try:
#         similar_results = search_similar_documents(vectorstore_cache, request.question, k=5)
#         llm_response = get_llm_response(request.question, similar_results)
#         return {"answer": llm_response}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

import os
from dotenv import load_dotenv
from groq import AsyncGroq

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

FOLDER_PATH = "txt_dataset"

PROMPT = """
You are a coding and conversational assistant specialized in Angular development.

PROJECT CONTEXT:
- The project is built using Angular (version 19+) with custom-built Angular Material wrapper components (e.g., lib-button, lib-text-field, lib-date-picker, etc.).
- These wrappers completely replace direct usage of Angular Material components (like mat-button, mat-form-field, etc.).
- You must never use or suggest direct Material UI or Angular Material syntax (mat-*, Material UI, MUI, @mui/material, etc.).
- Always use the existing project library components and follow the custom naming conventions.
- Assume that all UI components and services already exist within the library (e.g., toast service, throttling service, etc.).

INSTRUCTIONS:
1. Always analyze my question or provided files carefully before responding.
2. When I ask for code, provide complete, working TypeScript and HTML code.
3. Use only the custom library components from my Angular project — never Material UI or third-party code.
4. Match the code style, syntax, and architecture already used in my project.
5. If I ask a conceptual or conversational question, respond naturally and professionally.
6. When giving code, use markdown formatting for clarity.
7. Always provide a short, clear explanation after the code — unless I specifically say “code only.”
8. Keep all responses aligned with my Angular setup, not any React, Vue, or MUI framework.

When responding:
- Write code that fits naturally with my existing project files.
- Follow the same naming conventions, formatting, and structure I use.
- Output complete, working code (no placeholders or incomplete snippets).
- Use markdown formatting only for actual code blocks.
- After the code, give a short, clear explanation (unless I ask for "code only").
- Avoid unnecessary text or unrelated suggestions.

GOAL:
Ensure all generated code perfectly fits into my Angular project and uses my custom UI library components instead of Material UI or any external UI framework.
"""


# ---------- GROQ CLIENT ----------

client = AsyncGroq(
    api_key=os.environ.get("GROQ_API_KEY")  # Yahan apni Groq key daalo
)

# ---------- DOCUMENT LOADING ----------

def load_documents(folder_path):
    loader = DirectoryLoader(
        folder_path,
        glob="**/*.txt",
        loader_cls=TextLoader,
        show_progress=True
    )
    docs = loader.load()
    print(f"Loaded {len(docs)} documents")
    return docs


# ---------- TEXT SPLITTING ----------

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks")
    return chunks


# ---------- VECTOR STORE ----------

def create_vectorstore(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = FAISS.from_documents(chunks, embeddings)
    print("✅ Vector store created successfully")
    return vectorstore


# ---------- SEARCH ----------

def search_documents(vectorstore, query):
    results = vectorstore.similarity_search(query, k=5)
    return results


# ---------- LLM RESPONSE ----------

async def get_llm_response(question, docs):
    context = "\n\n".join([doc.page_content for doc in docs])
    try:
        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": PROMPT},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion:{question}"}
            ]
        )
        print("✅ Groq response received")
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ Groq ERROR: {type(e).__name__}: {e}")
        return "LLM connection failed"


# ---------- FASTAPI ----------

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

vectorstore_cache = None


@app.on_event("startup")
async def startup():
    global vectorstore_cache
    documents = load_documents(FOLDER_PATH)
    if not documents:
        print("No documents found")
        return
    chunks = split_documents(documents)
    vectorstore_cache = create_vectorstore(chunks)
    print("Vectorstore ready")


@app.post("/ask")
async def ask(request: QuestionRequest):
    global vectorstore_cache
    if vectorstore_cache is None:
        raise HTTPException(status_code=500, detail="Vector store not ready")
    docs = search_documents(vectorstore_cache, request.question)
    answer = await get_llm_response(request.question, docs)
    return {"answer": answer}


# ---------- RUN ----------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)