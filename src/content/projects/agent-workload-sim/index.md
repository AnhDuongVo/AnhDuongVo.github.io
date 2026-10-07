---
card_cover: card.jpg
title: Agent workload simulation and cost model
summary: "A discrete-event simulator for LLM agent workloads on a serving cluster: how many concurrent agents the cluster sustains, what fan-out and synchronization cost, and which scheduler wins."
date: 2026-10-07
weight: 8
tags:
  - Agentic AI
  - LLM Serving
  - Simulation
  - Scheduling
  - Systems
short: "agentsim"
card: "A discrete-event simulator for what agents cost to serve: concurrency, schedulers, fan-out and joins."
---

After building and evaluating agents, the next question a team asks is practical: how many of them can we run on our GPUs, how fast, and at what cost? Chat benchmarks do not answer that, because an agent is not one prompt. agentsim is a small simulator that answers it for agent workloads, and it can be calibrated against a real serving endpoint.

## The gap

A chat request is one prompt and one answer. An agent run is a sequence of model calls, tool calls and waits. Prompts grow with every tool result, and research-style agents fan out into several sub-agents that all have to finish before the run continues. Two consequences:

- The load on the serving cluster depends on the shape of the agent, not just the number of users.
- Some of the time a run takes is spent waiting for its slowest branch, which more GPUs do not fix.

Serving benchmarks measure tokens per second for independent requests, so they miss both effects.

## The idea

Describe agent runs as small graphs (stages of parallel branches made of model calls and tool calls), replay thousands of them against a model of a serving cluster, and measure what matters for agents: run latency, time to first token, time lost waiting at joins, GPU utilisation and cost per thousand runs.

## How it is modelled

![Model overview: workload, scheduler, cluster, metrics](model.png)

| Part | What is modelled | Why |
| --- | --- | --- |
| Workload | Stages of parallel branches; four built-in agent shapes (single chat, ReAct loop, plan / fan-out / summarise, and the shape of consult-to-note); real traces imported from agenteval | Agents differ in shape, and shape drives load |
| Cluster | Replicas with continuous batching, a KV-cache budget, a batch limit and a prefix cache | These are the mechanisms that decide throughput in vLLM, NIM or TGI |
| Scheduler | Who gets served next (first come, fewest steps left, or runs already started) and which replica gets a run | Once GPUs are busy, the scheduler decides whose run waits |
| Load | A fixed number of concurrent agents, or random arrivals | Matches both "N users" and "requests per second" views |

The simulator is plain Python with one dependency, runs a 300-run sweep in seconds, and has tests including a check against a hand-computed latency.

## Results

![Sweep over concurrent agents for three admission policies](sweep.png)

The figure sweeps the number of concurrent agents for a mixed workload (half chat, 30% ReAct, 20% fan-out) on two replicas with a batch limit of 32. Three things stand out:

1. **Throughput saturates near 32 agents.** Beyond that, extra agents only queue: latency and time to first token climb, and cost per run stops falling.
2. **The scheduler only matters once the cluster is full.** At 128 agents, serving the runs with the fewest steps left first cuts the median latency of chat runs from 23.5 s to 10.0 s and of ReAct runs from 162 s to 56 s. The fan-out runs pay for it (138 s to 168 s). That is a product decision, not a technical one.
3. **Waiting at joins is a property of the agent.** For the fan-out workload, adding replicas cuts latency almost linearly, but about 11% of each run is still spent waiting for the slowest branch. Only changing the agent design reduces that.

## What the recording shows (64 s)

The fan-out profile, a fifo versus shortest-first comparison on the mixed workload, the sweep that produces the figure, and the benchmark and calibration steps.

{{< video src="agentsim.mp4" controls="yes" >}}

## Calibration and limits

The default cluster numbers are of the order of an 8B model on one data-centre GPU; they are not measurements. To anchor them, `agentsim bench` sends concurrent streaming requests to any OpenAI-compatible server (vLLM, NIM, TGI, Ollama, a hosted API) and records time to first token and time between tokens, and `agentsim calibrate` fits the model to that. The model leaves out tensor parallelism, disaggregated prefill and decode, and speculative decoding, so comparisons (policy A against B, two replicas against four) are more reliable than absolute numbers.

## Try it

```
git clone https://github.com/AnhDuongVo/agentsim && cd agentsim
pip install -e ".[dev]"
agentsim run --profile fanout --runs 200 --gpus 2 --agents 32
agentsim sweep --profile chat:0.5,react:0.3,fanout:0.2 --gpus 2 --agents 4,8,16,32,64,128 --plot sweep.png
```

## What to take away

Before buying more GPUs for agents, look at the shape of the agent and at the scheduler. The [clinical agents](../clinical-agentic-ai/) provide the workload shapes, and [agenteval](../agentic-tooling/) traces can be fed straight into the simulator.

**Code:** [agentsim](https://github.com/AnhDuongVo/agentsim) (Apache-2.0)
