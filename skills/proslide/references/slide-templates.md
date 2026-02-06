# Slidev Slide Templates

Mẫu Slidev Markdown cho từng slide type. `slidev` skill PHẢI follow patterns này khi generate `slides.md`. Thay thế nội dung placeholder bằng content thực tế từ outline.

**Quy tắc chung:**

* Mỗi slide bắt đầu bằng `---` separator (trừ slide đầu tiên dùng headmatter)

* Layout được chỉ định qua YAML front matter mỗi slide

* Speaker notes dùng HTML comment `<!-- notes -->`

* Code blocks dùng native Markdown fenced blocks (triple backtick)

* KHÔNG dùng image, chỉ text-only

## title → cover

```md
---
layout: cover
---

# {Title Text}

{Subtitle Text}

<!--
Speaker notes here
-->
```

## agenda → default

```md
---
layout: default
---

# {Agenda Title}

1. **01** — Section name
2. **02** — Section name
3. **03** — Section name

<!--
Speaker notes here
-->
```

## content → default

```md
---
layout: default
---

# {Assertion Title}

- Bullet point text
- **Label:** detail text
- Another point

<!--
Speaker notes here
-->
```

Content slide với sub-bullets (L2/L3):

```md
---
layout: default
---

# {Assertion Title}

- Main bullet 1
  - Sub-detail hoặc ví dụ
- **Label:** detail text
  - Sub-detail
- Another point

<!--
Speaker notes here
-->
```

## comparison → two-cols-header

```md
---
layout: two-cols-header
---

# {Comparison Title}

::left::

### {Left Header}

- Point A
- Point B

::right::

### {Right Header}

- Point A
- Point B

<!--
Speaker notes here
-->
```

## summary → default

```md
---
layout: default
---

# Key Takeaways

- ✅ Takeaway point 1
- ✅ Takeaway point 2
- ✅ Takeaway point 3

<!--
Speaker notes here
-->
```

## cta → end

```md
---
layout: end
---

# {CTA Message}

{Supporting detail / contact info}

<!--
Speaker notes here
-->
```

## transition → section

```md
---
layout: section
---

# {Section Title}

Part X of Y

<!--
Speaker notes here
-->
```

## statement → statement

```md
---
layout: statement
---

# {Bold assertion or key insight}

{Optional source or context}

<!--
Speaker notes here
-->
```

## metric → fact

```md
---
layout: fact
---

# {85%}

{Metric Label}

{Brief context or comparison}

<!--
Speaker notes here
-->
```

## code → default

Basic code block:

```md
---
layout: default
---

# {Code Slide Title}

\`\`\`python
def example():
    return "Hello World"
\`\`\`

- Key point about the code

<!--
Speaker notes here
-->
```

Với line highlighting (highlight dòng cụ thể):

```md
---
layout: default
---

# {Code Slide Title}

\`\`\`python {3,4}
def process_data(items):
    results = []
    for item in items:        # highlighted
        results.append(item)  # highlighted
    return results
\`\`\`

- Dòng 3-4: vòng lặp xử lý chính

<!--
Speaker notes here
-->
```

Với click-based highlighting (highlight từng phần khi click):

```md
---
layout: default
---

# {Code Slide Title}

\`\`\`python {1|3-4|6|all}
def process_data(items):
    results = []
    for item in items:
        results.append(item)
    return results
\`\`\`

<!--
Click 1: highlight dòng 1 (function signature)
Click 2: highlight dòng 3-4 (loop logic)
Click 3: highlight dòng 6 (return)
Click 4: highlight all
-->
```

**Lưu ý code blocks:**

* Dùng ngôn ngữ cụ thể sau triple backtick (python, javascript, bash, etc.) để có syntax highlighting tự động
* Max 10-15 dòng code/slide
* **Line highlighting** `{2,3}`: highlight cố định — dùng khi muốn nhấn mạnh dòng quan trọng ngay lập tức
* **Click-based highlighting** `{1|3-4|all}`: highlight theo click — dùng khi muốn giải thích code từng phần, phù hợp cho walkthrough/tutorial
* Ưu tiên click-based highlighting cho L2/L3 technical presentations để tạo progressive disclosure
