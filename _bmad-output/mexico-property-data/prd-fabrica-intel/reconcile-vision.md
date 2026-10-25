# Reconcile — User Vision Input

## Input: User vision statement (verbatim)

> La visión central de Fábrica Inmobiliaria es construir un sistema industrializado y estandarizado —similar a una fábrica— que produzca transacciones inmobiliarias exitosas y repetibles utilizando propiedades, datos y preguntas como materia prima. Resuelve el problema de operar con procesos aislados y desconectados, transformando la dispersión del día a día en una arquitectura empresarial con rutinas claras, especialización territorial y comercial, y la capacidad de convertir datos complejos en asesoría de alto valor para cerrar operaciones.

## Gaps found vs prd.md

| # | Gap | Location in PRD | Severity |
|---|-----|-----------------|----------|
| 1 | **"Preguntas como materia prima" (questions as raw material) not surfaced as a product capability.** The vision names *preguntas* (questions) as a third input alongside properties and data. The PRD's Sentiment Intelligence module ingests community Q&A but there is no explicit product capability for a *broker submitting questions to the system* and getting advisory back. | §5 Module 2 (Sentiment Intelligence) | Medium |
| 2 | **"Especialización territorial y comercial" (territorial + commercial specialization) not modeled as a feature.** The vision implies territorial specialization (per-colonia expertise) and commercial specialization (broker vs. developer vs. investor workflows). PRD has role-based views (FR-1.6) but no explicit "territorial specialization" capability (e.g., per-colonia market briefs, territory-level expertise profiles). | §5 Module 1 | Medium |
| 3 | **"Arquitectura empresarial con rutinas claras" (enterprise architecture with clear routines) not captured.** The vision describes a *system of routines*, not just a dashboard. No "broker workflow routines" or "deal pipeline" capability. | §1 Vision, §5 | Low |
| 4 | **"Produce transacciones exitosas y repetibles" (produces successful, repeatable transactions) — success metric gap.** The vision's outcome is *closed transactions*. PRD §7 success metrics measure activity (subscribers, MAU, exports) but none measure *transactions influenced/closed*. | §7 Success Metrics | High |
| 5 | **Vision text in PRD is a paraphrase, not the user's own words.** The user supplied the vision in Spanish; PRD §1 is an English paraphrase. Should carry the user's framing. | §1 Vision | Low |

## Qualitative ideas the FR structure silently drops

- **"Materia prima" metaphor** — properties/data/questions as raw material → suggests an *industrial pipeline* mental model (ingest → refine → product). Worth naming in the architecture narrative (addendum), not necessarily in PRD FRs.
- **"Rutinas claras"** — suggests a *broker operating system* with daily/weekly/monthly routines, not a passive analytics tool. This is a positioning difference from competitors and should inform the value proposition.
- **"Asesoría de alto valor para cerrar operaciones"** — high-value advisory *to close deals*. This is the actual product outcome; the PRD should anchor all features to this.