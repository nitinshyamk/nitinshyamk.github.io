# nitinshyamk.github.io

A single-page site. Markdown in `content/` is the source of truth; `build.py`
renders it into `index.html` using `template.html` and `style.css`.

## Editing

1. Edit the markdown under `content/`:
   - `links.md` — the masthead icon row, one `- [Label](url)` per line; the
     label picks the mark from `ICONS` in `build.py`, and the build fails if a
     label has no icon
   - `future.md`, `current.md`, `past.md` — one file per section, plain prose;
     the section labels themselves live in `template.html`
   - `publications/*.md` — one file per paper, ordered newest-first by the
     `YYYY-MM-DD-` filename prefix, with `title`, `authors`, `venue`, `date`,
     `url`, and `summary` front matter; the body is the abstract, folded behind
     the summary on the page
2. Preview while you edit:
   ```
   python3 serve.py          # http://localhost:8000, rebuilds on save
   ```
   Or build once, without a server:
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
| `serve.py` | local preview: rebuild on save, serve on :8000 |
| `vendor/markdown2.py` | vendored MIT parser, never edited |
| `index.html`, `404.html`, `*/index.html` | **generated** — do not hand-edit |
| `files/`, `images/` | PDFs and the headshot |
