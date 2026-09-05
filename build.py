#!/usr/bin/env python3
"""Build the single-page site from the markdown in content/.

Source of truth is content/*.md; this script renders it into OUT/index.html
using template.html. Run `python3 build.py` and commit the result.
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "vendor"))
import markdown2  # noqa: E402  (vendored, see vendor/README.md)

# "v2" builds the parallel preview site; "." builds in place at the repo root.
OUT = "."

EXTRAS = [
    "metadata",
    "tables",
    "fenced-code-blocks",
    "footnotes",
    "cuddled-lists",
    "header-ids",
    "strike",
]

# Old Jekyll permalink -> where it lives on the single page now.
REDIRECTS = {
    "about": "/",
    "publications": "/#publications",
    "resume": "/#resume",
    "cv": "/#resume",
    "publication/2016-sublinear-estimation-sparse": "/#sublinear-estimation-sparse",
    "publication/2019-automated-center-out-task-for-motor-variability": "/#automated-center-out-reach-task",
    "publication/2020-solving-control-problems-with-physics-informed-ml": "/#physics-informed-ml-control",
    "publication/2021-steady-state-analysis-of-bbr-using-network-calculus": "/#bbr-network-calculus",
    "publication/2022-06-10-context-aware-control-stability-and-learning-error": "/#context-aware-control",
}

DATE_PREFIX = re.compile(r"^\d{4}-\d{2}-\d{2}-")


def render(path):
    """Render a markdown file to (metadata dict, html string).

    The `metadata` extra also accepts fence-less MultiMarkdown headers, which
    would silently eat the first paragraph of a plain content file -- so it is
    only enabled for files that actually open with a `---` fence.
    """
    text = path.read_text(encoding="utf-8")
    fenced = text.startswith("---\n")
    extras = EXTRAS if fenced else [e for e in EXTRAS if e != "metadata"]
    out = markdown2.markdown(text, extras=extras)
    meta = {k: unquote(v) for k, v in (getattr(out, "metadata", None) or {}).items()}
    return meta, str(out).strip()


def unquote(value):
    """Strip the surrounding quotes YAML needs but markdown2 leaves in place."""
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def render_publications():
    """One <article> per publication, newest first (filenames are date-prefixed)."""
    parts = []
    for path in sorted((ROOT / "content" / "publications").glob("*.md"), reverse=True):
        meta, abstract = render(path)
        for key in ("title", "authors", "venue", "date", "url"):
            if key not in meta:
                raise SystemExit(f"{path.name}: missing front matter key '{key}'")
        slug = DATE_PREFIX.sub("", path.stem)
        title = html.escape(meta["title"])
        url = html.escape(meta["url"], quote=True)
        parts.append(
            f'<article class="pub" id="{slug}">\n'
            f'  <h3><a href="{url}">{title}</a></h3>\n'
            f'  <p class="authors">{html.escape(meta["authors"])}</p>\n'
            f'  <p class="venue">{html.escape(meta["venue"])} '
            f'<span class="year">{html.escape(meta["date"][:4])}</span></p>\n'
            f'  <div class="abstract">{abstract}</div>\n'
            f"</article>"
        )
    if not parts:
        raise SystemExit("no publications found in content/publications/")
    return "\n".join(parts)


NOT_FOUND = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Not found - Nitin Shyamkumar</title>
<link rel="icon" href="/images/site-logo.png">
<link rel="stylesheet" href="/style.css">
</head>
<body>
<main>
<section>
<h2>404</h2>
<p>There's nothing at this address.</p>
<p><a href="/">Back to nitinshyamk.github.io</a></p>
</section>
</main>
</body>
</html>
"""


def stub(target):
    esc = html.escape(target, quote=True)
    return (
        "<!doctype html>\n"
        '<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        f'<meta http-equiv="refresh" content="0; url={esc}">\n'
        f'<link rel="canonical" href="https://nitinshyamk.github.io{esc}">\n'
        "<title>Moved</title>\n</head>\n<body>\n"
        f'<p>This page has moved to <a href="{esc}">nitinshyamk.github.io{esc}</a>.</p>\n'
        "</body>\n</html>\n"
    )


def write(relpath, text):
    dest = ROOT / OUT / relpath
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8")
    print(f"  {dest.relative_to(ROOT)}")


def main():
    fragments = {
        "links": render(ROOT / "content" / "links.md")[1],
        "about": render(ROOT / "content" / "about.md")[1],
        "publications_intro": render(ROOT / "content" / "publications-intro.md")[1],
        "publications": render_publications(),
        "resume": render(ROOT / "content" / "resume.md")[1],
    }

    page = (ROOT / "template.html").read_text(encoding="utf-8")
    for key, value in fragments.items():
        page = page.replace("{{" + key + "}}", value)
    leftover = re.findall(r"\{\{(\w+)\}\}", page)
    if leftover:
        raise SystemExit(f"template.html has unfilled placeholders: {leftover}")

    print(f"building into {OUT}/")
    write("index.html", page)
    write("404.html", NOT_FOUND)

    if OUT == ".":
        for path, target in sorted(REDIRECTS.items()):
            write(f"{path}/index.html", stub(target))
        write("about.html", stub("/"))


if __name__ == "__main__":
    main()
