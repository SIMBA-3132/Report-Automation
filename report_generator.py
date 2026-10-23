import os
import time
from datetime import datetime
from google import genai
from google.genai import types
from dotenv import load_dotenv
from data_processor import analyze_financial_data

load_dotenv()

def get_available_text_models(client):
    exclude_keywords = ["tts", "vision", "image", "embedding", "aqa", "audio", "thinking", "learnlm", "2.5", "2.0", "1.5"]
    models = []
    for m in client.models.list():
        name = m.name.lower()
        if "gemini" in name and "generateContent" in m.supported_actions:
            if not any(bad_word in name for bad_word in exclude_keywords):
                models.append(m.name)
    models.sort(key=lambda x: ("lite" in x, "3.8" in x, "flash" in x), reverse=True)
    return models

def generate_report_safely(client, prompt_text):
    candidate_models = get_available_text_models(client)
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
            print(f"⚠️ {model_name} var upptagen ({type(e).__name__}). Byter direkt...")
            time.sleep(0.5)
    raise RuntimeError("Alla modeller var tillfälligt upptagna.")

def create_ai_report():
    """Huvudfunktion som kan anropas både lokalt och från Azure Functions."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Hittade ingen GEMINI_API_KEY!")

    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(timeout=10000)
    )

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
    return generate_report_safely(client, prompt)

# Om du kör "python report_generator.py" lokalt på datorn körs detta block:
if __name__ == "__main__":
    print("Kör rapporten lokalt...")
    rapport_text = create_ai_report()
    dagens_datum = datetime.now().strftime("%Y-%m-%d")
    filnamn = f"manadsrapport_{dagens_datum}.md"
    with open(filnamn, "w", encoding="utf-8") as f:
        f.write(rapport_text)
    print(rapport_text)
    print(f"\n📄 Rapporten har sparats lokalt som: {filnamn}")