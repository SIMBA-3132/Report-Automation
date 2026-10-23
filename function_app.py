import azure.functions as func
import logging
from report_generator import create_ai_report
from email_sender import send_report_email, format_as_html

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="generate_report")
def generate_report_http(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Startar generering av AI-rapport på begäran (On-Demand)...")

    try:
        # 1. Generera AI-rapporten (Markdown)
        rapport_markdown = create_ai_report()
        
        # 2. Försök skicka rapporten på mejl
        email_skickat = send_report_email(rapport_markdown)
        
        # 3. Gör om råtexten till en snygg HTML-sida för webbläsaren
        html_sida = format_as_html(rapport_markdown)
        
        status_banner = "<p style='text-align:center; color:green;'><b>✅ Rapporten har även skickats till era mejladresser!</b></p>" if email_skickat else "<p style='text-align:center; color:orange;'><b>ℹ️ Rapporten visas nedan (E-post ej konfigurerat i Azure än).</b></p>"
        
        return func.HttpResponse(
            status_banner + html_sida,
            status_code=200,
            mimetype="text/html; charset=utf-8"
        )
    except Exception as e:
        logging.error(f"Fel vid rapportgenerering: {str(e)}")
        return func.HttpResponse(
            f"Ett fel uppstod: {str(e)}",
            status_code=500
        )