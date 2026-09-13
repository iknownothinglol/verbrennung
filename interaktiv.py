"""
Interaktive Verbrennungsrechnung (Kästchen-Modell, ν).

Links die Kästchen (Luftrahmen + Rauchgas), rechts eine **Werte-Tabelle**;
unten Schieberegler für λ, Brennstoff (C, H, S, W) und Luftfeuchte.
Der Sauerstoff O ergibt sich aus O = 1 − C − H − S − N − Asche − W (N, Asche fest).

Start:   python interaktiv.py
(Benötigt ein interaktives Matplotlib-Backend, z. B. MacOSX oder TkAgg.)
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.widgets import Slider

from verbrennungsrechnung import Brennstoff, vorwaerts
from visualisierung import zeichne_luftrahmen, zeichne_rauchgas

N_FEST = 0.02
ASCHE_FEST = 0.05


def tabellentext(bs, luft, rg) -> str:
    a = rg.anteile()
    L = []
    L.append("BRENNSTOFF (M.-%)")
    L.append(f"  C {100*bs.c:5.1f}   H {100*bs.h:5.1f}   S {100*bs.s:5.1f}")
    L.append(f"  O {100*bs.o:5.1f}   N {100*bs.n:5.1f}   W {100*bs.w:5.1f}")
    L.append("")
    L.append("LUFT (kmol/kg_BS)")
    L.append(f"  lambda        {luft.lam:7.3f}")
    L.append(f"  v_O2,min      {luft.v_O2_min:7.4f}")
    L.append(f"  v_L,tr        {luft.v_luft_tr:7.4f}")
    L.append(f"  v_H2O,Luft    {luft.v_H2O_luft:7.4f}")
    L.append(f"  v_L,feucht    {luft.v_luft_feucht:7.4f}")
    L.append(f"  v_O2,ueber.   {luft.v_O2_ueberschuss:7.4f}")
    L.append(f"  v_N2          {luft.v_N2_luft:7.4f}")
    L.append("")
    L.append("RAUCHGAS      kmol/kg   Vol.-%")
    for k, name in [("CO2", "CO2"), ("H2O", "H2O"), ("SO2", "SO2"),
                    ("N2", "N2"), ("O2", "O2")]:
        L.append(f"  {name:<4}       {getattr(rg, k):7.4f}   {100*a[k]:6.2f}")
    L.append(f"  {'Summe':<4}      {rg.gesamt:7.4f}   {100:6.2f}")
    return "\n".join(L)


def main():
    fig = plt.figure(figsize=(13, 6.5))
    gs = GridSpec(1, 3, width_ratios=[1.0, 1.0, 0.95], figure=fig)
    axL = fig.add_subplot(gs[0, 0])
    axM = fig.add_subplot(gs[0, 1])
    axT = fig.add_subplot(gs[0, 2]); axT.axis("off")
    plt.subplots_adjust(bottom=0.36, top=0.9, left=0.06, right=0.98, wspace=0.3)
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

    hinweis = fig.text(0.5, 0.925, "", ha="center", fontsize=9, color="#a33")
    tab_text = axT.text(0.0, 1.0, "", va="top", ha="left", family="monospace",
                        fontsize=8.5, transform=axT.transAxes)

    def update(_=None):
        c, h, s, w = sl["c"].val, sl["h"].val, sl["s"].val, sl["w"].val
        o = 1.0 - c - h - s - N_FEST - ASCHE_FEST - w
        if o < 0:
            hinweis.set_text(f"⚠ C+H+S+N+Asche+W > 1 — bitte reduzieren (O = {o:.2f})")
            o = 0.0
        else:
            hinweis.set_text(f"O (Rest) = {100*o:.1f} M.-%  ·  N {100*N_FEST:.0f} · Asche {100*ASCHE_FEST:.0f} fest")

        bs = Brennstoff(c=c, h=h, s=s, n=N_FEST, o=o, asche=ASCHE_FEST, w=w)
        luft, rg = vorwaerts(bs, sl["lam"].val, x_H2O_luft=sl["feuchte"].val)
        zeichne_luftrahmen(axL, luft)
        zeichne_rauchgas(axM, rg)
        tab_text.set_text(tabellentext(bs, luft, rg))
        fig.canvas.draw_idle()

    for s_ in sl.values():
        s_.on_changed(update)

    update()
    plt.show()


if __name__ == "__main__":
    main()
