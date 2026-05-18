# Thinking Machine Project Instructions

This project includes a Thinking Machine skill pack under `.claude/skills/`.

Use the `tm-*` skills when a task matches their descriptions. For broad or mixed tasks, use `/thinking-machine` as the router, then load only the needed topic references.

The skills are model-agnostic. Do not assume a specific LLM provider unless the user asks for Claude, OpenAI, local open-weight models, or another target explicitly.

Prefer concrete artifacts: training recipe, eval plan, interface spec, prompt, API abstraction, or implementation checklist.

Always include verification: baselines, raw examples, tests, metrics, or failure-mode checks.
