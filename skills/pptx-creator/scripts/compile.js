/**
 * PPTX Slide Compiler Template
 *
 * Usage: Copy this file into your slides/ directory, adjust theme + slideCount,
 * then run: node compile.js
 *
 * Each slide-XX.js must export: { createSlide(pres, theme), slideConfig }
 *
 * Boundary safety: position validation lives in layout-helpers.js.
 * Slides hardcoding positions should call `assertBounds(elements)` themselves.
 * Slides using `calcStack` get automatic throw on overflow.
 */

const pptxgen = require("pptxgenjs");
const path = require("path");
const fs = require("fs");

// --- CUSTOMIZE THESE ---
const SLIDE_COUNT = 10;
const OUTPUT_DIR = "./output";
const OUTPUT_FILE = "presentation.pptx";

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "Author Name";
pres.title = "Presentation Title";

// Theme object — 7 keys: 5 colors + 2 fonts (see design-system.md)
// Auto-detect series-config.json for consistent style across multiple decks
const seriesPaths = ["series-config.json", "../series-config.json"];
const seriesFile = seriesPaths.find((p) => fs.existsSync(path.join(__dirname, p)));
const seriesConfig = seriesFile
  ? JSON.parse(fs.readFileSync(path.join(__dirname, seriesFile), "utf-8"))
  : null;

const theme = seriesConfig?.theme || {
  primary: "264653",   // darkest — titles, dark backgrounds
  secondary: "2a9d8f", // dark accent — body text, icons
  accent: "e9c46a",    // mid-tone — highlights, badges
  light: "f4a261",     // light accent — subtle fills
  bg: "FAFAFA",        // background — slide base color
  titleFont: "Montserrat",     // title + section headers
  bodyFont: "Be Vietnam Pro",  // body, bullets, captions, badge
};

if (seriesConfig) {
  console.log(`Using series config: ${seriesFile} (${seriesConfig.series || "unnamed"})`);
}

// --- COMPILE SLIDES ---
for (let i = 1; i <= SLIDE_COUNT; i++) {
  const num = String(i).padStart(2, "0");
  const slidePath = path.join(__dirname, `slide-${num}.js`);

  if (!fs.existsSync(slidePath)) {
    console.error(`Missing: slide-${num}.js`);
    process.exit(1);
  }

  const slideModule = require(slidePath);
  try {
    slideModule.createSlide(pres, theme);
  } catch (err) {
    console.error(`Error in slide-${num}: ${err.message}`);
    process.exit(1);
  }
  console.log(`Compiled slide ${num}: ${slideModule.slideConfig?.title || "untitled"}`);
}

// --- WRITE OUTPUT ---
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

const outputPath = path.join(OUTPUT_DIR, OUTPUT_FILE);
const absPath = path.resolve(outputPath);
pres
  .writeFile({ fileName: outputPath })
  .then(() => {
    console.log(`\nDone! ${absPath}`);
    console.log(`Open with PowerPoint, Keynote, or LibreOffice.`);
  })
  .catch((err) => {
    console.error(`\nWrite failed: ${err.message}`);
    process.exit(1);
  });
