# Haru Unabara profile implementation

## Audit — 2026-10-15

- Target confirmed via GitHub CLI: `ejhay27/ejhay27`, default branch `main`, write permission available. Session branch: `arena/2142c005-ejhay27`; clean starting tree at `cacb987`.
- Initial repository contained only GitHub's starter README; no reusable artwork, logos, cards, configurations, or local website existed. No existing functional profile content was removed.
- Public account API and repository listing verified five repositories: `ejhay27`, `Oasis-Ai`, `carbon-digital-drawing-studio`, `Haru`, `Portfolio`.
- Read Carbon's README and package manifest, OASIS-AI's README, and Haru/Portfolio package manifests. Carbon's source supports the displayed stack. OASIS-AI's README contains only its title; the video-studio direction comes from the owner's supplied inventory.
- Eight inventory destinations could not be independently identified in that public listing. They are explicitly pending review in the README, with no guessed URLs. Purge and MyClassmate could not be enriched from verified source.
- No public contact email or deployed portfolio destination was supplied by the account API. GitHub and Portfolio's source repository are linked; no deployed website is claimed.
- No website was added or unrelated repository modified.

## Rendering decisions

GitHub image markup supports ordinary JPG, GIF, and self-contained SVG images. This implementation uses no embedded scripts, SVG animation, foreignObject, external stylesheets, or interactive widgets. All visual assets are local.

The GIF is 900 × 76 with an infinite-loop extension. Each phrase is held for 4,500 ms and followed by ten 50 ms crossfade frames. Each phrase starts 5,000 ms after the previous phrase; the complete loop is 15,000 ms. Browser playback may vary with background-tab throttling and client animation preferences. The artwork is static, not a flight animation.

A GIF cannot react to prefers-reduced-motion inside GitHub Markdown. A text-only disclosure and direct static artwork link are provided; they do not stop the GIF elsewhere in the README. Essential text, project content, technology names, and contact links remain readable without images. The wide hero is decorative; the primary identity and signature also appear as real text outside it.

A three-column Markdown table avoids rigid-width project cards. GitHub may horizontally scroll it on very narrow displays. No custom mobile CSS is assumed. The language chart uses a two-column legend with a plain-text alternative.

Statistics are a dated public GitHub API snapshot, not an official GitHub statistics product. Language bytes are summed across the five repositories, so shared code may be counted more than once. No contribution counts, rankings, or skills are inferred. Live GitHub profile links supplement the static snapshot. Re-run the updater to refresh; no workflow or external card service is needed.

## Validation scope

`scripts/validate_profile.py` checks inventory, status labels, local image paths, image alternatives, prohibited markup, SVG safety, GIF duration/order/loop metadata, and the snapshot chart's labels. The asset builder was rerun and the hero visually inspected. GitHub's Markdown API is used separately to check renderer output. This is not a claim of pixel-level browser verification on GitHub desktop or mobile. Post-push content checks and the pull request provide reviewable remote evidence.
