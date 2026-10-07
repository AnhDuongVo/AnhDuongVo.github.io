---
title: Clinical agentic AI (four end-to-end agents)
summary: "Four end-to-end examples of agentic AI for healthcare and the life sciences, built with the NVIDIA NeMo stack."
date: 2026-09-01
weight: 10
tags:
  - Agentic AI
  - LLM Agents
  - Healthcare
  - NVIDIA
  - RAG
---

Four open, end-to-end examples of agentic AI for healthcare and the life sciences, built with the NVIDIA NeMo stack (NeMo Agent Toolkit, NIM, Nemotron, NeMo Guardrails, BioNeMo). They run on synthetic and public data only, so the code can be shared and reproduced without any protected data.

All four follow the same pattern: the model drafts, code checks the numbers and citations, and a person reviews the result before it is used. Each example below has a short video recorded from the interactive demo. The checks in the videos run live; the generated clinical text is a bundled sample.

## 1. consult-to-note: ambient clinical documentation

Turns a consultation transcript into a structured SOAP note. Each sentence of the note cites the transcript lines it came from, numbers such as doses and vitals are compared against those lines in code, and a clinician accepts or rejects each sentence before the note is exported as a FHIR document. Speech recognition uses Riva/Parakeet with boosting for drug names, and the pipeline runs in batch mode, live during the consultation, and as a served endpoint.

The video (36 s) shows two consultations. For each, the note is generated with its numbers verified, then an error is planted (250 mg instead of 25 mg; 25 units instead of 2.5 units) and the check flags the sentence against the transcript line.

{{< video src="consult-to-note.mp4" controls="yes" >}}

## 2. trial-matcher: clinical-trial screening

Checks a patient's FHIR record against the eligibility criteria of a ClinicalTrials.gov study. Each criterion gets a status (met, not met, or unknown) together with the FHIR resources it rests on and a confidence value. Age, sex and lab thresholds are evaluated in code; criteria that need reading are passed to the model; a lab value that is missing or older than a year is reported as unknown. A study coordinator reviews the result before the patient is contacted.

The video (33 s) shows two patients. For the first, the eGFR criterion is unknown until a value is added, and lowering HbA1c flips that criterion to not met. For the second, two criteria start as not met and are resolved by editing the record.

{{< video src="trial-matcher.mp4" controls="yes" >}}

## 3. csr-assistant: clinical study report review

Checks a draft clinical study report against the ICH E3 section structure, drafts missing sections from the source tables with a row citation on every sentence, and reviews the text: every number is compared in code against the row it cites, and qualitative claims such as "well tolerated" are checked against the data by the model. A medical writer accepts or rejects each finding.

The video (29 s) shows two sections. In the efficacy section a placebo-arm change of -1.4 is flagged against the table's -0.35 and verified once corrected; in the safety section a discontinuation count of 3 is flagged against the table's 2.

{{< video src="csr-assistant.mp4" controls="yes" >}}

## 4. ai-scientist: protein binder design

For a target protein, the agent writes a literature brief that cites only retrieved abstracts, then chains three BioNeMo models: RFdiffusion designs backbones for the epitope, ProteinMPNN designs sequences for each backbone, and Boltz-2 co-folds each binder with the target and scores the complex. Candidates are ranked by a composite score into a report that states its method and limits. The project runs on a deterministic simulator by default; one flag switches each step to the real BioNeMo NIMs.

The video (25 s) changes the target, the random seed and the number of candidates and shows the ranking update. The scores come from the simulator and are placeholders.

{{< video src="ai-scientist.mp4" controls="yes" >}}

## Stack

NeMo Agent Toolkit, NIM, Nemotron, NeMo Guardrails, Riva/Parakeet ASR, guided JSON (constrained decoding), BioNeMo NIMs, FHIR, Python.

Code: [consult-to-note](https://github.com/AnhDuongVo/consult-to-note), [trial-matcher](https://github.com/AnhDuongVo/trial-matcher), [csr-assistant](https://github.com/AnhDuongVo/csr-assistant), [ai-scientist](https://github.com/AnhDuongVo/ai-scientist).

## Related

The interactive app the videos were recorded from, which runs offline without a key: [clinical-agentic-ai-demo](https://github.com/AnhDuongVo/clinical-agentic-ai-demo). An MCP server for the BioNeMo models: [mcp-bionemo](https://github.com/AnhDuongVo/mcp-bionemo). An evaluation harness that scores the four projects' claims and agent behavior: [agenteval](https://github.com/AnhDuongVo/agenteval).
