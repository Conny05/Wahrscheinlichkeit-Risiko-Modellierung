"""
project_risk.py
---------------
Projektrisiko-Modellierung: Zeitplan & Kosten

Was wird hier modelliert?
    In realen Projekten wissen wir nie genau, wie lange eine Aufgabe dauert
    oder was sie kostet. Wir schaetzen stattdessen:
        - Optimistische Dauer (bestes Szenario)
        - Wahrscheinlichste Dauer (normaler Fall)
        - Pessimistische Dauer (schlechtestes Szenario)

    Die PERT-Methode (Program Evaluation and Review Technique) nutzt diese
    drei Schaetzungen, um eine Wahrscheinlichkeitsverteilung zu berechnen.

    Mit Monte Carlo simulieren wir tausende Projektverlaeufe und erhalten:
        - Wahrscheinlichkeit der Termineinhaltung
        - Erwartete Gesamtdauer und -kosten
        - Konfidenzintervalle fuer die Planung
"""

import numpy as np
import matplotlib.pyplot as plt


# ── Projektstruktur definieren ────────────────────────────────────────────────
# Jede Aufgabe hat: Name, optimist. Dauer, wahrscheinl. Dauer, pessimist. Dauer (in Tagen)
# sowie: optimist. Kosten, wahrscheinl. Kosten, pessimist. Kosten (in Euro)

AUFGABEN = [
    # (Name,           t_min, t_wahrsch, t_max,  k_min,   k_wahrsch, k_max)
    ("Anforderungsanalyse",    3,   5,    8,    2_000,   3_000,   5_000),
    ("System-Design",          5,   8,   14,    4_000,   6_000,  10_000),
    ("Implementierung",       15,  25,   40,   15_000,  20_000,  35_000),
    ("Testing & QA",           5,   8,   15,    5_000,   7_000,  12_000),
    ("Deployment",             2,   3,    6,    1_500,   2_500,   5_000),
    ("Dokumentation",          3,   5,    9,    2_000,   3_500,   6_000),
]


def simuliere_projekt(n_simulationen=10_000):
    """
    Simuliert Projektdauer und -kosten mit Dreieckverteilungen.

    Fuer jede Aufgabe wird eine Dreieckverteilung (min, wahrscheinlichst, max)
    verwendet - dies ist das Standard-PERT-Modell.

    Rueckgabe:
    ---------
    gesamtdauer  : numpy array - Simulierte Gesamtdauern in Tagen
    gesamtkosten : numpy array - Simulierte Gesamtkosten in Euro
    """
    np.random.seed(42)

    # Arrays fuer Ergebnisse initialisieren
    gesamtdauer  = np.zeros(n_simulationen)
    gesamtkosten = np.zeros(n_simulationen)

    for aufgabe in AUFGABEN:
        name, t_min, t_ml, t_max, k_min, k_ml, k_max = aufgabe

        # Dauer simulieren (Dreieckverteilung)
        dauer = np.random.triangular(t_min, t_ml, t_max, size=n_simulationen)

        # Kosten simulieren (Dreieckverteilung)
        kosten = np.random.triangular(k_min, k_ml, k_max, size=n_simulationen)

        gesamtdauer  += dauer
        gesamtkosten += kosten

    return gesamtdauer, gesamtkosten


