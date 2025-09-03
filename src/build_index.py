import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Please add it to your .env file.")

try:
    from langchain_community.vectorstores import FAISS
    from langchain_openai import OpenAIEmbeddings
    from langchain.text_splitter import CharacterTextSplitter
    from langchain.docstore.document import Document
except ImportError:
    raise ImportError("FAISS or related dependencies not installed. Run: pip install faiss-cpu chromadb")

def build_faiss_index():
    # Example documents (replace with your dataset)
    texts = [
        "LangChain is a framework for building applications with LLMs.",
        "FAISS is a library for efficient similarity search."
    ]
    docs = [Document(page_content=t) for t in texts]

    splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    split_docs = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(api_key=api_key)
    vectorstore = FAISS.from_documents(split_docs, embeddings)

    vectorstore.save_local("faiss_index")
    print("✅ FAISS index saved at ./faiss_index")

if __name__ == "__main__":
    build_faiss_index()
