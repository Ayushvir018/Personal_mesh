import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyBB9KRk95nUVBG6lu1BrXcHOrA53KrlLYQ")
model = genai.GenerativeModel('gemini-2.0-flash')

try:
    response = model.generate_content("Hello, are you working?")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
