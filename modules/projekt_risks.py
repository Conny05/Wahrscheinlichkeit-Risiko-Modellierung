"""
project_risk.py
---------------
Projektrisiko-Modellierung: Zeitplan & Kosten

Fuer jede Aufgabe schätzen wir:
    - Optimistische Dauer (bestes Szenario)
    - Wahrscheinlichste Dauer (normaler Fall)
    - Pessimistische Dauer (schlechtestes Szenario)
"""

import numpy as np
import matplotlib.pyplot as plt

AUFGABEN = [
    # (Name, t_min, t_wahrsch, t_max, k_min, k_wahrsch, k_max)
    ("Anforderungsanalyse",  3,  5,  8,  2000,  3000,  5000),
    ("System-Design",        5,  8, 14,  4000,  6000, 10000),
    ("Implementierung",     15, 25, 40, 15000, 20000, 35000),
    ("Testing & QA",         5,  8, 15,  5000,  7000, 12000),
    ("Deployment",           2,  3,  6,  1500,  2500,  5000),
    ("Dokumentation",        3,  5,  9,  2000,  3500,  6000),
]


def simuliere_projekt(n_simulationen=10_000):
    """
    Simuliert Projektdauer und -kosten mit Dreieckverteilungen.

    Rueckgabe:
    ---------
    gesamtdauer  : numpy array - Simulierte Gesamtdauern in Tagen
    gesamtkosten : numpy array - Simulierte Gesamtkosten in Euro
    """
    np.random.seed(42)

    gesamtdauer  = np.zeros(n_simulationen)
    gesamtkosten = np.zeros(n_simulationen)

    for aufgabe in AUFGABEN:
        name, t_min, t_ml, t_max, k_min, k_ml, k_max = aufgabe

        # Dauer simulieren
        dauer  = np.random.triangular(t_min, t_ml, t_max, size=n_simulationen)

        # Kosten simulieren
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

    geplante_dauer   = sum(a[2] for a in AUFGABEN)
    geplantes_budget = sum(a[5] for a in AUFGABEN)

    print(f"\n  Geplante Dauer:   {geplante_dauer} Tage")
    print(f"  Geplantes Budget: {geplantes_budget:,.0f} Euro")

    dauern, kosten = simuliere_projekt(n_simulationen=10_000)

    p50_dauer  = np.percentile(dauern, 50)
    p80_dauer  = np.percentile(dauern, 80)
    p50_kosten = np.percentile(kosten, 50)
    p80_kosten = np.percentile(kosten, 80)

    prob_termin = np.mean(dauern <= geplante_dauer)  * 100
    prob_budget = np.mean(kosten <= geplantes_budget) * 100

    print(f"\n  SIMULATIONSERGEBNISSE:")
    print(f"  {'─'*40}")
    print(f"  Dauer  P50:  {p50_dauer:.1f} Tage")
    print(f"  Dauer  P80:  {p80_dauer:.1f} Tage")
    print(f"  Kosten P50:  {p50_kosten:,.0f} Euro")
    print(f"  Kosten P80:  {p80_kosten:,.0f} Euro")
    print(f"\n  Termineinhaltung:  {prob_termin:.1f}%")
    print(f"  Budgeteinhaltung:  {prob_budget:.1f}%")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    ax1 = axes[0]
    ax1.hist(dauern, bins=60, color='steelblue',
             edgecolor='white', alpha=0.8, density=True)
    ax1.axvline(geplante_dauer, color='red',    linewidth=2, linestyle='--',
                label=f'Geplant: {geplante_dauer} Tage')
    ax1.axvline(p50_dauer,      color='green',  linewidth=2,
                label=f'P50: {p50_dauer:.0f} Tage')
    ax1.axvline(p80_dauer,      color='orange', linewidth=2,
                label=f'P80: {p80_dauer:.0f} Tage')
    ax1.set_title(f'Projektdauer\n(Termineinhaltung: {prob_termin:.1f}%)',
                  fontweight='bold')
    ax1.set_xlabel('Gesamtdauer (Tage)')
    ax1.set_ylabel('Haeufigkeitsdichte')
    ax1.legend()
    ax1.grid(alpha=0.3)

    ax2 = axes[1]
    ax2.hist(kosten / 1000, bins=60, color='coral',
             edgecolor='white', alpha=0.8, density=True)
    ax2.axvline(geplantes_budget / 1000, color='red',    linewidth=2,
                linestyle='--', label=f'Geplant: {geplantes_budget/1000:.0f}k Euro')
    ax2.axvline(p50_kosten / 1000,       color='green',  linewidth=2,
                label=f'P50: {p50_kosten/1000:.0f}k Euro')
    ax2.axvline(p80_kosten / 1000,       color='orange', linewidth=2,
                label=f'P80: {p80_kosten/1000:.0f}k Euro')
    ax2.set_title(f'Projektkosten\n(Budgeteinhaltung: {prob_budget:.1f}%)',
                  fontweight='bold')
    ax2.set_xlabel('Gesamtkosten (Tausend Euro)')
    ax2.set_ylabel('Haeufigkeitsdichte')
    ax2.legend()
    ax2.grid(alpha=0.3)

    plt.suptitle('Projektrisiko-Analyse - Monte Carlo Simulation',
                 fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig(speicherpfad, dpi=150, bbox_inches='tight')
    print(f"\n  Grafik gespeichert: {speicherpfad}")
    plt.close()
