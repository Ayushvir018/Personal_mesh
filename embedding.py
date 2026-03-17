from sentence_transformers import SentenceTransformer
import chromadb

model=SentenceTransformer('all-MiniLM-L6-v2')
client=chromadb.PersistentClient(path="./chroma_db")
collection=client.get_or_create_collection(name="memories")


def add_embedding(memory_id,content):
    embedding=model.encode(content).tolist()
    collection.add(
        ids=str(memory_id),
        embeddings=[embedding],
        documents=[content]
    )

def search_similar(query, n_results=3):
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    return results