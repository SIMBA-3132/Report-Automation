import os
import time
from datetime import datetime
from google import genai
from dotenv import load_dotenv
from data_processor import analyze_financial_data  # <-- Importerar Person B:s kod!

# 1. Ladda in variabler från .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Hittade ingen GEMINI_API_KEY i .env-filen!")

client = genai.Client(api_key=api_key)

# 2. Hämta tillgängliga textmodeller
def get_available_text_models():
    exclude_keywords = ["tts", "vision", "image", "embedding", "aqa", "audio", "thinking", "learnlm"]
    models = []
    for m in client.models.list():
        name = m.name.lower()
        if "gemini" in name and "generateContent" in m.supported_actions:
            if not any(bad_word in name for bad_word in exclude_keywords):
                models.append(m.name)
    models.sort(key=lambda x: ("3.8" in x, "flash" in x), reverse=True)
    return models

# 3. Generera rapport med fallback
def generate_report_safely(prompt_text):
    candidate_models = get_available_text_models()
    for model_name in candidate_models:
        try:
            print(f"Provar modell: {model_name}...")
            response = client.models.generate_content(
                model=model_name,
                contents=prompt_text
            )
            if response.text:
                print(f"✅ Lyckades med {model_name}!\n")
                return response.text
        except Exception as e:
            print(f"⚠️ {model_name} var upptagen ({type(e).__name__}). Byter till nästa...")
            time.sleep(1)
    raise RuntimeError("Alla modeller var tillfälligt upptagna.")

# 4. Hämta den uträknade datan från Person B:s Pandas-modul
print("Läser in och analyserar ekonomi.csv med Pandas...")
beraknad_data = analyze_financial_data("ekonomi.csv")

prompt = f"""
Du är en senior ekonomisk analytiker. Analysera följande månadsdata som har 
sammanställts från vårt ekonomisystem.

Uppgift:
1. Ge en kort Executive Summary av det totala resultatet jämfört med budget.
2. Lyft fram de starkaste positiva prestationerna.
3. Varna tydligt för poster där kostnaderna dragit iväg eller intäkterna svikit (ange både kr och %).
4. Ge 2 konkreta rekommendationer till ledningsgruppen för nästa månad.

Dataunderlag:
{beraknad_data}
"""

# 5. Kör AI-analysen och spara till en rapportfil
print("Hämtar analys från Gemini...\n")
rapport_text = generate_report_safely(prompt)

# Spara resultatet i en Markdown-fil med dagens datum
dagens_datum = datetime.now().strftime("%Y-%m-%d")
filnamn = f"manadsrapport_{dagens_datum}.md"

with open(filnamn, "w", encoding="utf-8") as f:
    f.write(rapport_text)

print(rapport_text)
print(f"\n📄 Rapporten har sparats som: {filnamn}")