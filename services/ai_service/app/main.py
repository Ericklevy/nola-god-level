from fastapi import FastAPI
import os
import google.generativeai as genai

app = FastAPI(title="Nola AI Service")

# Configura a API Key
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("ALERTA: GEMINI_API_KEY não configurada.")
    genai = None
else:
    genai.configure(api_key=API_KEY)


@app.get("/")
def ai_root():
    return {"message": "Serviço de IA para Nola"}

@app.post("/generate-insight")
async def generate_insight(prompt: str):
    if not genai:
         return {"error": "API Key do Gemini não está configurada."}, 500
         
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return {"insight": response.text}
    except Exception as e:
        return {"error": str(e)}, 500