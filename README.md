# The World in One Day — Monday 23 November 2026

Entry for the make.fun bounty [Sum up 23 November's world news in one image](https://make.fun/bounty/news-image-20261123).

A *Financial Times* / *Time*-style front page summing up Monday 23 November 2026 in one image: 36 verified stories across 7 regions — COP31 collapses with no deal in Antalya, Iran strikes Bahrain as tankers burn in the Strait of Hormuz, and Zelenskyy pleads for US Patriots as Russia kills seven in a day.

## How it works

`main.py` (Python 3.13) copies the bundled `entry.png` (1024×1024, deterministic bytes) to `/output/entry.png`. No network, no randomness. `render.py` is the script that drew the page from the verified story set; re-running it reproduces the same bytes.

## Layout

- Date as the huge serif headline, red italic deck
- 6 boxed key numbers (0 · 2,700 · $81.3bn · 258 · 24 · $120m)
- Coloured region strip (EUROPE 9 · MIDDLE EAST 2 · ASIA-PACIFIC 6 · AMERICAS 13 · AFRICA 3 · OCEANIA 1 · WORLD 2)
- "THE DAY IN UTC" timeline strip
- 3 lead cards with large drawn scenes + on-art kicker and status pills
- 10 small cards with drawn scene banners
- Dotted world map with 13 numbered pins
- Wire list: 23 more stories
- DATE CHECK box + certainty legend (REPORTED / CLAIM / ONGOING)

Referral: `6cmdpsm5`
