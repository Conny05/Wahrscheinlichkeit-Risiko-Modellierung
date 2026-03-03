"""
insurance_risk.py
-----------------
Versicherungsrisikomodelle: Collective Risk Model

Was wird hier modelliert?
    Ein Versicherungsunternehmen zahlt im Laufe eines Jahres viele Schaeden.
    Das Collective Risk Model beschreibt den GESAMTSCHADEN S als:

        S = X1 + X2 + ... + X_N

    wobei:
        N = zufaellige Anzahl der Schaeden (z.B. Poissonverteilt)
        Xi = zufaellige Hoehe des i-ten Schadens (z.B. Exponentialverteilt)

    Mit Monte Carlo koennen wir berechnen:
        - Erwarteter Gesamtschaden
        - Wahrscheinlichkeit, dass die Ruecklage reicht
        - Benoetiger Sicherheitspuffer (Ruin-Wahrscheinlichkeit)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def simuliere_gesamtschaden(lambda_schaeden, mean_schadenshoehe,
                             n_simulationen=10_000):
    """
    Simuliert den Jahres-Gesamtschaden nach dem Collective Risk Model.

    Parameter:
    ----------
    lambda_schaeden   : float - Erwartete Anzahl der Schaeden pro Jahr
                                (Parameter der Poisson-Verteilung)
    mean_schadenshoehe: float - Mittlere Schadenshoehe in Euro
                                (Parameter der Exponentialverteilung)
    n_simulationen    : int   - Anzahl der Simulationen

    Rueckgabe:
    ---------
    numpy array mit simulierten Gesamtschaeden
    """
    np.random.seed(42)
    gesamtschaeden = np.zeros(n_simulationen)

    for i in range(n_simulationen):
        # Schritt 1: Wie viele Schaeden gibt es in diesem Jahr?
        n_schaeden = np.random.poisson(lambda_schaeden)

        # Schritt 2: Wie hoch ist jeder einzelne Schaden?
        if n_schaeden > 0:
            einzelschaeden = np.random.exponential(mean_schadenshoehe, size=n_schaeden)
            gesamtschaeden[i] = np.sum(einzelschaeden)
        else:
            gesamtschaeden[i] = 0.0  # Kein Schaden in diesem Jahr

    return gesamtschaeden


def berechne_pramie(erwarteter_schaden, sicherheitszuschlag=0.20):
    """
    Berechnet die Netto-Praemie nach dem Aequivalenzprinzip.

    Die Pramie muss den erwarteten Schaden PLUS einen Sicherheitszuschlag decken.

    Parameter:
    ----------
    erwarteter_schaden  : float - Mittlerer simulierter Gesamtschaden
    sicherheitszuschlag : float - z.B. 0.20 fuer 20% Aufschlag (Standard: 20%)

    Rueckgabe:
    ---------
    Nettopraemie in Euro
    """
    return erwarteter_schaden * (1 + sicherheitszuschlag)


def versicherungsrisiko_analyse(speicherpfad="results/versicherungsrisiko.png"):
    """
    Vollstaendige Versicherungsrisikoanalyse.
    """
    print("\n" + "=" * 60)
    print("  VERSICHERUNGSRISIKO-ANALYSE  (Collective Risk Model)")
    print("=" * 60)

    # ── Parameter ────────────────────────────────────────────────
    lambda_schaeden    = 50      # Erwartete Schaeden pro Jahr
    mean_schadenshoehe = 2_000   # Mittlere Schadenshoehe in Euro
    ruecklage          = 120_000 # Vorhandene Ruecklage in Euro
    n_sims             = 10_000

    erwarteter_gesamtschaden = lambda_schaeden * mean_schadenshoehe

    print(f"\n  Erwartete Schaeden/Jahr:  {lambda_schaeden}")
    print(f"  Mittlere Schadenshoehe:   {mean_schadenshoehe:,.0f} Euro")
    print(f"  Erw. Gesamtschaden:       {erwarteter_gesamtschaden:,.0f} Euro")
    print(f"  Vorhandene Ruecklage:     {ruecklage:,.0f} Euro")
    print(f"  Simulationen:             {n_sims:,}")

    # ── Simulation ────────────────────────────────────────────────
    gesamtschaeden = simuliere_gesamtschaden(lambda_schaeden, mean_schadenshoehe, n_sims)

    # ── Kennzahlen ────────────────────────────────────────────────
    mean_sim   = np.mean(gesamtschaeden)
    std_sim    = np.std(gesamtschaeden)
    p95        = np.percentile(gesamtschaeden, 95)
    p99        = np.percentile(gesamtschaeden, 99)
    ruin_prob  = np.mean(gesamtschaeden > ruecklage) * 100
    pramie     = berechne_pramie(mean_sim, sicherheitszuschlag=0.20)

    print(f"\n  SIMULATIONSERGEBNISSE:")
    print(f"  {'─'*40}")
    print(f"  Mittl. Gesamtschaden:  {mean_sim:,.0f} Euro")
    print(f"  Standardabweichung:    {std_sim:,.0f} Euro")
    print(f"  95%-Quantil (P95):     {p95:,.0f} Euro")
    print(f"  99%-Quantil (P99):     {p99:,.0f} Euro")
    print(f"\n  Ruin-Wahrscheinlichkeit: {ruin_prob:.2f}%")
    print(f"  (Schaden > Ruecklage von {ruecklage:,.0f} Euro)")
    print(f"\n  Empfohlene Jahrespraemie (+20%): {pramie:,.0f} Euro")

    # ── Visualisierung ────────────────────────────────────────────
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: Verteilung der Gesamtschaeden
    ax1 = axes[0]
    ax1.hist(gesamtschaeden / 1000, bins=70, color='steelblue',
             edgecolor='white', alpha=0.8, density=True, label='Simulationen')
    ax1.axvline(ruecklage / 1000, color='red',    linewidth=2.5, linestyle='--',
                label=f'Ruecklage: {ruecklage/1000:.0f}k Euro')
    ax1.axvline(mean_sim  / 1000, color='green',  linewidth=2,
                label=f'Mittelwert: {mean_sim/1000:.0f}k Euro')
    ax1.axvline(p95       / 1000, color='orange', linewidth=2, linestyle=':',
                label=f'P95: {p95/1000:.0f}k Euro')

    # Ruin-Bereich markieren
    x_max = np.max(gesamtschaeden) / 1000
    ax1.axvspan(ruecklage / 1000, x_max, color='red', alpha=0.1,
                label=f'Ruin-Bereich ({ruin_prob:.1f}%)')

    ax1.set_title('Gesamtschaden-Verteilung\n(Collective Risk Model)', fontweight='bold')
    ax1.set_xlabel('Gesamtschaden (Tausend Euro)')
    ax1.set_ylabel('Haeufigkeitsdichte')
    ax1.legend(fontsize=9)
    ax1.grid(alpha=0.3)

    # Plot 2: Schadensanzahl-Verteilung (Poisson)
    ax2 = axes[1]
    # Schadensanzahlen aus der Poisson-Verteilung simulieren
    np.random.seed(42)
    schadensanzahlen = np.random.poisson(lambda_schaeden, size=n_sims)
    unique, counts   = np.unique(schadensanzahlen, return_counts=True)

    ax2.bar(unique, counts / n_sims * 100, color='coral',
            edgecolor='white', alpha=0.8)
    ax2.axvline(lambda_schaeden, color='red', linewidth=2, linestyle='--',
                label=f'Lambda = {lambda_schaeden}')
    ax2.set_title('Schadensanzahl pro Jahr\n(Poisson-Verteilung)', fontweight='bold')
    ax2.set_xlabel('Anzahl der Schaeden')
    ax2.set_ylabel('Haeufigkeit (%)')
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)

    plt.suptitle('Versicherungsrisiko-Analyse - Monte Carlo Simulation',
                 fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig(speicherpfad, dpi=150, bbox_inches='tight')
    print(f"\n  Grafik gespeichert: {speicherpfad}")
    plt.close()
