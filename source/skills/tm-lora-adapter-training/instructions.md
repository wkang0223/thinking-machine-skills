# LoRA Adapter Training

Use this skill when a model should be customized without full fine-tuning.

## Core guidance

- LoRA is most attractive for post-training, personalization, RL, and medium-size domain adaptation.
- LoRA can match full fine-tuning when the adapter has enough capacity for the information being learned.
- Apply LoRA broadly across the network, especially MLP and MoE layers. Attention-only LoRA is often weaker even when parameter count is matched.
- Capacity matters. As data size and information content grow, increase rank or expect slower learning.
- LoRA can be less tolerant of large batch sizes than full fine-tuning. Sweep batch size rather than assuming bigger is better.
- Sweep learning rate. A useful starting heuristic is LoRA LR around 10x the full fine-tuning LR for longer runs, and possibly higher for very short runs.
- For RL post-training, smaller ranks may be sufficient because the update often carries less new information than large-scale SFT.

## Decision workflow

1. Classify the training goal: style, instruction following, domain knowledge, reasoning, tool use, RL behavior, or multimodal task.
2. Estimate information load: number of examples, diversity, novelty, and whether the model already has the behavior.
3. Choose target modules:
   - default: all major linear projections, including attention, MLP, and MoE where applicable.
   - avoid attention-only unless constrained by serving or memory.
4. Choose initial rank:
   - small behavior/RL update: low to medium rank.
   - domain adaptation or reasoning SFT: medium to high rank.
   - large dataset or high novelty: high rank or consider full fine-tuning.
5. Sweep learning rate around the expected LoRA regime.
6. Sweep batch size if loss stalls or LoRA underperforms a full fine-tune baseline.
7. Track train loss, validation loss, task metrics, raw examples, and adapter size.
8. Compare against full fine-tuning where affordable, and against a smaller LoRA rank where not.

## Minimal experiment grid

```text
ranks: [8, 32, 128]
target_modules: [all_linear, attention_only_if_needed]
learning_rates: [base_lora_lr / 3, base_lora_lr, base_lora_lr * 3]
batch_sizes: [small, medium, large]
baselines: [base_model, prompt_only, full_finetune_if_affordable]
```

## Evaluation

- Use log loss for clean supervised comparisons when possible.
- Include task-specific evals because lower loss does not always mean better behavior.
- Include raw generations from fixed prompts.
- Look for forgetting when training on domain documents or narrow formats.
- Measure serving constraints: adapter load time, memory, throughput, and multi-tenant needs.

## Failure modes

- Picking rank by folklore instead of capacity and data scale.
- Applying LoRA only to attention because it is convenient.
- Reusing full fine-tuning learning rates without a sweep.
- Increasing batch size to improve throughput while silently harming learning.
- Assuming LoRA preserves behavior under domain mid-training without evals.
