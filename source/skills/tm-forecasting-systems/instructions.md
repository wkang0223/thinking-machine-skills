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
