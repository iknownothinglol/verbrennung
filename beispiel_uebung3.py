"""
Worked Example — ERT2 Übung 3, Aufgabe 1 (Verbrennungsrechnung, volumetrisch/ν).

Kohle-Brennstoffanalyse (Rohzustand, M.-%):
    C 55 | H 4 | O 15 | N 2 | S 4 | Asche 5 | Wasser 15
Gegeben: x_O2,L = 21 Vol.-% ;  x_H2O,L = 4,82 Vol.-% (feuchte Luft) ;  λ = 1,3

Aufgabe c): spezifische feuchte Verbrennungsluftmenge, feuchte Abgasmenge und
feuchte volumetrische Abgaszusammensetzung.

Das Skript rechnet mit dem Kästchen-Modell und vergleicht mit der Musterlösung.
"""

from verbrennungsrechnung import Brennstoff, vorwaerts

# --- Gegeben ---------------------------------------------------------------
kohle = Brennstoff(c=0.55, h=0.04, s=0.04, n=0.02, o=0.15, asche=0.05, w=0.15)
lam = 1.3
x_O2_luft = 0.21
x_H2O_luft = 0.0482

luft, rg = vorwaerts(kohle, lam, x_O2_luft=x_O2_luft, x_H2O_luft=x_H2O_luft)


def zeile(label, wert, einheit, loesung=None):
    txt = f"  {label:<40s} {wert:10.4f} {einheit}"
    if loesung is not None:
        txt += f"   (Musterlösung: {loesung})"
    print(txt)


if __name__ == "__main__":
    print("=" * 74)
    print("ERT2 Übung 3 · Aufgabe 1 — Verbrennungsrechnung (volumetrisch, ν)")
    print("=" * 74)

    print("\nBrennstoff (Kontrolle): Summe =", f"{100*kohle.summe():.1f} M.-%")

    print("\nLuftrahmen (kmol/kg_BS):")
    zeile("v_O2,min  stöch. O2-Bedarf", luft.v_O2_min, "kmol_O2/kg", "0,0524")
    zeile("v_L,tr    trockene Luft (Höhe λ)", luft.v_luft_tr, "kmol_L/kg", "0,3243")
    zeile("v_H2O,L   H2O aus feuchter Luft", luft.v_H2O_luft, "kmol/kg")
    zeile("v_L,feucht feuchte Luft", luft.v_luft_feucht, "kmol_L/kg")
    zeile("v_O2,ü    Überschuss-O2 (λ−1)", luft.v_O2_ueberschuss, "kmol/kg")
    zeile("v_N2      N2 aus Luft", luft.v_N2_luft, "kmol_N2/kg", "≈0,2562")

    print("\nRauchgas-Kästchen (kmol/kg_BS):")
    for name, wert in rg.__dict__.items():
        zeile(name, wert, "kmol/kg")
    zeile("v_G  gesamt (feucht)", rg.gesamt, "kmol_G/kg", "0,3637")

    print("\nFeuchte volumetrische Abgaszusammensetzung (Vol.-%):")
    for name, a in rg.anteile().items():
        zeile(name, 100 * a, "Vol.-%")
