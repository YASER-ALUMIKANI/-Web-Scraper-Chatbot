def retrieve_relevant_chunks(query, chunks, faiss_index, embedding_model):
    """Finds the most relevant website content based on the user query."""
    query_vector = embedding_model.encode([query])
    distances, indices = faiss_index.search(query_vector, k=3)

    retrieved_text = "\n".join([chunks[idx] for idx in indices[0] if idx < len(chunks)])
    return retrieved_text
