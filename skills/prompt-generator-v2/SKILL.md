---
name: prompt-generator-v2
description: "KERNEL-based prompt engineering skill that transforms vague requests into high-performance, structured prompts. Uses the proven KERNEL framework (Keep simple, Easy to verify, Reproducible, Narrow scope, Explicit constraints, Logical structure) to generate prompts with 94% first-try success rate. Use this skill whenever the user wants to create, write, refine, optimize, or improve ANY prompt for AI models — including system prompts, task prompts, coding prompts, writing prompts, or analysis prompts. Triggers on: 'create a prompt', 'write a prompt for', 'improve this prompt', 'optimize my prompt', 'make a better prompt', 'prompt engineer', 'KERNEL prompt', 'refine prompt', or when the user pastes a weak/vague prompt and wants it improved."
---

# Prompt Generator V2 — KERNEL Framework

Generate prompts that work on the first try. Based on the KERNEL framework, validated across 1000+ real-world prompts with measurable improvements: 94% first-try success, 58% less token usage, 67% faster time-to-result.

## The KERNEL Framework

Each letter represents a principle that separates effective prompts from mediocre ones:

### K — Keep It Simple

A prompt should have one clear goal stated upfront. Complexity is the enemy of precision — when a prompt tries to do too much, the AI spreads attention thin and quality drops everywhere.

**The test**: Can you describe what this prompt does in one sentence? If not, it needs simplifying or splitting.

**Before**: "I need help writing something about Redis that covers caching strategies, includes performance benchmarks, discusses alternatives, and also mentions deployment best practices"

**After**: "Write a technical tutorial on Redis caching patterns for Python web applications"

### E — Easy to Verify

Every prompt needs success criteria that both human and AI can objectively check. Vague quality words ("make it engaging", "write something good") give the AI no target to aim at — and give you no way to judge the result.

**The test**: Could a stranger verify whether the output meets your requirements without asking you questions?

**Before**: "Write an engaging blog post about TypeScript"

**After**: "Write a 1500-word blog post about TypeScript generics. Include 3 working code examples, a comparison table with Java generics, and a 'Common Mistakes' section with at least 4 entries"

### R — Reproducible Results

Prompts should produce consistent quality regardless of when they're run. Temporal references ("current trends", "latest best practices") and ambiguous terms create drift — the same prompt gives different results next week.

**The test**: Would this prompt produce equally good results if run 30 days from now?

**Before**: "Summarize the latest developments in AI"

**After**: "Summarize the key architectural changes introduced in Transformer models between 2017 (Vaswani et al.) and 2024 (Mixture of Experts). Focus on attention mechanisms, training efficiency, and inference optimization"

### N — Narrow Scope

One prompt = one goal. Multi-goal prompts have a 41% satisfaction rate vs 89% for single-goal. When you need multiple things, chain separate prompts — each does one thing well and feeds into the next.

**The test**: Does this prompt ask for exactly one deliverable?

**Before**: "Create the API endpoint, write tests, update the docs, and add error handling"

**After**: Chain of 4 prompts:

1. "Design the REST API endpoint for user registration with input validation"
2. "Write pytest test cases for the user registration endpoint covering happy path, validation errors, and duplicate emails"
3. "Write API documentation for the user registration endpoint in OpenAPI 3.0 format"
4. "Add error handling to the user registration endpoint: rate limiting, malformed JSON, and database connection failures"

### E — Explicit Constraints

Tell the AI what NOT to do. Unconstrained prompts produce generic, unfocused outputs. Constraints act as guardrails — they eliminate entire categories of unwanted results and dramatically increase relevance.

**The test**: Have you specified at least 2-3 things the output should NOT include or do?

**Before**: "Write Python code for data processing"

**After**: "Write Python code to merge CSV files by date column. Constraints: pandas only, no external libraries beyond stdlib+pandas, no functions longer than 20 lines, no global variables, include type hints, handle missing values with forward-fill"

### L — Logical Structure

Every effective prompt follows a consistent structure: Context → Task → Constraints → Format. This structure maps naturally to how AI models process instructions — context sets the frame, task defines the goal, constraints narrow the space, and format specifies the deliverable.

**The test**: Does the prompt follow Context → Task → Constraints → Format order?

**Before**: "I want Python code. It should be clean. The task is parsing JSON. Use requests library. Output should be a CSV. Don't use pandas. The JSON comes from an API endpoint."

**After**:

```
Context: Fetching JSON data from a REST API endpoint
Task: Write a Python script that parses the JSON response and converts it to CSV
Constraints: Use requests library only, no pandas, handle pagination
Output Format: Single .csv file with headers matching JSON keys
```

## Workflow

### Step 1: Understand Intent

