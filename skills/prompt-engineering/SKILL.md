---
name: prompt-engineering
description: "Use this skill when writing commands, hooks, skills for Agent, or prompts for sub agents or any other LLM interaction, including optimizing prompts, improving LLM outputs, or designing production prompt templates. Trigger when user mentions 'write a prompt', 'optimize prompt', 'improve prompt', 'system prompt', 'few-shot', 'chain of thought', 'prompt template', 'agent prompt', 'skill prompt', 'hook prompt', or any task involving crafting instructions for an LLM. Also trigger when writing SKILL.md, agent definitions, hook scripts that include LLM instructions, or designing sub-agent prompts within Claude Code workflows."
disable-model-invocation: true
---

# Prompt Engineering Patterns

Advanced prompt engineering techniques to maximize LLM performance, reliability, and controllability.

## Core Capabilities

### 1. Few-Shot Learning

Teach the model by showing examples instead of explaining rules. Include 2-5 input-output pairs that demonstrate the desired behavior. Use when you need consistent formatting, specific reasoning patterns, or handling of edge cases. More examples improve accuracy but consume tokens, balance based on task complexity.

**Example:**

```markdown
Extract key information from support tickets:

Input: "My login doesn't work and I keep getting error 403"
Output: {"issue": "authentication", "error_code": "403", "priority": "high"}

Input: "Feature request: add dark mode to settings"
Output: {"issue": "feature_request", "error_code": null, "priority": "low"}

Now process: "Can't upload files larger than 10MB, getting timeout"
```

### 2. Chain-of-Thought Prompting

Request step-by-step reasoning before the final answer. Add "Let's think step by step" (zero-shot) or include example reasoning traces (few-shot). Use for complex problems requiring multi-step logic, mathematical reasoning, or when you need to verify the model's thought process. Improves accuracy on analytical tasks by 30-50%.

**Example:**

```markdown
Analyze this bug report and determine root cause.

Think step by step:
1. What is the expected behavior?
2. What is the actual behavior?
3. What changed recently that could cause this?
4. What components are involved?
5. What is the most likely root cause?

Bug: "Users can't save drafts after the cache update deployed yesterday"
```

### 3. Prompt Optimization

Systematically improve prompts through testing and refinement. Start simple, measure performance (accuracy, consistency, token usage), then iterate. Test on diverse inputs including edge cases. Use A/B testing to compare variations. Critical for production prompts where consistency and cost matter.

**Example:**

```markdown
Version 1 (Simple): "Summarize this article"
→ Result: Inconsistent length, misses key points

Version 2 (Add constraints): "Summarize in 3 bullet points"
→ Result: Better structure, but still misses nuance

Version 3 (Add reasoning): "Identify the 3 main findings, then summarize each"
→ Result: Consistent, accurate, captures key information
```

### 4. Template Systems

Build reusable prompt structures with variables, conditional sections, and modular components. Use for multi-turn conversations, role-based interactions, or when the same pattern applies to different inputs. Reduces duplication and ensures consistency across similar tasks.

**Example:**

```python
# Reusable code review template
template = """
Review this {language} code for {focus_area}.

Code:
{code_block}

Provide feedback on:
{checklist}
"""

# Usage
prompt = template.format(
    language="Python",
    focus_area="security vulnerabilities",
    code_block=user_code,
    checklist="1. SQL injection\n2. XSS risks\n3. Authentication"
)
```

### 5. System Prompt Design

Set global behavior and constraints that persist across the conversation. Define the model's role, expertise level, output format, and safety guidelines. Use system prompts for stable instructions that shouldn't change turn-to-turn, freeing up user message tokens for variable content.

**Example:**

```markdown
System: You are a senior backend engineer specializing in API design.

Rules:
- Always consider scalability and performance
- Suggest RESTful patterns by default
- Flag security concerns immediately
- Provide code examples in Python
- Use early return pattern

Format responses as:
1. Analysis
2. Recommendation
3. Code example
4. Trade-offs
```

## Key Patterns

### Progressive Disclosure

Start with simple prompts, add complexity only when needed:

1. **Level 1**: Direct instruction
   - "Summarize this article"

2. **Level 2**: Add constraints
   - "Summarize this article in 3 bullet points, focusing on key findings"

3. **Level 3**: Add reasoning
   - "Read this article, identify the main findings, then summarize in 3 bullet points"

4. **Level 4**: Add examples
   - Include 2-3 example summaries with input-output pairs

### Instruction Hierarchy

```
[System Context] → [Task Instruction] → [Examples] → [Input Data] → [Output Format]
```

### Error Recovery

Build prompts that gracefully handle failures:

- Include fallback instructions
- Request confidence scores
- Ask for alternative interpretations when uncertain
- Specify how to indicate missing information

## Best Practices

