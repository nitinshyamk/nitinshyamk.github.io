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
    "resume": "/",
    "cv": "/",
    "publication/2016-sublinear-estimation-sparse": "/#sublinear-estimation-sparse",
    "publication/2019-automated-center-out-task-for-motor-variability": "/#automated-center-out-reach-task",
    "publication/2020-solving-control-problems-with-physics-informed-ml": "/#physics-informed-ml-control",
    "publication/2021-steady-state-analysis-of-bbr-using-network-calculus": "/#bbr-network-calculus",
    "publication/2022-06-10-context-aware-control-stability-and-learning-error": "/#context-aware-control",
}

DATE_PREFIX = re.compile(r"^\d{4}-\d{2}-\d{2}-")

# Any link that leaves this page opens in a new tab; in-page anchors stay put.
OFFSITE_LINK = re.compile(r'<a\s+href="(?!#)([^"]*)"')


def new_tab(markup):
    return OFFSITE_LINK.sub(
        lambda m: f'<a href="{m.group(1)}" target="_blank" rel="noopener noreferrer"',
        markup,
    )


# Masthead icons, keyed by the label used in content/links.md. Single-path
# monochrome marks at a 24x24 viewBox; they inherit color from the link.
def _icon(*paths):
    shapes = "".join('<path d="' + d + '"/>' for d in paths)
    return (
        '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" '
        'focusable="false">' + shapes + "</svg>"
    )


ICONS = {
    "github": _icon(
        "M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113"
        ".82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042"
        "-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729"
        " 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998"
        ".108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31"
        ".465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3"
        " 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552"
        " 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91"
        " 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0"
        " 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24"
        " 17.592 24 12.297c0-6.627-5.373-12-12-12"
    ),
    "linkedin": _icon(
        "M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0"
        "-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637"
        "-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c"
        "-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0"
        " 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3"
        ".555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0"
        " 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24"
        " .774 23.2 0 22.225 0z"
    ),
    "x": _icon(
        "M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99"
        " 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833"
        "L7.084 4.126H5.117z"
    ),
    # A whole cap over a ball that carries the cut-out. The notch follows the
    # cap's lower edges pushed out 1.2 units, so the gap survives at 18px.
    "google scholar": _icon(
        "M12 2.5 0 7.75 12 13 24 7.75Z",
        "M6.99 12.12A7 7 0 1 0 17.01 12.12L12 14.31Z",
    ),
}

LINK_ITEM = re.compile(r"^-\s*\[([^\]]+)\]\(([^)]+)\)\s*$", re.M)


def link_items():
    """content/links.md is the source of truth: one `- [Label](url)` per line."""
    text = (ROOT / "content" / "links.md").read_text(encoding="utf-8")
    items = [(l.strip(), u.strip()) for l, u in LINK_ITEM.findall(text)]
    if not items:
        raise SystemExit("content/links.md: no `- [Label](url)` entries found")
    return items


def link_url(label):
    for name, url in link_items():
        if name.lower() == label:
            return url
    raise SystemExit(f"content/links.md: no '{label}' entry")


def render_publications_heading():
    """The section heading is the link to the Scholar profile."""
    return (
        f'<a href="{html.escape(link_url("google scholar"), quote=True)}"'
        ' target="_blank" rel="noopener noreferrer"'
        ' title="Google Scholar profile"'
        ' aria-label="Publications on Google Scholar">Publications'
        f'{ICONS["google scholar"]}</a>'
    )


def render_links():
    """The masthead icon row; the label picks the icon."""
    items = link_items()
    parts = []
    for label, url in items:
        icon = ICONS.get(label.strip().lower())
        if icon is None:
            raise SystemExit(
                f"content/links.md: no icon for '{label}'"
                " -- add one to ICONS in build.py"
            )
        esc_label = html.escape(label, quote=True)
        parts.append(
            f'<li><a href="{html.escape(url, quote=True)}"'
            ' target="_blank" rel="noopener noreferrer"'
            f' aria-label="{esc_label}" title="{esc_label}">{icon}</a></li>'
        )
    return '<ul class="icons">\n' + "\n".join(parts) + "\n</ul>"


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
    return meta, new_tab(str(out).strip())


def unquote(value):
    """Strip the surrounding quotes YAML needs but markdown2 leaves in place."""
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def render_publications():
    """One <article> per publication, newest first (filenames are date-prefixed).

    The abstract starts folded away behind a one-line summary; the two swap
    places on click (see the .pub-body rules in style.css).
    """
    parts = []
    for path in sorted((ROOT / "content" / "publications").glob("*.md"), reverse=True):
        meta, abstract = render(path)
        for key in ("title", "authors", "venue", "date", "url", "summary"):
            if key not in meta:
                raise SystemExit(f"{path.name}: missing front matter key '{key}'")
        slug = DATE_PREFIX.sub("", path.stem)

        title = html.escape(meta["title"])
        url = html.escape(meta["url"], quote=True)
        parts.append(
            f'<article class="pub" id="{slug}">\n'
            f'  <h3><a href="{url}" target="_blank" rel="noopener noreferrer">{title}</a></h3>\n'
            f'  <p class="meta">{html.escape(meta["authors"])} \u00b7 '
            f'<span class="venue">{html.escape(meta["venue"])}</span> \u00b7 '
            f'{html.escape(meta["date"][:4])}</p>\n'
            f'  <div class="pub-body">\n'
            f'    <div class="pub-fold pub-fold-summary">\n'
            f'      <button class="pub-summary" type="button" data-toggle\n'
            f'              aria-expanded="false" aria-controls="{slug}-abstract">'
            f'{html.escape(meta["summary"])}</button>\n'
            f'    </div>\n'
            f'    <div class="pub-fold pub-fold-abstract">\n'
            f'      <div class="abstract" id="{slug}-abstract" data-toggle>'
            f'{abstract}</div>\n'
            f'      <button class="pub-collapse" type="button" data-toggle>'
            f'Collapse</button>\n'
            f'    </div>\n'
            f'  </div>\n'
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
        "links": render_links(),
        "future": render(ROOT / "content" / "future.md")[1],
        "current": render(ROOT / "content" / "current.md")[1],
        "past": render(ROOT / "content" / "past.md")[1],
        "publications_heading": render_publications_heading(),
        "publications": render_publications(),
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
