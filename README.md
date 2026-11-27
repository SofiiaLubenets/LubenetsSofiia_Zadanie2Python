# Zadanie 2 – Python program

Aplikácia v Pythone (Tkinter + Matplotlib) na výpočet podľa vzorca z oblasti priemyslu.

## Čo program robí
1. Vygeneruje pole 60 náhodných hodnôt.
2. Spracuje pole: zoradenie, priemer, minimum a maximum.
3. Vypočíta hodnoty podľa zvoleného vzorca:
   - Napätie v ťahu: σ = F / A (A = 200 mm²)
   - Kinetická energia: E = ½·m·v² (m = 10 kg)
4. V jednom grafe zobrazí pôvodné aj vypočítané hodnoty.
5. Používateľ môže zadať ľubovoľné číslo, program ho vypočíta a zvýrazní v grafe.

## Ovládanie
- Zo zoznamu vyberte vzorec.
- Do vstupného poľa zadajte číslo a kliknite na **Vypočítať**.
- Tlačidlo **Nové dáta** vygeneruje nové náhodné pole.

## Spustenie
**Verzia .exe:** stiahnite `zadanie2.exe` (priečinok Releases alebo `dist`) a spustite ho. Python nie je potrebný.

**Zo zdrojového kódu:**
```
pip install matplotlib
python zadanie2.py
```

## Autor
Lubenets Sofiia
