import azure.functions as func
import logging
from report_generator import create_ai_report

# Skapar en HTTP-app som bara kan triggas med en hemlig nyckel (FUNCTION) eller av er
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="generate_report")
def generate_report_http(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Startar generering av AI-rapport på begäran (On-Demand)...")

    try:
        rapport_text = create_ai_report()
        return func.HttpResponse(
            rapport_text,
            status_code=200,
            mimetype="text/markdown; charset=utf-8"
        )
    except Exception as e:
        logging.error(f"Fel vid rapportgenerering: {str(e)}")
        return func.HttpResponse(
            f"Ett fel uppstod: {str(e)}",
            status_code=500
        )