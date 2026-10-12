---
card_cover: card.jpg
title: 'Clinical agentic AI: four workflow prototypes'
summary: Prototypes for drafting clinical notes, screening trial criteria, reviewing
  study reports and exploring protein-design workflows.
date: 2026-09-01
weight: 10
tags:
- Agentic AI
- LLM Agents
- Healthcare
- NVIDIA
- RAG
short: Clinical agents
card: From consultation transcripts to reviewable notes; from patient records and
  study tables to evidence-linked screening and reports.
---

These independent projects explore clinical documentation, trial pre-screening, clinical study reporting and protein-design research. They draw on problems encountered during my research and industry collaborations, reconstructed in my own time as developer examples.

The common engineering problem is reviewing generated outputs against evidence. The projects combine structured outputs, source references, deterministic checks where applicable, and human-review steps using Nemotron, NVIDIA NIM, NeMo Agent Toolkit and BioNeMo. The scope of each check is documented; these are research and developer examples and have not been clinically validated.

## Watch the workflows

The consult-to-note recording runs the full repository’s SOAP pipeline with synthetic input and clearly labeled scripted model responses. The other three recordings come from [clinical-agentic-ai-demo](https://github.com/AnhDuongVo/clinical-agentic-ai-demo), which uses synthetic data, bundled text and simplified checking logic. The recording scope is stated for each project.

### consult-to-note

**Input:** a consultation transcript. **Output:** a structured SOAP draft with **Subjective, Objective, Assessment and Plan**, transcript citations, check findings and a preliminary FHIR export.

**Motivation:** Turning a consultation into a structured clinical note requires preserving details such as doses, symptoms and follow-up plans. A fluent draft can still omit evidence or introduce an incorrect value, making it difficult to review.

**What the program does:** consult-to-note turns a consultation transcript, or speech processed through its optional speech integration, into a structured SOAP note. Draft sentences link back to transcript evidence. The pipeline screens selected numerical, dose, citation and consistency errors, supports clinician review, and exports a preliminary FHIR document. Its aim is to make drafting and review more traceable; it does not replace clinical judgment.

**Engineering decision:** keep each note sentence linked to transcript evidence. Numerical, dose/unit, citation, negation and laterality failures remain flagged even when a model judge is configured. Ambiguous lexical matches can use a probabilistic judge. Clinician review remains necessary for the whole note.

{{< video src="consult-to-note.mp4" controls="yes" >}}

**Recording scope:** The actual extract → draft → ground → revise → FHIR workflow runs in the full repository’s [SOAP interface](https://github.com/AnhDuongVo/consult-to-note/blob/main/examples/soap_workflow.py). A synthetic consultation and scripted model responses make the example reproducible offline. The video shows all four SOAP sections, inspects source evidence, and revises a planted 800 mg error to 400 mg. This demonstrates the software pipeline; it does not demonstrate live model generation or complete clinical correctness.

**Try it offline:** clone [consult-to-note](https://github.com/AnhDuongVo/consult-to-note), install `pip install -e ".[dev]"`, then run `pytest -q`. Tests use synthetic fixtures and model stubs. `c2n demo --no-trials` generates text using a configured model endpoint and requires its credentials; it is a separate live path.

The repository includes batch, streaming and FHIR export paths, plus an ACI-Bench evaluation harness. A NAT invocation returns a preliminary, reviewable draft; clinician approval requires the explicit review workflow. Hosted and self-hosted NVIDIA runs need separate validation.

### trial-matcher

**Motivation:** Trial pre-screening requires comparing a patient record with many eligibility criteria. Missing laboratory results, stale measurements and complex criteria can make a confident yes-or-no answer misleading.

**What the program does:** trial-matcher compares a patient’s FHIR record with a ClinicalTrials.gov study and produces an evidence-linked status for each criterion: met, not met or unknown. It applies deterministic rules to supported criteria and leaves unsupported quantitative criteria for review. A study coordinator reviews the proposed result before a candidate status can be changed. The project supports pre-screening rather than making enrollment decisions.

**Engineering decision:** preserve missing or unsupported evidence as “unknown.” Parsed age, sex and simple laboratory thresholds use deterministic rules. Labs require compatible units and usable dates. A criterion-specific measurement window takes precedence over the documented demo fallback. Unsupported compound thresholds and quantitative criteria require review rather than model arithmetic.

{{< video src="trial-matcher.mp4" controls="yes" >}}

**Demo scope:** Simplified threshold illustration with synthetic scalar inputs. This does not exercise FHIR parsing, trial retrieval or model assessment.

**Try it offline:** clone [trial-matcher](https://github.com/AnhDuongVo/trial-matcher), install `pip install -e ".[dev]"`, then run `pytest -q`. The synthetic fixtures test extraction, rules and review overrides. `ctm demo` requires a model endpoint.

Criteria parsing and qualitative assessments remain probabilistic. Confidence scores are heuristics, not calibrated probabilities. Coordinator review is needed before screening decisions are used.

### csr-assistant

**Motivation:** Writing a clinical study report means translating source tables into a consistent narrative. Numbers, treatment arms and outcome descriptions can drift during drafting, and missing sections create additional review work.

**What the program does:** csr-assistant takes a draft report, study tables and a protocol synopsis. It screens the report’s ICH E3 structure, drafts supported missing sections with table-row citations, and returns findings about selected numerical inconsistencies and qualitative claims. A medical writer can review the proposed sections and findings before exporting revised text and a review report. The project aims to make the source-to-report review trail easier to inspect.

**Engineering decision:** cite table rows for generated data sentences, check numerical values and explicit directions, and flag detectable treatment-arm or endpoint mismatches. Model review handles qualitative claims and ambiguous numerical context; neither layer establishes complete clinical correctness.

{{< video src="csr-assistant.mp4" controls="yes" >}}

**Demo scope:** Selected values are compared with synthetic table rows; counts are exact and continuous rounding tolerance is explicit. This is not ICH E3 document review.

**Try it offline:** clone [csr-assistant](https://github.com/AnhDuongVo/csr-assistant), install `pip install -e ".[dev]"`, then run `pytest -q`. The bundled synthetic study includes planted errors and correct claims. `csr demo` requires a model endpoint.

Medical writers must review the revised text and unresolved findings. The repository includes an evaluation harness for error detection and false alarms.

### ai-scientist

**Motivation:** Exploring protein binder candidates involves several separate steps: reviewing literature, generating backbones, designing sequences and examining structural scores. Connecting these steps and keeping candidate inputs and results traceable is an engineering problem in its own right.

**What the program does:** ai-scientist orchestrates a candidate-design workflow around RFdiffusion, ProteinMPNN and Boltz-2, then assembles a ranked report for a scientist to inspect. It includes a reproducible simulator for testing the workflow without model endpoints. The project demonstrates orchestration and candidate comparison; its heuristic ranking and simulated scores do not establish binding or biological effectiveness.

**Engineering decision:** orchestrate RFdiffusion, ProteinMPNN and Boltz-2 with traceable candidate reports. Sequence design is restricted to the generated binder chain and checks sequence length. Stable simulation seeds make offline results reproducible across Python processes.

{{< video src="ai-scientist.mp4" controls="yes" >}}

**Demo scope:** Simulated scores with the protein-only ranking formula. No RFdiffusion, ProteinMPNN or Boltz-2 inference is performed.

**Try it offline:** clone [ai-scientist](https://github.com/AnhDuongVo/ai-scientist), install `pip install -e ".[dev]"`, then run `sci demo` and `pytest -q`.

The offline structures and scores are synthetic. The composite ranking is a heuristic, not a validated binding prediction. Folding a binder alone does not measure binding. Live BioNeMo calls require real target inputs and separate endpoint validation; experimental follow-up is necessary for scientific conclusions.

## Reproduce and inspect

Each repository documents installation, environment variables, architecture, tests and limits. Its validation matrix distinguishes unit tests, mocked integrations, live hosted tests, self-hosted tests and domain validation. Passing offline tests establishes software behavior on the tested fixtures.
