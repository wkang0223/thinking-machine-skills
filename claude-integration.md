# Claude Integration

This workspace is prepared for Claude in three ways.

## 1. Claude Code project skills

The individual skills are installed under:

```text
.claude/skills/<skill-name>/SKILL.md
```

Start Claude Code from this workspace and the skills should be discoverable automatically. You can invoke them directly, for example:

```text
/tm-interaction-models design a live voice+screen collaboration loop
/tm-reproducible-inference audit this inference stack for nondeterminism
/tm-lora-adapter-training choose LoRA settings for a small domain model
```

There is also a single router skill:

```text
/thinking-machine design a model-agnostic human-AI collaboration system
```

## 2. claude.ai custom Skill upload

Upload this zip in claude.ai through Settings > Features:

```text
claude/thinking-machine-skill.zip
```

The zip contains one Skill named `thinking-machine` plus topic references. This is the easiest path for chat usage because one upload contains the whole pack.

## 3. Claude API custom Skill

Upload `claude/thinking-machine-skill.zip` through the Skills API, then include the returned custom `skill_id` in the Messages API `container.skills` list.

Required API pieces from Anthropic's docs:

- beta headers: `code-execution-2025-08-25`, `skills-2025-10-02`, and `files-api-2025-04-14` when uploading/downloading files
- code execution tool: `{"type": "code_execution_20250825", "name": "code_execution"}`
- custom Skill reference:

```python
container = {
    "skills": [
        {
            "type": "custom",
            "skill_id": "skill_...",
            "version": "latest",
        }
    ]
}
```

For production, pin `version` instead of using `latest`.

## Security notes

- These skills contain only markdown instructions and references.
- They do not include scripts, dynamic shell injection, network calls, or `allowed-tools` grants.
- Claude API Skills run without network access, so this pack is designed to work from bundled files only.
- Custom Skills do not sync across Claude Code, claude.ai, and the Claude API; install or upload separately for each surface.