Before generating anything, understand what the user actually needs. Extract or ask (max 3 questions, skip if obvious):

1. **What's the single goal?** — If multiple goals detected, suggest splitting into a prompt chain
2. **What does success look like?** — Specific, verifiable criteria (numbers, formats, concrete deliverables)
3. **What should it NOT do?** — Constraints and exclusions

If the user provides a vague request like "help me write a prompt for X", don't just ask questions — propose a draft immediately and iterate. Action beats interrogation.

### Step 2: Apply KERNEL

Transform the user's intent into a structured prompt. Run each principle as a mental checklist:

| Principle                | Check                            | Action if failing                   |
| ------------------------ | -------------------------------- | ----------------------------------- |
| **K**eep simple          | One sentence description?        | Split into prompt chain             |
| **E**asy to verify       | Stranger could verify?           | Add measurable criteria             |
| **R**eproducible         | Works in 30 days?                | Remove temporal refs, add versions  |
| **N**arrow scope         | One deliverable?                 | Extract goals into separate prompts |
| **E**xplicit constraints | 2-3 "do NOT" rules?              | Add negative constraints            |
| **L**ogical structure    | Context→Task→Constraints→Format? | Restructure                         |


### Step 3: Generate the Prompt

Use this structure. Include only relevant sections — omit what doesn't apply:

```
## Context
[Background information the AI needs. Keep minimal — only what's necessary to understand the task. Include domain, audience, and relevant technical context.]

## Task
[One clear, specific goal. Start with an action verb. This is the single sentence that passes the K-test.]

## Constraints
- [What to do — specific, measurable behaviors]
- Do NOT [negative constraint 1]
- Do NOT [negative constraint 2]
- [Additional bounds: length, format, libraries, scope limits]

## Output Format
[Exact structure of the expected output. Include: format (markdown, JSON, code), length bounds, sections/headers if applicable, delimiters.]

## Verification
[How to check success — specific criteria that make the E-principle concrete. Think: "I'll know this worked when..."]
```

**Optional sections** (include when they add value):

- **Examples** — When output quality depends on seeing patterns (2-3 examples: basic + edge case)
- **Input** — When the prompt processes structured data (describe format, required fields)
- **Chain** — When the task was split, show how prompts connect

### Step 4: Verify with KERNEL Checklist

Before delivering, run this quick self-review:

- [ ] **K**: Can I describe this prompt's goal in one sentence?
- [ ] **E**: Are there at least 2 measurable success criteria?
- [ ] **R**: No temporal references, no version-ambiguous terms?
- [ ] **N**: Exactly one deliverable per prompt?
- [ ] **E**: At least 2 explicit "do NOT" constraints?
- [ ] **L**: Follows Context → Task → Constraints → Format structure?

Also check:

- [ ] No vague virtue words ("good", "helpful", "detailed") without concrete definition
- [ ] No contradictions (e.g., "be concise" + "cover everything")
- [ ] All implicit assumptions made explicit

### Step 5: Deliver and Iterate

Present the prompt in a clean code block. If the original request was complex and got split:

- Show each prompt in the chain, numbered
- Explain how outputs feed into subsequent prompts
- Suggest which prompts can run in parallel vs sequential

Always offer: "Want me to adjust the constraints, add examples, or split this differently?"

## Advanced: Prompt Chaining

When a task is too complex for one prompt (fails N-principle), decompose into a chain. Each link in the chain:

- Has a single clear goal (passes all KERNEL checks independently)
- Produces output that feeds cleanly into the next prompt
- Can be verified independently before moving to the next step

**Pattern**: Task → subtask analysis → ordered chain with data flow

**Example chain for "Build a REST API"**:

1. Design data models (output: schema)
2. Generate endpoint specifications (input: schema → output: OpenAPI spec)
3. Implement endpoints (input: OpenAPI spec → output: code)
4. Write tests (input: code + spec → output: test suite)

## Common Transformations

Quick fixes for the most frequent prompt problems:

| Problem        | Before                          | After                                                                                      |
| -------------- | ------------------------------- | ------------------------------------------------------------------------------------------ |
| Vague virtue   | "Write a good summary"          | "Write a 3-sentence summary covering: finding, impact, recommendation"                     |
| Overloaded     | "Code + test + document this"   | Split into 3 chained prompts                                                               |
| Temporal drift | "Current best practices for..." | "Best practices as of Python 3.12 for..."                                                  |
| No constraints | "Write Python code"             | "Python 3.12+, no external libs, type hints, <50 lines per function"                       |
| Unclear format | "Analyze this data"             | "Output: markdown table with columns [Metric, Value, Trend, Action]"                       |
| Unverifiable   | "Make it production-ready"      | "Include: error handling, input validation, logging, retry logic with exponential backoff" |

