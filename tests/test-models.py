# Tests fuer alle Risikomodelle
# Ausführen: python tests/test_models.py

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from modules.monte_carlo import monte_carlo_simulation, berechne_kennzahlen

def test_monte_carlo_normal():
    werte = monte_carlo_simulation(
        'normal', {'mean': 100, 'std': 15}, n_simulationen=10_000
    )
    assert len(werte) == 10_000
    assert abs(np.mean(werte) - 100) < 1.0
    print("  [OK] monte_carlo_simulation (normal)")

def test_kennzahlen():
    np.random.seed(0)
    werte = np.random.normal(50, 10, 10_000)
    kz = berechne_kennzahlen(werte)
    assert kz['minimum'] < kz['median'] < kz['maximum']
    print("  [OK] berechne_kennzahlen")

if __name__ == "__main__":
    print("\n" + "="*50)
    print("  UNIT-TESTS  -  Risiko-Modellierung")
    print("="*50 + "\n")
    test_monte_carlo_normal()
    test_kennzahlen()
    print("\n  Alle Tests bestanden! ")
