# Thinking Machine Skills for Gemini

Open-source skills that help any LLM collaborate, customize, and prove its thinking.

Use this prompt pack as a model-agnostic operating layer. Select only the relevant skills for a given task when context is limited.

## Skill catalog

- `tm-experiment-rigor`: planning, running, reviewing, or writing up ML experiments with strong baselines, ablations, hyperparameter sweeps, raw examples, clean charts, and transparent assumptions.
- `tm-forecasting-systems`: building LLM systems for judgmental forecasting, probability prediction, world-event analysis, proper scoring, forecasting-specific fine-tuning, or ensemble forecasts.
- `tm-interaction-models`: designing real-time human-AI collaboration, live voice/video/text interfaces, interruption handling, micro-turn interaction, concurrent tool use, visual proactivity, or foreground/background model coordination.
- `tm-lora-adapter-training`: choosing LoRA, adapters, PEFT settings, target modules, rank, learning rate, batch size, or baseline comparisons for efficient LLM post-training.
- `tm-modular-optimization`: exploring optimizer and architecture co-design, manifold constraints, tensor health, Stiefel constraints, modular manifolds, Lipschitz-aware learning-rate budgets, or principled neural network training research.
- `tm-multimodal-customization`: customizing or fine-tuning models for image, audio, video, screenshot, diagram, classification, or mixed-modality tasks, especially with low data or VLM adapters.
- `tm-on-policy-distillation`: training a student model with its own sampled rollouts and dense teacher feedback for reasoning, personalization, behavior recovery, continual learning, or context distillation.
- `tm-reproducible-inference`: diagnosing nondeterministic LLM outputs, designing reproducible inference, aligning trainer and sampler numerics, or evaluating batch-size and load-related output drift.
- `tm-research-principles`: shaping an LLM product, research plan, or agent behavior around Thinking Machines-style principles: shared science, customization, human-AI collaboration, solid infrastructure, multimodality, product-research co-design, empirical safety, and real-world value measurement.
- `tm-training-api`: designing a model-agnostic training API, fine-tuning loop, RL loop, distillation backend, checkpoint workflow, or LLM training abstraction inspired by Tinker-style primitives.

## Response contract

For design or implementation tasks, produce:

- `goal`
- `selected_skills`
- `plan_or_workflow`
- `artifacts`
- `verification`
- `open_decisions`

## Skills

## Experiment Rigor

Use when: planning, running, reviewing, or writing up ML experiments with strong baselines, ablations, hyperparameter sweeps, raw examples, clean charts, and transparent assumptions.

# Experiment Rigor

Use this skill to make ML research and model customization work credible.

## Standard

Prefer diligent, transparent experiments over novelty or hype. A strong result should survive comparison to simpler methods, reasonable hyperparameter sweeps, and raw output inspection.

## Planning workflow

1. State the hypothesis in one sentence.
2. Define the unit of comparison: model, dataset, prompt, reward, optimizer, adapter, interface, or infrastructure change.
3. Choose baselines:
   - current production or base model.
   - simplest method likely to work.
   - strong known method if affordable.
4. Define metrics before running experiments.
5. Define qualitative evidence: raw outputs, failure cases, traces, or examples.
6. Identify sensitive hyperparameters, especially learning rate, batch size, rank, reward scale, and sampling temperature.
7. Decide ablations that isolate the claimed contribution.
8. Log enough metadata to reproduce results.

## Minimum evidence package

- Dataset description and splits.
- Training or inference configuration.
- Baseline table.
- Hyperparameter sweep or reason it was unnecessary.
- At least one ablation.
- Raw examples showing success and failure.
- Clean, labeled charts with units and confidence where relevant.
- Discussion of assumptions and deviations from prior work.

## Evaluation patterns

- For SFT or LoRA: train/validation log loss plus task evals.
- For RL: reward curves, policy KL, pass rate, rollout examples, and reward hacking checks.
- For interaction: latency, timing correctness, interruption recovery, and user control.
- For forecasting: Brier score, log score, calibration, resolution rules, and ensemble diversity.
- For infrastructure: reproducibility, throughput, latency, cost, and failure recovery.

