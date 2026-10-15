import io
import json
import re
import tarfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'logos'
TARBALL = 'https://registry.npmjs.org/simple-icons/-/simple-icons-{v}.tgz'
VERSIONS = {'16': '16.35.0', '12': '12.4.0'}

FIELD = '#0c1a2e'
ACCENTS = {'creative': '#8fa7c0', 'dev': '#5f9fd4', 'langs': '#a9c8e4'}

# slug, file stem, label, source version, sections
TILES = [
    ('adobephotoshop',    'photoshop',     'Adobe Photoshop',    '12', ['creative']),
    ('adobeillustrator',  'illustrator',   'Adobe Illustrator',  '12', ['creative']),
    ('adobepremierepro',  'premiere-pro',  'Adobe Premiere Pro', '12', ['creative']),
    ('adobeaftereffects', 'after-effects', 'Adobe After Effects','12', ['creative']),
    ('figma',             'figma',         'Figma',              '16', ['creative']),
    ('krita',             'krita',         'Krita',              '16', ['creative']),
    ('blender',           'blender',       'Blender',            '16', ['creative']),
    ('visualstudiocode',  'vscode',        'Visual Studio Code', '12', ['dev']),
    ('intellijidea',      'intellij-idea', 'IntelliJ IDEA',      '16', ['dev']),
    ('git',               'git',           'Git',                '16', ['dev']),
    ('github',            'github',        'GitHub',             '16', ['dev']),
    ('nodedotjs',         'nodejs',        'Node.js',            '16', ['dev']),
    ('npm',               'npm',           'npm',                '16', ['dev']),
    ('vite',              'vite',          'Vite',               '16', ['dev', 'langs']),
    ('electron',          'electron',      'Electron',           '16', ['dev', 'langs']),
    ('typescript',        'typescript',    'TypeScript',         '16', ['langs']),
    ('javascript',        'javascript',    'JavaScript',         '16', ['langs']),
    ('html5',             'html5',         'HTML5',              '16', ['langs']),
    ('css3',              'css3',          'CSS3',               '12', ['langs']),
    ('react',             'react',         'React',              '16', ['langs']),
    ('tailwindcss',       'tailwindcss',   'Tailwind CSS',       '16', ['langs']),
]

TILE = '''<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64" role="img" aria-labelledby="{uid}">
<title id="{uid}">{label} logo</title>
<rect x="1" y="1" width="62" height="62" rx="13" fill="{field}"/>
<rect x="1" y="1" width="62" height="62" rx="13" fill="none" stroke="{accent}" stroke-width="1.6"/>
<path transform="translate(14 14) scale(1.5)" fill="{fill}" d="{d}"/>
</svg>
'''

ALIGHT = '''<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64" role="img" aria-labelledby="ti-alightmotion">
<title id="ti-alightmotion">Alight Motion lettermark (original placeholder; no official glyph is distributed in open icon sets)</title>
<rect x="1" y="1" width="62" height="62" rx="13" fill="{field}"/>
<rect x="1" y="1" width="62" height="62" rx="13" fill="none" stroke="{accent}" stroke-width="1.6"/>
<text x="32" y="42" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="26" letter-spacing="1.5" fill="#dce7f2">AM</text>
</svg>
'''


def parse_hex(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luminance(rgb):
    def lin(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    l1, l2 = sorted((luminance(a), luminance(b)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def adjust(hexcolor, target=2.3):
    """Lighten a brand colour until it is clearly visible on the midnight field.

    Near-black marks (GitHub, IntelliJ IDEA) are pushed toward moonlit silver
    with a higher target instead of stopping at muddy gray.
    """
    rgb = list(parse_hex(hexcolor))
    bg = parse_hex(FIELD)
    near_black = luminance(rgb) < 0.03
    goal = (230, 238, 247) if near_black else (255, 255, 255)
    target = 3.0 if near_black else target
    steps = 0
    while contrast(rgb, bg) < target and steps < 32:
        rgb = [round(c * 0.78 + g * 0.22) for c, g in zip(rgb, goal)]
        steps += 1
    return '#%02x%02x%02x' % tuple(rgb), steps > 0


def slugify(title):
    s = title.lower().replace('.', 'dot').replace('+', 'plus')
    return re.sub(r'[^a-z0-9]', '', s)


def load(version):
    url = TARBALL.format(v=VERSIONS[version])
    raw = urllib.request.urlopen(url).read()
    tf = tarfile.open(fileobj=io.BytesIO(raw))
    names = set(tf.getnames())
    data_member = next(m for m in ('package/data/simple-icons.json',
                                   'package/_data/simple-icons.json') if m in names)
    data = json.loads(tf.extractfile(data_member).read())
    if isinstance(data, dict) and 'icons' in data:
        entries = data['icons']          # v12: list of {title, hex, ...}, no slug field
    elif isinstance(data, list):
        entries = data                   # v16: list of {title, slug, hex, ...}
    else:
        entries = list(data.values())
    meta = {(e.get('slug') or slugify(e['title'])): e for e in entries}
    paths = {}
    for slug in meta:
        member = f'package/icons/{slug}.svg'
        try:
            svg = tf.extractfile(member).read().decode()
        except KeyError:
            continue
        m = re.search(r'<path[^>]*\sd="([^"]+)"', svg)
        if m:
            paths[slug] = m.group(1)
    return meta, paths


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sources = {}
    for version in VERSIONS:
        sources[version] = load(version)

    written, adjusted = [], []
    for slug, stem, label, version, sections in TILES:
        meta, paths = sources[version]
        if slug not in paths:
            raise SystemExit(f'missing glyph: {slug} in simple-icons {VERSIONS[version]}')
        fill, was_adjusted = adjust('#' + meta[slug]['hex'])
        if was_adjusted:
            adjusted.append(f'{label}: #{meta[slug]["hex"]} -> {fill}')
        for section in sections:
            name = stem if section != 'langs' or len(sections) == 1 else f'{stem}-langs'
            svg = TILE.format(uid=f'ti-{name.replace("-", "")}', label=label,
                              field=FIELD, accent=ACCENTS[section], fill=fill, d=paths[slug])
            (OUT / f'{name}.svg').write_text(svg)
            written.append(f'{name}.svg  ({label}, simple-icons {VERSIONS[version]}, {section})')

    svg = ALIGHT.format(field=FIELD, accent=ACCENTS['creative'])
    (OUT / 'alight-motion.svg').write_text(svg)
    written.append('alight-motion.svg  (Alight Motion, original lettermark, creative)')

    print('\n'.join(written))
    print('\ncontrast-adjusted glyphs (lightened toward silver):')
    print('\n'.join(adjusted) if adjusted else '  none')
    print(f'\n{len(written)} tiles written to {OUT}')


if __name__ == '__main__':
    main()
