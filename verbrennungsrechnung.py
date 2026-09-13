"""
Verbrennungsrechnung auf molarer/volumetrischer Basis (ν) — das "Kästchen-Modell".

Denkmodell (aus ERT2, RWTH Aachen):
-----------------------------------
1) Luftrahmen: Die Verbrennungsluft als Rahmen, volumetrisch geteilt in
   O2 (21 %) und N2 (79 %). Die stöchiometrische *Mindestluft* hat die Höhe 1,
   ein zweiter, gleicher Rahmen der Höhe (λ − 1) ist die *Überschussluft*.
   Gesamthöhe = Luftzahl λ.

        Mindestluft (Höhe 1)       Überschussluft (Höhe λ−1)
        +----------+-----------+   +----------+-----------+
        | O2 21 %  |  N2 79 %  |   | O2 21 %  |  N2 79 %  |
        +----------+-----------+   +----------+-----------+

2) Rauchgas: fünf Kästchen — CO2 | H2O | SO2 | N2 | O2 (Überschuss).

3) Verbunden über die Elementarreaktionen (je kmol):
        C  + O2      -> CO2
        H2 + 1/2 O2  -> H2O
        S  + O2      -> SO2
        N            -> N2   (unverändert ins Rauchgas)
   Gebundener Brennstoffsauerstoff senkt den O2-Bedarf.
   Feuchte Verbrennungsluft bringt zusätzlich H2O ins Rauchgas.

Alle mengenspezifischen Größen sind molar, pro kg Brennstoff (kmol/kg_BS).

Autor: Zeming Wang
"""

from __future__ import annotations

from dataclasses import dataclass

# --- Molare Massen [kg/kmol] ----------------------------------------------
# gerundete, in der Verbrennungsrechnung übliche Werte (wie in der ERT2-Übung)
M = {"C": 12.0, "H": 1.0, "O": 16.0, "S": 32.0, "N": 14.0}
M_H2O = 2 * M["H"] + M["O"]

# --- Standard-Luft (volumetrisch = molar) ---------------------------------
X_O2_LUFT = 0.21        # O2-Anteil in trockener Luft
X_H2O_LUFT = 0.0        # H2O-Anteil in feuchter Luft (0 = trocken)


@dataclass
class Brennstoff:
    """Gravimetrische Zusammensetzung (Massenanteile, kg/kg_BS)."""
    c: float = 0.0   # Kohlenstoff
    h: float = 0.0   # Wasserstoff
    s: float = 0.0   # Schwefel
    n: float = 0.0   # Stickstoff
    o: float = 0.0   # (gebundener) Sauerstoff
    asche: float = 0.0
    w: float = 0.0   # Wasser (Feuchte)

    def summe(self) -> float:
        return self.c + self.h + self.s + self.n + self.o + self.asche + self.w


@dataclass
class Luftrahmen:
    """Luftmengen pro kg Brennstoff [kmol/kg_BS] — das Rahmen-Modell (ν)."""
    v_O2_min: float           # stöch. O2-Bedarf (Mindestluft-Rahmen)
    lam: float                # Luftzahl λ
    x_O2_luft: float = X_O2_LUFT
    x_H2O_luft: float = X_H2O_LUFT

    @property
    def v_luft_min_tr(self) -> float:
        """Mindestluft, trocken (Höhe 1) = O2_min / 0.21."""
        return self.v_O2_min / self.x_O2_luft

    @property
    def v_luft_tr(self) -> float:
        """Tatsächliche trockene Luft (Höhe λ) = λ · Mindestluft."""
        return self.lam * self.v_luft_min_tr

    @property
    def v_H2O_luft(self) -> float:
        """H2O, das die feuchte Luft mitbringt."""
        if self.x_H2O_luft <= 0:
            return 0.0
        return self.v_luft_tr * self.x_H2O_luft / (1 - self.x_H2O_luft)

    @property
    def v_luft_feucht(self) -> float:
        return self.v_luft_tr + self.v_H2O_luft

    @property
    def v_O2_ueberschuss(self) -> float:
        """Überschuss-O2 = (λ − 1) · O2_min."""
        return (self.lam - 1) * self.v_O2_min

    @property
    def v_N2_luft(self) -> float:
        """N2 aus der Luft = trockene Luft · 0.79."""
        return self.v_luft_tr * (1 - self.x_O2_luft)


@dataclass
class Rauchgas:
    """Die fünf Rauchgas-Kästchen [kmol/kg_BS] (feucht)."""
    CO2: float = 0.0
    H2O: float = 0.0
    SO2: float = 0.0
    N2: float = 0.0
    O2: float = 0.0     # Überschuss

    @property
    def gesamt(self) -> float:
        return self.CO2 + self.H2O + self.SO2 + self.N2 + self.O2

    def anteile(self) -> dict[str, float]:
        """Volumen-/Molanteile, feucht [-]."""
        g = self.gesamt
        return {k: v / g for k, v in self.__dict__.items()}

    def anteile_trocken(self) -> dict[str, float]:
        """Volumen-/Molanteile im trockenen Rauchgas (ohne H2O) [-]."""
        g = self.gesamt - self.H2O
        return {k: (0.0 if k == "H2O" else v / g) for k, v in self.__dict__.items()}


# ---------------------------------------------------------------------------
# Vorwärtsrechnung:  Brennstoff + λ (+ feuchte Luft)  ->  Luftrahmen + Rauchgas
# ---------------------------------------------------------------------------

def vorwaerts(
    bs: Brennstoff,
    lam: float,
    x_O2_luft: float = X_O2_LUFT,
    x_H2O_luft: float = X_H2O_LUFT,
) -> tuple[Luftrahmen, Rauchgas]:
    """Aus Brennstoffanalyse und Luftzahl die Luft- und Rauchgasmengen berechnen.

    Elementbilanzen pro kg Brennstoff (kmol/kg_BS):
        n_C  = c / M_C        -> 1 CO2, braucht 1 O2
        n_H2 = h / (2 M_H)    -> 1 H2O, braucht 1/2 O2
        n_S  = s / M_S        -> 1 SO2, braucht 1 O2
        n_N2 = n / (2 M_N)    -> geht als N2 ins Rauchgas
        geb. O2 = o / (2 M_O) senkt den O2-Bedarf
    """
    n_C = bs.c / M["C"]
    n_H2 = bs.h / (2 * M["H"])
    n_S = bs.s / M["S"]
    n_N2_bs = bs.n / (2 * M["N"])
    n_O2_geb = bs.o / (2 * M["O"])
    n_H2O_feuchte = bs.w / M_H2O

    v_O2_min = n_C + 0.5 * n_H2 + n_S - n_O2_geb
    luft = Luftrahmen(v_O2_min=v_O2_min, lam=lam,
                      x_O2_luft=x_O2_luft, x_H2O_luft=x_H2O_luft)

    rg = Rauchgas(
        CO2=n_C,
        H2O=n_H2 + n_H2O_feuchte + luft.v_H2O_luft,   # H-Verbrennung + Feuchte + Luftfeuchte
        SO2=n_S,
        N2=luft.v_N2_luft + n_N2_bs,
        O2=luft.v_O2_ueberschuss,
    )
    return luft, rg
