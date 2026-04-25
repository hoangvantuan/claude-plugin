#!/usr/bin/env node

import { SonioxNodeClient } from "@soniox/node";
import { readFile, writeFile, unlink } from "node:fs/promises";
import { existsSync } from "node:fs";
import { basename, resolve, extname } from "node:path";
import { execSync } from "node:child_process";
import { tmpdir } from "node:os";
import { join } from "node:path";

function parseArgs(args) {
  const parsed = { lang: "vi", format: "timestamps", output: null, file: null };
  let i = 0;
  while (i < args.length) {
    if (args[i] === "--lang" && args[i + 1]) {
      parsed.lang = args[++i];
    } else if (args[i] === "--format" && args[i + 1]) {
      parsed.format = args[++i];
    } else if (args[i] === "--output" && args[i + 1]) {
      parsed.output = args[++i];
    } else if (!args[i].startsWith("--")) {
      parsed.file = args[i];
    }
    i++;
  }
  return parsed;
}

function formatMs(ms) {
  const totalSeconds = Math.floor(ms / 1000);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  const millis = ms % 1000;
  return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}.${String(millis).padStart(3, "0")}`;
}

function formatSrtTime(ms) {
  const totalSeconds = Math.floor(ms / 1000);
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;
  const millis = ms % 1000;
  return `${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")},${String(millis).padStart(3, "0")}`;
}

function groupTokensIntoSegments(tokens, maxGapMs = 1500) {
  const segments = [];
  let current = { text: [], startMs: 0, endMs: 0 };

  for (const token of tokens) {
    if (!token.text.trim()) continue;

    if (current.text.length === 0) {
      current.startMs = token.start_ms;
      current.endMs = token.end_ms;
      current.text.push(token.text);
      continue;
    }

    const gap = token.start_ms - current.endMs;
    if (gap > maxGapMs) {
      segments.push({
        text: current.text.join("").trim(),
        startMs: current.startMs,
        endMs: current.endMs,
      });
      current = { text: [token.text], startMs: token.start_ms, endMs: token.end_ms };
    } else {
      current.text.push(token.text);
      current.endMs = token.end_ms;
    }
  }

  if (current.text.length > 0) {
    segments.push({
      text: current.text.join("").trim(),
      startMs: current.startMs,
      endMs: current.endMs,
    });
  }

  return segments;
}

function formatTimestamps(segments) {
  return segments
    .map((s) => `[${formatMs(s.startMs)} -> ${formatMs(s.endMs)}] ${s.text}`)
    .join("\n");
}

function formatSrt(segments) {
  return segments
    .map(
      (s, i) =>
        `${i + 1}\n${formatSrtTime(s.startMs)} --> ${formatSrtTime(s.endMs)}\n${s.text}\n`
    )
    .join("\n");
}

function formatPlainText(segments) {
  return segments.map((s) => s.text).join("\n");
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (!args.file) {
    console.error("Cách dùng: node transcribe.js <file-audio-hoặc-video> [--lang vi] [--format timestamps|text|srt] [--output file.txt]");
    process.exit(1);
  }

  if (!process.env.SONIOX_API_KEY) {
    console.error("Lỗi: SONIOX_API_KEY chưa được set.");
    console.error("Chạy: export SONIOX_API_KEY=<your-key>");
    process.exit(1);
  }

  const filePath = resolve(args.file);
  if (!existsSync(filePath)) {
    console.error(`Lỗi: Không tìm thấy file: ${filePath}`);
    process.exit(1);
  }

  const AUDIO_NATIVE = new Set([
    ".aac", ".aiff", ".amr", ".asf", ".flac", ".mp3",
    ".ogg", ".wav", ".m4a",
  ]);
  const VIDEO_EXTRACT = new Set([
    ".mp4", ".webm", ".mov", ".mkv", ".avi", ".flv", ".wmv", ".ts", ".mts", ".3gp",
  ]);

  const ext = extname(filePath).toLowerCase();
  let audioPath = filePath;
  let tempFile = null;

  if (VIDEO_EXTRACT.has(ext)) {
    console.error(`Video format (${ext}) phát hiện. Đang trích xuất audio bằng ffmpeg...`);
    try {
      execSync("ffmpeg -version", { stdio: "ignore" });
    } catch {
      console.error("Lỗi: ffmpeg chưa được cài. Chạy: brew install ffmpeg");
      process.exit(1);
    }
    tempFile = join(tmpdir(), `stt-${Date.now()}.wav`);
    execSync(`ffmpeg -i "${filePath}" -vn -acodec pcm_s16le -ar 16000 -ac 1 "${tempFile}" -y`, {
      stdio: ["ignore", "ignore", "pipe"],
    });
    audioPath = tempFile;
    console.error("Trích xuất audio xong.");
  } else if (!AUDIO_NATIVE.has(ext)) {
    console.error(`Cảnh báo: Format ${ext} có thể không được hỗ trợ. Thử gửi trực tiếp...`);
  }

  console.error(`Đang đọc file: ${audioPath}`);
  const audio = await readFile(audioPath);
  const filename = tempFile ? "audio.wav" : basename(filePath);

  console.error(`Đang transcribe (${(audio.length / 1024 / 1024).toFixed(1)} MB)...`);

  const client = new SonioxNodeClient();
  const transcription = await client.stt.transcribe({
    model: "stt-async-v4",
    file: audio,
    filename,
    wait: true,
    language_hints: [args.lang],
  });

  if (!transcription.transcript) {
    console.error("Lỗi: Không nhận được transcript từ API.");
    process.exit(1);
  }

  const tokens = transcription.transcript.tokens || [];
  const segments = groupTokensIntoSegments(tokens);

  let output;
  switch (args.format) {
    case "srt":
      output = formatSrt(segments);
      break;
    case "text":
      output = formatPlainText(segments);
      break;
    default:
      output = formatTimestamps(segments);
  }

  if (args.output) {
    await writeFile(args.output, output, "utf-8");
    console.error(`Đã lưu transcript vào: ${args.output}`);
  } else {
    console.log(output);
  }

  if (tempFile && existsSync(tempFile)) {
    await unlink(tempFile);
  }
}

main().catch((err) => {
  console.error(`Lỗi: ${err.message}`);
  process.exit(1);
});
