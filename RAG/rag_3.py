from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.vector_stores.duckdb import DuckDBVectorStore
from llama_index.core import StorageContext
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

def setup_rag_system():
    """Setup RAG system with LlamaIndex and Ollama"""
    print("=== RAG Demo with LlamaIndex + Ollama ===")

    # Configure models
    print("Configuring Ollama models...")
    Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")
    Settings.llm = Ollama(model="gemma3:1b", temperature=0, request_timeout=360.0)

    # Load documents
    print("Loading documents from facts.txt...")
    documents = SimpleDirectoryReader(input_files=["facts.txt"]).load_data(show_progress=True)
    print(f"✓ Loaded {len(documents)} documents")

    # Setup text splitter
    print("Setting up text splitter...")
    splitter = TokenTextSplitter(separator="\n", chunk_size=64, chunk_overlap=0)
    nodes = splitter.get_nodes_from_documents(documents)
    print(f"✓ Created {len(nodes)} text chunks")

    # Setup vector store
    print("Setting up DuckDB vector store...")
    vector_store = DuckDBVectorStore()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Create index
    print("Creating vector index...")
    index = VectorStoreIndex(nodes, storage_context=storage_context, show_progress=True)
    print("✓ Vector index created successfully")

    # Create query engine
    query_engine = index.as_query_engine()
    print("✓ Query engine ready")

    return query_engine

def demo_queries(query_engine):
    """Run demo queries to show RAG capabilities"""
    print("\n=== Demo Queries ===")

    demo_questions = [
        "What is Ollama and how does it work?",
        "Explain what RAG is and how it works",
        "What are the benefits of using vector databases?",
        "How does LlamaIndex help with building LLM applications?"
    ]

    for i, question in enumerate(demo_questions, 1):
        print(f"\n{i}. Query: {question}")
        print("-" * 50)

        try:
            response = query_engine.query(question)
            print(f"Answer: {response}")

            # Show source information if available
            if hasattr(response, 'source_nodes') and response.source_nodes:
                print(f"\nSources used: {len(response.source_nodes)} chunks")
                for j, node in enumerate(response.source_nodes[:2], 1):  # Show first 2 sources
                    print(f"  Source {j}: {node.text[:100]}...")
        except Exception as e:
            print(f"Error: {e}")

def interactive_mode(query_engine):
    """Interactive query mode"""
    print("\n=== Interactive Mode ===")
    print("Enter your questions (Ctrl+C to exit):")

    try:
        while True:
            user_query = input("\n>>> ")
            if user_query.strip():
                try:
                    response = query_engine.query(user_query)
                    print(f"\nAnswer: {response}")
                except Exception as e:
                    print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nExiting...")

def show_system_info():
    """Show information about the RAG system components"""
    print("\n=== LlamaIndex RAG System Components ===")
    print("• Embedding Model: nomic-embed-text (via Ollama)")
    print("• LLM: gemma3:1b (via Ollama)")
    print("• Vector Store: DuckDB (in-memory)")
    print("• Text Splitter: TokenTextSplitter (64 tokens per chunk)")
    print("• Framework: LlamaIndex")
    print("• Data Source: facts.txt")
    print("• Processing: All local through Ollama")

def main():
    """Main function to run the RAG demo"""
    try:
        # Setup the RAG system
        query_engine = setup_rag_system()

        # Show system information
        show_system_info()

        # Run demo queries
        demo_queries(query_engine)

        # Interactive mode
        interactive_mode(query_engine)

    except Exception as e:
        print(f"Error setting up RAG system: {e}")
        print("\nMake sure you have:")
        print("1. Ollama running: ollama serve")
        print("2. Required models: ollama pull nomic-embed-text && ollama pull gemma3:1b")
        print("3. Required packages: pip install llama-index llama-index-llms-ollama llama-index-embeddings-ollama llama-index-vector-stores-duckdb")

if __name__ == "__main__":
    main()