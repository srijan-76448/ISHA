import os, json, sys
import google.generativeai as genai

mainDir = "C:/Users/bhoja/OneDrive/Desktop/Projects/ISHA/src"
credentials = dict(json.load(open(os.path.join(mainDir, 'credentials.json'), 'r'))["gemini"])
settings = dict(dict(json.load(open(os.path.join(mainDir, 'settings.json'), 'r'))["genAI-config"])['GeminiAI'])

genai.configure(api_key=credentials["api-key"])

model = genai.GenerativeModel(
    model_name=credentials["model-name"],
    generation_config=settings,
)

chat_session = model.start_chat(history=[])
response = chat_session.send_message("essay on AI")

print(response.text)