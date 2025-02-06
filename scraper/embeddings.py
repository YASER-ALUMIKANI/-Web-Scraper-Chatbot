import faiss
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load free embedding model
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def store_embeddings(text):
    """Split text into chunks and store as vector embeddings."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(text)
    
    vectors = embedding_model.encode(chunks)

    faiss_index = faiss.IndexFlatL2(vectors.shape[1])
    faiss_index.add(vectors)

    return chunks, faiss_index
