---
name: tm-modular-optimization
description: Use when exploring optimizer and architecture co-design, manifold constraints, tensor health, Stiefel constraints, modular manifolds, Lipschitz-aware learning-rate budgets, or principled neural network training research.
---

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
