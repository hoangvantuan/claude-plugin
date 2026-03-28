/**
 * PPTX Slide Compiler Template
 *
 * Usage: Copy this file into your slides/ directory, adjust theme + slideCount,
 * then run: node compile.js
 *
 * Each slide-XX.js must export: { createSlide(pres, theme), slideConfig }
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

// Theme object — 5 keys only (see design-system.md for palette options)
const theme = {
  primary: "264653",   // darkest — titles, dark backgrounds
  secondary: "2a9d8f", // dark accent — body text, icons
  accent: "e9c46a",    // mid-tone — highlights, badges
  light: "f4a261",     // light accent — subtle fills
  bg: "FAFAFA",        // background — slide base color
};

// --- COMPILE SLIDES ---
for (let i = 1; i <= SLIDE_COUNT; i++) {
  const num = String(i).padStart(2, "0");
  const slidePath = path.join(__dirname, `slide-${num}.js`);

  if (!fs.existsSync(slidePath)) {
    console.error(`Missing: slide-${num}.js`);
    process.exit(1);
  }

  const slideModule = require(slidePath);
  slideModule.createSlide(pres, theme);
  console.log(`Compiled slide ${num}: ${slideModule.slideConfig?.title || "untitled"}`);
}

// --- WRITE OUTPUT ---
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

const outputPath = path.join(OUTPUT_DIR, OUTPUT_FILE);
pres.writeFile({ fileName: outputPath }).then(() => {
  console.log(`\nDone! ${outputPath}`);
});
