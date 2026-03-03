"""
insurance_risk.py
-----------------
Versicherungsrisikomodelle: Collective Risk Model

Das Collective Risk Model beschreibt den Gesamtschaden S als:
    S = X1 + X2 + ... + X_N

    N  = zufällige Anzahl der Schäden (Poisson-verteilt)
    Xi = zufällige Höhe des i-ten Schadens (Exponential-verteilt)
"""

import numpy as np
import matplotlib.pyplot as plt


def simuliere_gesamtschaden(lambda_schäden, mean_schadenshöhe,
                             n_simulationen=10_000):
    """
    Simuliert den Jahres-Gesamtschaden.

    Parameter:
    ----------
    lambda_schäden    : float - Erwartete Anzahl Schäden pro Jahr
    mean_schadenshöhe : float - Mittlere Schadenshöhe in Euro
    n_simulationen     : int   - Anzahl der Simulationen

    Rueckgabe:
    ---------
    numpy array mit simulierten Gesamtschaeden
    """
    np.random.seed(42)
    gesamtschäden = np.zeros(n_simulationen)

    for i in range(n_simulationen):
        # Schritt 1: Wie viele Schäden gibt es in diesem Jahr?
        n_schäden = np.random.poisson(lambda_schäden)

        # Schritt 2: Wie hoch ist jeder einzelne Schaden?
        if n_schäden > 0:
            einzelschäden = np.random.exponential(
                mean_schadenshöhe, size=n_schäden
            )
            gesamtschäden[i] = np.sum(einzelschäden)
        else:
            gesamtschäden[i] = 0.0

    return gesamtschäden


def berechne_pramie(erwarteter_schaden, sicherheitszuschlag=0.20):
    """
    Berechnet die Netto-Praemie.

    Parameter:
    ----------
    erwarteter_schaden  : float - Mittlerer Gesamtschaden
    sicherheitszuschlag : float - z.B. 0.20 fuer 20% Aufschlag

    Rueckgabe:
    ---------
    Nettopraemie in Euro
    """
    return erwarteter_schaden * (1 + sicherheitszuschlag)


def versicherungsrisiko_analyse(speicherpfad="results/versicherungsrisiko.png"):
    """
    Vollständige Versicherungsrisikoanalyse.
    """
    print("\n" + "=" * 60)
    print("  VERSICHERUNGSRISIKO-ANALYSE  (Collective Risk Model)")
    print("=" * 60)

    lambda_schäden    = 50
    mean_schadenshöhe = 2_000
    rücklage          = 120_000
    n_sims             = 10_000

    print(f"\n  Erwartete Schäden/Jahr: {lambda_schäden}")
    print(f"  Mittlere Schadenshoehe:   {mean_schadenshöhe:,.0f} Euro")
    print(f"  Vorhandene Ruecklage:     {rücklage:,.0f} Euro")

    gesamtschäden = simuliere_gesamtschaden(
        lambda_schäden, mean_schadenshöhe, n_sims
    )

    mean_sim  = np.mean(gesamtschäden)
    std_sim   = np.std(gesamtschäden)
    p95       = np.percentile(gesamtschäden, 95)
    p99       = np.percentile(gesamtschäden, 99)
    ruin_prob = np.mean(gesamtschäden > rücklage) * 100
    pramie    = berechne_pramie(mean_sim, sicherheitszuschlag=0.20)

    print(f"\n  SIMULATIONSERGEBNISSE:")
    print(f"  {'─'*40}")
    print(f"  Mittl. Gesamtschaden:  {mean_sim:,.0f} Euro")
    print(f"  Standardabweichung:    {std_sim:,.0f} Euro")
    print(f"  P95:                   {p95:,.0f} Euro")
    print(f"  P99:                   {p99:,.0f} Euro")
    print(f"\n  Ruin-Wahrscheinlichkeit:  {ruin_prob:.2f}%")
    print(f"  Empfohlene Jahrespraemie: {pramie:,.0f} Euro")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    ax1 = axes[0]
    ax1.hist(gesamtschäden / 1000, bins=70, color='steelblue',
             edgecolor='white', alpha=0.8, density=True)
    ax1.axvline(rücklage / 1000, color='red',    linewidth=2.5,
                linestyle='--', label=f'Ruecklage: {ruecklage/1000:.0f}k Euro')
    ax1.axvline(mean_sim  / 1000, color='green',  linewidth=2,
                label=f'Mittelwert: {mean_sim/1000:.0f}k Euro')
    ax1.axvline(p95       / 1000, color='orange', linewidth=2,
                linestyle=':', label=f'P95: {p95/1000:.0f}k Euro')
    ax1.axvspan(ruecklage / 1000, np.max(gesamtschaeden) / 1000,
                color='red', alpha=0.1, label=f'Ruin ({ruin_prob:.1f}%)')
    ax1.set_title('Gesamtschaden-Verteilung', fontweight='bold')
    ax1.set_xlabel('Gesamtschaden (Tausend Euro)')
    ax1.set_ylabel('Häufigkeitsdichte')
    ax1.legend(fontsize=9)
    ax1.grid(alpha=0.3)

    ax2 = axes[1]
    np.random.seed(42)
    anzahlen        = np.random.poisson(lambda_schäden, size=n_sims)
    unique, counts  = np.unique(anzahlen, return_counts=True)
    ax2.bar(unique, counts / n_sims * 100, color='coral', edgecolor='white', alpha=0.8)
    ax2.axvline(lambda_schäden, color='red', linewidth=2,
                linestyle='--', label=f'Lambda = {lambda_schäden}')
    ax2.set_title('Schadensanzahl pro Jahr\n(Poisson-Verteilung)', fontweight='bold')
    ax2.set_xlabel('Anzahl der Schäden')
    ax2.set_ylabel('Häufigkeit (%)')
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)

    plt.suptitle('Versicherungsrisiko-Analyse - Monte Carlo Simulation',
                 fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig(speicherpfad, dpi=150, bbox_inches='tight')
    print(f"\n  Grafik gespeichert: {speicherpfad}")
    plt.close()
