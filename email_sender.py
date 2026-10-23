import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import markdown
from dotenv import load_dotenv

load_dotenv()

def format_as_html(markdown_text: str) -> str:
    """Omvandlar rå Markdown-text (### och **) till en snygg HTML-sida/mejl."""
    html_body = markdown.markdown(markdown_text)
    dagens_datum = datetime.now().strftime("%Y-%m-%d")
    
    return f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #2c3e50; max-width: 750px; margin: 20px auto; padding: 20px; background-color: #f4f7f6; }}
            .card {{ background: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); }}
            h1 {{ color: #1a365d; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }}
            h3 {{ color: #2b6cb0; margin-top: 25px; }}
            li {{ margin-bottom: 8px; }}
            .footer {{ margin-top: 30px; font-size: 12px; color: #718096; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>📊 Ekonomisk Månadsrapport ({dagens_datum})</h1>
            {html_body}
            <div class="footer">Genererad automatiskt med Python, Pandas & Gemini AI i Microsoft Azure</div>
        </div>
    </body>
    </html>
    """

def send_report_email(markdown_text: str) -> bool:
    """Skickar rapporten som ett snyggt HTML-mejl."""
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receivers_raw = os.getenv("EMAIL_RECEIVER")

    if not sender or not password or not receivers_raw:
        print("⚠️ Mejlvariabler saknas i .env/Azure. Hoppar över mejlutskick.")
        return False

    receivers = [r.strip() for r in receivers_raw.split(",")]
    dagens_datum = datetime.now().strftime("%Y-%m-%d")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"📊 Ekonomisk AI-Månadsrapport ({dagens_datum})"
    msg["From"] = sender
    msg["To"] = ", ".join(receivers)

    # Lägg till både råtext (reserv) och snygg HTML
    html_content = format_as_html(markdown_text)
    msg.attach(MIMEText(markdown_text, "plain", "utf-8"))
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    # Skicka via Gmails säkra SMTP-server
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, receivers, msg.as_string())

    print(f"📧 Rapporten har mejlats till: {', '.join(receivers)}!")
    return True

# Testblock så att Person B kan testa mejlet direkt i terminalen!
if __name__ == "__main__":
    test_text = "### Testrapport\nDetta är ett **test** med snygg formatering!"
    send_report_email(test_text)