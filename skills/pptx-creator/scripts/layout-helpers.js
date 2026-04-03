/**
 * Layout Helpers for PPTX Creator
 *
 * Pure functions to calculate element positions and prevent overlap.
 * All functions return plain {x, y, w, h} objects — spread directly
 * into PptxGenJS addText/addShape options.
 *
 * Canvas: 10" × 5.625" (LAYOUT_16x9). Unit: inches.
 */

// --- Layout Constants ---
const CANVAS = { w: 10, h: 5.625 };
const SAFE_AREA = { x: 0.5, y: 1.2, w: 9.0, h: 3.8 }; // After title, before badge
const TITLE_AREA = { x: 0.5, y: 0.3, w: 9.0, h: 0.85 };
const PAGE_BADGE = { x: 9.3, y: 5.1, w: 0.4, h: 0.4 };

// Line height lookup (inches per line) — based on Vietnamese text measurements
const LINE_HEIGHTS = {
  44: 0.85,
  36: 0.65,
  28: 0.55,
  24: 0.45,
  20: 0.38,
  18: 0.35,
  14: 0.28,
};

/**
 * Estimate text box height needed for Vietnamese content.
 * @param {number} lineCount - Number of text lines
 * @param {number} fontSize - Font size in pt
 * @param {object} opts - { vietnamese: true } (default true)
 * @returns {number} Height in inches
 */
function estimateTextHeight(lineCount, fontSize, opts = {}) {
  const { vietnamese = true } = opts;
  const closest = Object.keys(LINE_HEIGHTS)
    .map(Number)
    .reduce((a, b) => (Math.abs(b - fontSize) < Math.abs(a - fontSize) ? b : a));
  const baseH = LINE_HEIGHTS[closest];
  const h = lineCount * baseH * (vietnamese ? 1.3 : 1.0);
  return Math.round(h * 100) / 100;
}

/**
 * Calculate vertical stack positions for N items.
 * Throws if total height exceeds available area.
 * @param {number} count - Number of items
 * @param {number} itemHeight - Height per item (inches)
 * @param {object} opts - { gap, area, startY }
 * @returns {Array<{x, y, w, h}>}
 */
function calcStack(count, itemHeight, opts = {}) {
  const { gap = 0.15, area = SAFE_AREA } = opts;
  const startY = opts.startY ?? area.y;
  const availableH = area.y + area.h - startY;
  const totalH = count * itemHeight + (count - 1) * gap;

  if (totalH > availableH) {
    throw new Error(
      `calcStack: ${count} items × ${itemHeight}" + ${count - 1} gaps × ${gap}" = ${totalH.toFixed(2)}" ` +
        `exceeds available ${availableH.toFixed(2)}". Reduce count or itemHeight.`
    );
  }

  const result = [];
  let curY = startY;
  for (let i = 0; i < count; i++) {
    result.push({ x: area.x, y: round(curY), w: area.w, h: itemHeight });
    curY += itemHeight + gap;
  }
  return result;
}

/**
 * Calculate N equal columns within an area.
 * @param {number} count - Number of columns
 * @param {object} opts - { gap, area }
 * @returns {Array<{x, y, w, h}>}
 */
function calcColumns(count, opts = {}) {
  const { gap = 0.2, area = SAFE_AREA } = opts;
  const totalGap = (count - 1) * gap;
  const colW = (area.w - totalGap) / count;

  return Array.from({ length: count }, (_, i) => ({
    x: round(area.x + i * (colW + gap)),
    y: area.y,
    w: round(colW),
    h: area.h,
  }));
}

/**
 * Calculate grid cell positions (row-major order).
 * @param {number} cols - Number of columns
 * @param {number} rows - Number of rows
 * @param {object} opts - { colGap, rowGap, area }
 * @returns {Array<{x, y, w, h}>}
 */
function calcGrid(cols, rows, opts = {}) {
  const { colGap = 0.2, rowGap = 0.15, area = SAFE_AREA } = opts;
  const cellW = (area.w - (cols - 1) * colGap) / cols;
  const cellH = (area.h - (rows - 1) * rowGap) / rows;

  const result = [];
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      result.push({
        x: round(area.x + c * (cellW + colGap)),
        y: round(area.y + r * (cellH + rowGap)),
        w: round(cellW),
        h: round(cellH),
      });
    }
  }
  return result;
}

/**
 * Validate elements don't exceed canvas or overlap page badge.
 * @param {Array<{x, y, w, h}>} elements
 * @returns {{ valid: boolean, warnings: string[], errors: string[] }}
 */
function assertBounds(elements) {
  const warnings = [];
  const errors = [];

  elements.forEach((el, i) => {
    const { x = 0, y = 0, w = 0, h = 0 } = el;
    const right = x + w;
    const bottom = y + h;

    if (right > CANVAS.w)
      errors.push(`Element ${i}: right edge ${right.toFixed(2)}" > canvas ${CANVAS.w}"`);
    if (bottom > CANVAS.h)
      errors.push(`Element ${i}: bottom ${bottom.toFixed(2)}" > canvas ${CANVAS.h}"`);
    if (x < 0 || y < 0)
      errors.push(`Element ${i}: negative position (${x}, ${y})`);
    if (x < 0.4)
      warnings.push(`Element ${i}: x=${x}" near left margin (min 0.5")`);
    if (bottom > 5.0)
      warnings.push(`Element ${i}: bottom ${bottom.toFixed(2)}" encroaches page badge zone (5.1")`);
  });

  return { valid: errors.length === 0, warnings, errors };
}

function round(n) {
  return Math.round(n * 100) / 100;
}

module.exports = {
  CANVAS,
  SAFE_AREA,
  TITLE_AREA,
  PAGE_BADGE,
  LINE_HEIGHTS,
  estimateTextHeight,
  calcStack,
  calcColumns,
  calcGrid,
  assertBounds,
};
