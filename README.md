# The Anoplura Traits Database Project ![CI](https://github.com/rafelafrance/AnopluraTraiter/workflows/CI/badge.svg)

After years of slumber this project is back and sassier than ever. TODOs for the resurrection:

- Update based upon the previous owner's notes & notebooks.
- Update to newer Traiter techniques.

**Thanks to Dr. Vjay Barve for providing the initial species list of Anoplura.**

## What we're doing

Extract traits and locations from scientific literature about lice (Anoplura). That is, if I'm given text like

```
Maximum head width, 0.150–0.163 mm (mean, 0.17 mm, n = 4).
One long Dorsal Principal Head Seta (DPHS), one small Dorsal
Accessory Head Seta (DAcHS) anteromedial to DPHS, one
Dorsal Posterior Central Head Seta (DPoCHS), two to three Dorsal
Preantennal Head Setae (DPaHS), two Sutural Head Setae (SHS),
three Dorsal Marginal Head Setae (DMHS), three to four Apical
Head Setae (ApHS). Head, thorax, and abdomen lightly sclerotized.
```

I will extract:

- max width: part = head, n = 4, mean = 0.17, mean_units = mm, low = 0.15, high = 0.163, length_units = mm,
- dorsal principal head setae: count = 1
- dorsal accessory head setae: count = 1
- dorsal posterior central head setae: count = 1
- dorsal preantennal head setae: low = 2, high = 3
- sutural head setae: count = 2
- dorsal marginal head setae: count = 3
- apical head setae: low = 3, high = 4
- sclerotized part: part = [head, thorax, abdomen], sclerotized = lightly
- etc.

## Methods for parsing

1. Rule-based parsing. Most machine learning models require a substantial training dataset. I use this method to bootstrap the training data. And, if other methods fail, I can fall back to this method. The downside of this method is that rule-based matchers are tricky and time-consuming to get right.
   - There is one set of rules for identifying the traits themselves. This is called Named Entity Recognition (NER).
   - There is another set of rules for associating traits with one another. For instance, determining that a maximum width measurement is for a male _Lemurpediculus robbinsi_ (holotype).
2. ~~Machine learning models. Once we have enough relevant data from the rules we can train models with that data. We are using two different models.~~
   - ~~One for named entity recognition (NER) to identify the traits.~~
   - ~~And another model for associating traits with one another. As mentioned above.~~
   - ~~It may be possible to combine these models.~~
   - I probably do not have time to do this.

## Rule-based parsing strategy

For example, given the text: `Head, thorax, and abdomen lightly sclerotized.`

1. I start with a vocabulary of terms stored in one or more CSV files. These are words related to louse anatomy or other descriptions of lice. Some terms from the example above are: "head", "thorax", "abdomen", "mm", "sclerotized", "dorsal", "setae", etc. I then use spaCy phrase matchers to find the terms in the document. In this example the following vocabulary these terms are recognized:
   - `Head`
   - `thorax`
   - `abdomen`
   - `sclerotized`
2. These terms are used as anchors for finding phrase patterns in the document using spaCy's rule based matchers. Relevant patterns for this example are:
   - Body part words separated by commas or conjunctions. Here we get `Head, thorax, and abdomen` and the extracted data is `part = [head, thorax, abdomen]`
   - An adverb followed by the word "sclerotin". Which would recognize `lightly sclerotized` which yields the data `sclerotized = lightly`
3. Now I recognize the full trait by looking for patterns that work on the previous matches:
   - In this case, a body part followed by some possible filler which is then followed by a sclerotin notation. So we now have the full trait: `Head, thorax, and abdomen lightly sclerotized.` and its data `sclerotized part: part = [head, thorax, abdomen], sclerotized = lightly`.
   - Please note that there may be more levels of matching.
4. Finally, I associate traits with a species, sex, holotype/allotype/paratype, etc. using a different set of spaCy matchers and some simple heuristics.

## Install

You will need to have Python 3.12 (or later) installed. You can install the requirements into your python environment like so:

```
make install
```

## Run

```
./extract.py ... TODO ...
```

## Tests

Having a test suite is absolutely critical. The strategy I use is every new trait gets its own test set. Any time there is a parser error I add the parts that caused the error to the test suite and correct the parser. I.e. I use the standard red/green testing methodology.

You can run the tests like so:

```
make test
```
