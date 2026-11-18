[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/Agusgarut/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/Agusgarut/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

# The World in One Day — Tuesday 17 November 2026

Entry for the [make.fun bounty "Sum up 17 November's world news in one image"](https://make.fun/bounty/news-image-20261117)
(`news-image-20261117`, $250 prize pool, 50 paid places).

## The image

`entry.png` (1024×1024, PNG) is a newspaper front page summing up
Tuesday 17 November 2026, drawn programmatically with Pillow
(`tools/generate-image.py`) — no photos, no downloaded artwork, all
headlines and drawings written/drawn for this entry.

- **Header:** "Tuesday 17 November 2026" in giant serif, the day named
  unambiguously at the top of the page.
- **13 main stories in 3 rows:** (1) Kerch Bridge falls, (2) drone strike
  on a US radar base in Bahrain, (3) Trump at the Quad summit in Manila,
  (4) four nations demand Gaza aid crossings open, (5) Japan protests a
  Russian airspace breach, (6) EU Rwanda return hubs, (7) Mongolia's
  president steps aside, (8) Nvidia beats ($115.8bn) as the Dow drops 849,
  (9) Ebola cases pass 11,000 in DR Congo, (10) COP31 splits on fossil
  phase-out, (11) students lead Serbia's new parliament, (12) An-12 crash
  in Siberia kills 19, (13) Mozambique tries opposition leader Mondlane.
- **"Where it happened":** a world map with numbered pins 1–13 and a
  colour legend per region.
- **"Also on Tuesday 17 November":** 11 more stories (Kyiv's Dnipro
  bridges, Russia's 1,441-drone claim, UK sanctions, Prague train crash,
  French strikes, Tusk's confidence vote, Moldova airspace, Darwin quake,
  Pattinson as Bond, Depardieu's guilty plea, Houthis in Aden).

## The program

`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png` locally).
It runs with no network and is fully deterministic — two runs produce
byte-identical output.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Regenerating the image

```sh
python3 tools/generate-image.py   # writes entry.png
```

## License

MIT — see `LICENSE`.