1. **Be Specific**: Vague prompts produce inconsistent results
2. **Show, Don't Tell**: Examples are more effective than descriptions
3. **Test Extensively**: Evaluate on diverse, representative inputs
4. **Iterate Rapidly**: Small changes can have large impacts
5. **Monitor Performance**: Track metrics in production
6. **Version Control**: Treat prompts as code with proper versioning
7. **Document Intent**: Explain why prompts are structured as they are

## Common Pitfalls

- **Over-engineering**: Starting with complex prompts before trying simple ones
- **Example pollution**: Using examples that don't match the target task
- **Context overflow**: Exceeding token limits with excessive examples
- **Ambiguous instructions**: Leaving room for multiple interpretations
- **Ignoring edge cases**: Not testing on unusual or boundary inputs

## Integration Patterns

### With RAG Systems

```python
prompt = f"""Given the following context:
{retrieved_context}

{few_shot_examples}

Question: {user_question}

Provide a detailed answer based solely on the context above. If the context doesn't contain enough information, explicitly state what's missing."""
```

### With Validation

```python
prompt = f"""{main_task_prompt}

After generating your response, verify it meets these criteria:
1. Answers the question directly
2. Uses only information from provided context
3. Cites specific sources
4. Acknowledges any uncertainty

If verification fails, revise your response."""
```

## Performance Optimization

### Token Efficiency

- Remove redundant words and phrases
- Use abbreviations consistently after first definition
- Consolidate similar instructions
- Move stable content to system prompts

### Latency Reduction

- Minimize prompt length without sacrificing quality
- Use streaming for long-form outputs
- Cache common prompt prefixes
- Batch similar requests when possible

## Agent Prompting Best Practices

Based on Anthropic's official best practices for agent prompting.

### Context Window Management

Context window = "working memory" of the model (200K tokens for Claude). Token accumulation grows linearly with each turn. Context window is a shared resource: system prompt, conversation history, other commands/skills/hooks, metadata all compete for space.

**Default assumption**: Claude is already very smart. Only add context Claude doesn't already have. Challenge each piece of information:

- "Does Claude really need this explanation?"
- "Can I assume Claude knows this?"
- "Does this paragraph justify its token cost?"

### Degrees of Freedom

Match specificity to the task's fragility and variability.

**High freedom** (text-based instructions): Multiple approaches are valid, decisions depend on context, heuristics guide the approach.

**Medium freedom** (pseudocode/scripts with parameters): A preferred pattern exists, some variation is acceptable.

**Low freedom** (specific scripts, few parameters): Operations are fragile and error-prone, consistency is critical, a specific sequence must be followed.

**Analogy**: Think of Claude as a robot exploring a path:
- **Narrow bridge with cliffs**: Only one safe way forward. Provide exact instructions (low freedom).
- **Open field**: Many paths lead to success. Give general direction (high freedom).

## Persuasion Principles for Prompt Design

LLMs respond to the same persuasion principles as humans. Research foundation: Meincke et al. (2025) tested 7 principles with N=28,000 AI conversations. Persuasion techniques more than doubled compliance rates (33% → 72%, p < .001).

### Effective Principles

| Principle | What it is | When to use | Example |
|-----------|-----------|-------------|---------|
| Authority | Deference to expertise. "YOU MUST", "Never", "No exceptions" | Discipline-enforcing, safety-critical | "Write code before test? Delete it. Start over." |
| Commitment | Consistency with prior actions. Require announcements, force explicit choices | Multi-step processes, accountability | "You MUST announce: I'm using [Skill Name]" |
| Scarcity | Urgency from time limits. "Before proceeding", "Immediately after X" | Immediate verification, preventing procrastination | "IMMEDIATELY request review before proceeding" |
| Social Proof | Conformity to norms. "Every time", "X without Y = failure" | Universal practices, warning about failures | "Checklists without tracking = steps get skipped" |
| Unity | Shared identity. "our codebase", "we're colleagues" | Collaborative workflows, team culture | "We're colleagues. I need honest judgment." |

### Principles to Avoid

- **Reciprocity**: Use sparingly, can feel manipulative
- **Liking**: Don't use for compliance, creates sycophancy

### Principle Combinations by Prompt Type

| Prompt Type | Use | Avoid |
|------------|-----|-------|
| Discipline-enforcing | Authority + Commitment + Social Proof | Liking, Reciprocity |
| Guidance/technique | Moderate Authority + Unity | Heavy authority |
| Collaborative | Unity + Commitment | Authority, Liking |
| Reference | Clarity only | All persuasion |

### Why This Works

- Bright-line rules reduce rationalization: "YOU MUST" removes decision fatigue
- Implementation intentions create automatic behavior: "When X, do Y" > "generally do Y"
- LLMs are parahuman: trained on human text containing these patterns

### Ethical Check

Would this technique serve the user's genuine interests if they fully understood it?

### Quick Reference for Prompt Design

1. What type is it? (Discipline vs. guidance vs. reference)
2. What behavior am I trying to change?
3. Which principle(s) apply? (Usually authority + commitment for discipline)
4. Am I combining too many? (Don't use all seven)
5. Is this ethical? (Serves user's genuine interests?)
