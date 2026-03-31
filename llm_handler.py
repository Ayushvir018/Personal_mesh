import requests
import json

def ask_llm(prompt, max_tokens=300, temperature=0.7):
    """Send prompt to local LLM (LM Studio) and get response"""
    url = "http://10.21.70.156:1234/v1/completions"
    
    data = {
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['text'].strip()
            else:
                return "Error: No response from model"
        else:
            return f"Error: Status {response.status_code}"
            
    except requests.exceptions.ConnectionError:
        return "Error: LM Studio is not running. Please start the server."
    except requests.exceptions.Timeout:
        return "Error: Request timed out. Model might be too slow."
    except Exception as e:
        return f"Error: {e}"


def ask_about_memories(question, memories):
    """
    Ask LLM a question with memory context
    
    Args:
        question: User's question
        memories: List of memory tuples from database
    
    Returns:
        LLM's response
    """
    
    # Build context from memories
    if not memories:
        return "I don't have any memories to answer this question."
    
    context = "Here are your relevant memories:\n\n"
    
    for mem in memories[:10]:  # Limit to 10 most relevant
        # mem = (id, content, timestamp, user_id, type, priority, tags)
        context += f"- [{mem[2]}] {mem[1]} (Type: {mem[4]}, Priority: {mem[5]})\n"
    
    # Build the full prompt
    prompt = f"""{context}

Based on the above memories, answer this question:
{question}

Answer concisely and naturally. If the memories don't contain enough information, say so.

Answer:"""
    
    return ask_llm(prompt, max_tokens=400, temperature=0.7)