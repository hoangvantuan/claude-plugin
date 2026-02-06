# Slide HTML Templates

Mẫu HTML cho từng slide type. pptx skill PHẢI follow patterns này khi generate HTML. Thay thế colors/fonts/sizes từ style YAML đã chọn.

**Quy tắc chung:**

* Mọi text PHẢI trong `<p>`, `<h1>`-`<h6>`, `<ul>`, `<ol>`

* KHÔNG nested `<ul>`/`<ol>`

* Dùng `<div>` cho shapes/backgrounds/borders

* Dimensions: `width: {layout.width}pt; height: {layout.height}pt`

* Body: `display: flex; flex-direction: column;`

## title

Centered, vertical middle. Title lớn + subtitle nhỏ hơn. Optional accent divider.

```html
<body style="width: 720pt; height: 405pt; margin: 0; padding: 0; display: flex; flex-direction: column; justify-content: center; align-items: center; background: {colors.background}; font-family: {fonts.heading}, sans-serif;">
  <!-- Accent divider (if decorations.title_slide_divider = true) -->
  <div style="width: {decorations.accent_width}pt; height: {decorations.accent_thickness}pt; background: {colors.accent}; margin-bottom: 16pt;"></div>
  <h1 style="color: {slide_styles.title.title_color}; font-size: {slide_styles.title.title_size}pt; margin: 0 {layout.margin}pt 12pt; text-align: center;">{Title Text}</h1>
  <p style="color: {slide_styles.title.subtitle_color}; font-size: {slide_styles.title.subtitle_size}pt; margin: 0; text-align: center;">{Subtitle Text}</p>
</body>
```

## agenda

Left-aligned numbered list. Title top, items below.

```html
<body style="width: 720pt; height: 405pt; margin: 0; padding: 0; display: flex; flex-direction: column; background: {colors.background}; font-family: {fonts.body}, sans-serif;">
  <div style="margin: {layout.margin}pt;">
    <h1 style="color: {slide_styles.agenda.title_color}; font-size: {slide_styles.agenda.title_size}pt; margin: 0 0 20pt 0;">{Agenda Title}</h1>
    <ol style="color: {slide_styles.agenda.item_color}; font-size: {slide_styles.agenda.item_size}pt; margin: 0; padding-left: 24pt; line-height: {layout.line_spacing};">
      <li style="margin-bottom: {layout.bullet_spacing}pt;"><b style="color: {slide_styles.agenda.number_color};">01</b> — Section name</li>
      <li style="margin-bottom: {layout.bullet_spacing}pt;"><b style="color: {slide_styles.agenda.number_color};">02</b> — Section name</li>
      <li style="margin-bottom: {layout.bullet_spacing}pt;"><b style="color: {slide_styles.agenda.number_color};">03</b> — Section name</li>
    </ol>
  </div>
</body>
```

## content

Left-aligned. Title top + accent underline + bullet list. Optional left bar.

```html
<body style="width: 720pt; height: 405pt; margin: 0; padding: 0; display: flex; background: {colors.background}; font-family: {fonts.body}, sans-serif;">
  <!-- Left accent bar (if decorations.content_left_bar = true) -->
  <div style="width: {decorations.content_left_bar_width}pt; background: {colors.accent}; flex-shrink: 0;"></div>
  <div style="margin: {layout.margin}pt; flex: 1;">
    <h2 style="color: {slide_styles.content.title_color}; font-size: {slide_styles.content.title_size}pt; margin: 0 0 4pt 0;">{Assertion Title}</h2>
    <!-- Accent underline (if decorations.title_accent = "underline") -->
    <div style="width: {decorations.accent_width}pt; height: {decorations.accent_thickness}pt; background: {colors.accent}; margin-bottom: 16pt;"></div>
    <ul style="color: {slide_styles.content.body_color}; font-size: {fonts.bullet_size}pt; margin: 0; padding-left: 20pt; line-height: {layout.line_spacing};">
      <li style="margin-bottom: {layout.bullet_spacing}pt;">Bullet point text</li>
      <li style="margin-bottom: {layout.bullet_spacing}pt;"><b>Label:</b> detail text (for L2/L3 sub-items)</li>
      <li style="margin-bottom: {layout.bullet_spacing}pt;">Another point</li>
    </ul>
  </div>
</body>
```

## comparison

Two-column layout. Title top, 2 equal columns with divider.

```html
<body style="width: 720pt; height: 405pt; margin: 0; padding: 0; display: flex; flex-direction: column; background: {colors.background}; font-family: {fonts.body}, sans-serif;">
  <div style="margin: {layout.margin}pt {layout.margin}pt 0;">
    <h2 style="color: {slide_styles.comparison.title_color}; font-size: {slide_styles.comparison.title_size}pt; margin: 0 0 16pt 0;">{Comparison Title}</h2>
  </div>
  <div style="display: flex; flex: 1; margin: 0 {layout.margin}pt {layout.margin}pt;">
    <!-- Left column (48%) -->
    <div style="flex: 0 0 48%;">
      <h3 style="color: {slide_styles.comparison.left_header_color}; font-size: 22pt; margin: 0 0 10pt 0;">{Left Header}</h3>
      <ul style="color: {colors.text}; font-size: {fonts.bullet_size}pt; margin: 0; padding-left: 18pt;">
        <li style="margin-bottom: {layout.bullet_spacing}pt;">Point A</li>
        <li style="margin-bottom: {layout.bullet_spacing}pt;">Point B</li>
      </ul>
    </div>
    <!-- Divider (4%) -->
    <div style="flex: 0 0 4%; display: flex; justify-content: center;">
      <div style="width: 1pt; background: {slide_styles.comparison.divider_color};"></div>
    </div>
    <!-- Right column (48%) -->
    <div style="flex: 0 0 48%;">
      <h3 style="color: {slide_styles.comparison.right_header_color}; font-size: 22pt; margin: 0 0 10pt 0;">{Right Header}</h3>
      <ul style="color: {colors.text}; font-size: {fonts.bullet_size}pt; margin: 0; padding-left: 18pt;">
        <li style="margin-bottom: {layout.bullet_spacing}pt;">Point A</li>
        <li style="margin-bottom: {layout.bullet_spacing}pt;">Point B</li>
      </ul>
    </div>
  </div>
</body>
```

