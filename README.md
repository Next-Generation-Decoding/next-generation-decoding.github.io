# Beyond Next Token Prediction — NeurIPS 2026 Workshop

Website for the NeurIPS 2026 workshop
**“Beyond Next Token Prediction: Diffusion and Flow Models for Next-Generation Decoding.”**

Explore the theory, algorithms, and applications of discrete diffusion and flow models for
parallel, non-causal generation — beyond next-token prediction.

## Local preview

The site is a single static `index.html` with no build step. Serve the folder with any static
server:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## Structure

- `index.html` — the entire site (HTML + CSS + JS in one file)
- `assets/people/` — speaker, panel, and organizer headshots
- `assets/og.png` — social share (Open Graph) image
- `assets/make_og.py` — script that regenerates `og.png` (requires Pillow)

## Deployment

Hosted on **GitHub Pages** from the `main` branch. All paths are relative, so the site also works
from a subpath.

## Status

A few details are still being finalized and are shown as **“TBD”** on the site:
location, OpenReview submission link, shared contact email, paper page limits, and sponsors.
