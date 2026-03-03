"""
monte_carlo.py
--------------
Allgemeine Monte Carlo Simulationsengine.

Was ist Monte Carlo?
    Monte Carlo ist eine Methode, bei der wir ein Zufallsexperiment
    sehr oft wiederholen (z.B. 10.000 Mal) und aus den Ergebnissen
    statistische Schluesse ziehen.

Beispiel: Wie hoch ist die Wahrscheinlichkeit, dass ein Projekt
          ueber Budget laeuft? -> 10.000 Mal simulieren & zaehlen!
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def monte_carlo_simulation(verteilung, parameter, n_simulationen=10_000):
    """
    Fuehrt eine einfache Monte Carlo Simulation durch.

    Parameter:
    ----------
    verteilung    : str  - Art der Zufallsverteilung
                          ('normal', 'uniform', 'triangular', 'lognormal')
    parameter     : dict - Parameter der Verteilung
    n_simulationen: int  - Anzahl der Simulationen (Standard: 10.000)

    Rueckgabe:
    ---------
    numpy array mit den simulierten Werten
    """

    np.random.seed(42)  # Seed fuer Reproduzierbarkeit

    if verteilung == 'normal':
        # Normalverteilung: symmetrisch um den Mittelwert
        ergebnisse = np.random.normal(
            loc=parameter['mean'],
            scale=parameter['std'],
            size=n_simulationen
        )

    elif verteilung == 'uniform':
        # Gleichverteilung: alle Werte zwischen min und max gleich wahrscheinlich
        ergebnisse = np.random.uniform(
            low=parameter['min'],
            high=parameter['max'],
            size=n_simulationen
        )

    elif verteilung == 'triangular':
        # Dreieckverteilung: typisch fuer Projektschaetzungen
        ergebnisse = np.random.triangular(
            left=parameter['min'],
            mode=parameter['most_likely'],
            right=parameter['max'],
            size=n_simulationen
        )

    elif verteilung == 'lognormal':
        # Lognormalverteilung: fuer Groessen die nicht negativ sein koennen
        ergebnisse = np.random.lognormal(
            mean=parameter['mean'],
            sigma=parameter['sigma'],
            size=n_simulationen
        )

    else:
        raise ValueError(f"Unbekannte Verteilung: {verteilung}")

    return ergebnisse


def berechne_kennzahlen(simulierte_werte, konfidenzniveau=0.95):
    """
    Berechnet wichtige statistische Kennzahlen.

    Parameter:
    ----------
    simulierte_werte  : numpy array - Ergebnisse der Simulation
    konfidenzniveau   : float       - z.B. 0.95 fuer 95% Konfidenz

    Rueckgabe:
    ---------
    Dictionary mit allen Kennzahlen
    """
    kennzahlen = {
        'mittelwert': np.mean(simulierte_werte),
        'median':     np.median(simulierte_werte),
        'std':        np.std(simulierte_werte),
        'minimum':    np.min(simulierte_werte),
        'maximum':    np.max(simulierte_werte),
        'P95':        np.percentile(simulierte_werte, 95),
        'P5':         np.percentile(simulierte_werte, 5),
    }
    return kennzahlen


def visualisiere_simulation(simulierte_werte, titel="Monte Carlo Simulation",
                            xlabel="Wert", schwellenwert=None, speicherpfad=None):
    """
    Erstellt ein Histogramm der Simulationsergebnisse.

    Parameter:
    ----------
    simulierte_werte : numpy array - Simulationsergebnisse
    titel            : str         - Titel des Diagramms
    xlabel           : str         - Beschriftung der X-Achse
    schwellenwert    : float       - Optional: Markierung einer Grenze
    speicherpfad     : str         - Optional: Pfad zum Speichern
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Histogramm zeichnen
    ax.hist(simulierte_werte, bins=60, color='steelblue',
            edgecolor='white', alpha=0.8, density=True, label='Simulationen')

    # Normalverteilung als Referenzkurve
    mu, sigma = np.mean(simulierte_werte), np.std(simulierte_werte)
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 300)
    ax.plot(x, stats.norm.pdf(x, mu, sigma), 'orange', linewidth=2,
            label='Normalverteilung')

    # Mittelwert markieren
    ax.axvline(mu, color='red', linestyle='--', linewidth=1.5,
               label=f'Mittelwert: {mu:.2f}')

    # P5 und P95 markieren
    p5  = np.percentile(simulierte_werte, 5)
    p95 = np.percentile(simulierte_werte, 95)
    ax.axvline(p5,  color='green', linestyle=':', linewidth=1.5,
               label=f'P5: {p5:.2f}')
    ax.axvline(p95, color='green', linestyle=':', linewidth=1.5,
               label=f'P95: {p95:.2f}')

    # Schwellenwert markieren
    if schwellenwert is not None:
        ax.axvline(schwellenwert, color='black', linestyle='-', linewidth=2,
                   label=f'Schwellenwert: {schwellenwert:.2f}')
        prob = np.mean(simulierte_werte > schwellenwert) * 100
        ax.text(0.98, 0.95, f'Ueberschreitungswahrsch.: {prob:.1f}%',
                transform=ax.transAxes, ha='right', va='top', fontsize=11,
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    ax.set_title(titel, fontsize=14, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel('Haeufigkeitsdichte', fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()

    if speicherpfad:
        plt.savefig(speicherpfad, dpi=150, bbox_inches='tight')
    else:
        plt.show()

    plt.close()
