"""
Visualisierung des Kästchen-Modells (ν):
  - Luftrahmen: Mindestluft (Höhe 1) + Überschussluft (Höhe λ−1),
    volumetrisch geteilt in O2 (21 %) und N2 (79 %).
  - Rauchgas: fünf gestapelte Kästchen CO2 | H2O | SO2 | N2 | O2.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from verbrennungsrechnung import Brennstoff, Luftrahmen, Rauchgas, vorwaerts

FARBE = {
    "O2": "#7ec8e3", "N2": "#d9d9d9", "CO2": "#595959",
    "H2O": "#4a90d9", "SO2": "#f2c744",
}


def _kasten(ax, x, y, b, h, farbe, text=None, fs=9):
    ax.add_patch(Rectangle((x, y), b, h, facecolor=farbe, edgecolor="black", lw=1.1))
    if text and h > 0.045:
        ax.text(x + b / 2, y + h / 2, text, ha="center", va="center", fontsize=fs)


def zeichne_luftrahmen(ax, luft: Luftrahmen):
    ax.clear()
    xO2 = luft.x_O2_luft
    lam = luft.lam

    # trockene Luft: O2/N2 über die volle Höhe λ (Mindestluft 0..1 + Überschuss 1..λ)
    _kasten(ax, 0, 0, xO2, 1, FARBE["O2"], "O₂\n21 %")
    _kasten(ax, xO2, 0, 1 - xO2, 1, FARBE["N2"], "N₂\n79 %")

    hue = max(lam - 1, 0)
    if hue > 0:
        _kasten(ax, 0, 1, xO2, hue, FARBE["O2"], "O₂")
        _kasten(ax, xO2, 1, 1 - xO2, hue, FARBE["N2"], "N₂")

    # Luftfeuchte: rechts als Spalte über die GANZE Höhe λ — jede Portion Luft
    # (Mindest- wie Überschussluft) bringt ihren proportionalen H2O-Anteil mit.
    w_feucht = 0.0
    if luft.x_H2O_luft > 0:
        w_feucht = luft.x_H2O_luft / (1 - luft.x_H2O_luft)   # Breite rel. zur trockenen Luft (=1)
        _kasten(ax, 1, 0, w_feucht, lam, FARBE["H2O"], "H₂O", fs=8)

    xr = 1 + w_feucht + 0.05
    ax.annotate("Mindestluft\n(Höhe 1)", xy=(xr, 0.4), va="center", fontsize=9)
    if hue > 0:
        ax.annotate(f"Überschussluft\n(Höhe λ−1 = {hue:.2f})",
                    xy=(xr, 1 + hue / 2), va="center", fontsize=9)
    if w_feucht > 0:
        ax.annotate(f"H₂O-Luftfeuchte {100*luft.x_H2O_luft:.1f} %\n"
                    "(jede Portion Luft bringt\nihren H₂O-Anteil mit)",
                    xy=(xr, 0.85), va="center", fontsize=7.5, color="#2f5f9e")

    ax.set_xlim(0, xr + 0.75)
    ax.set_ylim(0, max(lam, 1.05) + 0.1)
    ax.set_title(f"Luftrahmen — Luftzahl λ = {lam:.2f}", fontsize=11)
    ax.set_xticks([])
    ax.set_ylabel("Höhe (× trockene Mindestluft)")


def zeichne_rauchgas(ax, rg: Rauchgas):
    ax.clear()
    anteile = rg.anteile()
    reihenfolge = ["CO2", "H2O", "SO2", "N2", "O2"]
    labels = {"CO2": "CO₂", "H2O": "H₂O", "SO2": "SO₂", "N2": "N₂", "O2": "O₂ (Überschuss)"}

    y = 0.0
    for k in reihenfolge:
        h = anteile[k]
        _kasten(ax, 0, y, 1, h, FARBE[k], f"{labels[k]}\n{100*h:.1f} %")
        y += h

    ax.set_xlim(0, 1.5)
    ax.set_ylim(0, 1.0)
    ax.set_title("Rauchgas (feucht)", fontsize=11)
    ax.set_xticks([])
    ax.set_ylabel("Volumenanteil")


def bild_erzeugen(bs: Brennstoff, lam: float, x_H2O_luft=0.0, speichern=None):
    luft, rg = vorwaerts(bs, lam, x_H2O_luft=x_H2O_luft)
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11, 5))
    zeichne_luftrahmen(axL, luft)
    zeichne_rauchgas(axR, rg)
    fig.suptitle("Verbrennungsrechnung — Kästchen-Modell (ν)", fontsize=13)
    fig.tight_layout()
    if speichern:
        fig.savefig(speichern, dpi=130, bbox_inches="tight")
        print(f"Bild gespeichert: {speichern}")
    return fig


if __name__ == "__main__":
    # ERT2 Übung 3, Aufgabe 1 (Kohle)
    kohle = Brennstoff(c=0.55, h=0.04, s=0.04, n=0.02, o=0.15, asche=0.05, w=0.15)
    bild_erzeugen(kohle, lam=1.3, x_H2O_luft=0.0482, speichern="kaestchen_modell.png")
    plt.show()
