"""Build the animated hero title card (assets/hero-title-card.gif).

Requires Pillow and numpy; the Cormorant Garamond variable font is bundled
under assets/fonts/. No background photograph or illustration is used: the
card is pure typography on a midnight-navy field.

Timing model: three phrases, each held 4,550 ms and followed by nine 50 ms
dissolve steps (450 ms), so every phrase begins exactly 5 s after the
previous one and the whole card loops every 15 s (loop=0, infinite). All
durations are exact GIF centiseconds and no two adjacent frames are
identical, so nothing is merged by the encoder. The GIF autoplays wherever
GitHub renders it; there are no controls and no scripting.
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'assets'
FONT = str(A / 'fonts/CormorantGaramond.ttf')
PHRASES = ['Creative and Illustrative', 'Breathe and Relax', 'Play the Game']

W, H = 1200, 420
INK = '#e9f1fa'        # moonlit silver, phrase text
OVERLINE = '#a7bed6'   # muted silver-blue, name line
RULE = '#33507a'       # steel blue, thin rules and frame
RULE_INNER = '#223b5e'
DIAMOND = '#7d97b5'    # silver diamond accents
DIAMOND_DIM = '#46648f'


def font(size, weight=300):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_axes([weight])
    return f


def tracked(draw, cx, cy, text, f, fill, tracking=0.0):
    """Draw letterspaced text centred on (cx, cy)."""
    widths = [draw.textlength(ch, font=f) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        if ch != ' ':
            draw.text((x + w / 2, cy), ch, font=f, fill=fill, anchor='mm')
        x += w + tracking


def background():
    """Subtle vertical gradient with a soft moonlit glow behind the phrases."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    top = np.array([10, 19, 34], np.float32)
    mid = np.array([15, 29, 52], np.float32)
    bot = np.array([9, 17, 31], np.float32)
    t = (yy / (H - 1))[..., None]
    grad = np.where(t < 0.5, top + (mid - top) * (t / 0.5), mid + (bot - mid) * ((t - 0.5) / 0.5))
    dx = (xx - W / 2) / (W * 0.45)
    dy = (yy - H * 0.52) / (H * 0.42)
    r = np.clip(np.sqrt(dx * dx + dy * dy), 0, 1)
    g = np.clip(1.0 - (3 * r * r - 2 * r * r * r), 0, 1) ** 1.5 * 0.5  # smoothstep falloff, no rim
    glow = np.array([28, 50, 86], np.float32)
    grad = grad * (1 - g[..., None]) + glow * g[..., None]
    grad = np.clip(np.round(grad / 4) * 4, 0, 255)  # snap tones: fewer palette entries
    return Image.fromarray(grad.astype(np.uint8), 'RGB')


def ornament(draw, y, small=False):
    half = 145 if not small else 0
    if not small:
        draw.line((415, y, 560, y), fill=RULE, width=1)
        draw.line((640, y, 785, y), fill=RULE, width=1)
        draw.ellipse((406, y - 2, 410, y + 2), fill=RULE)
        draw.ellipse((790, y - 2, 794, y + 2), fill=RULE)
        r = 6
        draw.polygon([(600, y - r), (600 + r, y), (600, y + r), (600 - r, y)], fill=DIAMOND)
    else:
        r = 3.5
        draw.polygon([(600, y - r), (600 + r, y), (600, y + r), (600 - r, y)], fill=DIAMOND_DIM)
        draw.ellipse((574, y - 1.6, 577, y + 1.6), fill=RULE)
        draw.ellipse((623, y - 1.6, 626, y + 1.6), fill=RULE)


def static_card():
    base = background()
    d = ImageDraw.Draw(base)
    d.rounded_rectangle((16, 16, W - 17, H - 17), radius=14, outline=RULE, width=2)
    d.rounded_rectangle((26, 26, W - 27, H - 27), radius=9, outline=RULE_INNER, width=1)
    tracked(d, 600, 96, 'HARU UNABARA', font(26, 500), OVERLINE, tracking=14)
    ornament(d, 140)
    ornament(d, 296)
    ornament(d, 344, small=True)
    return base


def phrase_frame(base, text):
    im = base.copy()
    tracked(ImageDraw.Draw(im), 600, 218, text, font(76, 300), INK, tracking=2)
    return im


def main():
    base = static_card()
    frames, durations = [], []
    for i, phrase in enumerate(PHRASES):
        current = phrase_frame(base, phrase)
        following = phrase_frame(base, PHRASES[(i + 1) % 3])
        frames.append(current)
        durations.append(4550)  # exact centiseconds: GIF timing has 10 ms granularity
        for step in range(1, 10):  # nine 50 ms dissolve steps = 450 ms
            frames.append(Image.blend(current, following, step / 10))
            durations.append(50)

    # One shared palette for every frame keeps static areas perfectly still.
    probe = Image.new('RGB', (W, H * 2))
    probe.paste(frames[0], (0, 0))
    probe.paste(frames[5], (0, H))  # mid-crossfade tones
    palette = probe.quantize(colors=256, method=Image.MEDIANCUT)
    quantized = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]

    out = A / 'hero-title-card.gif'
    quantized[0].save(out, save_all=True, append_images=quantized[1:],
                      duration=durations, loop=0, disposal=2, optimize=True)
    print(f'{out.name}: {out.stat().st_size / 1024:.0f} KB, {len(frames)} frames, '
          f'{sum(durations)} ms loop')

    # Previews for visual inspection (not committed).
    frames[0].save('/tmp/hero-frame-a.png')
    frames[5].save('/tmp/hero-frame-fade.png')
    frames[10].save('/tmp/hero-frame-b.png')
    frames[0].resize((375, int(H * 375 / W)), Image.Resampling.LANCZOS).save('/tmp/hero-frame-mobile.png')


if __name__ == '__main__':
    main()
