# Die Aufgabe — Verbrennungsrechnung einer Kohle

Diese Aufgabenstellung ist das Beispiel, das das Werkzeug löst und gegen das es
validiert wird (`beispiel_uebung3.py`). Sinngemäß nach *ERT2 — Energierohstoffe
und -technik 2, Übung 3, Aufgabe 1* (RWTH Aachen); Daten und Aufgabe hier eigen
formuliert.

## Situation

Zur Bestimmung des Verbrennungsverhaltens einer Kohle wurde eine
**Brennstoffanalyse** durchgeführt. Die Kohle wird mit **feuchter Luft** und
einer **Luftzahl λ = 1,3** vollständig verbrannt. Gesucht sind der Luftbedarf
und das entstehende Rauchgas auf **molarer/volumetrischer Basis**.

## Brennstoffanalyse (Rohzustand)

| Bestandteil | Symbol | Massenanteil |
|---|---|---|
| Kohlenstoff | C | 55 M.-% |
| Wasserstoff | H | 4 M.-% |
| Sauerstoff | O | 15 M.-% |
| Stickstoff | N | 2 M.-% |
| Schwefel | S | 4 M.-% |
| Asche | – | 5 M.-% |
| Wasser | W | 15 M.-% |
| **Summe** | | **100 M.-%** |

## Gegeben

| Größe | Wert |
|---|---|
| O₂-Anteil der Luft | x\_O₂,L = 21 Vol.-% (= 23,14 M.-%) |
| H₂O-Anteil der (feuchten) Luft | x\_H₂O,L = 4,82 Vol.-% (= 3 M.-%) |
| Luftzahl | λ = 1,3 |
| molare Massen (gerundet) | C 12 · H 1 · O 16 · N 14 · S 32 · H₂O 18 kg/kmol |

## Aufgaben

- **a)** Die allgemeine Verbrennungsgleichung aufstellen.
- **b)** Die Summenformel des Brennstoffs pro kg\_Br bestimmen.
- **c)** Für die Verbrennung der Kohle berechnen:
  - die spezifische **feuchte Verbrennungsluftmenge**,
  - die **feuchte Abgasmenge** und
  - die **feuchte volumetrische Abgaszusammensetzung**.

## Lösungsweg (Kästchen-Modell)

1. Elementmengen pro kg Brennstoff: n\_C = C/M\_C usw.
2. Stöchiometrischer O₂-Bedarf: v\_O₂,min = n\_C + ½·n\_H₂ + n\_S − n\_O(geb.)
3. Trockene Luft (Rahmen der Höhe λ): v\_L,tr = v\_O₂,min · λ / x\_O₂,L
4. Luftfeuchte ergänzen → feuchte Luft.
5. Rauchgas-Kästchen füllen: CO₂, H₂O (H-Verbrennung + Brennstoff- und
   Luftfeuchte), SO₂, N₂ (aus Luft), O₂ (Überschuss = (λ−1)·v\_O₂,min).

## Musterlösung (zur Validierung)

| Größe | Wert |
|---|---|
| v\_O₂,min | 0,0524 kmol\_O₂/kg\_BS |
| v\_L,tr (trockene Luft) | 0,3243 kmol\_L/kg\_BS |
| v\_N₂ (aus Luft) | ≈ 0,2562 kmol\_N₂/kg\_BS |
| v\_G (feuchtes Rauchgas) | 0,3637 kmol\_G/kg\_BS |

Der Vergleich Skript ↔ Musterlösung steht in [`README`](README.md#validierung-ert2-übung-3-aufgabe-1)
und wird von den Tests geprüft.
