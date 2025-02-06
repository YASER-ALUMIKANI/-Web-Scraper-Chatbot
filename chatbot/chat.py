from langchain_openai import ChatOpenAI
from chatbot.retriever import retrieve_relevant_chunks
from scraper.embeddings import embedding_model
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def chat_with_gpt(prompt, chunks, faiss_index):
    """Generates chatbot response using GPT and relevant retrieved content."""
    context = retrieve_relevant_chunks(prompt, chunks, faiss_index, embedding_model)

    chat = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://models.inference.ai.azure.com",
        model="gpt-4o",
        streaming=True,
        temperature=0.9,
        top_p=1.0
    )

    messages = [
        {"role": "system", "content": "You are a helpful AI assistant. Use the following website data to respond to queries."},
        {"role": "user", "content": context},
        {"role": "user", "content": prompt}
    ]

    response = chat.invoke(messages, max_tokens=300)
    return response.content
