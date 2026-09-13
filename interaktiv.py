"""
Interaktive Verbrennungsrechnung (Kästchen-Modell, ν).

Schieberegler für Luftzahl λ, Brennstoffzusammensetzung (C, H, S, W) und
Luftfeuchte. Der Sauerstoffgehalt O ergibt sich aus der Schließbedingung
O = 1 − C − H − S − N − Asche − W (N und Asche fest).

Start:   python interaktiv.py
(Benötigt ein interaktives Matplotlib-Backend, z. B. TkAgg oder MacOSX.)
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

from verbrennungsrechnung import Brennstoff, vorwaerts
from visualisierung import zeichne_luftrahmen, zeichne_rauchgas

N_FEST = 0.02       # Stickstoff (fest)
ASCHE_FEST = 0.05   # Asche (fest)


def main():
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11, 6))
    plt.subplots_adjust(bottom=0.36, top=0.9, wspace=0.35)
    fig.suptitle("Interaktive Verbrennungsrechnung — Kästchen-Modell (ν)", fontsize=13)

    start = dict(lam=1.30, c=0.55, h=0.04, s=0.04, w=0.15, feuchte=0.0482)

    ax = {
        "lam":     plt.axes([0.15, 0.26, 0.70, 0.03]),
        "c":       plt.axes([0.15, 0.21, 0.70, 0.03]),
        "h":       plt.axes([0.15, 0.16, 0.70, 0.03]),
        "s":       plt.axes([0.15, 0.11, 0.70, 0.03]),
        "w":       plt.axes([0.15, 0.06, 0.70, 0.03]),
        "feuchte": plt.axes([0.15, 0.01, 0.70, 0.03]),
    }
    sl = {
        "lam":     Slider(ax["lam"], "λ  Luftzahl", 1.0, 3.0, valinit=start["lam"]),
        "c":       Slider(ax["c"], "C", 0.30, 0.90, valinit=start["c"]),
        "h":       Slider(ax["h"], "H", 0.00, 0.15, valinit=start["h"]),
        "s":       Slider(ax["s"], "S", 0.00, 0.06, valinit=start["s"]),
        "w":       Slider(ax["w"], "W  Wasser", 0.00, 0.30, valinit=start["w"]),
        "feuchte": Slider(ax["feuchte"], "Luftfeuchte x_H2O,L", 0.0, 0.10, valinit=start["feuchte"]),
    }

    hinweis = fig.text(0.5, 0.955, "", ha="center", fontsize=9, color="#a33")

    def update(_=None):
        c, h, s, w = sl["c"].val, sl["h"].val, sl["s"].val, sl["w"].val
        o = 1.0 - c - h - s - N_FEST - ASCHE_FEST - w
        if o < 0:
            hinweis.set_text(f"⚠ C+H+S+N+Asche+W > 1 — bitte reduzieren (O = {o:.2f})")
            o = 0.0
        else:
            hinweis.set_text(f"O (Rest) = {100*o:.1f} M.-%  |  N {100*N_FEST:.0f} · Asche {100*ASCHE_FEST:.0f} fest")

        bs = Brennstoff(c=c, h=h, s=s, n=N_FEST, o=o, asche=ASCHE_FEST, w=w)
        luft, rg = vorwaerts(bs, sl["lam"].val, x_H2O_luft=sl["feuchte"].val)
        zeichne_luftrahmen(axL, luft)
        zeichne_rauchgas(axR, rg)
        fig.canvas.draw_idle()

    for s_ in sl.values():
        s_.on_changed(update)

    update()
    plt.show()


if __name__ == "__main__":
    main()
