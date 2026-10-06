---
title: Agentic AI tooling and evaluation
summary: "Open developer tools for agentic AI, beyond any single vendor: an MCP server for BioNeMo, a cross-framework evaluation harness, and a RAG service with citation verification."
date: 2026-10-01
weight: 9
tags:
  - Agentic AI
  - MCP
  - Evaluation
  - RAG
  - Developer Tools
---

Open tools that make agentic AI easier to build, trust and evaluate. These are framework and vendor neutral, which is the point: the hard parts of agentic AI (discovery, evaluation, grounding) are the same whatever model you run.

## Tools

**mcp-bionemo.** A Model Context Protocol server that exposes NVIDIA BioNeMo NIMs (RFdiffusion, ProteinMPNN, Boltz-2) as typed tools, so any MCP client can call them. BioNeMo ships as agent skills and raw endpoints but not as MCP, so this closes a real gap. Runs on a simulator by default, one flag switches to the live NIMs. [github.com/AnhDuongVo/mcp-bionemo](https://github.com/AnhDuongVo/mcp-bionemo)

**clinical-agent-eval.** A reusable harness that scores clinical agent outputs on grounding, number accuracy, hallucinated-citation rate and calibration, and renders a leaderboard. [github.com/AnhDuongVo/clinical-agent-eval](https://github.com/AnhDuongVo/clinical-agent-eval)

**[agenteval](https://github.com/AnhDuongVo/agenteval) (framework-agnostic).** The same evaluation ideas generalized across agent frameworks (LangGraph, LlamaIndex, OpenAI tool-calling), so one harness scores traces from any of them.

**[rag-guidelines](https://github.com/AnhDuongVo/rag-guidelines).** Retrieval-augmented generation over public clinical guidelines and drug labels, with every answer verified against its cited source, on a neutral open stack.

## Live demo

An interactive app (offline, no key needed) that runs the verification logic of the clinical agents: [github.com/AnhDuongVo/clinical-agentic-ai-demo](https://github.com/AnhDuongVo/clinical-agentic-ai-demo)
