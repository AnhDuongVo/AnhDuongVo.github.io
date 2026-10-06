---
title: Clinical Agentic AI (open examples)
summary: Four end-to-end examples of agentic AI for healthcare and the life sciences, built on the open NVIDIA stack.
date: 2026-09-01
weight: 10
tags:
  - Agentic AI
  - LLM Agents
  - Healthcare
  - NVIDIA
  - RAG
---

Four open, end-to-end examples of agentic AI for healthcare and the life sciences, built on the open NVIDIA stack (NeMo Agent Toolkit, NIM, Nemotron, NeMo Guardrails, BioNeMo). They run on synthetic and public data only, so the implementations can be shared and reproduced without any protected data.

One design principle runs through all of them: in healthcare, a fluent wrong answer is the real risk. So the model cites its evidence, code checks every number, the model judges only meaning, and a human signs off.

## The four examples

**[consult-to-note](https://github.com/AnhDuongVo/consult-to-note), ambient clinical documentation.** Turns a consultation transcript into a structured clinical note in which every sentence cites the evidence it rests on, code verifies doses and numbers, and a clinician accepts or rejects each item. Speech recognition uses Riva/Parakeet, and the project ships in batch, live, and served modes.

**[trial-matcher](https://github.com/AnhDuongVo/trial-matcher), clinical-trial screening.** Checks a patient's FHIR record against a study's eligibility criteria and marks each criterion met, not met, or unknown, with the facts it rests on and a calibrated confidence. Rules decide age, sex, and lab thresholds in code; the model handles the rest; a coordinator confirms before anyone is contacted.

**[csr-assistant](https://github.com/AnhDuongVo/csr-assistant), regulatory writing.** Checks a draft clinical study report against the ICH E3 structure, drafts missing sections from the source tables with a row citation per sentence, and verifies every number in code against the cited row. A medical writer accepts or rejects each finding.

**[ai-scientist](https://github.com/AnhDuongVo/ai-scientist), protein binder design.** For a target protein, writes a cited literature brief, then chains the BioNeMo models (RFdiffusion, ProteinMPNN, Boltz-2) to design, fold, and score candidate binders into a ranked, honest report. It runs on a deterministic simulator by default; one flag switches each step to the real BioNeMo NIMs.

## Stack

NeMo Agent Toolkit, NIM, Nemotron, NeMo Guardrails, Riva/Parakeet ASR, guided JSON (constrained decoding), BioNeMo NIMs, FHIR, Python.

All four are open source on GitHub: [github.com/AnhDuongVo](https://github.com/AnhDuongVo).

## Try it and build on it

**Live demo.** An interactive app (offline, no key needed) that runs the verification logic of all four examples: [clinical-agentic-ai-demo](https://github.com/AnhDuongVo/clinical-agentic-ai-demo).

**Related tooling.** [mcp-bionemo](https://github.com/AnhDuongVo/mcp-bionemo), a Model Context Protocol server that exposes the BioNeMo NIMs (RFdiffusion, ProteinMPNN, Boltz-2) as tools, and [clinical-agent-eval](https://github.com/AnhDuongVo/clinical-agent-eval), a reusable harness that scores grounding, number accuracy, hallucinated citations and calibration across the four projects.
