"""
tests/test_models.py
--------------------
Einfache Unit-Tests fuer alle Risikomodelle.

Ausfuehren:
    python -m pytest tests/ -v
    oder direkt:
    python tests/test_models.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from models.monte_carlo import monte_carlo_simulation, berechne_kennzahlen
from models.financial_risk import simuliere_aktienkurspfade, berechne_var_cvar
from models.project_risk import simuliere_projekt
from models.insurance_risk import simuliere_gesamtschaden, berechne_pramie


def test_monte_carlo_normal():
    """Testet: Normalverteilungs-Simulation liefert richtige Kennzahlen."""
    werte = monte_carlo_simulation('normal', {'mean': 100, 'std': 15}, n_simulationen=50_000)

    assert len(werte) == 50_000, "Falsche Anzahl Simulationen"
    assert abs(np.mean(werte) - 100) < 1.0,  "Mittelwert weicht zu stark ab"
    assert abs(np.std(werte) - 15)   < 0.5,  "Standardabweichung weicht zu stark ab"
    print("  [OK] monte_carlo_simulation (normal)")


def test_monte_carlo_triangular():
    """Testet: Dreieckverteilung liegt immer zwischen min und max."""
    werte = monte_carlo_simulation('triangular',
                                   {'min': 10, 'most_likely': 20, 'max': 30},
                                   n_simulationen=10_000)
    assert np.all(werte >= 10),  "Werte unter dem Minimum gefunden!"
    assert np.all(werte <= 30),  "Werte ueber dem Maximum gefunden!"
    print("  [OK] monte_carlo_simulation (triangular)")


def test_kennzahlen():
    """Testet: Kennzahlenberechnung liefert plausible Werte."""
    np.random.seed(0)
    werte = np.random.normal(50, 10, 10_000)
    kz = berechne_kennzahlen(werte)

    assert 45 < kz['mittelwert'] < 55,   "Mittelwert ausserhalb Erwartungsbereich"
    assert kz['minimum'] < kz['median'], "Minimum groesser als Median - Fehler!"
    assert kz['median']  < kz['maximum'],"Median groesser als Maximum - Fehler!"
    print("  [OK] berechne_kennzahlen")


def test_aktienkurse_form():
    """Testet: GBM-Simulation hat korrekte Dimensionen und positive Kurse."""
    pfade = simuliere_aktienkurspfade(100, 0.08, 0.20, tage=252, n_simulationen=500)

    assert pfade.shape == (253, 500), f"Falsche Form: {pfade.shape}"
    assert np.all(pfade > 0),         "Negative Aktienkurse - GBM-Fehler!"
    assert np.all(pfade[0] == 100),   "Startpreis ist nicht 100"
    print("  [OK] simuliere_aktienkurspfade")


def test_var_kleiner_cvar():
    """Testet: CVaR muss immer schlechter (kleiner) sein als VaR."""
    np.random.seed(42)
    renditen = np.random.normal(5, 15, 10_000)
    ergebnis = berechne_var_cvar(renditen, investition=10_000, konfidenzniveau=0.95)

    assert ergebnis['cvar_pct'] <= ergebnis['var_pct'], \
        "CVaR muss <= VaR sein (schlechteres Szenario)!"
    assert ergebnis['var_euro'] >= 0,  "VaR in Euro muss nicht-negativ sein"
    assert ergebnis['cvar_euro'] >= 0, "CVaR in Euro muss nicht-negativ sein"
    print("  [OK] berechne_var_cvar (CVaR <= VaR)")


def test_projekt_simulation():
    """Testet: Projektdauer liegt im plausiblen Bereich."""
    dauern, kosten = simuliere_projekt(n_simulationen=5_000)

    # Minimale Summe: alle optimistischen Werte
    min_dauer  = sum(a[1] for a in __import__('models.project_risk',
                     fromlist=['AUFGABEN']).AUFGABEN)
    max_dauer  = sum(a[3] for a in __import__('models.project_risk',
                     fromlist=['AUFGABEN']).AUFGABEN)

    assert np.all(dauern >= min_dauer), "Dauer unter Minimum!"
    assert np.all(dauern <= max_dauer), "Dauer ueber Maximum!"
    assert np.all(kosten > 0),          "Negative Kosten!"
    print("  [OK] simuliere_projekt")


def test_versicherung_pramie():
    """Testet: Praemienberechnung mit Sicherheitszuschlag."""
    schaeden     = simuliere_gesamtschaden(50, 2000, n_simulationen=5_000)
    mean_schaden = np.mean(schaeden)
    pramie       = berechne_pramie(mean_schaden, sicherheitszuschlag=0.20)

    assert pramie > mean_schaden, "Praemie muss groesser als Erwartungsschaden sein!"
    assert abs(pramie / mean_schaden - 1.20) < 0.01, "Sicherheitszuschlag falsch berechnet!"
    print("  [OK] berechne_pramie")


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  UNIT-TESTS  -  Risiko-Modellierung")
    print("=" * 50 + "\n")

    tests = [
        test_monte_carlo_normal,
        test_monte_carlo_triangular,
        test_kennzahlen,
        test_aktienkurse_form,
        test_var_kleiner_cvar,
        test_projekt_simulation,
        test_versicherung_pramie,
    ]

    bestanden = 0
    for test in tests:
        try:
            test()
            bestanden += 1
        except AssertionError as e:
            print(f"  [FAIL] {test.__name__}: {e}")
        except Exception as e:
            print(f"  [ERROR] {test.__name__}: {e}")

    print(f"\n  Ergebnis: {bestanden}/{len(tests)} Tests bestanden")
    print("=" * 50)
