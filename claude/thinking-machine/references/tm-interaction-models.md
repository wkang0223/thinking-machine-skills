---
name: tm-interaction-models
description: Use when designing real-time human-AI collaboration, live voice/video/text interfaces, interruption handling, micro-turn interaction, concurrent tool use, visual proactivity, or foreground/background model coordination.
---

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
