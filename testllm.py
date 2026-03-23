import requests
import json

def ask_local_llm(prompt, max_tokens=200, temperature=0.7):
    """Send prompt to LM Studio and get response"""
    url = "http://10.21.70.156:1234/v1/completions"
    
    data = {
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    
    try:
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['text'].strip()
            else:
                return "Error: No response from model"
        else:
            return f"Error: Status {response.status_code}"
            
    except Exception as e:
        return f"Connection error: {e}"


# Test it
if __name__ == "__main__":
    print("=== Local LLM Test ===\n")
    
    # Test 1: Simple question
    q1 = "What is Python?"
    print(f"Q: {q1}")
    print(f"A: {ask_local_llm(q1)}\n")
    
    # Test 2: Code generation
    q2 = "Write a Python function to add two numbers"
    print(f"Q: {q2}")
    print(f"A: {ask_local_llm(q2)}\n")