## Writeup structure

1. Claim.
2. Why the task matters.
3. Method.
4. Baselines and controls.
5. Results.
6. Raw examples.
7. Limitations and failure cases.
8. Reproducibility details.
9. Next experiments.

## Failure modes

- Reporting a single best run.
- Moving the metric after seeing results.
- Comparing against weak baselines.
- Hiding raw outputs behind aggregate charts.
- Forgetting that hyperparameters can reverse a conclusion.
- Treating benchmark improvement as product value without user-task evidence.

## Forecasting Systems

Use when: building LLM systems for judgmental forecasting, probability prediction, world-event analysis, proper scoring, forecasting-specific fine-tuning, or ensemble forecasts.

# Forecasting Systems

Use this skill when an LLM must estimate probabilities for future events.

## Core pattern

Separate forecasting into:

- `research phase`: gather and summarize relevant evidence.
- `prediction phase`: reason from the evidence and output a calibrated probability distribution.

For binary event questions, define the event and date precisely, then score the probability assigned to the eventual outcome with a proper scoring rule.

## Workflow

1. Rewrite the question into a resolvable form:
   - event definition.
   - deadline.
   - source of resolution.
   - ambiguous edge cases.
2. Gather context:
   - recent facts.
   - base rates.
   - causal factors.
   - expert or market estimates.
   - indicators that would change the forecast.
3. Build a prediction prompt with evidence separated from reasoning instructions.
4. Ask the model for a probability, rationale, uncertainty drivers, and update triggers.
5. Use a proper scoring rule for evaluation, such as Brier score or log score.
6. Track calibration across bins, not only average score.
7. Ensemble forecasts when models are both accurate and decorrelated.
8. Revisit forecasts as new information arrives.

## Training pattern

For on-task fine-tuning:

- Use questions with known resolutions after the model's knowledge cutoff.
- Keep train and test time periods separate.
- Reward probabilities with a proper scoring rule.
- Prefer bounded rewards, such as Brier-derived rewards, when log score is too high variance.
- Include context-gathering outputs if the deployed system will use them.
- Evaluate with and without research tools to isolate where gains come from.

## Probability output contract

Return:

- `probability`: numeric probability from 0 to 1.
- `resolution_criteria`: how the outcome will be judged.
- `key_evidence`: evidence that moved the probability.
- `base_rate`: relevant historical or reference class estimate when available.
- `main_uncertainties`: factors that could change the forecast.
- `update_triggers`: facts that should cause revision.
- `calibration_note`: confidence in the forecast process.

## Ensemble guidance

- Do not ensemble models that make nearly identical errors unless the goal is variance reduction.
- Measure correlation or divergence between model predictions.
- Weight models by both accuracy and diversity.
- Include a fine-tuned specialist if it is accurate and decorrelated from frontier generalists.

## Failure modes

- Asking for a forecast before defining resolution criteria.
- Letting persuasive rationales substitute for calibrated probabilities.
- Training on questions the model may already know.
- Optimizing one tournament metric while degrading calibration.
- Reporting ensemble gains without testing replaceability of each member.
- Using outdated evidence for live forecasts.

## Interaction Models

Use when: designing real-time human-AI collaboration, live voice/video/text interfaces, interruption handling, micro-turn interaction, concurrent tool use, visual proactivity, or foreground/background model coordination.

# Interaction Models

Use this skill when the AI experience should feel collaborative instead of turn-based and isolated.

## Core idea

Most chat interfaces flatten interaction into alternating turns. A stronger collaboration pattern preserves time, overlap, interruption, silence, visual context, tool progress, and background reasoning. If the host model does not natively support this, emulate it with an orchestrator.

## Architecture pattern

- `interaction model`: foreground agent that remains present, receives streaming input, gives low-latency responses, tracks turn-taking, and handles interjections.
- `background model`: asynchronous reasoner that performs slow tasks, tool calls, search, coding, planning, or long-context work.
- `shared context`: event log containing user input, model output, tool progress, visual/audio observations, timing metadata, and current user activity.
- `micro-turns`: small time-aligned chunks of input and output. Use 200 ms as an inspiration, not a hard requirement unless the system supports it.
- `context broker`: decides what enters short-term foreground context, what moves to background memory, and what is summarized.

