from embedding import search_similar
from openai import OpenAI

client = OpenAI(
    base_url="http://10.21.70.156:1234/v1",
    api_key="lm-studio"
)

def ask_personal_mesh(question):
    # Step 1: Semantic search
    results = search_similar(question, n_results=5)
    memories = results['documents'][0]
    
    # Step 2: Also fetch memories by type from SQLite
    import sqlite3
    conn = sqlite3.connect("memories.db")
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM memories WHERE type = 'project'")
    project_rows = cursor.fetchall()
    conn.close()
    
    project_memories = [row[0] for row in project_rows]
    
    # Step 3: Combine both
    all_memories = list(set(memories + project_memories))
    
    # Step 4: Build context
    context = "\n".join([f"- {mem}" for mem in all_memories])
    
    # Step 3: Better prompt
    system_prompt = """You are Ayush's personal AI assistant. 
You have access to his personal memories, projects, achievements, and life events.
Rules:
- Answer only based on the provided memories
- Be specific and personal, not generic
- Keep answers concise and to the point
- If information is not in memories, say "I don't have that memory yet"
- Speak as if you know Ayush personally"""

    user_prompt = f"""Personal memories:
{context}

Question: {question}"""

    response = client.chat.completions.create(
        model="local-model",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=300
    )
    
    return response.choices[0].message.content