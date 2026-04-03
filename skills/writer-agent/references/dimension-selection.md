# Dimension Selection — Custom Mode

Load khi user chọn "Custom" thay vì preset ở Step 2.

**Flow:** Voice → Structure → Identity → Audience → Emotion (tất cả bắt buộc)

Mỗi chiều có default mapping dựa trên voice. Suggest defaults, user PHẢI confirm hoặc chọn khác.

## Voice

Hỏi user confirm voice (giọng văn, tone, persona).

| Voice | File | Mô tả |
| --- | --- | --- |
| Teacher | `teacher.md` | "Chúng ta" đồng hành, teaching, ấm áp |
| Personal | `personal.md` | "Tôi" personal journey, vulnerable |
| Objective | `objective.md` | Neutral, data-driven, formal |
| Guide | `guide.md` | Đồng hành mindful, Đông-Tây |
| Investigator | `investigator.md` | Tìm hiểu, đặt câu hỏi, challenge |
| Dialogue | `dialogue.md` | Thầy-trò đối thoại, Zen |
| Storyteller | `storyteller.md` | Kể chuyện ngôi thứ nhất, chánh niệm |
| **Custom** | User tạo mới | Theo `templates/voice-template.md` |

Voice files: `voices/{voice}.md`. Xem [dimension-comparison.md](dimension-comparison.md) để so sánh.

## Structure

Hỏi user confirm structure. Mỗi voice có `default_structure` trong frontmatter.

| Structure | File | Organization | Default cho |
| --- | --- | --- | --- |
| BLUF-Evidence | `bluf-evidence.md` | Executive Summary → Evidence → Action | Objective |
| Building Blocks | `building-blocks.md` | Hook → Intuition → Concept → Example → Apply | Teacher |
| Five Layers | `five-layers.md` | Surface → Structure → Tension → Connection → Synth | Investigator |
| Spiral Return | `spiral-return.md` | Moment → Spiral deeper → Open ending | Personal |
| Master-Student | `master-student.md` | Experience → Dialogue → Silence | Dialogue |
| Story Arc | `story-arc.md` | Scene → Encounter → Deepening → Transformation | Storyteller |
| Depth-Practice | `depth-practice.md` | Present moment → Layers → Practice invitation | Guide |
| Adaptive | `adaptive.md` | Content-driven, flexible | Mixed content |

Structure files: `structures/{structure}.md`

## Identity

Hỏi user chọn writer identity.

| Identity | File | Mô tả | Default cho |
| --- | --- | --- | --- |
| Tech Builder | `tech-builder.md` | Practitioner, pragmatic builder | Teacher |
| Contemplative Thinker | `contemplative-thinker.md` | Hành giả, tìm ý nghĩa | Personal, Guide, Dialogue, Storyteller |
| Knowledge Curator | `knowledge-curator.md` | Cross-domain connector | Objective, Investigator |
| **Custom** | User tạo mới | Theo `templates/identity-template.md` | - |

## Audience

Hỏi user viết cho ai.

| Audience | File | Mô tả | Default cho |
| --- | --- | --- | --- |
| Busy Professionals | `busy-professionals.md` | Bận, cần actionable | Objective |
| Curious Beginners | `curious-beginners.md` | Mới, cần clarity | Teacher, Guide |
| Deep Seekers | `deep-seekers.md` | Muốn chiều sâu | Personal, Investigator, Dialogue, Storyteller |
| **Custom** | User tạo mới | Theo `templates/audience-template.md` | - |

## Emotion

Hỏi user muốn người đọc cảm thấy gì.

| Emotion | File | Mô tả | Default cho |
| --- | --- | --- | --- |
| Empower & Challenge | `empower-challenge.md` | Growth qua discomfort | Teacher, Objective |
| Reflect & Discover | `reflect-discover.md` | Stillness, wonder | Personal, Guide, Dialogue, Storyteller |
| Provoke & Transform | `provoke-transform.md` | Challenge assumptions | Investigator |
| **Custom** | User tạo mới | Theo `templates/emotion-template.md` | - |

## Compatibility Check

Sau khi chọn xong 5 dimensions, kiểm tra compatibility:

```python
pairs_to_check = [(identity, voice), (audience, voice), (emotion, voice)]
low_compat = [pair for pair in pairs_to_check if compatibility(pair) == "★"]
if low_compat:
    warn(f"Combo {low_compat} có compatibility thấp (★)")
    # Hỏi user: tiếp tục hay chọn khác?
```

**Conflict Resolution**: Voice quyết định HOW (style/tone), Profile (Identity/Audience/Emotion) bổ sung WHAT (authority, đối tượng, cảm xúc).
