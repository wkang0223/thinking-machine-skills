---
name: tm-experiment-rigor
description: Use when planning, running, reviewing, or writing up ML experiments with strong baselines, ablations, hyperparameter sweeps, raw examples, clean charts, and transparent assumptions.
---

# Experiment Rigor

Use this skill to make ML research and model customization work credible.

## Standard

Prefer diligent, transparent experiments over novelty or hype. A strong result should survive comparison to simpler methods, reasonable hyperparameter sweeps, and raw output inspection.

## Planning workflow

1. State the hypothesis in one sentence.
2. Define the unit of comparison: model, dataset, prompt, reward, optimizer, adapter, interface, or infrastructure change.
3. Choose baselines:
   - current production or base model.
   - simplest method likely to work.
   - strong known method if affordable.
4. Define metrics before running experiments.
5. Define qualitative evidence: raw outputs, failure cases, traces, or examples.
6. Identify sensitive hyperparameters, especially learning rate, batch size, rank, reward scale, and sampling temperature.
7. Decide ablations that isolate the claimed contribution.
8. Log enough metadata to reproduce results.

## Minimum evidence package

- Dataset description and splits.
- Training or inference configuration.
- Baseline table.
- Hyperparameter sweep or reason it was unnecessary.
- At least one ablation.
- Raw examples showing success and failure.
- Clean, labeled charts with units and confidence where relevant.
- Discussion of assumptions and deviations from prior work.

## Evaluation patterns

- For SFT or LoRA: train/validation log loss plus task evals.
- For RL: reward curves, policy KL, pass rate, rollout examples, and reward hacking checks.
- For interaction: latency, timing correctness, interruption recovery, and user control.
- For forecasting: Brier score, log score, calibration, resolution rules, and ensemble diversity.
- For infrastructure: reproducibility, throughput, latency, cost, and failure recovery.

## Writeup structure

1. Claim.
2. Why the task matters.
3. Method.
4. Baselines and controls.
5. Results.
6. Raw examples.
7. Limitations and failure cases.
8. Reproducibility details.
9. Next experiments.

## Failure modes

- Reporting a single best run.
- Moving the metric after seeing results.
- Comparing against weak baselines.
- Hiding raw outputs behind aggregate charts.
- Forgetting that hyperparameters can reverse a conclusion.
- Treating benchmark improvement as product value without user-task evidence.
