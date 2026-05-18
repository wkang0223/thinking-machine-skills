---
name: tm-on-policy-distillation
description: Use when training a student model with its own sampled rollouts and dense teacher feedback for reasoning, personalization, behavior recovery, continual learning, or context distillation.
---

# On-Policy Distillation

Use this skill to combine the relevance of on-policy training with the dense feedback of distillation.

## Core idea

The student samples its own trajectories. A stronger teacher scores the student's actual tokens in the states the student visits. Training then pushes the student toward teacher-like behavior in its own distribution, reducing compounding error compared with purely off-policy imitation.

## When to use

- A student model has an SFT or mid-trained initialization but needs stronger reasoning.
- A domain fine-tune taught new knowledge but degraded instruction-following or chat behavior.
- You want continual learning without permanently losing earlier behavior.
- You want context distillation: a student with less context learns from a teacher with richer context.
- RL is too sparse or expensive, but a teacher model can provide token-level probabilities or scores.

## Requirements

- Student sampling with token logprobs.
- Teacher scoring of the same sampled trajectories, ideally `compute_logprobs`.
- Prompt or environment distribution.
- Training method that can consume per-token advantages, rewards, or weighted losses.
- Evals for both task skill and preserved behavior.

## Algorithm

```text
for each training step:
    prompts = sample_prompts()
    trajectories = student.sample(prompts, return_logprobs=True)
    student_logprobs = trajectories.logprobs
    teacher_logprobs = teacher.compute_logprobs(trajectories)
    reverse_kl = student_logprobs - teacher_logprobs
    per_token_advantage = -reverse_kl
    student.forward_backward(trajectories, loss_fn="policy_or_importance_sampling", advantages=per_token_advantage)
    student.optim_step()
```

Interpretation: tokens the teacher finds unlikely relative to the student receive a penalty; tokens aligned with the teacher receive little or no penalty.

## Workflow

1. Start from a model that already has partial support for the teacher behavior.
2. Choose a teacher: stronger model, earlier checkpoint, specialist model, or same model with richer context.
3. Choose prompts that exercise the target behavior and failure modes.
4. Sample from the student, not the teacher.
5. Score sampled tokens under the teacher.
6. Train with dense per-token feedback.
7. Alternate with domain learning if doing continual learning.
8. Evaluate target skill, preserved behavior, and regressions.

## Use patterns

- `reasoning lift`: SFT first, then on-policy distill from a stronger reasoning teacher.
- `behavior recovery`: after mid-training on new documents, distill from the earlier instruction-tuned checkpoint on chat prompts.
- `continual learning`: alternate new-data fine-tuning with behavior distillation.
- `context distillation`: teacher gets long context or retrieval, student learns compact behavior without that context.

## Evaluation

- For reasoning: task benchmarks, solution traces, final-answer accuracy, and failure taxonomy.
- For personalization: domain QA plus instruction-following evals.
- For continual learning: old-task retention, new-task improvement, and safety behavior.
- For compute: compare gradient steps, tokens, teacher FLOPs, and wall-clock cost against SFT and RL.

## Failure modes

- Teacher behavior lies outside the student's support, causing weak learning.
- Teacher scoring is unavailable, approximate, or inconsistent with training tokens.
- Distillation copies style without improving truthfulness or task accuracy.
- Prompt reuse becomes memorization if evals are too close to training prompts.
- Private or sensitive teacher context leaks into student outputs.