def projektrisiko_analyse(speicherpfad="results/projektrisiko.png"):
    """
    Vollstaendige Projektrisiko-Analyse mit Visualisierung.
    """
    print("\n" + "=" * 60)
    print("  PROJEKTRISIKO-ANALYSE  (PERT + Monte Carlo)")
    print("=" * 60)

    # Geplante Werte (Summe der wahrscheinlichsten Schaetzungen)
    geplante_dauer  = sum(a[2] for a in AUFGABEN)   # wahrscheinlichste Dauern
    geplantes_budget = sum(a[5] for a in AUFGABEN)  # wahrscheinlichste Kosten

    print(f"\n  Geplante Dauer:   {geplante_dauer} Tage")
    print(f"  Geplantes Budget: {geplantes_budget:,.0f} Euro")
    print(f"\n  Aufgaben im Projekt:")
    for a in AUFGABEN:
        print(f"    {a[0]:<25} {a[2]:>3} Tage  |  {a[5]:>7,.0f} Euro")

    # Simulation durchfuehren
    dauern, kosten = simuliere_projekt(n_simulationen=10_000)

    # Kennzahlen berechnen
    p50_dauer  = np.percentile(dauern, 50)
    p80_dauer  = np.percentile(dauern, 80)
    p50_kosten = np.percentile(kosten, 50)
    p80_kosten = np.percentile(kosten, 80)

    prob_termin  = np.mean(dauern <= geplante_dauer) * 100
    prob_budget  = np.mean(kosten <= geplantes_budget) * 100

    print(f"\n  SIMULATIONSERGEBNISSE:")
    print(f"  {'─'*40}")
    print(f"  Dauer  P50 (Median):  {p50_dauer:.1f} Tage")
    print(f"  Dauer  P80:           {p80_dauer:.1f} Tage")
    print(f"  Kosten P50 (Median):  {p50_kosten:,.0f} Euro")
    print(f"  Kosten P80:           {p80_kosten:,.0f} Euro")
    print(f"\n  Wahrsch. Termineinhaltung ({geplante_dauer} Tage):  {prob_termin:.1f}%")
    print(f"  Wahrsch. Budgeteinhaltung ({geplantes_budget:,.0f} Euro):  {prob_budget:.1f}%")

    # Visualisierung
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: Projektdauer
    ax1 = axes[0]
    ax1.hist(dauern, bins=60, color='steelblue', edgecolor='white', alpha=0.8, density=True)
    ax1.axvline(geplante_dauer, color='red',    linewidth=2, linestyle='--',
                label=f'Geplant: {geplante_dauer} Tage')
    ax1.axvline(p50_dauer,      color='green',  linewidth=2,
                label=f'P50: {p50_dauer:.0f} Tage')
    ax1.axvline(p80_dauer,      color='orange', linewidth=2,
                label=f'P80: {p80_dauer:.0f} Tage')
    ax1.set_title(f'Projektdauer\n(Termineinhaltung: {prob_termin:.1f}%)', fontweight='bold')
    ax1.set_xlabel('Gesamtdauer (Tage)')
    ax1.set_ylabel('Haeufigkeitsdichte')
    ax1.legend()
    ax1.grid(alpha=0.3)

    # Plot 2: Projektkosten
    ax2 = axes[1]
    ax2.hist(kosten / 1000, bins=60, color='coral', edgecolor='white', alpha=0.8, density=True)
    ax2.axvline(geplantes_budget / 1000, color='red',    linewidth=2, linestyle='--',
                label=f'Geplant: {geplantes_budget/1000:.0f}k Euro')
    ax2.axvline(p50_kosten / 1000,       color='green',  linewidth=2,
                label=f'P50: {p50_kosten/1000:.0f}k Euro')
    ax2.axvline(p80_kosten / 1000,       color='orange', linewidth=2,
                label=f'P80: {p80_kosten/1000:.0f}k Euro')
    ax2.set_title(f'Projektkosten\n(Budgeteinhaltung: {prob_budget:.1f}%)', fontweight='bold')
    ax2.set_xlabel('Gesamtkosten (Tausend Euro)')
    ax2.set_ylabel('Haeufigkeitsdichte')
    ax2.legend()
    ax2.grid(alpha=0.3)

    plt.suptitle('Projektrisiko-Analyse - Monte Carlo Simulation', fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig(speicherpfad, dpi=150, bbox_inches='tight')
    print(f"\n  Grafik gespeichert: {speicherpfad}")
    plt.close()
