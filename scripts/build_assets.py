"""Build local README assets. Install Pillow 12.3.0 to reproduce."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'assets'
FONT = str(A / 'fonts/CormorantGaramond.ttf')
PHRASES = ['Creative and Illustrative', 'Breathe and Relax', 'Play the Game']

def font(size):
    return ImageFont.truetype(FONT, size)

source = Image.open(A / 'dragon-landscape.png').convert('RGB')
banner = source.resize((1200, 396), Image.Resampling.LANCZOS)
d = ImageDraw.Draw(banner)
d.text((55, 101), 'Haru Unabara', font=font(68), fill='#e5edf5')
d.line((58, 185, 322, 185), fill='#6c859d', width=1)
d.text((58, 202), 'CREATIVE  /  DIGITAL  /  EXPLORATION', font=font(20), fill='#bacbdc')
banner.save(A / 'hero.jpg', quality=93)

# Each phrase starts exactly 5 seconds after the previous one.
# 4.5 seconds held + 0.5 seconds of crossfade; no flashing or scripts.
frames, durations = [], []
def phrase_image(text):
    im = Image.new('RGB', (900, 76), '#0b1628')
    draw = ImageDraw.Draw(im)
    draw.text((450, 38), text, font=font(43), fill='#dce7f2', anchor='mm')
    return im
for i, phrase in enumerate(PHRASES):
    current = phrase_image(phrase)
    following = phrase_image(PHRASES[(i + 1) % 3])
    frames.append(current)
    durations.append(4500)
    for step in range(1, 11):
        frames.append(Image.blend(current, following, step / 10))
        durations.append(50)
frames[0].save(A / 'hero-phrases.gif', save_all=True, append_images=frames[1:],
               duration=durations, loop=0, disposal=2, optimize=False)

# Silver treatments retain the original Simple Icons path geometry.
for path in (A / 'logos').glob('*.svg'):
    svg = path.read_text()
    if 'fill="#bdcede"' not in svg:
        svg = svg.replace('<svg ', '<svg fill="#bdcede" ', 1)
    path.write_text(svg)
