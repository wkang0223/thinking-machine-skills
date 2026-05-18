---
name: thinking-machine
description: Model-agnostic Thinking Machine skill router for designing collaborative, customizable, reproducible LLM systems. Use for interaction models, training APIs, LoRA, on-policy distillation, reproducible inference, experiment rigor, forecasting, modular optimization, and multimodal customization.
---

# Thinking Machine

Open-source skills that help any LLM collaborate, customize, and prove its thinking.

Use this Skill as the Claude-friendly router for the full Thinking Machine skill pack. It summarizes the operating stance and points Claude to topic files in `references/` when deeper procedure is needed.

## Operating stance

- Build AI people can understand, shape, and use for their own goals.
- Keep humans in the loop when judgment, feedback, tacit context, or control matter.
- Treat customization as a spectrum: prompt, memory, retrieval, tools, adapters, fine-tuning, and training loops.
- Treat infrastructure quality, reproducibility, evaluation, and safety as product features.
- Prefer empirical iteration: small tests, baselines, raw examples, and clear measurement.

## Topic routing

When the user asks about a topic, read the matching reference file before answering or acting:

- planning, running, reviewing, or writing up ML experiments with strong baselines, ablations, hyperparameter sweeps, raw examples, clean charts, and transparent assumptions.: `references/tm-experiment-rigor.md`
- building LLM systems for judgmental forecasting, probability prediction, world-event analysis, proper scoring, forecasting-specific fine-tuning, or ensemble forecasts.: `references/tm-forecasting-systems.md`
- designing real-time human-AI collaboration, live voice/video/text interfaces, interruption handling, micro-turn interaction, concurrent tool use, visual proactivity, or foreground/background model coordination.: `references/tm-interaction-models.md`
- choosing LoRA, adapters, PEFT settings, target modules, rank, learning rate, batch size, or baseline comparisons for efficient LLM post-training.: `references/tm-lora-adapter-training.md`
- exploring optimizer and architecture co-design, manifold constraints, tensor health, Stiefel constraints, modular manifolds, Lipschitz-aware learning-rate budgets, or principled neural network training research.: `references/tm-modular-optimization.md`
- customizing or fine-tuning models for image, audio, video, screenshot, diagram, classification, or mixed-modality tasks, especially with low data or VLM adapters.: `references/tm-multimodal-customization.md`
- training a student model with its own sampled rollouts and dense teacher feedback for reasoning, personalization, behavior recovery, continual learning, or context distillation.: `references/tm-on-policy-distillation.md`
- diagnosing nondeterministic LLM outputs, designing reproducible inference, aligning trainer and sampler numerics, or evaluating batch-size and load-related output drift.: `references/tm-reproducible-inference.md`
- shaping an LLM product, research plan, or agent behavior around Thinking Machines-style principles: shared science, customization, human-AI collaboration, solid infrastructure, multimodality, product-research co-design, empirical safety, and real-world value measurement.: `references/tm-research-principles.md`
- designing a model-agnostic training API, fine-tuning loop, RL loop, distillation backend, checkpoint workflow, or LLM training abstraction inspired by Tinker-style primitives.: `references/tm-training-api.md`
- Source provenance for this synthesis: `references/sources.md`

## Response contract

For design or implementation tasks, return:

- `goal`: the user-visible objective.
- `selected_skills`: which reference files guided the response.
- `plan_or_workflow`: concrete steps.
- `artifacts`: prompts, code, eval plan, interface spec, or training recipe.
- `verification`: tests, evals, examples, metrics, or review checks.
- `open_decisions`: choices that remain unresolved.

## Claude-specific behavior

- Do not require network access; these references are bundled locally.
- Do not assume a specific LLM vendor unless the user asks for one.
- If using Claude Code, direct slash commands may also exist for the individual `tm-*` skills.
- If using Claude API, this single bundled Skill avoids loading more Skills than the request needs.
- If the task needs multiple topic files, read the smallest useful set.
