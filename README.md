# 📊 Wahrscheinlichkeit & Risiko Modellierung

> Monte Carlo-Simulationen und stochastische Risikomodelle in Python  
> **Status:** 🟢 Laufend (2025–heute)

---

## 🎯 Projektübersicht

Dieses Projekt implementiert verschiedene Methoden zur Risikomodellierung und -quantifizierung:

- **Monte Carlo-Simulationen** zur Abschätzung von Unsicherheiten
- **Value at Risk (VaR)** für Finanzportfolios
- **Stochastische Projektplanung** (PERT/CPM)
- **Versicherungsrisikomodelle** (Collective Risk Model)
- **Allgemeine Risikoverteilungen** und statistische Analyse

---

## 📁 Projektstruktur

```
risk-modelling/
│
├── models/
│   ├── monte_carlo.py          # Kern-Monte-Carlo-Engine
│   ├── financial_risk.py       # VaR, CVaR, Portfolio-Risiko
│   ├── project_risk.py         # Projektzeit- & Kostenrisiko
│   └── insurance_risk.py       # Versicherungsrisikomodelle
│
├── notebooks/
│   └── beispiele.ipynb         # Jupyter Notebook mit Beispielen
│
├── results/                    # Gespeicherte Simulationsergebnisse
├── tests/
│   └── test_models.py          # Unit-Tests
│
├── main.py                     # Hauptskript – alle Modelle ausführen
├── requirements.txt
└── README.md
```

---

## 🚀 Installation & Quickstart

```bash
# 1. Repository klonen
git clone https://github.com/DEIN-USERNAME/risk-modelling.git
cd risk-modelling

# 2. Abhängigkeiten installieren
pip install -r requirements.txt

# 3. Alle Simulationen ausführen
python main.py
```

---

## 📦 Verwendete Bibliotheken

| Bibliothek | Zweck |
|------------|-------|
| `numpy` | Numerische Berechnungen |
| `scipy` | Statistische Verteilungen |
| `matplotlib` | Visualisierungen |
| `pandas` | Datenverarbeitung |

---

## 🧮 Modelle im Überblick

### 1. Monte Carlo Simulation (Allgemein)
Schätzt Ergebnisverteilungen durch wiederholte Zufallsstichproben.

### 2. Finanzrisiken
- **VaR (Value at Risk):** Maximaler Verlust bei gegebenem Konfidenzniveau
- **CVaR (Conditional VaR):** Erwarteter Verlust im schlimmsten Fall
- **Portfolio-Simulation:** Mehrere Aktien mit Korrelation

### 3. Projektrisiken
- **PERT-Analyse:** Schätzung von Projektdauer und -kosten
- **Kritischer Pfad:** Wahrscheinlichkeit der Termineinhaltung

### 4. Versicherungsrisiken
- **Collective Risk Model:** Schadenanzahl × Schadenhöhe
- **Ruin-Wahrscheinlichkeit:** Simulationsbasierte Risikoabschätzung

---

## 📈 Beispielausgaben

Nach dem Ausführen von `main.py` werden Grafiken gespeichert in `/results/`.

---

## 👤 Autor

**Dein Name**  
GitHub: [@Conny05](https://github.com/dein-username)

---

## 📄 Lizenz

MIT License – frei verwendbar und anpassbar.
