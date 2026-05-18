# Thinking Machine Skills

**Open-source skills that help any LLM collaborate, customize, and prove its thinking.**

This is an unofficial, model-agnostic skill pack distilled from public Thinking Machines Lab themes: real-time interaction models, training APIs, LoRA, on-policy distillation, reproducible inference, experiment rigor, forecasting systems, modular optimization, and multimodal customization.

The goal is simple: edit skills once, then export them for Claude, OpenAI-style prompt packs, Gemini/Gems, MCP-style resources, and lightweight evals.

## What is inside

```text
source/                         # Source of truth
  pack.json                     # Pack metadata, punchline, sources, platform targets
  skills/<skill-id>/            # Universal skill source
    skill.json                  # Metadata, tags, routing, source pages
    instructions.md             # Skill instructions
  evals/smoke.json              # Qualitative behavior checks

thinking-machine-skill-pack/    # Generic generated skill pack
codex/thinking-machine/         # Codex router skill with references
.claude/skills/                 # Claude Code project skills
claude/thinking-machine-skill.zip
dist/openai/                    # OpenAI-style prompt pack
dist/gemini/                    # Gemini/Gems prompt pack
dist/mcp/resources/             # MCP-style markdown resources
scripts/skillpack.py            # Import, validate, and build exports
```

## Quick start

Validate the source files:

```sh
python3 scripts/skillpack.py validate
```

Build every platform export:

```sh
python3 scripts/skillpack.py build
```

Or use Make:

```sh
make validate
make build
```

## Claude

For Claude Code, open this repository as the project. Claude can discover project skills from:

```text
.claude/skills/
```

For claude.ai or the Claude API, upload:

```text
claude/thinking-machine-skill.zip
```

Use `/thinking-machine` for broad requests, or direct skills like `/tm-interaction-models`, `/tm-lora-adapter-training`, and `/tm-reproducible-inference` for precise work.

## Codex

Install the direct skills from:

```text
thinking-machine-skill-pack/skills/
```

Install the broad router from:

```text
codex/thinking-machine/
```

For a local install, copy those folders into `~/.codex/skills/`, or install from the public repo with Codex's skill installer.

## OpenAI, Gemini, and MCP

Use the generated prompt packs:

```text
dist/openai/thinking-machine-system.md
dist/gemini/thinking-machine-gem.md
```

Use MCP-style resources from:

```text
dist/mcp/resources/catalog.json
```

These are plain markdown resources with stable `thinking-machine://skills/<skill-id>` URIs.

## Skills

- `tm-research-principles`: product-research strategy and operating principles
- `tm-interaction-models`: live human-AI collaboration, interruption, foreground/background agents
- `tm-training-api`: low-level training API abstraction
- `tm-lora-adapter-training`: LoRA and adapter training decisions
- `tm-on-policy-distillation`: teacher-student training from student rollouts
- `tm-reproducible-inference`: deterministic inference and trainer-sampler alignment
- `tm-experiment-rigor`: baselines, ablations, writeups, and raw examples
- `tm-forecasting-systems`: probabilistic forecasting and proper scoring
- `tm-modular-optimization`: optimizer and architecture co-design
- `tm-multimodal-customization`: VLM and multimodal fine-tuning patterns

## Edit flow

1. Edit `source/pack.json` or files under `source/skills/<skill-id>/`.
2. Run `python3 scripts/skillpack.py validate`.
3. Run `python3 scripts/skillpack.py build`.
4. Commit both the source and generated exports.

## Provenance

This project is a research synthesis based on public Thinking Machines Lab pages and posts. It is not affiliated with, endorsed by, or maintained by Thinking Machines Lab.

Source URLs are recorded in `source/pack.json` and `thinking-machine-skill-pack/sources.md`.

## License

MIT
