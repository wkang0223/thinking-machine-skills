# Training API Abstraction

Use this skill to design training systems that separate research logic from infrastructure.

## Core primitives

Expose a small backend interface:

- `forward_backward(batch, loss_fn)`: run forward and backward passes and accumulate gradients.
- `optim_step()`: update trainable weights from accumulated gradients.
- `sample(prompt, params)`: generate trajectories for evaluation, interaction, RL actions, or data collection.
- `save_state(name)`: checkpoint training state for resumption, download, comparison, or deployment.

Useful extensions:

- `compute_logprobs(trajectories)`: score sampled tokens under a model or checkpoint.
- `load_state(name)`: resume from a checkpoint.
- `evaluate(dataset, metrics)`: run standardized evals.
- `export_adapter(name)`: export LoRA or adapter weights.

## Design goals

- Keep algorithms portable across hosted APIs, local open-weight models, and cluster backends.
- Let researchers control data, rollouts, rewards, losses, sampling parameters, and evals.
- Hide scheduling, device layout, retries, and distributed training details behind the backend.
- Support SFT, RL, on-policy distillation, offline distillation, and multimodal fine-tuning.
- Track enough metadata to reproduce a run: model, tokenizer, code version, data hashes, sampling params, seeds, backend versions, and checkpoint ids.

## Workflow

1. Define the training objective: SFT, RL, distillation, classification, tool use, personalization, or forecasting.
2. Identify required backend methods: sampling, logprobs, gradients, checkpointing, multimodal chunks, or tool rollouts.
3. Specify trainable parameters: full fine-tune, LoRA, adapter, head, prompt, memory, or hybrid.
4. Define the dataset or environment boundary.
5. Define evals before training starts.
6. Write the smallest loop using the primitive interface.
7. Save checkpoints at meaningful decision points.
8. Compare against a simpler baseline and one stronger baseline.

## Generic loop skeleton

```text
state = backend.load_or_create(base_model, trainable_config)
for step in training_steps:
    batch = data_or_env.next()
    artifacts = maybe_sample_or_score(batch, backend)
    loss_inputs = build_loss_inputs(batch, artifacts)
    backend.forward_backward(loss_inputs, loss_fn)
    if should_step(step):
        backend.optim_step()
    if should_eval(step):
        run_evals_and_log_examples()
    if should_checkpoint(step):
        backend.save_state(label)
```

## Portability notes

- If the provider supports OpenAI-compatible sampling, treat sampling as swappable and keep training-specific logic separate.
- If the provider cannot expose gradients or logprobs, the system can still run prompt optimization, evals, retrieval tuning, and preference data collection, but not true training.
- If only API inference is available, use adapters around `sample` and `evaluate`; keep `forward_backward` unimplemented and fail clearly.

## Failure modes

- Baking a specific vendor path into algorithm code.
- Running training without a frozen eval set.
- Saving checkpoints without enough metadata to know what they mean.
- Comparing models trained under different data, context, or sampling conditions.
- Treating infrastructure flakiness as experimental variance.
