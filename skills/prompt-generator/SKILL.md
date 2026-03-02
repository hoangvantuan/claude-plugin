---
name: prompt-generator
description: Meta-prompting skill that creates well-structured, verifiable, low-hallucination prompts for any use case. Use when the user wants to create, refine, or improve a prompt — including system prompts, role prompts, task prompts, or any AI instruction set. Triggers on requests like "create a prompt for...", "help me write a prompt", "refine this prompt", "make a better prompt for...", or "generate a prompt that...".
---

# Prompt Generator

Create high-quality, structured prompts using meta-prompting best practices: task decomposition, expert personas, iterative verification, and hallucination minimization.

## Workflow

### Phase 1: Gather Requirements

Ask the user (one at a time, maximum 4 questions). Skip when answers are obvious from context.

1. **Type**: Detect or ask — what type of prompt?
   - **System prompt**: Persistent AI behavior across a conversation
   - **Task prompt**: One-shot, input → specific output
   - **Conversational prompt**: Multi-turn, requires memory/context handling
   - **Role prompt**: Character/persona, tone-focused

2. **Goal**: "What is the primary goal or role of the system you want to create?"

3. **Output**: "What specific outputs do you expect? (format, length, style)"

4. **Accuracy**: "How should it handle uncertainty? (disclaim, ask for sources, or best-effort)"

Minimize friction — 1-2 questions usually suffice when context is clear.

### Phase 2: Decompose (if complex)

For complex requests, break into subtasks and assign expert personas:

- **Expert Writer** — copywriting, narrative, tone
- **Expert Analyst** — data, logic, verification
- **Expert Python** — code generation, computation
- **Expert [Domain]** — specialized knowledge

Each expert gets complete, self-contained instructions (no shared memory between experts).

Use "fresh eyes" — never assign the same expert to both create AND validate.

### Phase 3: Generate the Prompt

Consolidate into a single, cohesive prompt. Include applicable sections, omit what's not relevant:

```
## Role
You are [PERSONA] with expertise in [DOMAIN].
You communicate in a [STYLE] manner.
When uncertain, you [DISCLAIM/ASK] rather than guess.

## Context
[User's task, goals, background. Summarize clarifications from user input.]

## Input
[Format and constraints of input the AI will receive.
Include: expected format, required vs optional fields, length bounds.
REQUIRED for task prompts. Omit for system/role prompts without structured input.]

## Instructions
1. [Stepwise approach, including verification points]
2. [Expert assignments if needed]
3. If input is ambiguous: [specific fallback action — ask, disclaim, or reject]

## Constraints
**Must do:**
- [Positive constraints — specific, measurable behaviors]

**Must NOT do:**
- Do NOT fabricate data, citations, or statistics
- Do NOT proceed when requirements are ambiguous — ask for clarification
- Do NOT use filler phrases ("certainly", "of course", "great question")
- [Additional negative constraints specific to the use case]

## Output Format
[Exact structure — bullets, paragraphs, code blocks, XML tags, etc.
Include length bounds and delimiters when precision matters.]

## Examples
[Include 2-5 examples when output quality depends on seeing concrete patterns.
Cover: at least 1 basic case + 1 edge case. Add counter-examples when helpful.

### Example 1 (Basic)
Input: [...]
Output: [...]

### Example 2 (Edge case)
Input: [...]
Output: [...]

### Counter-example (What NOT to do) — optional
Input: [...]
Bad output: [...]
Why wrong: [...]
]

## Reasoning
[Include when task has >=3 logical steps, requires math/code, or benefits from
showing work. Use: "Think step by step before giving the final answer."
Omit for straightforward tasks.]

## Fallback
[What to do when input is invalid, ambiguous, or outside scope:
1. State clearly what is unclear
2. Ask one specific clarifying question
3. Do NOT attempt to guess or fill in missing information]
```

**Section inclusion guide:**
- Role, Context, Instructions, Constraints, Output Format — **always include**
- Input — required for task prompts, optional for others
- Examples — include when output depends on seeing patterns (2-5 examples)
- Reasoning — include for multi-step logic, math, or code tasks
- Fallback — include for user-facing prompts, multi-turn systems

### Phase 4: Verify and Deliver

Self-review checklist before delivering:

- [ ] No vague virtue words ("good", "helpful", "detailed") without specific definition
- [ ] No contradictory instructions (e.g., "be concise" + "include all details")
- [ ] No implicit assumptions — all context is explicitly stated
- [ ] Negative constraints are included (what NOT to do)
- [ ] Prompt type matches the use case (system vs task vs conversational vs role)
- [ ] If complex: suggest splitting into multi-prompt pipeline instead of mega-prompt

Then:
- Present the final prompt, organized and easy to follow
- Note expert reviews if used
- Offer to iterate if user wants adjustments

## Principles

- **Type-aware** — match prompt structure to the prompt type
- **Decompose** complex tasks into smaller subtasks
- **Fresh eyes** — separate creation from validation
- **Never guess** — disclaim uncertainty, ask for data
- **Explicit > implicit** — state all assumptions, avoid vague language
- **Negative framing** — "must NOT" often more effective than "should"
- **Concise** — only ask clarifying questions when critical
- **Iterative** — verify with checklist before delivering, offer refinement
- **Section-aware** — include only relevant sections, omit what doesn't apply

## Anti-patterns to Avoid

When reviewing or generating prompts, flag these issues:

- **Vague virtues**: "Write a good summary" → "Write a 3-sentence summary focusing on key findings and action items"
- **Overloaded prompt**: Too many tasks in one prompt → suggest splitting
- **Sycophancy traps**: "Always agree" or "Never say no" → remove
- **Missing scope**: "Write marketing copy" without audience, channel, tone → clarify
- **Prompt stuffing**: Repeating the same instruction in multiple sections → deduplicate
