import google.generativeai as genai

genai.configure(api_key="AIzaSyBB9KRk95nUVBG6lu1BrXcHOrA53KrlLYQ")

print("Listing supported models:")
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)
