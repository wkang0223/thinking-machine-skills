# Thinking Machine Skills Loader

Open-source skills that help any LLM collaborate, customize, and prove its thinking.

This pack is a model-agnostic synthesis of public Thinking Machines Lab themes. It is not official Thinking Machines Lab material. Use it as a compact operating layer for LLM agents that need to design collaborative, customizable, reproducible, and empirically grounded AI systems.

## How to use

1. Read `manifest.json` to select relevant skills.
2. Load only the selected `SKILL.md` files into the LLM's system, developer, or task context.
3. Treat each skill as procedural guidance, not a vendor-specific dependency.
4. If a skill mentions unavailable capabilities, emulate the pattern with available tools and state the limitation.
5. Prefer small experiments, measurable outputs, and source-grounded claims over broad speculation.

## Claude integration

- Claude Code: project skills are available under `.claude/skills/`.
- claude.ai and Claude API: upload `claude/thinking-machine-skill.zip` as one custom Skill bundle.
- For broad requests, invoke `thinking-machine`; for precise Claude Code work, invoke individual `tm-*` skills.

## Universal source

Edit `source/pack.json`, `source/skills/*/skill.json`, and `source/skills/*/instructions.md`, then run:

```sh
python3 scripts/skillpack.py build
```

## Skill routing

- planning, running, reviewing, or writing up ML experiments with strong baselines, ablations, hyperparameter sweeps, raw examples, clean charts, and transparent assumptions.: `tm-experiment-rigor`
- building LLM systems for judgmental forecasting, probability prediction, world-event analysis, proper scoring, forecasting-specific fine-tuning, or ensemble forecasts.: `tm-forecasting-systems`
- designing real-time human-AI collaboration, live voice/video/text interfaces, interruption handling, micro-turn interaction, concurrent tool use, visual proactivity, or foreground/background model coordination.: `tm-interaction-models`
- choosing LoRA, adapters, PEFT settings, target modules, rank, learning rate, batch size, or baseline comparisons for efficient LLM post-training.: `tm-lora-adapter-training`
- exploring optimizer and architecture co-design, manifold constraints, tensor health, Stiefel constraints, modular manifolds, Lipschitz-aware learning-rate budgets, or principled neural network training research.: `tm-modular-optimization`
- customizing or fine-tuning models for image, audio, video, screenshot, diagram, classification, or mixed-modality tasks, especially with low data or VLM adapters.: `tm-multimodal-customization`
- training a student model with its own sampled rollouts and dense teacher feedback for reasoning, personalization, behavior recovery, continual learning, or context distillation.: `tm-on-policy-distillation`
- diagnosing nondeterministic LLM outputs, designing reproducible inference, aligning trainer and sampler numerics, or evaluating batch-size and load-related output drift.: `tm-reproducible-inference`
- shaping an LLM product, research plan, or agent behavior around Thinking Machines-style principles: shared science, customization, human-AI collaboration, solid infrastructure, multimodality, product-research co-design, empirical safety, and real-world value measurement.: `tm-research-principles`
- designing a model-agnostic training API, fine-tuning loop, RL loop, distillation backend, checkpoint workflow, or LLM training abstraction inspired by Tinker-style primitives.: `tm-training-api`
