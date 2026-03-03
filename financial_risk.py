"""
financial_risk.py
-----------------
Finanzrisikomodelle: Value at Risk (VaR), CVaR, Portfolio-Simulation

Wichtige Begriffe:
    VaR (Value at Risk):
        "Mit 95% Wahrscheinlichkeit verliere ich NICHT mehr als X Euro."
        Stellt den maximalen Verlust bei einem gegebenen Konfidenzniveau dar.

    CVaR (Conditional VaR / Expected Shortfall):
        "Im schlimmsten 5% der Fälle verliere ich im Durchschnitt Y Euro."
        Realistischer als VaR, weil er das Tail-Risiko erfasst.
"""

import numpy as np
import matplotlib.pyplot as plt


def simuliere_aktienkurspfade(startpreis, mu, sigma, tage=252, n_simulationen=10_000):
    """
    Simuliert Aktienkurspfade mit dem Geometric Brownian Motion (GBM) Modell.

    Das GBM-Modell ist das Standardmodell fuer Aktienkurse.
    Formel: S(t+1) = S(t) * exp((mu - 0.5*sigma^2)*dt + sigma*sqrt(dt)*Z)

    Parameter:
    ----------
    startpreis     : float - Aktueller Aktienkurs (z.B. 100 Euro)
    mu             : float - Erwartete jaehrliche Rendite (z.B. 0.08 = 8%)
    sigma          : float - Jaehrliche Volatilitaet (z.B. 0.20 = 20%)
    tage           : int   - Simulationshorizont in Handelstagen (252 = 1 Jahr)
    n_simulationen : int   - Anzahl der Simulationspfade

    Rueckgabe:
    ---------
    numpy array der Form (tage+1, n_simulationen) mit allen Kurspfaden
    """
    dt = 1 / 252  # Zeitschritt: 1 Handelstag
    np.random.seed(42)

    zufallswerte = np.random.normal(0, 1, size=(tage, n_simulationen))

    taegliche_renditen = np.exp(
        (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * zufallswerte
    )

    kurspfade = np.zeros((tage + 1, n_simulationen))
    kurspfade[0] = startpreis

    for t in range(1, tage + 1):
        kurspfade[t] = kurspfade[t - 1] * taegliche_renditen[t - 1]

    return kurspfade


def berechne_var_cvar(renditen_pct, investition, konfidenzniveau=0.95):
    """
    Berechnet Value at Risk (VaR) und Conditional VaR (CVaR).

    Parameter:
    ----------
    renditen_pct    : numpy array - Portfolio-Jahresrenditen in %
    investition     : float       - Investiertes Kapital in Euro
    konfidenzniveau : float       - z.B. 0.95 fuer 95%

    Rueckgabe:
    ---------
    Dictionary mit VaR und CVaR in Prozent und Euro
    """
    alpha = (1 - konfidenzniveau) * 100

    var_pct  = np.percentile(renditen_pct, alpha)
    tail     = renditen_pct[renditen_pct <= var_pct]
    cvar_pct = np.mean(tail)

    return {
        'var_pct':         var_pct,
        'var_euro':        abs(var_pct) / 100 * investition,
        'cvar_pct':        cvar_pct,
        'cvar_euro':       abs(cvar_pct) / 100 * investition,
        'konfidenzniveau': konfidenzniveau,
    }


def finanzrisiko_analyse(speicherpfad="results/finanzrisiko.png"):
    """
    Vollstaendige Finanzrisikoanalyse: Aktienkurse simulieren, VaR & CVaR berechnen.
    """
    print("\n" + "=" * 60)
    print("  FINANZRISIKO-ANALYSE  (GBM + VaR + CVaR)")
    print("=" * 60)

    startpreis  = 100.0
    investition = 10_000
    mu          = 0.08
    sigma       = 0.20
    n_sims      = 10_000
    tage        = 252

    print(f"\n  Startpreis:    {startpreis:.2f} Euro")
    print(f"  Investition:   {investition:,.0f} Euro")
    print(f"  Erw. Rendite:  {mu*100:.1f}% p.a.")
    print(f"  Volatilitaet:  {sigma*100:.1f}% p.a.")
    print(f"  Simulationen:  {n_sims:,}")

    kurspfade = simuliere_aktienkurspfade(startpreis, mu, sigma, tage, n_sims)
    endkurse  = kurspfade[-1]
    renditen  = (endkurse - startpreis) / startpreis * 100

    rk = berechne_var_cvar(renditen, investition, konfidenzniveau=0.95)

    print(f"\n  ERGEBNISSE (95% Konfidenzniveau):")
    print(f"  {'─'*40}")
    print(f"  VaR  (95%):  {rk['var_pct']:+.2f}%  ->  {rk['var_euro']:,.0f} Euro")
    print(f"  CVaR (95%):  {rk['cvar_pct']:+.2f}%  ->  {rk['cvar_euro']:,.0f} Euro")
    print(f"\n  Mit 95% Wahrscheinlichkeit verlierst du NICHT mehr als {rk['var_euro']:,.0f} Euro.")
    print(f"  Im schlimmsten 5% der Faelle: durchschn. Verlust {rk['cvar_euro']:,.0f} Euro.")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    ax1 = axes[0]
    for i in range(200):
        ax1.plot(kurspfade[:, i], color='steelblue', alpha=0.05, linewidth=0.5)
    ax1.plot(np.mean(kurspfade, axis=1), color='red', linewidth=2, label='Mittelwert')
    ax1.axhline(startpreis, color='black', linestyle='--', linewidth=1, label='Startpreis')
    ax1.set_title('Simulierte Aktienkurspfade (GBM)', fontweight='bold')
    ax1.set_xlabel('Handelstage')
    ax1.set_ylabel('Kurs (Euro)')
    ax1.legend()
    ax1.grid(alpha=0.3)

    ax2 = axes[1]
    ax2.hist(renditen, bins=70, color='steelblue', edgecolor='white', alpha=0.8, density=True)
    ax2.axvline(rk['var_pct'],  color='orange', linewidth=2, label=f"VaR 95%: {rk['var_pct']:.1f}%")
    ax2.axvline(rk['cvar_pct'], color='red',    linewidth=2, linestyle='--',
                label=f"CVaR 95%: {rk['cvar_pct']:.1f}%")
    ax2.fill_betweenx([0, 0.025], np.min(renditen), rk['var_pct'],
                      color='red', alpha=0.15, label='Tail (5%)')
    ax2.set_title('Renditeverteilung mit VaR & CVaR', fontweight='bold')
    ax2.set_xlabel('Jahresrendite (%)')
    ax2.set_ylabel('Haeufigkeitsdichte')
    ax2.legend(fontsize=9)
    ax2.grid(alpha=0.3)

    plt.suptitle('Finanzrisiko-Analyse - Monte Carlo Simulation', fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig(speicherpfad, dpi=150, bbox_inches='tight')
    print(f"\n  Grafik gespeichert: {speicherpfad}")
    plt.close()

    return rk
