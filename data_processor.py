import pandas as pd

def analyze_financial_data(csv_path="ekonomi.csv"):
    # 1. Läs in CSV-filen till en Pandas DataFrame (tabell)
    df = pd.read_csv(csv_path)
    
    # 2. Räkna ut avvikelse i kronor och procent för varje rad
    df["Avvikelse_KR"] = df["Utfall"] - df["Budget"]
    df["Avvikelse_Procent"] = ((df["Avvikelse_KR"] / df["Budget"]) * 100).round(1)
    
    # 3. Räkna ut övergripande KPI:er (Intäkter, Kostnader, Resultat)
    intakter_utfall = df[df["Typ"] == "Intäkt"]["Utfall"].sum()
    intakter_budget = df[df["Typ"] == "Intäkt"]["Budget"].sum()
    
    kostnader_utfall = df[df["Typ"] == "Kostnad"]["Utfall"].sum()
    kostnader_budget = df[df["Typ"] == "Kostnad"]["Budget"].sum()
    
    resultat_utfall = intakter_utfall - kostnader_utfall
    resultat_budget = intakter_budget - kostnader_budget
    
    # 4. Bygg en tydlig textsammanfattning som AI:n enkelt kan läsa
    summary = f"""
=== ÖVERGRIPANDE KPI:ER ===
Totala intäkter: {intakter_utfall} kr (Budget: {intakter_budget} kr)
Totala kostnader: {kostnader_utfall} kr (Budget: {kostnader_budget} kr)
Resultat (Vinst): {resultat_utfall} kr (Budget: {resultat_budget} kr)

=== DETALJERAD TABELL PER KATEGORI ===
{df.to_string(index=False)}
"""
    return summary

# Gör så att du kan testa filen separat genom att köra: python data_processor.py
if __name__ == "__main__":
    print("Testkör datamotorn...")
    print(analyze_financial_data())