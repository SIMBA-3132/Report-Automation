import os
import time
from google import genai
from dotenv import load_dotenv

# 1. Ladda in variabler från .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Hittade ingen GEMINI_API_KEY i .env-filen!")

client = genai.Client(api_key=api_key)

# 2. Hämta en sorterad lista med ALLA rena textmodeller på ditt konto
def get_available_text_models():
    exclude_keywords = ["tts", "vision", "image", "embedding", "aqa", "audio", "thinking", "learnlm"]
    
    models = []
    for m in client.models.list():
        name = m.name.lower()
        if "gemini" in name and "generateContent" in m.supported_actions:
            if not any(bad_word in name for bad_word in exclude_keywords):
                models.append(m.name)
    
    # Sortera så att 3.8 och flash-modeller ligger först i kön
    models.sort(key=lambda x: ("3.8" in x, "flash" in x), reverse=True)
    return models

# 3. Funktion som testar modellerna en efter en om någon är överbelastad (503)
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
            print(f"⚠️ {model_name} var upptagen eller gav fel ({type(e).__name__}). Byter direkt till nästa...")
            time.sleep(1) # Kort paus på 1 sekund innan nästa modell testas
            
    raise RuntimeError("Alla modeller var tillfälligt upptagna. Vänta en minut och kör igen.")

# 4. Fiktiv data (detta byter vi mot CSV/Excel i nästa steg)
fiktiv_data = """
Försäljning: 150 000 kr (Budget: 120 000 kr)
Serverkostnader: 45 000 kr (Budget: 30 000 kr)
Marknadsföring: 20 000 kr (Budget: 25 000 kr)
"""

prompt = f"""
Du är en ekonomisk analytiker. Analysera följande data för månaden. 
Identifiera vad som gått bra och vilka avvikelser som är oroande. 
Skriv en kort, professionell sammanfattning till ledningsgruppen.

Data:
{fiktiv_data}
"""

# 5. Kör rapportgeneratorn
print("Hämtar analys från Gemini...\n")
rapport = generate_report_safely(prompt)
print(rapport)