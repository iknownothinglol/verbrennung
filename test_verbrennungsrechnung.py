"""
Tests / Validierung gegen ERT2 Übung 3, Aufgabe 1 und interne Konsistenz.
Ausführen:  python -m pytest   (oder das Fallback unten)
"""

import math
from verbrennungsrechnung import Brennstoff, vorwaerts, M


def nah(a, b, tol=1.5e-3):
    return math.isclose(a, b, abs_tol=tol)


def _uebung3():
    kohle = Brennstoff(c=0.55, h=0.04, s=0.04, n=0.02, o=0.15, asche=0.05, w=0.15)
    return vorwaerts(kohle, lam=1.3, x_O2_luft=0.21, x_H2O_luft=0.0482)


def test_brennstoff_summe():
    kohle = Brennstoff(c=0.55, h=0.04, s=0.04, n=0.02, o=0.15, asche=0.05, w=0.15)
    assert nah(kohle.summe(), 1.0, tol=1e-9)


def test_o2_min():
    luft, _ = _uebung3()
    assert nah(luft.v_O2_min, 0.0524)             # Musterlösung 0,0524


def test_luft_tr():
    luft, _ = _uebung3()
    assert nah(luft.v_luft_tr, 0.3243, tol=2e-3)  # Musterlösung 0,3243


def test_n2():
    luft, _ = _uebung3()
    assert nah(luft.v_N2_luft, 0.2562, tol=2e-3)  # Musterlösung ~0,2562


def test_rauchgas_gesamt():
    _, rg = _uebung3()
    assert nah(rg.gesamt, 0.3637, tol=2e-3)       # Musterlösung 0,3637


def test_anteile_summe_eins():
    _, rg = _uebung3()
    assert nah(sum(rg.anteile().values()), 1.0, tol=1e-9)


def test_vorwaerts_konsistenz():
    bs = Brennstoff(c=0.80, h=0.05, s=0.01, n=0.0, o=0.04, w=0.10)
    lam = 1.5
    luft, rg = vorwaerts(bs, lam)
    assert nah(rg.O2, (lam - 1) * luft.v_O2_min)
    assert nah(rg.CO2, bs.c / M["C"])
    assert nah(rg.SO2, bs.s / M["S"])
    assert nah(rg.N2, luft.v_luft_tr * 0.79)      # trockene Luft, N ohne


if __name__ == "__main__":
    import sys
    fns = [f for f in dir(sys.modules[__name__]) if f.startswith("test_")]
    ok = 0
    for f in fns:
        try:
            globals()[f](); print("PASS", f); ok += 1
        except Exception as e:
            print("FAIL", f, e)
    print(f"{ok}/{len(fns)} passed")
