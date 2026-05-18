---
name: tm-research-principles
description: Use when shaping an LLM product, research plan, or agent behavior around Thinking Machines-style principles: shared science, customization, human-AI collaboration, solid infrastructure, multimodality, product-research co-design, empirical safety, and real-world value measurement.
---

# Thinking Machine Research Principles

Use this skill to set the operating philosophy for an AI system or research project.

## Principles

- Make AI systems more understandable, customizable, collaborative, and capable.
- Prefer human-AI collaboration over defaulting to fully autonomous workflows.
- Preserve human context: intent, tacit judgment, feedback, domain knowledge, and constraints.
- Treat multimodality as a way to capture more intent and reduce interface bottlenecks.
- Build infrastructure correctly for the long haul: reliability, efficiency, reproducibility, and security are core product features.
- Co-design research and product. Product use reveals real problems; research expands what the product can do.
- Use empirical safety: red-team, monitor post-deployment behavior, and improve from observed failures.
- Measure genuine real-world value, not only benchmark movement.
- Share methods, code, data, and assumptions when doing so improves public understanding and reproducibility.

## Workflow

1. Restate the goal in terms of who benefits and what capability changes.
2. Identify which gap is primary: understanding, customization, capability, collaboration, infrastructure, or safety.
3. Decide where the human stays in the loop and what feedback the system should accept.
4. Define the customization path: prompt, memory, tools, retrieval, adapter, fine-tune, or training loop.
5. Define the infrastructure requirement: latency, reliability, reproducibility, privacy, cost, and observability.
6. Define the evaluation: user outcome, benchmark, ablation, raw examples, and failure cases.
7. Produce a small next experiment that can teach something concrete.

## Output contract

Return:

- `goal`: concise objective.
- `human_loop`: when and how humans guide the system.
- `customization_path`: how the system adapts to users or domains.
- `foundation_requirements`: model, data, tools, infra, and safety requirements.
- `evaluation`: how success and failure will be measured.
- `next_experiment`: the smallest useful test.

## Failure modes

- Optimizing autonomy while removing useful human feedback.
- Treating customization as a prompt-only problem when data, tools, or training are needed.
- Hiding infrastructure uncertainty behind vague claims.
- Reporting only aggregate scores without raw examples or error analysis.
- Measuring convenience instead of actual task value.
