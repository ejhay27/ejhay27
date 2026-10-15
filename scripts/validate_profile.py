import json
import re
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / 'README.md').read_text()

# --- 1. ten projects, exact names and statuses -----------------------------
expected = {
    'OASIS-AI': 'In Development', 'O.R.V.Y.N': 'Prototype',
    'Purge': 'In Development', 'IDE': 'In Development',
    'BASALT': 'Prototype', 'Carbon: Flux': 'Prototype',
    'Carbon': 'Working Build', 'Folian': 'Prototype',
    'Xenon Pro DAW': 'In Development', 'MyClassmate': 'Prototype',
}
rows = [line for line in text.splitlines() if line.startswith('| ') and '**' in line]
assert len(rows) == 10, f'expected 10 project rows, found {len(rows)}'
for name, status in expected.items():
    found = [row for row in rows if f'**{name}**' in row]
    assert len(found) == 1 and found[0].endswith(f'| {status} |'), name
assert sum('Carbon: Flux' in r for r in rows) == 1
assert sum(r.startswith('| [**Carbon**](') for r in rows) == 1, 'Carbon needs its own row'

# --- 2. identity, signature, no background imagery --------------------------
assert text.count('<h1 align="center">Haru Unabara</h1>') == 1
assert 'CREATIVE | SPECIALIST | BREATHING' in text
assert 'hero.jpg' not in text, 'old banner must not be referenced'
assert 'dragon' not in text.lower(), 'no dragon artwork may remain in the README'

# --- 3. three separate tools sections, exact titles -------------------------
for section in ('## Creative & Design Tools',
                '## Development Tools & Environment',
                '## Programming Languages & Technologies'):
    assert text.count(section) == 1, section
creative = ['Adobe Photoshop', 'Adobe Illustrator', 'Adobe Premiere Pro', 'Adobe After Effects',
            'Figma', 'Krita', 'Blender', 'Alight Motion']
dev = ['Visual Studio Code', 'IntelliJ IDEA', 'Git', 'GitHub', 'Node.js', 'npm', 'Vite', 'Electron']
langs = ['TypeScript', 'JavaScript', 'HTML5', 'CSS3']
frameworks = ['React', 'Tailwind CSS']
sec_creative = text.split('## Creative & Design Tools')[1].split('## Development')[0]
sec_dev = text.split('## Development Tools & Environment')[1].split('## Programming')[0]
sec_lang = text.split('## Programming Languages & Technologies')[1].split('## Public Code')[0]
for label in creative:
    assert f'<b>{label}</b>' in sec_creative, label
for label in dev:
    assert f'<b>{label}</b>' in sec_dev, label
for label in langs + frameworks:
    assert f'<b>{label}</b>' in sec_lang, label

# --- 4. excluded database technologies never appear ------------------------
for term in ('MariaDB', 'MySQL', 'PostgreSQL', 'MongoDB', 'SQLite', 'XAMPP', 'phpMyAdmin'):
    assert term.lower() not in text.lower(), term
assert not re.search(r'\bSQL\b', text), 'bare SQL must not appear'

# --- 5. markup safety, alt text, local assets exist ------------------------
assert not re.search(r'<(?:script|style|iframe|foreignObject)\b', text, re.I)
for tag in re.findall(r'<img\b[^>]+>', text):
    assert re.search(r'alt="[^"]+"', tag), tag
for path in re.findall(r'(?:src="|\()\s*(assets/[^")\s]+)', text):
    assert (ROOT / path).is_file(), path
    assert 'dragon' not in path and 'hero.jpg' not in path

# --- 6. SVG assets stay static and self-contained --------------------------
for path in (ROOT / 'assets').rglob('*.svg'):
    root = ET.parse(path).getroot()
    assert not any(el.tag.split('}')[-1] in {'script', 'foreignObject', 'animate'} for el in root.iter())
    assert 'http' not in path.read_text().replace('http://www.w3.org/2000/svg', '')

# --- 7. hero GIF: autoplay loop, 5 s per phrase, correct order -------------
with Image.open(ROOT / 'assets/hero-title-card.gif') as gif:
    assert gif.info['loop'] == 0, 'GIF must loop forever'
    durations = []
    for i in range(gif.n_frames):
        gif.seek(i)
        durations.append(gif.info['duration'])
    assert sum(durations) == 15000, sum(durations)
    starts, elapsed = [], 0
    for duration in durations:
        if duration >= 1000:  # hold frames
            starts.append(elapsed)
        elapsed += duration
    assert starts == [0, 5000, 10000], starts
source = (ROOT / 'scripts/build_assets.py').read_text()
assert "PHRASES = ['Creative and Illustrative', 'Breathe and Relax', 'Play the Game']" in source

# --- 8. snapshot chart matches its data file and README alt text -----------
snapshot = json.loads((ROOT / 'docs/languages.json').read_text())
assert len(snapshot['repositories']) == 5
totals = snapshot['total_bytes_by_language']
assert sum(totals.values()) > 0
grand = sum(totals.values())
for language, count in totals.items():
    pct = f'{count / grand * 100:.1f}%'
    assert pct in text, f'{language} {pct} missing from README'
svg_text = (ROOT / 'assets/languages.svg').read_text()
for language in totals:
    assert language in svg_text, language

# --- 9. link policy: only github.com destinations --------------------------
for url in re.findall(r'https?://[^)\s"<>]+', text):
    assert url.startswith('https://github.com/ejhay27'), url

print('PASS: ten projects/statuses, identity + signature, no background imagery,')
print('      three tool sections with all required labels, no DB technologies,')
print('      alt text + local assets + static SVG, GIF 3x5s infinite loop in order,')
print('      snapshot/alt-text consistency, github.com-only links.')
