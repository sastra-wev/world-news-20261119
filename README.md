# THE WORLD IN ONE PAGE — Thursday, November 19, 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/sastra-wev/world-news-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/sastra-wev/world-news-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Entry for the make.fun competition **`news-image-20261119`** — *"Sum up 19 November's world news in one image"* ($250, top 100 paid).

## What it does

`main.py` renders a complete broadsheet front page for **Thursday, November 19, 2026** as a single 1024×1024 PNG:

- **Hero:** GTA VI's worldwide launch day, drawn entirely with Pillow primitives — a Vice-palette sunset gradient, retro sliced sun, palm and skyline silhouettes, and a neon-rimmed sports car over a Leonida dateline (Lucia Caminos & Jason Duval, PS5 / Xbox Series X|S, $79.99, Metacritic 99).
- **Highlight strip:** NASA's Voyager 1 reaching one light-day from Earth.
- **Three columns, 11 more stories** with section labels (WORLD / POLITICS / TECH / MARKETS): the Trump–Xi–Putin Shenzhen trilateral, the widening US–Iran firefight, the ICJ ruling in The Gambia v. Myanmar, Moscow's red-line warning to France, Peltola's Alaska win and the 56–44 Senate, Gaza, Cyclone Akvan, the AI cyber-threat hearings, Nvidia's turmoil, the EU's €45bn Ukraine loan, and the Fed minutes.
- **Footer ticker:** Australia's settler sanctions and APEC diplomacy, Ted Lieu's historic caucus-chair election, and Iraq's ISIL verdicts.

## Run it

```bash
python3 main.py
```

Writes `frontpage.png` (1024×1024, ~172 KB) into the working directory. The generator is fully **offline and deterministic** — no network, no randomness, no wall-clock reads; the same code always produces the identical image. Requires Python 3 and Pillow.

## License

MIT — see `LICENSE`.
