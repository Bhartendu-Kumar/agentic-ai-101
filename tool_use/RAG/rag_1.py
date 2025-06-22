import requests

# Sample knowledge base - in real RAG, this would be much larger
documents = [
    "Python is a high-level programming language known for its simplicity and readability.",
    "Machine learning is a subset of artificial intelligence that uses algorithms to learn patterns.",
    "Ollama is a tool for running large language models locally on your machine.",
    "Vector databases store embeddings and enable semantic search capabilities.",
    "RAG combines retrieval of relevant documents with language model generation."
]

def simple_tokenize(text):
    """Basic tokenization - split and lowercase"""
    return text.lower().split()

def calculate_similarity(query_words, doc_words):
    """Calculate simple word overlap similarity"""
    query_set = set(query_words)
    doc_set = set(doc_words)
    intersection = len(query_set & doc_set)
    union = len(query_set | doc_set)
    return intersection / union if union > 0 else 0

def retrieve_relevant_docs(query, docs, top_k=2):
    """Retrieve most relevant documents using simple word matching"""
    query_words = simple_tokenize(query)
    similarities = []

    for doc in docs:
        doc_words = simple_tokenize(doc)
        similarity = calculate_similarity(query_words, doc_words)
        similarities.append(similarity)

    # Get top_k most similar documents
    indexed_sims = [(i, sim) for i, sim in enumerate(similarities)]
    indexed_sims.sort(key=lambda x: x[1], reverse=True)

    return [docs[i] for i, _ in indexed_sims[:top_k]]

def generate_with_context(query, context_docs):
    """Generate response using Ollama with retrieved context"""
    context = "\n".join(f"- {doc}" for doc in context_docs)
    prompt = f"""Context information:
{context}

Question: {query}
Answer based on the context above:"""

    body = {
        "model": "gemma3:1b",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post("http://localhost:11434/api/generate", json=body)
    return response.json()["response"]

def rag_demo():
    """Demonstrate RAG: Retrieve relevant docs, then generate answer"""
    print("=== RAG Demo ===")

    # 1. User query
    query = "What is Ollama and how does it work?"
    print(f"Query: {query}")

    # 2. Retrieve relevant documents
    relevant_docs = retrieve_relevant_docs(query, documents)
    print(f"\nRetrieved {len(relevant_docs)} relevant documents:")
    for i, doc in enumerate(relevant_docs, 1):
        print(f"{i}. {doc}")

    # 3. Generate answer with context
    print("\nGenerating answer...")
    answer = generate_with_context(query, relevant_docs)
    print(f"\nRAG Answer: {answer}")

if __name__ == "__main__":
    rag_demo()