from openai import OpenAI
from embedding import search_similar
import sqlite3

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key="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"
)

def ask_personal_mesh(question, user_id="ayush"):
    # Step 1: Semantic search
    results = search_similar(question, n_results=5, user_id=user_id)
    memories = results['documents'][0]
    
    # Step 2: Fetch user-specific memories from SQLite
    conn = sqlite3.connect("memories.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT content FROM memories WHERE user_id = ?",
        (user_id,)
    )
    user_rows = cursor.fetchall()
    conn.close()
    
    user_memories = [row[0] for row in user_rows]
    
    # Step 3: Combine both
    all_memories = list(set(memories + user_memories))
    
    # Step 4: Build context
    context = "\n".join([f"- {mem}" for mem in all_memories])
    
    # Step 5: Ask Groq
    prompt = f"""You are a personal AI assistant for {user_id}.

Personal memories of {user_id}:
{context if context.strip() else "No memories found for this user yet."}

STRICT RULES:
- Answer ONLY based on provided memories
- If no memories exist, say exactly: "I don't have any memories about you yet. Please add some memories first."
- NEVER make up or assume information
- NEVER hallucinate facts about the user

Question: {question}"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.7
    )
    
    return response.choices[0].message.content