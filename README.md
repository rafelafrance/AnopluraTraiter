# The Anoplura Traits Database Project [![Build Status](https://travis-ci.org/rafelafrance/traiter_anoplura.svg?branch=master)](https://travis-ci.org/rafelafrance/traiter_anoplura)


## What we're doing

Extract traits and locations from scientific literature about lice (Anoplura). That is, if I'm given some text like
```
Maximum head width, 0.150–0.163 mm (mean, 0.17 mm, n = 4).
One long Dorsal Principal Head Seta (DPHS), one small Dorsal
Accessory Head Seta (DAcHS) anteromedial to DPHS, one
Dorsal Posterior Central Head Seta (DPoCHS), two to three Dorsal
Preantennal Head Setae (DPaHS), two Sutural Head Setae (SHS),
three Dorsal Marginal Head Setae (DMHS), three to four Apical
Head Setae (ApHS).
```
We will extract:
- max_width: part: head, n: 4, mean: 0.17, mean_units: mm, low: 0.15, high: 0.163, length_units: mm,
- dorsal principal head setae: count: 1
- dorsal accessory head setae: count: 1
- dorsal posterior central head setae: count: 1
- dorsal preantennal head setae: low: 2, high: 3
- sutural head setae: count: 2
- dorsal marginal head setae: count: 3
- apical head setae: low: 3, high: 4
- etc.

## Multiple methods for parsing
1. Rule based parsing. Most machine learning models require a substantial training dataset. I use this method to bootstrap the training data. And, if other methods fail I can fall back to this.
1. Machine learning models. (In progress)

## Rule-based parsing strategy
1. Next I label terms using Spacy's phrase and rule-based matchers.
1. Then I match terms using rule-based matchers repeatedly until I have built up a recognizable trait like: Head width, setae count, etc.
1. Finally, I associate traits with plant parts.

## Tests
Having a test suite is absolutely critical. The strategy I use is every new trait gets its own test set. Any time there is a parser error I add the parts that caused the error to the test suite and correct the parser. I.e. I use the standard red/green testing methodology.

You can run the tests like so:
```
cd /my/path/to/eforas_traiter
python -m unittest discover
```
