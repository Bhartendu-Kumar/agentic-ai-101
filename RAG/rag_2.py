import requests
import numpy as np

# Sample knowledge base
documents = [
    "Python is a high-level programming language known for its simplicity and readability.",
    "Machine learning is a subset of artificial intelligence that uses algorithms to learn patterns.",
    "Ollama is a tool for running large language models locally on your machine.",
    "Vector databases store embeddings and enable semantic search capabilities.",
    "RAG combines retrieval of relevant documents with language model generation.",
    "Embeddings are numerical representations of text that capture semantic meaning.",
    "Local AI models can run without internet connection for privacy and speed."
]

def get_ollama_embedding(text, model="nomic-embed-text"):
    """Get embedding vector from Ollama"""
    body = {
        "model": model,
        "prompt": text
    }

    response = requests.post("http://localhost:11434/api/embeddings", json=body)
    if response.status_code == 200:
        return np.array(response.json()["embedding"])
    else:
        print(f"Error getting embedding: {response.status_code}")
        return None

def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors"""
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0
    return dot_product / (norm1 * norm2)

class OllamaVectorIndex:
    """Vector index using Ollama embeddings"""

    def __init__(self, embedding_model="nomic-embed-text"):
        self.embedding_model = embedding_model
        self.documents = []
        self.embeddings = []

    def add_documents(self, docs):
        """Add documents and create embeddings using Ollama"""
        print(f"Creating embeddings using Ollama model: {self.embedding_model}")
        self.documents = docs

        for i, doc in enumerate(docs):
            print(f"Processing document {i+1}/{len(docs)}...")
            embedding = get_ollama_embedding(doc, self.embedding_model)
            if embedding is not None:
                self.embeddings.append(embedding)
            else:
                print(f"Failed to get embedding for document {i+1}")
                return False

        print(f"✓ Created {len(self.embeddings)} embeddings with {len(self.embeddings[0])}-dimensional vectors")
        return True

    def search(self, query, top_k=2):
        """Search for most similar documents using Ollama embeddings"""
        # Get query embedding
        query_embedding = get_ollama_embedding(query, self.embedding_model)
        if query_embedding is None:
            return []

        # Calculate similarities
        similarities = []
        for i, doc_embedding in enumerate(self.embeddings):
            similarity = cosine_similarity(query_embedding, doc_embedding)
            similarities.append((i, similarity))

        # Sort by similarity and return top_k
        similarities.sort(key=lambda x: x[1], reverse=True)

        results = []
        for rank, (doc_idx, score) in enumerate(similarities[:top_k], 1):
            results.append({
                'document': self.documents[doc_idx],
                'similarity': float(score),
                'rank': rank
            })

        return results

def generate_with_context(query, context_results, model="gemma3:1b"):
    """Generate response using Ollama with retrieved context"""
    context = "\n".join(f"- {result['document']}" for result in context_results)
    prompt = f"""Context information:
{context}

Question: {query}
Answer based on the context above:"""

    body = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post("http://localhost:11434/api/generate", json=body)
    return response.json()["response"]

def rag_demo():
    """Demonstrate RAG using Ollama's embedding and generation capabilities"""
    print("=== RAG Demo with Ollama Embeddings ===")

    # 1. Initialize vector index with Ollama embeddings
    vector_index = OllamaVectorIndex()

    # 2. Add documents and create embeddings
    success = vector_index.add_documents(documents)
    if not success:
        print("Failed to create embeddings. Make sure Ollama is running and nomic-embed-text model is available.")
        print("Try: ollama pull nomic-embed-text")
        return

    # 3. User query
    query = "How does Ollama work with local AI models?"
    print(f"\nQuery: {query}")

    # 4. Vector-based retrieval using Ollama embeddings
    print("\nPerforming vector similarity search with Ollama embeddings...")
    search_results = vector_index.search(query, top_k=3)

    if not search_results:
        print("No search results found.")
        return

    print(f"Retrieved {len(search_results)} documents:")
    for result in search_results:
        print(f"  {result['rank']}. [Score: {result['similarity']:.3f}] {result['document']}")

    # 5. Generate answer with context using Ollama
    print("\nGenerating answer with Ollama...")
    answer = generate_with_context(query, search_results)
    print(f"\nRAG Answer: {answer}")

    # 6. Show what was demonstrated
    print(f"\n=== Ollama RAG Concepts Demonstrated ===")
    print(f"• Embeddings: Created using Ollama's nomic-embed-text model")
    print(f"• Vector Search: Cosine similarity between Ollama embeddings")
    print(f"• Generation: Context-augmented response using Ollama LLM")
    print(f"• Local Processing: Everything runs locally through Ollama")

if __name__ == "__main__":
    rag_demo()