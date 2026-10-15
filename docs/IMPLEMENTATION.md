# Haru Unabara profile implementation

## Audit — 2026-10-15 (redesign session)

- Target confirmed via GitHub CLI: `ejhay27/ejhay27`, default branch `main`. Session branch `arena/279f5510-ejhay27`, started from the merged state of the previous session's PR #1 (`ab2dd30`).
- Previous profile carried: a dragon banner (`hero.jpg` built from `dragon-landscape.png`), a 900×76 phrase-strip GIF, one five-logo tools row, the ten-project table, the language snapshot chart, and GitHub + Portfolio links.
- Live account API re-checked: five public repositories (`carbon-digital-drawing-studio`, `Haru`, `Oasis-Ai`, `Portfolio`, `ejhay27`); no bio, blog, email, or social handles — the contact section therefore stays GitHub + Portfolio source only.
- Verified project destinations remain exactly two: `Oasis-Ai` and `carbon-digital-drawing-studio`. The other eight inventory entries have no public repository; they are listed without links and without guessed URLs.
- Stack evidence: Carbon's manifest (TypeScript 5.9, React 19, Vite 7, Tailwind 4, Electron 33, Capacitor 8, three.js, Zustand) plus Haru/Portfolio manifests (React/Vite/Tailwind/TypeScript) and repository language bytes (TypeScript, JavaScript, CSS, HTML — and Python, contributed by this profile's own maintenance scripts).
- Owner instructions this session: remove every background image, make animated typography the centerpiece, split tools into three sections, keep all ten projects with exact statuses.

## Design decisions

- **No background image anywhere.** `hero.jpg` and `dragon-landscape.png` were deleted from the repository; the README references neither. The only wide visual is the animated title card, which is content, not wallpaper.
- **Hero:** `assets/hero-title-card.gif`, 1200×420, autoplays in every environment that renders GIFs — including GitHub's camo-proxied README images — with no controls, no click, and no scripting. Three phrases in order, each held 4,550 ms plus a nine-step 450 ms dissolve: exactly five seconds per phrase and a 15 s infinite loop (`loop=0`). All frames share one 256-colour palette so the static ornament never flickers; final size 721 KB. Known limitation: GIF cannot honour `prefers-reduced-motion`, so a text-only `<details>` fallback states the phrases statically.
- **Typography:** bundled Cormorant Garamond variable font (weight 300 for phrases, 500 for the letterspaced overline), manual letterspacing in the builder. Palette: midnight #0a1322–#0f1d34 field, silver ink #e9f1fa, steel rules #33507a, diamond accents #7d97b5.
- **Logo tiles:** 64×64 SVGs — navy field, rounded frame tinted per section (creative #8fa7c0, dev #5f9fd4, langs #a9c8e4) — wrapping Simple Icons glyph paths (v16.35.0; archived v12.4.0 for the Adobe, Visual Studio Code, and classic CSS3 marks removed upstream). Dark glyphs (GitHub #181717, IntelliJ IDEA #000000) are lightened toward moonlit silver until they clear a 3.0:1 contrast ratio against the field. Alight Motion has no official open glyph, so its tile is an original "AM" lettermark, disclosed in the README and attribution.
- **Skills honesty:** "Currently using" shows only what public code backs (TypeScript, JavaScript, HTML5, CSS3 + React, Tailwind CSS, Vite, Electron). "Learning" and "Exploring" are intentionally empty: the owner has confirmed no candidate there and the brief forbids inventing interest. Database engines and DB administration tools are excluded from the personal toolkit entirely; BASALT stays in the workshop as a concept row without implying a personal stack claim.
- **Statistics:** the self-hosted snapshot (`docs/languages.json` + `assets/languages.svg`) was refreshed on 2026-10-15 and now includes the Python bytes of this profile's maintenance scripts — disclosed in the README text. Live links point to the repositories and overview tabs. No third-party card services and no streak widgets, because none are dependable README-compatible sources; nothing can expire silently or mislabel an estimate as official GitHub data.
- **Contact:** GitHub profile and the Portfolio source repository only; the account API exposes no other destination, and none were invented.

## Validation performed

- `scripts/validate_profile.py`: ten project rows with exact names/statuses; single centred h1 and the exact signature; no `hero.jpg`/dragon references; the three section titles present exactly once; all 8 + 8 + 6 required labels inside their sections; no MariaDB/MySQL/PostgreSQL/MongoDB/SQLite/SQL/XAMPP/phpMyAdmin anywhere; alt text on every `<img>`; every referenced local asset exists; every SVG static and self-contained; GIF `loop=0`, 15,000 ms total, phrase starts at 0/5,000/10,000 ms; snapshot percentages agree between JSON, chart, and README alt text; every URL in the README belongs to `github.com/ejhay27`.
- GitHub's Markdown API (GFM in repository context) was used to confirm the final README survives sanitization: tables, `<sub>`, `<details>`, alignment attributes, and image tags all render; no script/style injection.
- GIF frames were inspected locally at desktop size and downscaled to 375 px for a mobile read: phrases stay legible, dissolves are smooth, ornament is stable across frames.
- Logo tiles were validated structurally (valid XML, one Simple Icons path each, affine transform keeping the glyph inside 14–50 px of the 64 px tile). The sandbox has no browser or SVG rasterizer, so in-browser tile rendering gets its final confirmation when the page is viewed on GitHub.

## Delivery

- Committed on `arena/279f5510-ejhay27`, pushed, and delivered through pull request #__ against `main` (same authorized flow as the previous session). No force-push; branch protections untouched.
