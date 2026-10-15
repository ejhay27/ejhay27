import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def api(path):
    return json.loads(subprocess.check_output(['gh', 'api', path], text=True))

repos = []
page = 1
while True:
    batch = api(f'users/ejhay27/repos?per_page=100&page={page}')
    repos.extend(batch)
    if len(batch) < 100:
        break
    page += 1
languages = {}
sources = {}
for repo in sorted(repos, key=lambda r: r['name'].lower()):
    counts = api(f"repos/ejhay27/{repo['name']}/languages")
    sources[repo['name']] = counts
    for language, count in counts.items():
        languages[language] = languages.get(language, 0) + count
snapshot = {
    'account': 'ejhay27',
    'checked_at': datetime.now(timezone.utc).isoformat(),
    'method': 'Sum GitHub language bytes for every public repository, including forks if present. Not contribution or skill data.',
    'repositories': sources,
    'total_bytes_by_language': languages,
}
(ROOT / 'docs/languages.json').write_text(json.dumps(snapshot, indent=2) + '\n')
total = sum(languages.values())
colors = ['#aec8e2', '#82a4c6', '#5c81a6', '#41628a', '#2e4a6c', '#22384f']
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="230" viewBox="0 0 900 230" role="img" aria-labelledby="title desc">',
       '<title id="title">Public code language snapshot — ejhay27</title>',
       '<desc id="desc">Language bytes reported by the GitHub API, not proficiency. See docs/languages.json for the raw snapshot.</desc>',
       '<rect width="900" height="230" rx="8" fill="#0b1628"/>',
       '<g font-family="sans-serif" fill="#dce7f2"><text x="30" y="40" font-size="19">PUBLIC CODE / LANGUAGE BYTES</text>']
x = 30
for i, (language, count) in enumerate(sorted(languages.items(), key=lambda p: -p[1])):
    fraction = count / total
    width = 840 * fraction
    color = colors[i % len(colors)]
    svg.append(f'<rect x="{x:.3f}" y="65" width="{width:.3f}" height="12" fill="{color}"/>')
    x += width
    # Two columns remain legible when the card scales down.
    lx, ly = 30 + (i % 2) * 440, 123 + (i // 2) * 43
    svg.append(f'<circle cx="{lx+5}" cy="{ly-5}" r="5" fill="{color}"/><text x="{lx+23}" y="{ly}" font-size="20">{language} · {fraction*100:.1f}%</text>')
svg.append('</g></svg>')
(ROOT / 'assets/languages.svg').write_text('\n'.join(svg) + '\n')
print(json.dumps(languages, indent=2))
