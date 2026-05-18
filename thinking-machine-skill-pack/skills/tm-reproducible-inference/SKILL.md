---
name: tm-reproducible-inference
description: Use when diagnosing nondeterministic LLM outputs, designing reproducible inference, aligning trainer and sampler numerics, or evaluating batch-size and load-related output drift.
---

# Reproducible Inference

Use this skill when outputs must be reproducible, auditable, or stable enough for training.

## Core insight

Temperature 0 removes sampling randomness, but it does not guarantee deterministic user-visible completions. A server can be run-to-run deterministic for the exact same global workload while still being nondeterministic from one user's perspective because variable load changes batch size, chunking, and reduction order.

## Determinism levels

- `sampling deterministic`: fixed decoding rule and seed.
- `run-to-run deterministic`: same full server inputs produce same outputs.
- `batch-invariant`: a request's numerics do not change when other requests are batched with it.
- `chunk-invariant`: a sequence's numerics do not change when prefill, decode, or cache chunks are sliced differently.
- `trainer-sampler aligned`: training and sampling produce bitwise-compatible logprobs for the same policy.
- `hardware/version invariant`: outputs survive changes in hardware, kernels, driver, or library version. This is much harder.

## Investigation workflow

1. Fix sampler settings: temperature, top-p, top-k, max tokens, stop sequences, seed if available.
2. Record model id, tokenizer, system prompt, full input, engine, hardware, library versions, and request timing.
3. Run repeated completions under low load and high load.
4. Compare token sequences, first divergence token, logits if available, and logprob deltas.
5. Vary batch size directly if you control serving.
6. Vary chunking: prefill size, decode path, prefix cache, KV cache layout, and request scheduling.
7. Isolate reduction-heavy kernels: normalization, matmul, attention, all-reduce, and reduce-scatter.
8. Decide whether exact reproducibility is required or whether caching, consensus, or tolerance is enough.

## Backend design guidance

If you control kernels:

- Keep reduction order fixed for each request independent of batch size.
- Avoid shape-dependent kernel choices when they alter numerics.
- Use consistent tile sizes for matmul where feasible.
- For attention, ensure KV cache layout and page tables produce the same reduction order across prefill and decode.
- Prefer fixed split-size strategies over strategies that choose split counts from current load.
- Test under realistic dynamic batching, prefix caching, and long-context decode.

If you only use an external API:

- Do not promise bitwise determinism.
- Cache outputs when exact replay matters.
- Store raw responses, model identifiers, parameters, and timestamps.
- Use regression tests that tolerate semantically equivalent outputs unless exact text is contractual.
- For high-stakes workflows, use multiple samples, adjudication, or human review.

## Trainer-sampler alignment

For RL or on-policy learning:

- Compare sampler logprobs and trainer logprobs on identical trajectories.
- If they differ, the update is partly off-policy.
- Use importance weighting or off-policy correction unless you can make numerics align.
- Track KL divergence between sampling and training policies as a stability metric.

## Failure modes

- Blaming all nondeterminism on GPU concurrency without checking batch invariance.
- Setting temperature 0 and assuming the system is reproducible.
- Ignoring prefix caching or chunked prefill.
- Treating tiny logprob differences as harmless in RL loops without measuring downstream stability.
- Raising numeric tolerances instead of understanding the root cause.
