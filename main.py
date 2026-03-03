"""
main.py
-------
Hauptskript - fuehrt alle Risikomodelle nacheinander aus.

Ausfuehren:
    python main.py

Ergebnisse werden gespeichert in: results/
"""

import os
import sys

# Ausgabeverzeichnis erstellen
os.makedirs("results", exist_ok=True)

print("=" * 60)
print("  WAHRSCHEINLICHKEIT & RISIKO-MODELLIERUNG")
print("  Monte Carlo Simulationen in Python")
print("=" * 60)
print(f"\n  Alle Ergebnisse werden gespeichert in: results/\n")

# ── 1. Allgemeine Monte Carlo Demo ──────────────────────────────
print("\n[1/3] Lade Finanzrisiko-Modell...")
from models.financial_risk import finanzrisiko_analyse
finanzrisiko_analyse(speicherpfad="results/finanzrisiko.png")

# ── 2. Projektrisiken ────────────────────────────────────────────
print("\n[2/3] Lade Projektrisiko-Modell...")
from models.project_risk import projektrisiko_analyse
projektrisiko_analyse(speicherpfad="results/projektrisiko.png")

# ── 3. Versicherungsrisiken ──────────────────────────────────────
print("\n[3/3] Lade Versicherungsrisiko-Modell...")
from models.insurance_risk import versicherungsrisiko_analyse
versicherungsrisiko_analyse(speicherpfad="results/versicherungsrisiko.png")

# ── Abschluss ─────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  FERTIG! Alle Simulationen abgeschlossen.")
print("  Gespeicherte Grafiken:")
print("    results/finanzrisiko.png")
print("    results/projektrisiko.png")
print("    results/versicherungsrisiko.png")
print("=" * 60)
