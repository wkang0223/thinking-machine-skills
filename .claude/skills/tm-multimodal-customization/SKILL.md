---
name: tm-multimodal-customization
description: Use when customizing or fine-tuning models for image, audio, video, screenshot, diagram, classification, or mixed-modality tasks, especially with low data or VLM adapters.
---

# Multimodal Customization

Use this skill when a model must learn from or act on more than text.

## Core idea

Multimodality can carry intent that text alone loses. For customization, treat images, screenshots, diagrams, audio, and video as first-class input chunks with task-specific evals.

## Task patterns

- Image classification framed as text generation.
- Screenshot or diagram understanding.
- Vision-language domain QA.
- Audio or speech instruction following.
- Video event detection or counting.
- Real-time multimodal collaboration, paired with `tm-interaction-models`.
- Multimodal RL or SFT using labeled examples, tool outcomes, or environment rewards.

## Workflow

1. Define the modality and output:
   - image to label.
   - screenshot to answer.
   - video to timed event.
   - audio to response.
   - mixed input to action.
2. Choose the customization path:
   - prompt examples for very small tasks.
   - LoRA or adapter for repeated domain patterns.
   - SFT for labeled examples.
   - RL for outcome-based behavior.
3. Build data as structured chunks: text plus image, audio, or video references.
4. Preserve labels and resolution rules separately from raw media.
5. Sweep data scale, starting with one or a few examples per class when data is scarce.
6. Compare to a simple non-LLM baseline where appropriate.
7. Evaluate data efficiency, robustness, and raw mistakes.

## Low-data classifier recipe

```text
Input: image + instruction
Output: class name as text
Train: LoRA or adapter on labeled examples
Eval: accuracy by examples-per-class sweep
Baseline: vision-only classifier or frozen embedding + linear head
Inspect: confusion pairs and raw generations
```

## Real-time multimodal notes

- For video or audio timing tasks, score both content and timing.
- Do not rely only on audio turn detection when visual context should trigger a response.
- Keep a compact event log of observed changes.
- Manage long sessions with summaries and salience filters.

## Safety and privacy

- Treat images, audio, and video as potentially sensitive.
- Avoid training on private media without explicit permission and retention rules.
- Redact faces, identifiers, and proprietary screens when possible.
- Record data provenance and allowed use.

## Failure modes

- Treating multimodal input as decoration while the model relies on text only.
- Evaluating only aggregate accuracy without inspecting confusions.
- Using labels that are ambiguous or inconsistent across annotators.
- Forgetting that timing is part of correctness in audio/video interaction.
- Comparing a large VLM to a weak baseline and overclaiming the result.
