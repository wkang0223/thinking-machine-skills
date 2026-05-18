#!/usr/bin/env python3
"""Build platform-specific skill packs from a universal source tree."""

from __future__ import annotations

import argparse
import json
import shutil
import textwrap
import zipfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "source"
SOURCE_SKILLS_DIR = SOURCE_DIR / "skills"
PACK_JSON = SOURCE_DIR / "pack.json"
EVALS_DIR = SOURCE_DIR / "evals"


@dataclass
class Skill:
    id: str
    name: str
    description: str
    display_name: str
    use_when: str
    tags: list[str]
    source_pages: list[str]
    body: str


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def parse_frontmatter(markdown: str) -> tuple[dict[str, str], str]:
    lines = markdown.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, markdown
    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        return {}, markdown
    meta: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"')
    body = "\n".join(lines[end + 1 :]).strip() + "\n"
    return meta, body


def slug_to_display(slug: str, body: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return slug.removeprefix("tm-").replace("-", " ").title()


def import_existing(args: argparse.Namespace) -> None:
    source = Path(args.source).resolve()
    target = Path(args.target).resolve()
    for skill_md in sorted(source.glob("*/SKILL.md")):
        raw = skill_md.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(raw)
        if not meta.get("name") or not meta.get("description"):
            raise SystemExit(f"Missing required frontmatter in {skill_md}")
        skill_id = meta["name"]
        out_dir = target / skill_id
        skill_meta = {
            "id": skill_id,
            "name": skill_id,
            "display_name": slug_to_display(skill_id, body),
            "description": meta["description"],
            "use_when": meta["description"].removeprefix("Use when ").strip(),
            "tags": infer_tags(skill_id, meta["description"]),
            "source_pages": infer_sources(skill_id),
        }
        write_json(out_dir / "skill.json", skill_meta)
        write_text(out_dir / "instructions.md", body)
    print(f"Imported {len(list(target.glob('*/skill.json')))} skills into {target}")


def infer_tags(skill_id: str, description: str) -> list[str]:
    keywords = {
        "interaction": ["interaction", "collaboration", "realtime", "multimodal"],
        "training": ["training", "fine-tuning", "api"],
        "lora": ["lora", "adapters", "peft"],
        "distillation": ["distillation", "teacher-student", "continual-learning"],
        "reproducibility": ["determinism", "reproducibility", "inference"],
        "experiments": ["experiments", "evaluation", "baselines"],
        "forecasting": ["forecasting", "probability", "calibration"],
        "optimization": ["optimization", "manifolds", "optimizer"],
        "multimodal": ["multimodal", "vision", "audio", "video"],
        "principles": ["strategy", "research", "principles"],
    }
    haystack = f"{skill_id} {description}".lower()
    tags: list[str] = []
    for tag, needles in keywords.items():
        if any(needle in haystack for needle in needles):
            tags.append(tag)
    return tags or ["llm-skill"]


def infer_sources(skill_id: str) -> list[str]:
    source_map = {
        "tm-interaction-models": ["https://thinkingmachines.ai/blog/interaction-models/"],
        "tm-training-api": [
            "https://thinkingmachines.ai/tinker/",
            "https://thinkingmachines.ai/news/announcing-tinker/",
            "https://thinkingmachines.ai/news/tinker-general-availability/",
        ],
        "tm-lora-adapter-training": ["https://thinkingmachines.ai/blog/lora/"],
        "tm-on-policy-distillation": ["https://thinkingmachines.ai/blog/on-policy-distillation/"],
        "tm-reproducible-inference": [
            "https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/"
        ],
        "tm-experiment-rigor": [
            "https://thinkingmachines.ai/news/call-for-community-projects/",
            "https://thinkingmachines.ai/blog/",
        ],
        "tm-forecasting-systems": [
            "https://thinkingmachines.ai/news/training-llms-to-predict-world-events/"
        ],
        "tm-modular-optimization": ["https://thinkingmachines.ai/blog/modular-manifolds/"],
        "tm-multimodal-customization": [
            "https://thinkingmachines.ai/news/tinker-general-availability/",
            "https://thinkingmachines.ai/blog/interaction-models/",
        ],
        "tm-research-principles": ["https://thinkingmachines.ai/"],
    }
    return source_map.get(skill_id, [])


def load_pack() -> dict:
    if not PACK_JSON.exists():
        raise SystemExit(f"Missing {PACK_JSON}")
    return read_json(PACK_JSON)


def load_skills() -> list[Skill]:
    skills: list[Skill] = []
    for skill_json in sorted(SOURCE_SKILLS_DIR.glob("*/skill.json")):
        meta = read_json(skill_json)
        body_path = skill_json.parent / "instructions.md"
        if not body_path.exists():
            raise SystemExit(f"Missing {body_path}")
        skills.append(
            Skill(
                id=meta["id"],
                name=meta.get("name", meta["id"]),
                description=meta["description"],
                display_name=meta.get("display_name", meta["id"]),
                use_when=meta.get("use_when", meta["description"]),
                tags=list(meta.get("tags", [])),
                source_pages=list(meta.get("source_pages", [])),
                body=body_path.read_text(encoding="utf-8").strip() + "\n",
            )
        )
    if not skills:
        raise SystemExit(f"No skills found in {SOURCE_SKILLS_DIR}")
    return skills


def skill_markdown(skill: Skill) -> str:
    return f"""---
name: {skill.name}
description: {skill.description}
---

{skill.body}"""


def clean_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def write_base_skill_pack(pack: dict, skills: list[Skill]) -> None:
    out = ROOT / "thinking-machine-skill-pack"
    clean_dir(out / "skills")
    for skill in skills:
        write_text(out / "skills" / skill.id / "SKILL.md", skill_markdown(skill))
    write_text(out / "loader.md", render_loader(pack, skills))
    write_json(out / "manifest.json", render_manifest(pack, skills))
    write_text(out / "sources.md", render_sources(pack, skills))


def write_claude(pack: dict, skills: list[Skill]) -> None:
    claude_skills = ROOT / ".claude" / "skills"
    clean_dir(claude_skills)
    for skill in skills:
        write_text(claude_skills / skill.id / "SKILL.md", skill_markdown(skill))
    write_text(ROOT / ".claude" / "CLAUDE.md", render_claude_project_instructions())

    bundle = ROOT / "claude" / "thinking-machine"
    clean_dir(bundle / "references")
    router = render_claude_router(pack, skills)
    write_text(bundle / "SKILL.md", router)
    write_text(claude_skills / "thinking-machine" / "SKILL.md", router)
    for skill in skills:
        content = skill_markdown(skill)
        write_text(bundle / "references" / f"{skill.id}.md", content)
        write_text(claude_skills / "thinking-machine" / "references" / f"{skill.id}.md", content)
    sources = render_sources(pack, skills)
    write_text(bundle / "references" / "sources.md", sources)
    write_text(claude_skills / "thinking-machine" / "references" / "sources.md", sources)
    zip_skill_bundle(bundle, ROOT / "claude" / "thinking-machine-skill.zip")


def write_openai(pack: dict, skills: list[Skill]) -> None:
    out = ROOT / "dist" / "openai"
    clean_dir(out)
    write_text(out / "thinking-machine-system.md", render_prompt_pack(pack, skills, "OpenAI"))
    for skill in skills:
        write_text(out / "skills" / f"{skill.id}.md", skill_markdown(skill))


def write_gemini(pack: dict, skills: list[Skill]) -> None:
    out = ROOT / "dist" / "gemini"
    clean_dir(out)
    write_text(out / "thinking-machine-gem.md", render_prompt_pack(pack, skills, "Gemini"))
    for skill in skills:
        write_text(out / "skills" / f"{skill.id}.md", skill_markdown(skill))


def write_mcp_resources(pack: dict, skills: list[Skill]) -> None:
    out = ROOT / "dist" / "mcp" / "resources"
    clean_dir(out)
    catalog = {
        "name": pack["name"],
        "description": pack["description"],
        "resources": [
            {
                "uri": f"thinking-machine://skills/{skill.id}",
                "name": skill.display_name,
                "description": skill.description,
                "mimeType": "text/markdown",
                "path": f"{skill.id}.md",
            }
            for skill in skills
        ],
    }
    write_json(out / "catalog.json", catalog)
    for skill in skills:
        write_text(out / f"{skill.id}.md", skill_markdown(skill))


def write_eval_pack() -> None:
    out = ROOT / "dist" / "evals"
    clean_dir(out)
    for eval_json in sorted(EVALS_DIR.glob("*.json")):
        shutil.copy2(eval_json, out / eval_json.name)


def zip_skill_bundle(source_dir: Path, target_zip: Path) -> None:
    if target_zip.exists():
        target_zip.unlink()
    target_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(source_dir.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(source_dir))


def render_loader(pack: dict, skills: list[Skill]) -> str:
    routing = "\n".join(f"- {skill.use_when}: `{skill.id}`" for skill in skills)
    return f"""# {pack['display_name']} Loader

{pack['punchline']}

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

{routing}
"""


def render_manifest(pack: dict, skills: list[Skill]) -> dict:
    return {
        "name": pack["name"],
        "version": pack["version"],
        "snapshot_date": pack["snapshot_date"],
        "purpose": pack["description"],
        "status": pack["status"],
        "punchline": pack["punchline"],
        "loader": "loader.md",
        "source_of_truth": {
            "pack": "source/pack.json",
            "skills": "source/skills/<skill-id>/",
            "evals": "source/evals/",
            "build_command": "python3 scripts/skillpack.py build",
        },
        "platforms": pack["platforms"],
        "skills": [
            {
                "id": skill.id,
                "path": f"skills/{skill.id}/SKILL.md",
                "display_name": skill.display_name,
                "use_when": skill.use_when,
                "tags": skill.tags,
                "source_pages": skill.source_pages,
            }
            for skill in skills
        ],
        "source_pages": pack["source_pages"],
    }


def render_sources(pack: dict, skills: list[Skill]) -> str:
    lines = [
        "# Source Map",
        "",
        f"Snapshot date: {pack['snapshot_date']}.",
        "",
        "This file records the public pages used to synthesize the skill pack. The skills paraphrase the ideas and convert them into reusable procedures.",
        "",
        "## Pack Sources",
        "",
    ]
    lines.extend(f"- {url}" for url in pack["source_pages"])
    lines.extend(["", "## Skill Sources", ""])
    for skill in skills:
        lines.append(f"### {skill.display_name}")
        lines.extend(f"- {url}" for url in skill.source_pages)
        lines.append("")
    return "\n".join(lines)


def render_claude_project_instructions() -> str:
    return """# Thinking Machine Project Instructions

This project includes a Thinking Machine skill pack under `.claude/skills/`.

Use the `tm-*` skills when a task matches their descriptions. For broad or mixed tasks, use `/thinking-machine` as the router, then load only the needed topic references.

The skills are model-agnostic. Do not assume a specific LLM provider unless the user asks for Claude, OpenAI, local open-weight models, or another target explicitly.

Prefer concrete artifacts: training recipe, eval plan, interface spec, prompt, API abstraction, or implementation checklist.

Always include verification: baselines, raw examples, tests, metrics, or failure-mode checks.
"""


def render_claude_router(pack: dict, skills: list[Skill]) -> str:
    routes = "\n".join(
        f"- {skill.use_when}: `references/{skill.id}.md`" for skill in skills
    )
    return f"""---
name: thinking-machine
description: Model-agnostic Thinking Machine skill router for designing collaborative, customizable, reproducible LLM systems. Use for interaction models, training APIs, LoRA, on-policy distillation, reproducible inference, experiment rigor, forecasting, modular optimization, and multimodal customization.
---

# Thinking Machine

{pack['punchline']}

Use this Skill as the Claude-friendly router for the full Thinking Machine skill pack. It summarizes the operating stance and points Claude to topic files in `references/` when deeper procedure is needed.

## Operating stance

- Build AI people can understand, shape, and use for their own goals.
- Keep humans in the loop when judgment, feedback, tacit context, or control matter.
- Treat customization as a spectrum: prompt, memory, retrieval, tools, adapters, fine-tuning, and training loops.
- Treat infrastructure quality, reproducibility, evaluation, and safety as product features.
- Prefer empirical iteration: small tests, baselines, raw examples, and clear measurement.

## Topic routing

When the user asks about a topic, read the matching reference file before answering or acting:

{routes}
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
"""


def render_prompt_pack(pack: dict, skills: list[Skill], platform: str) -> str:
    catalog = "\n".join(
        f"- `{skill.id}`: {skill.use_when}" for skill in skills
    )
    skill_sections = "\n\n".join(
        f"## {skill.display_name}\n\nUse when: {skill.use_when}\n\n{skill.body.strip()}"
        for skill in skills
    )
    return f"""# {pack['display_name']} for {platform}

{pack['punchline']}

Use this prompt pack as a model-agnostic operating layer. Select only the relevant skills for a given task when context is limited.

## Skill catalog

{catalog}

## Response contract

For design or implementation tasks, produce:

- `goal`
- `selected_skills`
- `plan_or_workflow`
- `artifacts`
- `verification`
- `open_decisions`

## Skills

{skill_sections}
"""


def build(_: argparse.Namespace) -> None:
    pack = load_pack()
    skills = load_skills()
    write_base_skill_pack(pack, skills)
    write_claude(pack, skills)
    write_openai(pack, skills)
    write_gemini(pack, skills)
    write_mcp_resources(pack, skills)
    write_eval_pack()
    print(f"Built {len(skills)} skills for Claude, OpenAI, Gemini, MCP, and eval exports")


def validate(_: argparse.Namespace) -> None:
    pack = load_pack()
    skills = load_skills()
    errors: list[str] = []
    ids = [skill.id for skill in skills]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate skill ids")
    for skill in skills:
        if not skill.description:
            errors.append(f"{skill.id}: missing description")
        if len(skill.description) > 360:
            errors.append(f"{skill.id}: description is longer than 360 characters")
        if not skill.body.lstrip().startswith("# "):
            errors.append(f"{skill.id}: instructions.md should start with a markdown H1")
    if not pack.get("punchline"):
        errors.append("pack.json missing punchline")
    if not list(EVALS_DIR.glob("*.json")):
        errors.append("No eval packs found")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Validated {len(skills)} skills and {len(list(EVALS_DIR.glob('*.json')))} eval pack(s)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(required=True)

    import_parser = subparsers.add_parser("import", help="Import existing SKILL.md files into universal source")
    import_parser.add_argument("--source", default=str(ROOT / "thinking-machine-skill-pack" / "skills"))
    import_parser.add_argument("--target", default=str(SOURCE_SKILLS_DIR))
    import_parser.set_defaults(func=import_existing)

    build_parser = subparsers.add_parser("build", help="Build all platform exports")
    build_parser.set_defaults(func=build)

    validate_parser = subparsers.add_parser("validate", help="Validate universal source")
    validate_parser.set_defaults(func=validate)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
