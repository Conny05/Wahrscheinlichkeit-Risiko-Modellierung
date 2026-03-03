"""
main.py
-------
Hauptskript - führt alle Risikomodelle aus.
Ausfuehren: python main.py
"""

import os
os.makedirs("results", exist_ok=True)

print("=" * 60)
print("  WAHRSCHEINLICHKEIT & RISIKO-MODELLIERUNG")
print("  Monte Carlo Simulationen in Python")
print("=" * 60)

from modules.financial_risks  import finanzrisiko_analyse
from modules.projekt_risks    import projektrisiko_analyse
from modules.insurance_risks  import versicherungsrisiko_analyse

finanzrisiko_analyse()
projektrisiko_analyse()
versicherungsrisiko_analyse()

print("\n  FERTIG! Alle Simulationen abgeschlossen.")
```

**Schritt 3** – **"Commit changes"** klicken

---

**Schritt 4** – Nochmal **"Add file"** → **"Create new file"**

**Name:** `requirements.txt`

**Inhalt:**
```
numpy>=1.24.0
scipy>=1.10.0
matplotlib>=3.7.0
pandas>=2.0.0
