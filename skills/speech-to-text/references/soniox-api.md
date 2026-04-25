# Soniox Node SDK: API Reference

Tài liệu tham khảo cho Soniox Node SDK (`@soniox/node`).

## Mục lục

1. [Client khởi tạo](#client-khởi-tạo)
2. [Async Transcription](#async-transcription)
3. [Files API](#files-api)
4. [Audio formats](#audio-formats)
5. [Models](#models)
6. [Language codes](#language-codes)

## Client khởi tạo

```javascript
import { SonioxNodeClient } from "@soniox/node";
const client = new SonioxNodeClient();
```

Biến môi trường:

| Biến | Mô tả | Bắt buộc |
|------|--------|----------|
| `SONIOX_API_KEY` | API key xác thực | Có |
| `SONIOX_REGION` | Region: `us` (mặc định), `eu`, `jp` | Không |
| `SONIOX_BASE_DOMAIN` | Custom domain | Không |

Thứ tự ưu tiên: explicit options > biến môi trường > base_domain > region > US mặc định.

## Async Transcription

### Transcribe từ file local

```javascript
import { SonioxNodeClient } from "@soniox/node";
import { readFile } from "node:fs/promises";

const client = new SonioxNodeClient();
const audio = await readFile("audio.mp3");

const transcription = await client.stt.transcribe({
  model: "stt-async-v4",
  file: audio,
  filename: "audio.mp3",
  wait: true,
});

console.log(transcription.transcript?.text);
```

### Transcribe từ URL

```javascript
const transcription = await client.stt.transcribe({
  model: "stt-async-v4",
  audio_url: "https://example.com/audio.mp3",
  wait: true,
});
```

### Options cho `client.stt.transcribe()`

| Option | Kiểu | Mô tả |
|--------|------|--------|
| `model` | string | Model dùng. Mặc định `stt-async-v4` |
| `file` | Buffer | Audio data (dùng khi upload file local) |
| `filename` | string | Tên file (giúp detect format) |
| `audio_url` | string | URL public của audio |
| `wait` | boolean | `true` = chờ hoàn thành, `false` = trả job ID |
| `language_hints` | string[] | Gợi ý ngôn ngữ, ví dụ `["vi", "en"]` |
| `context` | object | Context bổ sung cho accuracy |
| `client_reference_id` | string | ID tracking tùy chỉnh |

### Transcription result

```javascript
{
  id: "txn_abc123",
  status: "completed",
  transcript: {
    text: "Xin chào các bạn...",
    tokens: [
      {
        text: "Xin",
        start_ms: 0,
        end_ms: 250,
        is_final: true,
        language: "vi"
      },
      // ...
    ]
  }
}
```

Mỗi token có:

| Field | Kiểu | Mô tả |
|-------|------|--------|
| `text` | string | Nội dung text |
| `start_ms` | number | Thời điểm bắt đầu (ms) |
| `end_ms` | number | Thời điểm kết thúc (ms) |
| `is_final` | boolean | Token đã xác nhận hay chưa |
| `language` | string | Mã ngôn ngữ phát hiện |

### Quản lý transcription

```javascript
// Chờ hoàn thành (nếu wait: false)
const result = await client.stt.wait(transcription.id);

// Lấy thông tin
const info = await client.stt.get(transcription.id);

// Xóa
await transcription.delete();
```

## Files API

```javascript
// Upload file
const file = await client.files.upload(audioBuffer, {
  filename: "recording.mp3"
});

// Transcribe từ file đã upload
const transcription = await client.stt.transcribe({
  model: "stt-async-v4",
  file_id: file.id,
  wait: true,
});

// List files
const files = await client.files.list();

// Xóa file
await client.files.delete(file.id);
```

## Audio formats

Soniox tự phát hiện encoding cho các format sau:

**Container formats**: aac, aiff, amr, asf, flac, mp3, ogg, wav, webm, m4a, mp4

**Raw audio** (cần chỉ định thủ công): pcm_s16le, pcm_s16be, pcm_u8, pcm_f32le, mulaw, alaw

## Models

| Model | Mô tả |
|-------|--------|
| `stt-async-v4` | Model async mới nhất, accuracy cao nhất |
| `stt-rt-v4` | Model real-time, latency thấp |

## Language codes

Soniox hỗ trợ 60+ ngôn ngữ. Một số mã phổ biến:

| Mã | Ngôn ngữ |
|----|----------|
| `vi` | Tiếng Việt |
| `en` | Tiếng Anh |
| `zh` | Tiếng Trung |
| `ja` | Tiếng Nhật |
| `ko` | Tiếng Hàn |
| `fr` | Tiếng Pháp |
| `de` | Tiếng Đức |
| `es` | Tiếng Tây Ban Nha |
| `th` | Tiếng Thái |

Dùng `language_hints` để cải thiện accuracy khi biết trước ngôn ngữ.
