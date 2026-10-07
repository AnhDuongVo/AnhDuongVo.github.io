---
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

Three tools around the clinical agents, written so that they work with any model or framework. Each has a short terminal recording; everything in the recordings runs offline without an API key.

## 1. mcp-bionemo: BioNeMo models as MCP tools

BioNeMo's biology models are available as NeMo Agent Toolkit agent skills and as HTTP endpoints, but not as a Model Context Protocol server, so MCP clients such as Claude Desktop, Cursor or an IDE agent cannot discover or call them directly. This server wraps the RFdiffusion, ProteinMPNN and Boltz-2 endpoints in typed MCP tools (`design_backbone`, `design_sequences`, `fold_complex`, and a one-call `design_binder`). It runs on a deterministic simulator by default and switches to the real NIMs with one environment variable, including the asynchronous job polling the hosted biology NIMs use.

The recording (21 s) runs the tool tests against the simulator and shows the client configuration that registers the server.

{{< video src="mcp-bionemo.mp4" controls="yes" >}}

## 2. agenteval: agent evaluation at two levels

Level 1 scores how an agent behaves, from traces. Adapters normalise LangGraph, LlamaIndex and OpenAI tool-calling traces into one schema, and the metrics cover tool success, tool selection, grounding of citations in retrieved context, task success, mean steps, and repeated tool calls. Level 2 scores what the agent says: grounding rate, hallucinated-citation rate, number accuracy with rounding tolerance, and calibration (ECE and Brier), with a per-task leaderboard. The clinical agents emit the level 2 schema, so one harness scores all of them.

The recording (22 s) runs both levels on the bundled samples; the claims leaderboard picks up a planted wrong number and a planted citation that does not exist.

{{< video src="agenteval.mp4" controls="yes" >}}

## 3. rag-guidelines: retrieval with citation verification

Retrieves the relevant passages from a corpus of clinical guidelines and drug labels, answers only from those passages with a citation on every sentence, and then checks each sentence against the chunk it cites: enough overlap in content words, and every number present in the source. Sentences that fail are flagged. It uses any OpenAI-compatible endpoint (vLLM, Ollama, TGI, hosted APIs) and has an offline extractive mode that needs no key. The bundled corpus is synthetic.

The recording (21 s) answers two questions and shows the retrieved sources with their scores and the per-sentence check.

{{< video src="rag-guidelines.mp4" controls="yes" >}}

## Code

[mcp-bionemo](https://github.com/AnhDuongVo/mcp-bionemo) · [agenteval](https://github.com/AnhDuongVo/agenteval) · [rag-guidelines](https://github.com/AnhDuongVo/rag-guidelines) · [clinical-agentic-ai-demo](https://github.com/AnhDuongVo/clinical-agentic-ai-demo)