## Capability checklist

Design explicitly for:

- Seamless dialog management: thinking, yielding, self-correction, invitation to respond.
- Interruption and backchanneling: the model can stop, continue, or briefly acknowledge without derailing.
- Simultaneous input and output: listening while speaking, reading while writing, watching while responding.
- Time awareness: elapsed time, scheduled reminders, timed practice, latency-sensitive responses.
- Visual proactivity: respond when the screen, camera, or video changes, not only when the user asks.
- Concurrent tools: browse, search, compute, or generate UI while conversation continues.
- Graceful integration: background results arrive when useful, not as abrupt topic switches.

## Workflow

1. Classify the interaction: chat, voice, screen-share, camera, coding, tutoring, translation, monitoring, or mixed mode.
2. Set latency budgets for foreground responses and background work.
3. Define event types: text chunk, audio chunk, video frame, user interruption, tool event, silence, background result, UI action.
4. Specify when the foreground agent may interject, wait, backchannel, or delegate.
5. Specify what the background agent receives: full transcript, task brief, tool state, user preferences, and safety constraints.
6. Define the merge policy for background results: summarize, ask permission, insert answer, update UI, or keep working silently.
7. Add safety behavior for speech, visual context, long sessions, and modality-specific refusals.
8. Evaluate with timing, task success, interruption recovery, and user control.

## Orchestrator prompt pattern

```text
You are the foreground interaction model. Stay present with the user.
Respond quickly when the user needs coordination, clarification, or reassurance.
Delegate slow reasoning and tool work to background workers.
Track live events, interruptions, timing, visual changes, and tool progress.
When background work returns, integrate it at a natural moment.
Do not force turn-taking if the user is still speaking, typing, watching, or acting.
```

## Evaluation

Use targeted scenarios:

- User interrupts the model mid-response and changes direction.
- User asks for a timed cue or repeated reminder.
- User performs a visible action and expects the model to speak at the right moment.
- User asks the model to translate or coach while the user continues speaking.
- Background tool work completes while the user has moved to a new subtask.
- A long session requires memory compaction without losing the current thread.

Score both semantic correctness and timing. A correct answer at the wrong moment is a failure for interactive systems.

## Failure modes

- Treating real-time collaboration as speech-to-text plus normal chat.
- Freezing perception while generating.
- Letting background results interrupt the user at bad moments.
- Using audio-only turn detection when visual or textual context should matter.
- Optimizing benchmark intelligence while making the live experience too slow.

## LoRA Adapter Training

Use when: choosing LoRA, adapters, PEFT settings, target modules, rank, learning rate, batch size, or baseline comparisons for efficient LLM post-training.

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

## Modular Optimization

Use when: exploring optimizer and architecture co-design, manifold constraints, tensor health, Stiefel constraints, modular manifolds, Lipschitz-aware learning-rate budgets, or principled neural network training research.

# Modular Optimization

Use this skill for research designs that constrain model weights and co-design optimizers with architecture.

## Core idea

Large networks are easier to train when tensor scales stay healthy. Activations and gradients are commonly normalized; weight matrices can also be constrained. Manifold constraints make weight scale and conditioning explicit, then optimizer steps can be designed to respect those constraints.

## Concepts

- `tensor health`: weights, activations, and gradients avoid exploding, vanishing, or drifting into unstable scales.
- `manifold constraint`: weights are restricted to a structured surface such as a sphere or Stiefel manifold.
- `tangent step`: optimizer update lies in the local feasible direction before retraction.
- `retraction`: map updated weights back onto the manifold.
- `module triple`: forward function, weight manifold, and norm used to measure weight perturbations.
- `modular manifold`: composition of modules where constraints and norms combine, yielding layer-wise learning-rate budgets.

## Workflow

1. Identify the tensors whose scale or conditioning matters most.
2. Define the module:
   - forward function.
   - weight constraint or unconstrained space.
   - norm that reflects functional sensitivity.
3. Choose the optimizer family:
   - standard optimizer plus projection.
   - tangent-space optimizer plus retraction.
   - custom method such as manifold Muon for matrix constraints.
