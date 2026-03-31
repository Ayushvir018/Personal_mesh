from voice_input import voice_to_text

print("Speak for 5 seconds after this message...")
text = voice_to_text(duration=5)
print(f"You said: {text}")
