---
card_cover: card.jpg
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
short: "Clinical agents"
card: "Four end-to-end agents for the clinic, the trial, the regulatory submission and the lab, each with a recorded demo."
---

This page walks through four clinical agents I built in my own time with the NVIDIA NeMo stack. Each one has a short demo video, a "try it yourself" block, and notes on why the design looks the way it does. Everything runs on synthetic and public data, so you can clone any repository and reproduce what you see here.

## Why these four belong together

A new medicine passes through four places before it reaches a patient, and in each one a lot of time goes into writing and checking text:

| Stage | Who does the work today | Agent |
| --- | --- | --- |
| Lab | Scientists design and test candidate molecules | ai-scientist |
| Clinical trial | Study coordinators screen patients against eligibility criteria | trial-matcher |
| Regulatory submission | Medical writers turn trial tables into clinical study reports | csr-assistant |
| Clinic | Doctors document every consultation | consult-to-note |

Language models are good at drafting this kind of text. The problem is that a well-written draft can still contain a wrong dose, a wrong lab value or a wrong number from a table, and in these four places that mistake has real consequences. So all four agents share one design:

1. **The model drafts and cites.** Every sentence points to the transcript line, record field, table row or paper it came from.
2. **Code checks what code can check.** Numbers, units, thresholds and dates are compared against the cited source in plain Python, not by another model.
3. **A model judges the rest.** Only statements that need reading (for example "well tolerated") go to an LLM judge.
4. **A person signs off.** The clinician, coordinator or writer accepts or rejects each finding before anything is used.

Seeing the same pattern applied to four different problems is the point of putting them side by side: once you understand one, you can read the other three in minutes.

