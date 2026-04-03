# Prompt Template

Template chuẩn cho prompt output. Chỉ include sections phù hợp — omit phần không relevant.

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

## Section Inclusion Guide

| Section | Khi nào include |
|---------|----------------|
| Role, Context, Instructions, Constraints, Output Format | **Luôn include** |
| Input | Required cho task prompts, optional cho loại khác |
| Examples | Khi output phụ thuộc vào việc thấy patterns cụ thể (2-5 examples) |
| Reasoning | Cho multi-step logic, math, hoặc code tasks |
| Fallback | Cho user-facing prompts, multi-turn systems |
