---
name: deep-post-ideas
description: "Extract compelling post outlines from reference materials and transform into structured outlines for wisdom-style social media posts."
disable-model-invocation: true
---

# Deep Post Ideas

Extract distinct, high-engagement post outlines from reference materials. Focus on paradoxical truths, transformational narratives, and powerful insights — outlines only, not complete posts.

## Workflow

### Step 1: Analyze Reference Material

From the user's input, identify:

- Counterintuitive truths and paradoxes — these become the "Core Paradox" of each outline
- Core problems and pain points — what the reader is struggling with
- Powerful metaphors and narratives — elemental forces, identity shifts, transformation arcs
- Reader objections — the "yeah but..." that must be addressed
- Aspirational archetypes — who the reader wants to become

### Step 2: Select & Develop Post Concepts

From Step 1's analysis, select the insights with highest tension — where the counterintuitive truth clashes most strongly with common belief. Each concept must cover a different angle of the material to avoid repetition.

**Số lượng**: Mặc định 5 outlines. Nếu material chỉ đủ chất liệu cho ít hơn (insight lặp, chủ đề hẹp), giảm xuống 3 và giải thích cho user thay vì ép ra outline kém chất lượng.

For each concept:

1. Choose a counterintuitive truth from the reference material
2. Frame it as an absolute principle
3. Develop short, practical examples
4. Build a narrative arc: destruction/challenge -> revelation -> transcendence
5. Craft a memorable closing insight

### Step 3: Output Outlines

For each outline, provide:

```
POST OUTLINE [N]:

- Core Paradox: [Central counterintuitive truth]
  - [Rephrase 3 ways, getting shorter each time]

- Key Quotes:
  - [Quote 1 from reference material]
  - [Quote 2]
  - [Quote 3]

- Transformation Arc: [Challenge -> revelation -> transcendence]

- Core Problems:
  - [Problem 1 — tangible, relatable]
  - [Problem 2]
  - [Problem 3]

- Key Examples:
  - [Example 1 — concrete illustration]
  - [Example 2]
  - [Example 3]

- Reader Objections:
  - [Objection 1 — written as the reader]
  - [Objection 2]
  - [Objection 3]

- Aspirational Statement: [1-2 sentences on traits/skills to develop]

- Actionable Steps: [3+ staccato-style steps]

- Big Idea: [Transformational concept in 1-2 sentences]

- Memorable Closing Insight: [One sentence that ties everything together]
```

## Constraints

- Generate **outlines only**, not complete posts
- Focus on depth and emotional resonance over tactical advice
- Each outline must have a distinct theme
- Prioritize quality and engagement potential
- Don't add information not implied in the reference material

## Reference Examples

See [references/example-phrasing.md](references/example-phrasing.md) for example phrasing styles and language techniques to apply across all outlines.
