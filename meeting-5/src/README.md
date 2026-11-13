# Meeting 5 — source

Both decks are built with the [html-presentation skill](https://github.com/Amitro123/Presentation-skill).

- `gen.py` writes `meeting-5.json` (the main deck; raw slides hold the copy buttons and the Cowork prompt builder).
- `skills-example.json` is the separate "how to build a good skill" deck.

Rebuild from this folder:

```bash
python3 gen.py
node <skill>/scripts/build-deck.js meeting-5.json --out=../index.html --embed
node <skill>/scripts/build-deck.js skills-example.json --out=../skills-example.html --embed
```
