"""
Interaktive Verbrennungsrechnung (Kästchen-Modell, ν).

Links die Kästchen (Luftrahmen + Rauchgas), rechts eine **Werte-Tabelle**;
unten Schieberegler für λ, Brennstoff (C, H, S, W) und Luftfeuchte.
Der Sauerstoff O ergibt sich als Rest: O = 1 − C − H − S − N − Asche − W.

Start:   python interaktiv.py
(Benötigt ein interaktives Matplotlib-Backend, z. B. MacOSX oder TkAgg.)
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.widgets import Slider

from verbrennungsrechnung import Brennstoff, vorwaerts
from visualisierung import zeichne_luftrahmen, zeichne_rauchgas

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
    fig = plt.figure(figsize=(13, 7.2))
    gs = GridSpec(1, 3, width_ratios=[1.0, 1.0, 0.95], figure=fig)
    axL = fig.add_subplot(gs[0, 0])
    axM = fig.add_subplot(gs[0, 1])
    axT = fig.add_subplot(gs[0, 2]); axT.axis("off")
    plt.subplots_adjust(bottom=0.42, top=0.92, left=0.06, right=0.98, wspace=0.3)
    fig.suptitle("Interaktive Verbrennungsrechnung — Kästchen-Modell (ν)", fontsize=13)

    # (id, Label, min, max, startwert)  — Luft zuerst, dann Brennstoff
    REGLER = [
        ("lam",     "λ  Luftzahl",         1.0, 3.0,  1.30),
        ("feuchte", "Luftfeuchte x_H2O,L", 0.0, 0.10, 0.0482),
        ("c",       "C",                   0.20, 0.90, 0.55),
        ("h",       "H",                   0.0, 0.15, 0.04),
        ("s",       "S",                   0.0, 0.06, 0.04),
        ("n",       "N",                   0.0, 0.10, 0.02),
        ("asche",   "Asche",               0.0, 0.30, 0.05),
        ("w",       "W  Wasser",           0.0, 0.30, 0.15),
    ]
    sl = {}
    y = 0.02
    for (sid, lab, lo, hi, val) in reversed(REGLER):   # von unten nach oben aufbauen
        sl[sid] = Slider(plt.axes([0.15, y, 0.70, 0.025]), lab, lo, hi, valinit=val)
        y += 0.045

    hinweis = fig.text(0.5, 0.95, "", ha="center", fontsize=9, color="#a33")
    tab_text = axT.text(0.0, 1.0, "", va="top", ha="left", family="monospace",
                        fontsize=8.5, transform=axT.transAxes)

    def update(_=None):
        c, h, s, n = sl["c"].val, sl["h"].val, sl["s"].val, sl["n"].val
        asche, w = sl["asche"].val, sl["w"].val
        o = 1.0 - c - h - s - n - asche - w
        if o < 0:
            hinweis.set_text(f"⚠ C+H+S+N+Asche+W > 1 — bitte reduzieren (O = {o:.2f})")
            o = 0.0
        else:
            hinweis.set_text(f"O (Sauerstoff, Rest) = {100*o:.1f} M.-%   ·   Summe = 100 M.-%")

        bs = Brennstoff(c=c, h=h, s=s, n=n, o=o, asche=asche, w=w)
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
