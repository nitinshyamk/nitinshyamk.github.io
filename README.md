# nitinshyamk.github.io

A single-page site. Markdown in `content/` is the source of truth; `build.py`
renders it into `index.html` using `template.html` and `style.css`.

## Editing

1. Edit the markdown under `content/`:
   - `current.md`, `resume.md`, `links.md`, `publications-intro.md`
   - `past/*.md` — one file per subsection, ordered by the numeric filename
     prefix, each with a `title:` front matter key
   - `publications/*.md` — one file per paper, ordered newest-first by the
     `YYYY-MM-DD-` filename prefix, with `title`, `authors`, `venue`, `date`,
     and `url` front matter; the body is the abstract
2. Run the build:
   ```
   python3 build.py
   ```
   No dependencies beyond `python3` — the markdown parser is vendored in
   `vendor/` (see `vendor/README.md`).
3. Commit the regenerated `index.html`, `404.html`, and redirect stubs along
   with your content change. GitHub Pages serves the committed files as-is;
   `.nojekyll` keeps Jekyll out of it.

## Layout

| Path | What it is |
|---|---|
| `content/` | source of truth, hand-edited |
| `template.html` | page skeleton with `{{placeholders}}` |
| `style.css` | all styling, shipped as-is |
| `build.py` | the generator |
| `vendor/markdown2.py` | vendored MIT parser, never edited |
| `index.html`, `404.html`, `*/index.html` | **generated** — do not hand-edit |
| `files/`, `images/` | PDFs and the headshot |
