📊 Serverless AI-Driven Financial Reporting System

Ett automatiserat, molnbaserat rapporteringssystem som bearbetar finansiell rådata, beräknar budgetavvikelser med Pandas och genererar beslutsunderlag på ledningsgruppsnivå via Google Gemini AI. Systemet är driftsatt som en serverlös mikrotjänst i Microsoft Azure Functions och levererar färdigformaterade HTML-rapporter både direkt i webbläsaren (On-Demand) och via automatiska e-postutskick (SMTP).

🏗️ Systemarkitektur & Dataflöde

[ekonomi.csv] 
      │
      ▼
[data_processor.py] ──► Beräknar KPI:er, totalt resultat & budgetavvikelser (kr / %) via Pandas
      │
      ▼
[report_generator.py] ──► Anropar Gemini API med automatisk Model Fallback & 10s Timeout
      │
      ▼
[email_sender.py] ──► Konverterar Markdown till responsiv HTML & skickar via Gmail SMTP (SSL)
      │
      ▼
[function_app.py] ──► Exponerar flödet som en Serverless HTTP Trigger i Microsoft Azure


🚀 Huvudfunktioner

Automatiserad Databearbetning (ETL): Läser in strukturerad bokföringsdata (.csv), separerar intäkter och kostnader samt beräknar faktiska avvikelser mot budget i både kronor och procent med hjälp av pandas.

Hög tillgänglighet med AI Model Fallback: Implementerar dynamisk modellselektion mot Google Gemini API (google-genai). Om en primär AI-modell upplever hög belastning eller överskrider tidsgränsen (10 sekunders timeout) växlar systemet automatiskt till nästa tillgängliga lättviktsmodell utan att krascha.

Serverless Cloud Computing: Driftsatt i Microsoft Azure Functions (Flex Consumption Plan) på Linux. Arkitekturen skalar automatiskt ned till noll (Scale-to-Zero) när inga rapporter genereras, vilket ger minimal driftkostnad.

Dubbel Leveranskanal (HTML & E-post): Konverterar AI-genererad Markdown till stilren HTML/CSS. Vid anrop till molnlänken visas rapporten direkt i webbläsaren samtidigt som den distribueras till berörda intressenter via krypterad SMTP.

🛠️ Teknisk Stack

Kategori

Teknologi

Programmeringsspråk

Python 3.12

Molnplattform

Microsoft Azure Functions (Serverless HTTP Trigger)

AI & LLM

Google Gemini API (google-genai SDK)

Dataanalys

Pandas

Rapportering & Distribution

Markdown, HTML/CSS, smtplib (Gmail SSL)

Versionshantering & Säkerhet

Git, GitHub, python-dotenv, Azure Environment Variables

📂 Projektstruktur

Report-Automation/
├── data_processor.py      # Pandas-modul för aggregering och avvikelseanalys
├── report_generator.py    # AI-integration, prompt engineering och fallback-logik
├── email_sender.py        # HTML-rendering och automatiserat SMTP-utskick
├── function_app.py        # Azure Functions HTTP-endpoint (molnets startpunkt)
├── ekonomi.csv            # Finansiellt dataunderlag (Intäkter, Kostnader, Budget, Utfall)
├── requirements.txt       # Projektets Python-beroenden
├── host.json              # Konfigurationsfil för Azure Functions v2
├── .funcignore            # Exkluderar lokala filer vid molndriftsättning
└── .gitignore             # Skyddar API-nycklar (.env), virtuell miljö och lokala rapporter


⚙️ Installation & Lokal Körning

Följ dessa steg för att köra projektet lokalt på din egen maskin:

1. Klona repot och skapa en virtuell miljö

git clone <https://github.com/SIMBA-3132/Report-Automation.git>
cd Report-Automation
python -m venv venv

# Aktivera miljön (Windows):
venv\Scripts\activate
# Aktivera miljön (Mac/Linux):
source venv/bin/activate


2. Installera beroenden

pip install -r requirements.txt


3. Konfigurera miljövariabler (.env)

Skapa en fil med namnet .env i projektets rotmapp och lägg in dina uppgifter:

GEMINI_API_KEY="din_gemini_api_nyckel"
EMAIL_SENDER="din.adress@gmail.com"
EMAIL_PASSWORD="ditt_16_siffriga_app_losenord"
EMAIL_RECEIVER="mottagare1@gmail.com, mottagare2@gmail.com"


4. Kör rapportgeneratorn

python report_generator.py


Detta genererar rapporten i terminalen, sparar en lokal kopia (manadsrapport_YYYY-MM-DD.md) och skickar ut rapporten som ett HTML-formaterat e-postmeddelande.

☁️ Molndriftsättning (Microsoft Azure)

Projektet är förberett för direkt driftsättning till Azure Functions via VS Code:

Skapa en Function App i Azure Portal (Flex Consumption, Linux, Python 3.11/3.12).

Lägg in variablerna från .env under Settings -> Environment variables i Azure Portal.

Använd tillägget Azure Functions i VS Code, högerklicka på din Function App och välj Deploy to Function App....