---
card_cover: card.jpg
title: Agentic AI tooling and evaluation
summary: "Developer tools for agentic AI that are not tied to one vendor: an MCP server for BioNeMo, a two-level agent evaluation harness, and a RAG service with citation verification."
date: 2026-10-01
weight: 9
tags:
  - Agentic AI
  - MCP
  - Evaluation
  - RAG
  - Developer Tools
short: "Tooling"
card: "An MCP server for BioNeMo, a two-level evaluation harness and a citation-checked retrieval service."
---

These three tools came out of building the [four clinical agents](../clinical-agentic-ai/). Each agent needed the same three things, and none of them was specific to healthcare or to one vendor, so I pulled them out into their own repositories. They work with any model and any agent framework, and everything in the recordings below runs offline without an API key.

## Why these three belong together

Once you have an agent, three questions come up in roughly this order:

| Question | Tool | What it gives you |
| --- | --- | --- |
| How do other agents and apps call my models? | mcp-bionemo | Biology models exposed as tools that any MCP client can discover |
| Is my agent doing the right thing? | agenteval | Scores for how the agent behaves and whether what it says is true |
| Is the answer backed by a source? | rag-guidelines | Retrieval where every sentence is checked against the passage it cites |

Together they cover the path from "the model is available" to "the agent uses it" to "we can show the output is grounded". That is also the order in which a team adopting agents usually runs into problems.

## 1. mcp-bionemo: BioNeMo models as MCP tools

**The gap.** The Model Context Protocol (MCP) is how agents and desktop apps such as Claude Desktop, Cursor or an IDE agent discover and call tools. NVIDIA's biology models (RFdiffusion, ProteinMPNN, Boltz-2) are available as HTTP endpoints and as NeMo Agent Toolkit skills, but there was no MCP server for them, so an MCP client could not use them without custom code.

**The idea.** A small server that wraps each model as a typed MCP tool, so the client sees a clear name, a description and the input schema, and can call it like any other tool.

**How it works**

1. Five tools: `design_backbone` (RFdiffusion), `design_sequences` (ProteinMPNN), `fold_complex` (Boltz-2), a one-call `design_binder`, and `info`.
2. A deterministic simulator answers by default, so you can try it with no GPU and no key.
3. One environment variable switches to the hosted NIMs, including the "202, then poll for the result" pattern that long biology jobs use.
4. Tool descriptions carry the practical advice, for example that a binder must be folded together with its target to say anything about binding. The agent reads these descriptions, so that is where the advice belongs.

**Why these tools**

| Choice | Why |
| --- | --- |
| MCP rather than a framework-specific plugin | One server works for Claude Desktop, Cursor, NeMo Agent Toolkit's MCP client and others |
| Simulator by default | A developer can test the integration in a minute before getting access to GPUs |
| Pinned `mcp>=2,<3` | Version 2 of the MCP Python SDK renamed its server class, which broke older examples |

**What the recording shows (21 s).** The tool tests running against the simulator, then the client configuration that registers the server in Claude Desktop.

{{< video src="mcp-bionemo.mp4" controls="yes" >}}

**Try it**

```
git clone https://github.com/AnhDuongVo/mcp-bionemo && cd mcp-bionemo
pip install -e ".[dev]" && pytest
```

## 2. agenteval: evaluating agents at two levels

**The gap.** Most evaluation tools look at one thing: either the trace of what an agent did, or the quality of its final answer, and usually for one framework. An agent can call all the right tools and still state a wrong number, so you need both views.

**The idea.** Two levels in one package. Level 1 scores behaviour from traces; level 2 scores the claims the agent makes against its sources.

**How it works**

1. **Behaviour.** Adapters turn LangGraph, LlamaIndex and OpenAI tool-calling traces into one common format. Metrics: tool success rate, whether the expected tools were used, whether cited sources were actually retrieved, task success, number of steps, and repeated tool calls (loops).
2. **Claims.** Each claim carries its citations, numbers and confidence. Metrics: grounding rate, share of citations that do not exist, number accuracy (rounding allowed, sign flips not), and calibration (does 90% confidence mean right 90% of the time).
3. A leaderboard compares tasks or agent versions side by side.

**Why these tools**

| Choice | Why |
| --- | --- |
| Adapters that read plain trace dictionaries | No dependency on any agent framework; installs anywhere |
| Numbers checked with a tolerance | Rounding is fine in a report, a wrong sign is not |
| Calibration (ECE, Brier) | Tells you whether you can use the agent's confidence to decide what a person should review |

**What the recording shows (22 s).** Both levels on the bundled samples. The claims leaderboard picks up a planted wrong number and a citation to a source that does not exist.

{{< video src="agenteval.mp4" controls="yes" >}}

**Try it**

```
git clone https://github.com/AnhDuongVo/agenteval && cd agenteval
pip install -e ".[dev]"
agenteval behavior data/sample_traces.jsonl
agenteval claims data/clinical_samples
```

## 3. rag-guidelines: retrieval with citation checks

**The gap.** Retrieval-augmented generation (RAG) gives the model the right passage, but the model can still write a dose that is not in that passage. Retrieving the right source is not the same as staying faithful to it.

**The idea.** After the answer is written, check every sentence against the chunk it cites, and flag the ones that are not supported.

**How it works**

1. Retrieve the top passages from a corpus of guideline and drug-label snippets.
2. Ask the model to answer only from those passages, with a citation on every sentence.
3. For each sentence, check that enough content words appear in the cited passage and that every number in the sentence is in the source.
4. Flag sentences that fail.

**Why these tools**

| Choice | Why |
| --- | --- |
| Simple TF-IDF retriever | The point of the repository is the check after generation; no embedding model needed to run it |
| Any OpenAI-compatible endpoint | Works with vLLM, Ollama, TGI, NIM or a hosted API |
| Offline extractive mode | Runs in tests and CI without a key |
| Synthetic corpus | Nobody mistakes the demo for medical advice |

**What the recording shows (21 s).** Two questions answered from the bundled corpus, with the retrieved passages, their scores and the check result for each sentence.

{{< video src="rag-guidelines.mp4" controls="yes" >}}

**Limits.** Word overlap can misjudge a paraphrase. The next step is sending sentences that fail the simple check to an entailment model, the same two-stage idea consult-to-note uses.

**Try it**

```
git clone https://github.com/AnhDuongVo/rag-guidelines && cd rag-guidelines
pip install -e ".[dev]"
rag ask "what is the maximum metformin dose?"
```

## What to take away

None of these tools needs a particular model or framework, which is deliberate: teams rarely start from a clean slate, and a tool that works with what they already have gets used. The [clinical agents](../clinical-agentic-ai/) show these tools in context, and the [agent workload simulation](../agent-workload-sim/) answers the next question, what it costs to serve the agents.

**Code:** [mcp-bionemo](https://github.com/AnhDuongVo/mcp-bionemo) · [agenteval](https://github.com/AnhDuongVo/agenteval) · [rag-guidelines](https://github.com/AnhDuongVo/rag-guidelines)
