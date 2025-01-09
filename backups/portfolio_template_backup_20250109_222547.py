import os
import matplotlib.pyplot as plt
from fpdf import FPDF
import shutil
from datetime import datetime

# Backup erstellen
current_file_path = __file__
backup_folder = os.path.join(os.path.dirname(current_file_path), "backups")
os.makedirs(backup_folder, exist_ok=True)
backup_file_path = os.path.join(backup_folder, f"portfolio_template_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py")
shutil.copy2(current_file_path, backup_file_path)
print(f"Backup erstellt: {backup_file_path}")

# Portfolio-Name und Basispfad definieren
portfolio_name = "MeinPortfolio"  # Hier den Namen des Portfolios einfügen
base_path = r"C:\Users\jovis\OneDrive\Dokumente\PortfolioProject"

# Unterordner für das Portfolio erstellen
output_folder = os.path.join(base_path, portfolio_name)
os.makedirs(output_folder, exist_ok=True)  # Erstellt den Ordner, falls er nicht existiert

# Datei-Pfad für das PDF
output_path = os.path.join(output_folder, "portfolio_summary_with_tables.pdf")

# Beispiel-Daten
assets = [
    {"name": "Microsoft", "sector": "Technology", "allocation": 20, "div_yield": 0.9, "cagr": 12},
    {"name": "Apple", "sector": "Technology", "allocation": 15, "div_yield": 0.7, "cagr": 10},
    {"name": "Tesla", "sector": "Automotive", "allocation": 10, "div_yield": 0.0, "cagr": 15},
    {"name": "Meta", "sector": "Communication", "allocation": 8, "div_yield": 0.0, "cagr": 11},
    {"name": "Adobe", "sector": "Technology", "allocation": 7, "div_yield": 0.0, "cagr": 9},
    {"name": "iShares Core S&P 500", "sector": "Broad Market", "allocation": 25, "div_yield": 1.5, "cagr": 7},
    {"name": "BOTZ ETF", "sector": "Robotics", "allocation": 15, "div_yield": 0.3, "cagr": 8},
]

# Diagramme erstellen
# Pie Chart: Asset Allocation
fig1, ax1 = plt.subplots()
ax1.pie([a['allocation'] for a in assets], labels=[a['name'] for a in assets], autopct='%1.1f%%', startangle=140)
ax1.set_title('Portfolio Allocation by Assets')
allocation_chart_path = os.path.join(output_folder, "allocation_by_assets.png")
plt.savefig(allocation_chart_path, dpi=600)  # Erhöhte Auflösung
plt.close()

# Bar Chart: Sector Allocation
sector_allocations = {}
for asset in assets:
    sector = asset["sector"]
    sector_allocations[sector] = sector_allocations.get(sector, 0) + asset["allocation"]

fig2, ax2 = plt.subplots()
ax2.bar(sector_allocations.keys(), sector_allocations.values(), color='skyblue')
ax2.set_title('Portfolio Allocation by Sector')
ax2.set_ylabel('Allocation (%)')
plt.xticks(rotation=45)
sector_chart_path = os.path.join(output_folder, "allocation_by_sectors.png")
plt.savefig(sector_chart_path, dpi=600)  # Erhöhte Auflösung
plt.close()

# Line Chart: Value Growth
years = list(range(1, 21))
portfolio_growth = [10000 * (1 + 0.09) ** y for y in years]  # CAGR 9%
benchmark_growth = [10000 * (1 + 0.07) ** y for y in years]  # CAGR 7%

fig3, ax3 = plt.subplots()
ax3.plot(years, portfolio_growth, label='Portfolio', marker='o')
ax3.plot(years, benchmark_growth, label='Benchmark (S&P 500)', marker='x')
ax3.set_title('Cumulative Value Growth')
ax3.set_xlabel('Years')
ax3.set_ylabel('Value (USD)')
ax3.legend()
growth_chart_path = os.path.join(output_folder, "value_growth.png")
plt.savefig(growth_chart_path, dpi=600)  # Erhöhte Auflösung
plt.close()

# PDF-Erstellung starten
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", size=12)

# Legende hinzufügen
pdf.set_font("Arial", style="B", size=12)  # Anpassung an Aktien und ETFs
pdf.cell(0, 10, "Legende", ln=True)
pdf.set_font("Arial", size=10)
pdf.cell(0, 8, "Allok.: Anteil des Assets im Portfolio", ln=True)
pdf.cell(0, 8, "Div. Yld: Jährliche Dividendenrendite in %", ln=True)
pdf.cell(0, 8, "CAGR: Ø Jährliche Rendite (Compound Annual Growth Rate)", ln=True)
pdf.ln(5)

# Funktion zum Hinzufügen einer Tabelle
def add_table(title, data):
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 10, title, ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(60, 8, "Asset", border=1, align="C")
    pdf.cell(30, 8, "Allok.", border=1, align="C")
    pdf.cell(40, 8, "Div. Yld", border=1, align="C")
    pdf.cell(40, 8, "CAGR", border=1, align="C")
    pdf.ln()
    for asset in data:
        pdf.cell(60, 8, asset["name"], border=1)
        pdf.cell(30, 8, f"{asset['allocation']}%", border=1, align="C")
        pdf.cell(40, 8, f"{asset['div_yield']}%", border=1, align="C")
        pdf.cell(40, 8, f"{asset['cagr']}%", border=1, align="C")
        pdf.ln()
    pdf.ln(5)

# Aktien- und ETF-Daten filtern
stocks = [asset for asset in assets if asset["sector"] != "Broad Market"]
etfs = [asset for asset in assets if asset["sector"] == "Broad Market"]

# Tabellen hinzufügen
add_table("Aktien", stocks)
add_table("ETFs", etfs)

# Diagramme ins PDF einfügen
pdf.add_page()
pdf.set_font("Arial", style="B", size=12)
pdf.cell(0, 10, "Portfolio Allocation by Assets", ln=True)
pdf.image(allocation_chart_path, x=50, y=40, w=100)

pdf.add_page()
pdf.set_font("Arial", style="B", size=12)
pdf.cell(0, 10, "Portfolio Allocation by Sector", ln=True)
pdf.image(sector_chart_path, x=50, y=40, w=100)

pdf.add_page()
pdf.set_font("Arial", style="B", size=12)
pdf.cell(0, 10, "Cumulative Value Growth", ln=True)
pdf.image(growth_chart_path, x=50, y=40, w=100)

# PDF speichern
pdf.output(output_path)
print(f"PDF gespeichert unter: {output_path}")