4. Define how learning rates are budgeted across modules.
5. Measure overhead from constraint operations.
6. Track singular values, norms, train loss, eval loss, and wall-clock time.
7. Compare against AdamW, Muon, and an unconstrained version.

## Design heuristics

- Use constraints where they clarify update scale or conditioning.
- Avoid constraining tensors whose flexibility is essential and not yet understood.
- Prefer small experiments before scaling to large transformers.
- Treat architecture and optimizer as one design surface.
- Evaluate both optimization speed and generalization.

## Research questions

- Which transformer submodules benefit from manifold constraints?
- Do constraints improve low-precision training stability?
- Can dual optimization steps be made efficient enough for scale?
- Do better-conditioned weights improve convergence?
- Can modular norms automatically assign layer learning rates?

## Failure modes

- Adding constraints because they are elegant rather than useful.
- Ignoring GPU cost of retractions or matrix sign computations.
- Comparing against weakly tuned AdamW or Muon baselines.
- Assuming Riemannian geometry is the only useful frame for neural network weight spaces.
- Scaling up before validating tensor health metrics on small runs.

## Multimodal Customization

Use when: customizing or fine-tuning models for image, audio, video, screenshot, diagram, classification, or mixed-modality tasks, especially with low data or VLM adapters.

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

## On-Policy Distillation

Use when: training a student model with its own sampled rollouts and dense teacher feedback for reasoning, personalization, behavior recovery, continual learning, or context distillation.

# On-Policy Distillation

Use this skill to combine the relevance of on-policy training with the dense feedback of distillation.

## Core idea

The student samples its own trajectories. A stronger teacher scores the student's actual tokens in the states the student visits. Training then pushes the student toward teacher-like behavior in its own distribution, reducing compounding error compared with purely off-policy imitation.

## When to use

- A student model has an SFT or mid-trained initialization but needs stronger reasoning.
- A domain fine-tune taught new knowledge but degraded instruction-following or chat behavior.
- You want continual learning without permanently losing earlier behavior.
- You want context distillation: a student with less context learns from a teacher with richer context.
- RL is too sparse or expensive, but a teacher model can provide token-level probabilities or scores.

## Requirements

- Student sampling with token logprobs.
- Teacher scoring of the same sampled trajectories, ideally `compute_logprobs`.
- Prompt or environment distribution.
- Training method that can consume per-token advantages, rewards, or weighted losses.
- Evals for both task skill and preserved behavior.

## Algorithm

```text
for each training step:
    prompts = sample_prompts()
    trajectories = student.sample(prompts, return_logprobs=True)
    student_logprobs = trajectories.logprobs
    teacher_logprobs = teacher.compute_logprobs(trajectories)
    reverse_kl = student_logprobs - teacher_logprobs
    per_token_advantage = -reverse_kl
    student.forward_backward(trajectories, loss_fn="policy_or_importance_sampling", advantages=per_token_advantage)
    student.optim_step()
```

Interpretation: tokens the teacher finds unlikely relative to the student receive a penalty; tokens aligned with the teacher receive little or no penalty.

## Workflow

1. Start from a model that already has partial support for the teacher behavior.
2. Choose a teacher: stronger model, earlier checkpoint, specialist model, or same model with richer context.
3. Choose prompts that exercise the target behavior and failure modes.
4. Sample from the student, not the teacher.
5. Score sampled tokens under the teacher.
6. Train with dense per-token feedback.
7. Alternate with domain learning if doing continual learning.
8. Evaluate target skill, preserved behavior, and regressions.

## Use patterns

- `reasoning lift`: SFT first, then on-policy distill from a stronger reasoning teacher.
- `behavior recovery`: after mid-training on new documents, distill from the earlier instruction-tuned checkpoint on chat prompts.
- `continual learning`: alternate new-data fine-tuning with behavior distillation.
- `context distillation`: teacher gets long context or retrieval, student learns compact behavior without that context.

## Evaluation

