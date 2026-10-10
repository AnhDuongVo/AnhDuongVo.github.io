---
card_cover: card.jpg
title: 'Clinical agentic AI: four workflow prototypes'
summary: Four reproducible AI workflow prototypes for healthcare and life sciences.
date: 2026-09-01
weight: 10
tags:
- Agentic AI
- LLM Agents
- Healthcare
- NVIDIA
- RAG
short: Clinical agents
card: Clinical documentation, trial screening, study reports and protein-design orchestration.
---

These independent projects explore clinical documentation, trial pre-screening, clinical study reporting and protein-design research. They draw on problems encountered during my research and industry collaborations, reconstructed in my own time as developer examples.

The common engineering problem is reviewing generated outputs against evidence. The projects combine structured outputs, source references, deterministic checks where applicable, and human-review steps using Nemotron, NVIDIA NIM, NeMo Agent Toolkit and BioNeMo. The scope of each check is documented; these are research and developer examples and have not been clinically validated.

## Watch the workflows

The recordings below come from [clinical-agentic-ai-demo](https://github.com/AnhDuongVo/clinical-agentic-ai-demo). That interactive page uses synthetic data, bundled text and simplified checking logic. It illustrates the workflows; the full repositories contain additional functionality and optional model integrations.

### consult-to-note

**Engineering decision:** keep each note sentence linked to transcript evidence. Numerical, dose/unit, citation, negation and laterality failures remain flagged even when a model judge is configured. Ambiguous lexical matches can use a probabilistic judge. Clinician review remains necessary for the whole note.

{{< video src="consult-to-note.mp4" controls="yes" >}}

**Try it offline:** clone [consult-to-note](https://github.com/AnhDuongVo/consult-to-note), install `pip install -e ".[dev]"`, then run `pytest -q`. Tests use synthetic fixtures and model stubs. `c2n demo --no-trials` generates text using a configured model endpoint and requires its credentials; it is a separate live path.

The repository includes batch, streaming and FHIR export paths, plus an ACI-Bench evaluation harness. A NAT invocation returns a preliminary, reviewable draft; clinician approval requires the explicit review workflow. Hosted and self-hosted NVIDIA runs need separate validation.

### trial-matcher

**Engineering decision:** preserve missing or unsupported evidence as “unknown.” Parsed age, sex and simple laboratory thresholds use deterministic rules. Labs require compatible units and usable dates. A criterion-specific measurement window takes precedence over the documented demo fallback. Unsupported compound thresholds and quantitative criteria require review rather than model arithmetic.

{{< video src="trial-matcher.mp4" controls="yes" >}}

**Try it offline:** clone [trial-matcher](https://github.com/AnhDuongVo/trial-matcher), install `pip install -e ".[dev]"`, then run `pytest -q`. The synthetic fixtures test extraction, rules and review overrides. `ctm demo` requires a model endpoint.

Criteria parsing and qualitative assessments remain probabilistic. Confidence scores are heuristics, not calibrated probabilities. Coordinator review is needed before screening decisions are used.

### csr-assistant

**Engineering decision:** cite table rows for generated data sentences, check numerical values and explicit directions, and flag detectable treatment-arm or endpoint mismatches. Model review handles qualitative claims and ambiguous numerical context; neither layer establishes complete clinical correctness.

{{< video src="csr-assistant.mp4" controls="yes" >}}

**Try it offline:** clone [csr-assistant](https://github.com/AnhDuongVo/csr-assistant), install `pip install -e ".[dev]"`, then run `pytest -q`. The bundled synthetic study includes planted errors and correct claims. `csr demo` requires a model endpoint.

Medical writers must review the revised text and unresolved findings. The repository includes an evaluation harness for error detection and false alarms.

### ai-scientist

**Engineering decision:** orchestrate RFdiffusion, ProteinMPNN and Boltz-2 with traceable candidate reports. Sequence design is restricted to the generated binder chain and checks sequence length. Stable simulation seeds make offline results reproducible across Python processes.

{{< video src="ai-scientist.mp4" controls="yes" >}}

**Try it offline:** clone [ai-scientist](https://github.com/AnhDuongVo/ai-scientist), install `pip install -e ".[dev]"`, then run `sci demo` and `pytest -q`.

The offline structures and scores are synthetic. The composite ranking is a heuristic, not a validated binding prediction. Folding a binder alone does not measure binding. Live BioNeMo calls require real target inputs and separate endpoint validation; experimental follow-up is necessary for scientific conclusions.

## Reproduce and inspect

Each repository documents installation, environment variables, architecture, tests and limits. Its validation matrix distinguishes unit tests, mocked integrations, live hosted tests, self-hosted tests and domain validation. Passing offline tests establishes software behavior on the tested fixtures.
