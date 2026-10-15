"""Local structural checks; requires Pillow. No network access."""
import json
import re
from pathlib import Path
from xml.etree import ElementTree as ET
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / 'README.md').read_text()
expected = {
    'OASIS-AI': 'In Development', 'O.R.V.Y.N': 'Prototype',
    'Purge': 'In Development', 'IDE': 'In Development',
    'BASALT': 'Prototype', 'Carbon: Flux': 'Prototype',
    'Carbon': 'Working Build', 'Folian': 'Prototype',
    'Xenon Pro DAW': 'In Development', 'MyClassmate': 'Prototype',
}
rows = [line for line in text.splitlines() if line.startswith('| ') and '**' in line]
assert len(rows) == 10
for name, status in expected.items():
    found = [row for row in rows if f'**{name}**' in row]
    assert len(found) == 1 and found[0].endswith(f'| {status} |'), name
assert text.count('# Haru Unabara') == 1
assert 'CREATIVE | SPECIALIST | BREATHING' in text
assert not re.search(r'<(?:script|style|iframe|foreignObject)\b', text, re.I)
for tag in re.findall(r'<img\b[^>]+>', text):
    assert re.search(r'alt="[^"]+"', tag)
for path in re.findall(r'(?:src="|\]\()(assets/[^"\)]+)', text):
    assert (ROOT / path).is_file(), path
for path in (ROOT / 'assets').rglob('*.svg'):
    root = ET.parse(path).getroot()
    assert not any(el.tag.split('}')[-1] in {'script', 'foreignObject', 'animate'} for el in root.iter())
    assert 'http' not in path.read_text().replace('http://www.w3.org/2000/svg', '')
with Image.open(ROOT / 'assets/hero-phrases.gif') as gif:
    assert gif.info['loop'] == 0
    assert gif.n_frames == 31  # Pillow merges identical adjacent hold frames.
    durations = []
    for i in range(gif.n_frames):
        gif.seek(i)
        durations.append(gif.info['duration'])
    assert sum(durations) == 15000
    # Crossfades start at 4.5s, 9.5s, 14.5s; identical endpoint frames
    # are merged into the following hold without changing playback time.
    starts, elapsed = [], 0
    for duration in durations:
        if duration >= 4500:
            starts.append(elapsed)
        elapsed += duration
    assert starts == [0, 4950, 9950]
source = (ROOT / 'scripts/build_assets.py').read_text()
assert "PHRASES = ['Creative and Illustrative', 'Breathe and Relax', 'Play the Game']" in source
snapshot = json.loads((ROOT / 'docs/languages.json').read_text())
assert len(snapshot['repositories']) == 5
assert sum(snapshot['total_bytes_by_language'].values()) > 0
print('PASS: ten projects/statuses, identity, local images/alt text, safe SVG/markup, GIF 3 × 5s infinite loop, public snapshot.')