- For reasoning: task benchmarks, solution traces, final-answer accuracy, and failure taxonomy.
- For personalization: domain QA plus instruction-following evals.
- For continual learning: old-task retention, new-task improvement, and safety behavior.
- For compute: compare gradient steps, tokens, teacher FLOPs, and wall-clock cost against SFT and RL.

## Failure modes

- Teacher behavior lies outside the student's support, causing weak learning.
- Teacher scoring is unavailable, approximate, or inconsistent with training tokens.
- Distillation copies style without improving truthfulness or task accuracy.
- Prompt reuse becomes memorization if evals are too close to training prompts.
- Private or sensitive teacher context leaks into student outputs.

## Reproducible Inference

Use when: diagnosing nondeterministic LLM outputs, designing reproducible inference, aligning trainer and sampler numerics, or evaluating batch-size and load-related output drift.

# Reproducible Inference

Use this skill when outputs must be reproducible, auditable, or stable enough for training.

## Core insight

Temperature 0 removes sampling randomness, but it does not guarantee deterministic user-visible completions. A server can be run-to-run deterministic for the exact same global workload while still being nondeterministic from one user's perspective because variable load changes batch size, chunking, and reduction order.

## Determinism levels

- `sampling deterministic`: fixed decoding rule and seed.
- `run-to-run deterministic`: same full server inputs produce same outputs.
- `batch-invariant`: a request's numerics do not change when other requests are batched with it.
- `chunk-invariant`: a sequence's numerics do not change when prefill, decode, or cache chunks are sliced differently.
- `trainer-sampler aligned`: training and sampling produce bitwise-compatible logprobs for the same policy.
- `hardware/version invariant`: outputs survive changes in hardware, kernels, driver, or library version. This is much harder.

## Investigation workflow

1. Fix sampler settings: temperature, top-p, top-k, max tokens, stop sequences, seed if available.
2. Record model id, tokenizer, system prompt, full input, engine, hardware, library versions, and request timing.
3. Run repeated completions under low load and high load.
4. Compare token sequences, first divergence token, logits if available, and logprob deltas.
5. Vary batch size directly if you control serving.
6. Vary chunking: prefill size, decode path, prefix cache, KV cache layout, and request scheduling.
7. Isolate reduction-heavy kernels: normalization, matmul, attention, all-reduce, and reduce-scatter.
8. Decide whether exact reproducibility is required or whether caching, consensus, or tolerance is enough.

## Backend design guidance

If you control kernels:

- Keep reduction order fixed for each request independent of batch size.
- Avoid shape-dependent kernel choices when they alter numerics.
- Use consistent tile sizes for matmul where feasible.
- For attention, ensure KV cache layout and page tables produce the same reduction order across prefill and decode.
- Prefer fixed split-size strategies over strategies that choose split counts from current load.
- Test under realistic dynamic batching, prefix caching, and long-context decode.

If you only use an external API:

- Do not promise bitwise determinism.
- Cache outputs when exact replay matters.
- Store raw responses, model identifiers, parameters, and timestamps.
- Use regression tests that tolerate semantically equivalent outputs unless exact text is contractual.
- For high-stakes workflows, use multiple samples, adjudication, or human review.

## Trainer-sampler alignment

For RL or on-policy learning:

- Compare sampler logprobs and trainer logprobs on identical trajectories.
- If they differ, the update is partly off-policy.
- Use importance weighting or off-policy correction unless you can make numerics align.
- Track KL divergence between sampling and training policies as a stability metric.

## Failure modes

- Blaming all nondeterminism on GPU concurrency without checking batch invariance.
- Setting temperature 0 and assuming the system is reproducible.
- Ignoring prefix caching or chunked prefill.
- Treating tiny logprob differences as harmless in RL loops without measuring downstream stability.
- Raising numeric tolerances instead of understanding the root cause.

## Thinking Machine Research Principles

Use when: shaping an LLM product, research plan, or agent behavior around Thinking Machines-style principles: shared science, customization, human-AI collaboration, solid infrastructure, multimodality, product-research co-design, empirical safety, and real-world value measurement.

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

## Training API Abstraction

Use when: designing a model-agnostic training API, fine-tuning loop, RL loop, distillation backend, checkpoint workflow, or LLM training abstraction inspired by Tinker-style primitives.

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
