# Intercept — site reflow (review build)

A full rebuild of the Intercept marketing site from the 2026-08-06/07 wireframe set —
homepage, Our Work (31 case studies), What We Do (6 services), Intercept Labs, About Us,
Careers (hub, open roles, 9 role pages, apply), Contact, Insights (hub + 4 articles),
and legal (Terms, Privacy, AI Policy).

Local-review build, not connected to the production interceptgroup.com deploy pipeline.
Static HTML, no build step required to view — served as-is via GitHub Pages.

Build pipeline (Python, generates every page deterministically from the wireframe source)
lives in `_build/`.