## summary

Key takeaways with checkmarks. Max 3 points.

```html
<body style="width: 720pt; height: 405pt; margin: 0; padding: 0; display: flex; flex-direction: column; background: {colors.background}; font-family: {fonts.body}, sans-serif;">
  <div style="margin: {layout.margin}pt;">
    <h2 style="color: {slide_styles.summary.title_color}; font-size: {slide_styles.summary.title_size}pt; margin: 0 0 20pt 0;">Key Takeaways</h2>
    <ul style="list-style: none; margin: 0; padding: 0; font-size: {slide_styles.summary.point_size}pt; color: {colors.text};">
      <li style="margin-bottom: 14pt;"><b style="color: {slide_styles.summary.check_color}; font-size: 22pt;">&#10003;</b> &nbsp; Takeaway point 1</li>
      <li style="margin-bottom: 14pt;"><b style="color: {slide_styles.summary.check_color}; font-size: 22pt;">&#10003;</b> &nbsp; Takeaway point 2</li>
      <li style="margin-bottom: 14pt;"><b style="color: {slide_styles.summary.check_color}; font-size: 22pt;">&#10003;</b> &nbsp; Takeaway point 3</li>
    </ul>
  </div>
</body>
```

## cta

Centered. Main CTA message + supporting detail.

```html
<body style="width: 720pt; height: 405pt; margin: 0; padding: 0; display: flex; flex-direction: column; justify-content: center; align-items: center; background: {colors.background}; font-family: {fonts.heading}, sans-serif;">
  <h1 style="color: {slide_styles.cta.message_color}; font-size: {slide_styles.cta.message_size}pt; margin: 0 {layout.margin}pt 16pt; text-align: center;">{CTA Message}</h1>
  <div style="width: 60pt; height: {decorations.accent_thickness}pt; background: {colors.accent}; margin-bottom: 16pt;"></div>
  <p style="color: {slide_styles.cta.detail_color}; font-size: {slide_styles.cta.detail_size}pt; margin: 0; text-align: center;">{Supporting detail / contact info}</p>
</body>
```

## transition

Section divider. Centered title + progress indicator. Light/different background.

```html
<body style="width: 720pt; height: 405pt; margin: 0; padding: 0; display: flex; flex-direction: column; justify-content: center; align-items: center; background: {slide_styles.transition.bg_color}; font-family: {fonts.heading}, sans-serif;">
  <h1 style="color: {slide_styles.transition.section_color}; font-size: {slide_styles.transition.section_size}pt; margin: 0 0 12pt 0; text-align: center;">{Section Title}</h1>
  <p style="color: {slide_styles.transition.progress_color}; font-size: {slide_styles.transition.progress_size}pt; margin: 0; text-align: center;">Part X of Y</p>
</body>
```

## statement (NEW)

1 assertion sentence lớn, centered. Dùng cho key messages, quotes, insights. Tạo visual rhythm.

```html
<body style="width: 720pt; height: 405pt; margin: 0; padding: 0; display: flex; flex-direction: column; justify-content: center; align-items: center; background: {colors.background}; font-family: {fonts.heading}, sans-serif;">
  <div style="max-width: 580pt; text-align: center;">
    <h1 style="color: {colors.primary}; font-size: {slide_styles.statement.message_size}pt; margin: 0 0 16pt 0; line-height: 1.3;">{Bold assertion or key insight}</h1>
    <!-- Optional: source/attribution -->
    <p style="color: {colors.muted}; font-size: {slide_styles.statement.source_size}pt; margin: 0;">{Optional source or context}</p>
  </div>
</body>
```

## metric (NEW)

1 số liệu lớn + context. Dùng cho key data points, statistics, KPIs.

```html
<body style="width: 720pt; height: 405pt; margin: 0; padding: 0; display: flex; flex-direction: column; justify-content: center; align-items: center; background: {colors.background}; font-family: {fonts.heading}, sans-serif;">
  <div style="text-align: center;">
    <h1 style="color: {colors.accent}; font-size: {slide_styles.metric.number_size}pt; margin: 0 0 8pt 0;">{85%}</h1>
    <p style="color: {colors.primary}; font-size: {slide_styles.metric.label_size}pt; margin: 0 0 8pt 0;">{Metric Label}</p>
    <p style="color: {colors.muted}; font-size: {slide_styles.metric.context_size}pt; margin: 0;">{Brief context or comparison}</p>
  </div>
</body>
```

