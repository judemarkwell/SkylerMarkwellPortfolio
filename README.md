# Skyler Markwell — Portfolio

Portfolio site for Skyler Markwell, educator of multilingual learners and curriculum designer.

## Working on the site

```bash
npm install
npm run previews   # renders preview images from source-materials/ (needs LibreOffice + Python: pypdfium2, Pillow)
npm run dev        # http://localhost:4321/SkylerMarkwellPortfolio/
npm run build
```

- Product context: `PRODUCT.md`. Visual system: `DESIGN.md`.
- Each portfolio piece is a Markdown file in `src/content/work/`. Its preview pages are listed in `scripts/previews.json`.
- `source-materials/` (Skyler's original files) and `public/previews/` (rendered images) are **not committed**. The repo is public, and images go in only after Skyler approves which documents are published. Until then the site shows "Preview coming soon" sheets when built without them.
- Deploy: the GitHub Pages workflow runs manually (Actions → Deploy to GitHub Pages).

## Design skills (vendored)

| Skill | Source | Version | License |
|---|---|---|---|
| `impeccable` | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | 5e745ac | Apache 2.0 |
| `taste-skill` (design-taste-frontend) | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | 12af471 | MIT |

Both live in `.claude/skills/`, so any Claude session opened on this repo loads them automatically.
To update, re-copy from upstream (or run `npx impeccable update` / `npx skills add https://github.com/Leonxlnx/taste-skill --skill design-taste-frontend`).
