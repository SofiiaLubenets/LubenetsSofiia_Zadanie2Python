import random
import statistics
import tkinter as tk
from tkinter import messagebox

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------------------------------------------------------------
# VZORCE (3. bod) - dva vzorce z oblasti priemyslu
# ---------------------------------------------------------------
A = 200.0   # plocha prierezu [mm^2]
M = 10.0    # hmotnosť [kg]

FORMULY = {
    "Napätie v ťahu: σ = F / A": {
        "vstup": "Sila F [N]",
        "vystup": "σ [MPa]",
        "lo": 100, "hi": 5000,
        "f": lambda F: F / A,
        "popis": "σ = F / A,  A = 200 mm²",
    },
    "Kinetická energia: E = ½·m·v²": {
        "vstup": "Rýchlosť v [m/s]",
        "vystup": "E [J]",
        "lo": 1, "hi": 30,
        "f": lambda v: 0.5 * M * v ** 2,
        "popis": "E = ½·m·v²,  m = 10 kg",
    },
}


# 1. bod - pole vstupných hodnôt (min. 50 náhodných hodnôt)
def generuj_pole(lo, hi, n=60):
    return [round(random.uniform(lo, hi), 1) for _ in range(n)]


# 2. bod - práca s poľom (zoradenie, priemer, min, max)
def spracuj_pole(pole):
    return {
        "zoradene": sorted(pole),
        "priemer": statistics.mean(pole),
        "min": min(pole),
        "max": max(pole),
    }


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Zadanie 2 - Výpočet podľa vzorca")
        self.geometry("900x750")

        # ---- výber vzorca ----
        self.zvolena = tk.StringVar(value=list(FORMULY.keys())[0])
        vyber = tk.Frame(self)
        vyber.pack(pady=8)
        tk.Label(vyber, text="Vzorec:", font=("Arial", 12)).pack(side="left", padx=5)
        tk.OptionMenu(vyber, self.zvolena, *FORMULY.keys(),
                      command=lambda _: self.zmen_vzorec()).pack(side="left")

        self.popis = tk.Label(self, text="", font=("Arial", 11, "italic"))
        self.popis.pack()

        # ---- vstup, tlačidlá ----
        horna = tk.Frame(self)
        horna.pack(pady=10)
        self.vstup_label = tk.Label(horna, text="", font=("Arial", 12))
        self.vstup_label.grid(row=0, column=0, padx=5)
        self.vstup = tk.Entry(horna, width=12, font=("Arial", 12))
        self.vstup.grid(row=0, column=1, padx=5)
        tk.Button(horna, text="Vypočítať", command=self.vypocitaj).grid(row=0, column=2, padx=5)
        tk.Button(horna, text="Nové dáta", command=self.nove_data).grid(row=0, column=3, padx=5)

        self.vysledok = tk.Label(self, text="Výsledok: -", font=("Arial", 13, "bold"))
        self.vysledok.pack()
        self.info = tk.Label(self, text="", font=("Arial", 11))
        self.info.pack(pady=5)

        # ---- graf ----
        self.fig = Figure(figsize=(8, 4.5), dpi=100)
        self.ax1 = self.fig.add_subplot(111)
        self.ax2 = self.ax1.twinx()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.zmen_vzorec()

    def aktualny(self):
        return FORMULY[self.zvolena.get()]

    def zmen_vzorec(self):
        v = self.aktualny()
        self.popis.config(text=v["popis"])
        self.vstup_label.config(text=v["vstup"] + ":")
        self.vysledok.config(text="Výsledok: -")
        self.vlastne = None
        self.nove_data()

    def nove_data(self):
        v = self.aktualny()
        self.pole = generuj_pole(v["lo"], v["hi"])
        self.data = spracuj_pole(self.pole)
        self.obnov()

    def vypocitaj(self):
        v = self.aktualny()
        try:
            x = float(self.vstup.get().replace(",", "."))
        except ValueError:
            messagebox.showerror("Chyba", "Zadajte číslo.")
            return
        self.vysledok.config(text=f"Výsledok: {v['vystup'].split()[0]} = {v['f'](x):.3f} {v['vystup'].split()[1]}")
        self.vlastne = x
        self.obnov()

    def obnov(self):
        v = self.aktualny()
        d = self.data
        self.info.config(
            text=f"Počet: {len(self.pole)} | priemer: {d['priemer']:.1f} | "
                 f"min: {d['min']:.1f} | max: {d['max']:.1f}"
        )
        # ak používateľ zadal vlastné číslo, zaradí sa do zoradeného radu
        vstup = list(d["zoradene"])
        if self.vlastne is not None:
            vstup.append(self.vlastne)
            vstup.sort()
        vypocet = [v["f"](val) for val in vstup]
        x = list(range(1, len(vstup) + 1))

        self.ax1.clear()
        self.ax2.clear()
        self.ax1.plot(x, vstup, "b-", linewidth=4, alpha=0.5, label="Pôvodné hodnoty: " + v["vstup"])
        self.ax2.plot(x, vypocet, "r--o", markersize=3, label="Vypočítané: " + v["vystup"])

        # zvýraznenie vlastného čísla v grafe
        if self.vlastne is not None:
            poz = vstup.index(self.vlastne) + 1
            self.ax1.plot(poz, self.vlastne, "g*", markersize=24,
                          label=f"Vaše číslo: {self.vlastne:g}")
            self.ax2.plot(poz, v["f"](self.vlastne), "m*", markersize=16,
                          label=f"Výsledok: {v['f'](self.vlastne):.3f}")
        self.ax1.set_xlabel("Poradie (zoradené)")
        self.ax1.set_ylabel(v["vstup"], color="b")
        self.ax2.set_ylabel(v["vystup"], color="r")
        self.ax1.set_title("Pôvodné a vypočítané hodnoty")
        self.ax1.grid(True)
        h1, l1 = self.ax1.get_legend_handles_labels()
        h2, l2 = self.ax2.get_legend_handles_labels()
        self.ax1.legend(h1 + h2, l1 + l2, loc="upper left")
        self.fig.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    App().mainloop()
