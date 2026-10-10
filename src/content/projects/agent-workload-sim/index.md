---
card_cover: card.jpg
title: Agent workload simulation
summary: Exploring latency, scheduling and GPU-serving economics for LLM agents.
date: 2026-10-07
weight: 8
tags:
- Agentic AI
- LLM Serving
- Simulation
- Scheduling
- Systems
short: agentsim
card: Model how agent concurrency, batching, caching and scheduling affect latency
  and estimated costs.
---

Agent workloads involve repeated model calls, tool use, parallel branches and synchronization delays. These patterns can behave very differently from a single chat request.

[agentsim](https://github.com/AnhDuongVo/agentsim) is a discrete-event simulator that models these workflows across configurable serving replicas. It explores how concurrency, batching, caching and scheduling policies affect latency, throughput and estimated costs.

## Watch and reproduce

{{< video src="agentsim.mp4" controls="yes" >}}

```bash
pip install -e ".[dev]"
agentsim run --profile fanout --runs 200 --gpus 2 --agents 32
pytest -q
```

The default results use explicit assumptions and synthetic workload profiles. They are modeled results, not measured GPU performance. The repository documents the replica model, scheduling policies, cache assumptions and phenomena it leaves out.

## Calibrate to observed serving behavior

The benchmark requests server-reported prompt and completion token usage. Streaming content chunks are recorded separately because one chunk can contain several tokens. When usage is unavailable, counts are explicitly estimated and excluded from token-latency calibration. Failed requests are recorded rather than disappearing from the result.

```bash
agentsim bench --url http://localhost:8000/v1 --model <model-id> --concurrency 1,4,16 --prompt-tokens 500,2000 --out measurement.jsonl
agentsim calibrate measurement.jsonl --out cluster.json
agentsim run --cluster cluster.json --profile clinical --gpus 1 --agents 16
```

These commands require a running endpoint supporting streaming usage. The effective decode interval is derived from aggregate usage and chunk arrival times; it is not a timestamp for every token. Network latency, server batching and estimated prompt lengths limit the fit. Validate the calibrated model on held-out workloads before using it for capacity planning.
