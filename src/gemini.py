import google.generativeai as GenAi
import os, json, sys


class GeminiAI:
    def __init__(self, api_key: str):
        GenAi.configure(api_key=api_key)
        self.model = GenAi.GenerativeModel("gemini-1.5-flash")

    def get_text_response(self, prompt: str):
        response = self.model.generate_content(prompt)
        return response.text
    

