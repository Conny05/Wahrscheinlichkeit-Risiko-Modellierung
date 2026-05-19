# 📊 Wahrscheinlichkeit & Risiko Modellierung

> **Stochastische Risikomodelle und Monte Carlo-Simulationen in Python**  
> Entwickelt im Rahmen des Mathematikstudiums (B.Sc.) an der Goethe-Universität Frankfurt am Main  
> **Status:** 🟢 Aktiv (2025–heute)

---

## 🎯 Projektübersicht

Dieses Projekt verbindet mathematische Wahrscheinlichkeitstheorie mit praktischer Risikomodellierung. Es implementiert vier eigenständige Risikomodelle, die alle auf stochastischen Simulationen basieren:

| Modul | Methode | Anwendungsbereich |
|---|---|---|
| Monte Carlo (allgemein) | Wiederholte Zufallsstichproben | Beliebige Unsicherheitsquantifizierung |
| Finanzrisiko | VaR, CVaR, Portfolio-Simulation | Verlustabschätzung bei Aktienportfolios |
| Projektrisiko | PERT/CPM-Analyse | Projektdauer- und Kostenrisiko |
| Versicherungsrisiko | Collective Risk Model | Schadenhäufigkeit und Ruinwahrscheinlichkeit |

---

## 📈 Beispielausgaben

### Value at Risk & CVaR – Portfolioverlustverteilung

![VaR und CVaR Simulation](results/var_cvar_simulation.png)

*Die Grafik zeigt die simulierte Verlustverteilung eines Portfolios über 10.000 Monte-Carlo-Pfade. Die vertikalen Linien markieren VaR (95%) und CVaR (95%).*

---

### Monte Carlo – Portfolioentwicklung über Zeit

![Monte Carlo Portfoliopfade](results/monte_carlo_portfolio.png)

*Simulierte Kursentwicklung eines Drei-Aktien-Portfolios (10.000 Pfade, 252 Handelstage). Das Konfidenzband zeigt das 5%- und 95%-Quantil.*

---

### Versicherungsrisiko – Collective Risk Model

![Collective Risk Model](results/insurance_collective_risk.png)

*Schadensummenverteilung nach dem Collective Risk Model: Poisson-verteilte Schadensanzahl (λ=50), exponentialverteilte Schadenshöhe.*

---

### Projektrisiko – PERT-Analyse

![PERT Projektdauer](results/pert_projektdauer.png)

*Simulierte Projektdauerverteilung auf Basis von PERT-Schätzungen. Eingezeichnet: Wahrscheinlichkeit für Termineinhaltung bei gegebenem Deadline.*

---

## 🗂️ Projektstruktur

```
Wahrscheinlichkeit-Risiko-Modellierung/
│
├── modules/
│   ├── monte_carlo.py       # Kern-Monte-Carlo-Engine (allgemein)
│   ├── financial_risk.py    # VaR, CVaR, korrelierte Portfolio-Simulation
│   ├── project_risk.py      # PERT-Analyse, kritischer Pfad
│   └── insurance_risk.py    # Collective Risk Model, Ruinwahrscheinlichkeit
│
├── tests/
│   └── test_models.py       # Unit-Tests für alle Module
│
├── results/                 # Gespeicherte Plots (.png)
├── main.py                  # Führt alle Modelle aus und speichert Grafiken
├── requirements.txt
└── README.md
```

---

## 🚀 Installation & Quickstart

```bash
# 1. Repository klonen
git clone https://github.com/Conny05/Wahrscheinlichkeit-Risiko-Modellierung.git
cd Wahrscheinlichkeit-Risiko-Modellierung

# 2. Abhängigkeiten installieren
pip install -r requirements.txt

# 3. Alle Simulationen ausführen (Grafiken werden in /results/ gespeichert)
python main.py
```

---

## 📦 Verwendete Bibliotheken

| Bibliothek | Zweck |
|---|---|
| `numpy` | Vektorisierte numerische Berechnungen, Zufallszahlen |
| `scipy` | Statistische Verteilungen (Normal, Poisson, Exponential) |
| `matplotlib` | Visualisierungen aller Simulationsergebnisse |
| `pandas` | Datenverarbeitung und strukturierte Ausgabe |

---

## 🧮 Mathematischer Hintergrund

### Value at Risk (VaR) & CVaR

Sei $L$ der Verlust eines Portfolios und $\alpha \in (0,1)$ das Konfidenzniveau. Dann gilt:

$$\text{VaR}_\alpha(L) = \inf\{l \in \mathbb{R} : P(L > l) \leq 1 - \alpha\}$$

$$\text{CVaR}_\alpha(L) = \mathbb{E}[L \mid L \geq \text{VaR}_\alpha(L)]$$

Die Monte-Carlo-Schätzung basiert auf $N = 10{.}000$ simulierten Portfoliorenditen mit korrelierten geometrischen Brownschen Bewegungen.

---

### Collective Risk Model (Versicherung)

Der Gesamtschaden $S$ ergibt sich als Zufallssumme:

$$S = \sum_{i=1}^{N} X_i, \quad N \sim \text{Poisson}(\lambda), \quad X_i \sim \text{Exp}(\mu)$$

Die Ruinwahrscheinlichkeit $\psi(u)$ bei Anfangskapital $u$ wird simulationsbasiert geschätzt.

---

### PERT-Projektdauer

Für jede Aktivität mit optimistischer Dauer $a$, wahrscheinlichster Dauer $m$ und pessimistischer Dauer $b$:

$$\mu = \frac{a + 4m + b}{6}, \qquad \sigma^2 = \left(\frac{b-a}{6}\right)^2$$

Die Gesamtprojektdauer ergibt sich durch Monte-Carlo-Aggregation über den kritischen Pfad.

---

## 👤 Autor

**Bambe Conny**  
B.Sc. Mathematik – Goethe-Universität Frankfurt am Main (4. Semester)  
GitHub: [@Conny05](https://github.com/Conny05)

---

## 📄 Lizenz

MIT License – frei verwendbar und anpassbar.