All four demos below were recorded from one interactive page ([clinical-agentic-ai-demo](https://github.com/AnhDuongVo/clinical-agentic-ai-demo)) that runs the real checking code offline. The clinical text in the videos is a bundled sample; to generate it live you add a free API key from build.nvidia.com.

## 1. consult-to-note: documentation from a consultation

**The gap.** Doctors spend a large part of their day writing notes after consultations. Ambient documentation tools listen to the conversation and draft the note, but a clinician then has to reread everything, because a single wrong dose in a signed note is a patient safety issue.

**The idea.** Make every sentence of the note carry its evidence, and check the numbers automatically, so the clinician only has to look at the sentences that failed a check.

**How it works**

1. Speech recognition (Riva with the Parakeet model) turns audio into numbered transcript lines. Drug names are boosted so they are recognised correctly.
2. A fast Nemotron model extracts structured facts (complaints, vitals, medications) as JSON that has to match a schema.
3. A reasoning Nemotron model drafts a SOAP note in which every sentence cites the transcript lines it used.
4. Code compares every number, unit, negation and left or right side against the cited lines. Unclear sentences go to an LLM judge.
5. Sentences that fail are sent back to the model once with the reason. The clinician then accepts or rejects each sentence, and the approved note is exported as a FHIR R4 document.

**Why these tools**

| Tool | What it does here | Why this one |
| --- | --- | --- |
| Riva / Parakeet | Speech to text, streaming or batch | Runs on the hospital's own GPUs; word boosting for drug names |
| Nemotron via NIM | Extraction, drafting, judging | Open model behind an OpenAI-compatible API, so the same code runs hosted during development and on premises in production |
| Guided JSON | Structured output | The output is machine-checkable instead of free text |
| NeMo Guardrails + Presidio | Masks personal data before it reaches a hosted model | Data minimisation when a hosted endpoint is used |
| NeMo Agent Toolkit | Runs, profiles and evaluates the workflow | Per-step latency and token use without writing my own profiler |
| LangGraph | Pauses the run for clinician approval | Human sign-off is a built-in step, not an afterthought |

**What the demo shows (38 s).** Two consultations. For each one the note appears with every number verified against its transcript line. Then an error is planted (250 mg instead of 25 mg, then 25 units instead of 2.5 units) and the check flags exactly that sentence, showing the transcript value next to it.

{{< video src="consult-to-note.mp4" controls="yes" >}}

**Results and limits.** The pipeline runs end to end in batch mode, live during the consultation (the note updates within about a second of each utterance by sending small edits instead of rewriting the note), and as a served endpoint. Evaluation on the public ACI-Bench dataset is built in (support rate, omissions, hallucinations, ROUGE, latency per step). Limits: FHIR resources carry free text rather than SNOMED or RxNorm codes, and the grounding check reduces but does not remove the need for clinician review.

**Try it**

```
git clone https://github.com/AnhDuongVo/consult-to-note && cd consult-to-note
pip install -e ".[dev]"
c2n demo --no-trials        # synthetic diabetes follow-up, end to end
pytest                      # runs offline, no key needed
```

## 2. trial-matcher: screening patients for clinical trials

**The gap.** Many trials struggle to recruit enough patients, and screening is manual: a coordinator reads a long eligibility text and checks it against a patient's record, criterion by criterion. A model can read both quickly, but if it guesses a missing lab value it can wrongly exclude or include a patient.

**The idea.** Split the eligibility text into single criteria and give each one a clear status (met, not met, or unknown), together with the record fields it rests on. When the evidence is missing or out of date, the answer is "unknown", which tells the coordinator which test to order instead of making a decision on their behalf.

**How it works**

1. Read the patient's FHIR record and the study's eligibility text from ClinicalTrials.gov.
2. Split the text into individual criteria.
3. Evaluate thresholds (age, sex, lab values with units and dates) in code. A lab value older than a year counts as missing.
4. Send only the criteria that need reading to Nemotron.
5. Return each criterion with its status, the FHIR resources it used and a confidence. A coordinator reviews the result, which is written back as a FHIR ResearchSubject.

**Why these tools**

| Tool | What it does here | Why this one |
| --- | --- | --- |
| FHIR R4 | Patient record in, screening result out | The standard hospitals already exchange data in |
| Rules in Python | Thresholds, units, dates | Auditable, free and never inconsistent |
| Nemotron via NIM | Free-text criteria | Handles wording that rules cannot |
| NeMo Agent Toolkit | Packaging and evaluation | Same run, profile and evaluate workflow as the other agents |

**What the demo shows (38 s).** Two synthetic patients. For the first, the kidney function criterion is "unknown" until a value is added; lowering HbA1c then flips the HbA1c criterion to "not met". For the second, two criteria start as "not met" and change as the record is edited, so you can see each status follow the data.

{{< video src="trial-matcher.mp4" controls="yes" >}}

**Results and limits.** The repository includes 51 hand-labelled criteria as an evaluation set. That is enough to catch regressions, not to claim clinical accuracy, and all patients are synthetic.

**Try it**

```
git clone https://github.com/AnhDuongVo/trial-matcher && cd trial-matcher
pip install -e ".[dev]"
ctm demo
```

## 3. csr-assistant: reviewing clinical study reports

**The gap.** A clinical study report summarises a trial for regulators and follows a fixed structure (ICH E3). Medical writers spend days checking that every number in the text matches the source tables. Language models help with drafting, but they round, swap and occasionally invert numbers.

**The idea.** Let the model draft and review the text, but check every number in code against the table row it cites.

**How it works**

1. Check the draft against the ICH E3 section structure and list missing sections.
2. Draft missing sections from the source tables, with a row citation on every sentence.
3. Compare every number in the text with the row it cites. Whole counts must match exactly; percentages may be rounded.
4. A reviewer agent checks qualitative claims (for example "well tolerated") against the data.
5. The medical writer accepts or rejects each finding in a review report.

**Why these tools**

| Tool | What it does here | Why this one |
| --- | --- | --- |
| Nemotron via NIM | Drafting and the reviewer agent | Same model family as the other agents, open weights |
| Python number checks | Text against table rows | Exact and explainable to a regulator |
| NeMo Agent Toolkit | Runs drafter and reviewer as one workflow | Built-in profiling and evaluation |

**What the demo shows (32 s).** Two report sections. In the efficacy section, a placebo-arm change of -1.4 is flagged because the table says -0.35, and it turns green once corrected. In the safety section, a count of 3 discontinuations is flagged against the table's 2.

{{< video src="csr-assistant.mp4" controls="yes" >}}

**Results and limits.** The checks run on one synthetic study. Cross-section consistency (the same number reported differently in two sections) is the next step.

**Try it**

```
git clone https://github.com/AnhDuongVo/csr-assistant && cd csr-assistant
pip install -e ".[dev]"
csr demo
```

## 4. ai-scientist: designing protein binders

**The gap.** Designing a protein that binds a disease target takes several separate models: one designs a backbone, one designs a sequence for it, one predicts whether the result binds. Chaining them by hand is slow, and the scores are easy to misread.

**The idea.** An agent that writes a short literature brief on the target, runs the three models in order, ranks the candidates and writes a report that states its method and its limits.

**How it works**

1. Retrieve abstracts about the target and write a brief that cites only what was retrieved.
2. RFdiffusion designs backbones for the binding site.
3. ProteinMPNN designs sequences for each backbone.
4. Boltz-2 folds each binder together with the target and scores the complex.
5. Rank candidates by a combined score and write the report.

**Why these tools**

| Tool | What it does here | Why this one |
| --- | --- | --- |
| BioNeMo NIMs (RFdiffusion, ProteinMPNN, Boltz-2) | The three design steps | Each model behind the same kind of endpoint, no local installs |
| Reasoning Nemotron | Literature brief and report | Writes the text around the numbers, with citations |
| Built-in simulator | Stands in for the models by default | Anyone can run the full workflow without a GPU or key |

**What the demo shows (29 s).** The target, the random seed and the number of candidates are changed, and the ranking updates each time. The scores come from the simulator and are placeholders.

{{< video src="ai-scientist.mp4" controls="yes" >}}

**Results and limits.** The workflow follows NVIDIA's protein binder design blueprint and switches to the real models with one flag. Computational scores are not lab results. A natural next step is adding Proteina-Complexa as a fourth design tool, and moving the model calls onto the BioNeMo Agent Toolkit released in June 2026.

**Try it**

```
git clone https://github.com/AnhDuongVo/ai-scientist && cd ai-scientist
pip install -e ".[dev]"
sci demo                    # simulator; add --real-bio with an NVIDIA API key
```

## What to take away

If you build agents for regulated domains, the reusable part is the pattern, not the model: ask for citations at generation time, check numbers in code, send only what code cannot decide to a model, and keep a person in the loop. The tooling around these agents (an MCP server for BioNeMo, an evaluation harness, a citation-checked retrieval service) is on the [Agentic AI tooling](../agentic-tooling/) page, and what it costs to serve them is on the [agent workload simulation](../agent-workload-sim/) page.

**Code:** [consult-to-note](https://github.com/AnhDuongVo/consult-to-note) · [trial-matcher](https://github.com/AnhDuongVo/trial-matcher) · [csr-assistant](https://github.com/AnhDuongVo/csr-assistant) · [ai-scientist](https://github.com/AnhDuongVo/ai-scientist) · [clinical-agentic-ai-demo](https://github.com/AnhDuongVo/clinical-agentic-ai-demo)
