---
name: speech-to-text
description: >
  Chuyển đổi file audio/video thành văn bản (speech-to-text) qua Soniox API.
  Hỗ trợ audio (mp3, wav, flac, ogg, aac, m4a) và video (mp4, webm, mov, mkv, avi).
  Video format ngoài mp4/webm sẽ tự trích xuất audio bằng ffmpeg.
  Output là text kèm timestamps theo từng đoạn.
  Sử dụng skill này khi user muốn: transcribe audio/video, chuyển giọng nói thành text,
  lấy nội dung từ file ghi âm, trích xuất lời nói từ podcast/cuộc họp/phỏng vấn/video,
  hoặc bất kỳ yêu cầu nào liên quan đến chuyển đổi audio/video sang văn bản.
---

# Speech-to-Text (Soniox)

Transcribe file audio/video thành text kèm timestamps qua Soniox async API.

## Yêu cầu

- **API key**: Biến môi trường `SONIOX_API_KEY` phải được set. Nếu chưa có, hướng dẫn user tạo tài khoản tại https://console.soniox.com và lấy API key.
- **Node.js**: Cần Node.js >= 18.
- **Package**: `@soniox/node` (đã khai báo trong `scripts/package.json`).
- **ffmpeg** (tùy chọn): Cần khi transcribe file video. Script trích xuất audio trước khi gửi API để giảm dung lượng upload. Cài bằng `brew install ffmpeg`.

## Workflow

### Bước 1: Kiểm tra điều kiện

Kiểm tra `SONIOX_API_KEY` đã set chưa:

```bash
echo $SONIOX_API_KEY
```

Nếu chưa có, yêu cầu user tạo tài khoản tại https://console.soniox.com, lấy API key và set:

```bash
export SONIOX_API_KEY=<key>
```

Cài dependency (chỉ cần chạy lần đầu):

```bash
cd skills/speech-to-text/scripts && npm install && cd -
```

### Bước 2: Chạy transcription

Chạy script transcribe với đường dẫn file audio hoặc video:

```bash
node skills/speech-to-text/scripts/transcribe.js <đường-dẫn-file>
```

Script hỗ trợ các option:

| Flag       | Mô tả                                         | Mặc định     |
| ---------- | --------------------------------------------- | ------------ |
| `--lang`   | Gợi ý ngôn ngữ (mã ISO 639-1)                 | `vi`         |
| `--output` | Đường dẫn file output                         | stdout       |
| `--format` | Định dạng output: `text`, `timestamps`, `srt` | `timestamps` |

**Ví dụ:**

```bash
# Transcribe file audio tiếng Việt
node skills/speech-to-text/scripts/transcribe.js recording.mp3

# Transcribe video (mp4 gửi trực tiếp, mov/mkv/avi trích xuất audio qua ffmpeg)
node skills/speech-to-text/scripts/transcribe.js lecture.mp4 --output transcript.txt
node skills/speech-to-text/scripts/transcribe.js meeting.mov --lang en --output notes.txt

# Xuất ra định dạng SRT (phụ đề)
node skills/speech-to-text/scripts/transcribe.js podcast.mp3 --format srt --output subtitle.srt
```

### Bước 3: Xử lý kết quả

Script trả về text kèm timestamps dạng:

```
[00:00.000 -> 00:03.500] Xin chào các bạn, hôm nay chúng ta sẽ nói về AI.
[00:03.500 -> 00:07.200] Đây là một chủ đề rất thú vị trong thời đại hiện nay.
```

Nếu user cần, có thể chuyển đổi sang các format khác (markdown, SRT, plain text) từ output này.

## Format hỗ trợ

**Audio** (gửi trực tiếp cho Soniox): aac, aiff, amr, asf, flac, mp3, ogg, wav, m4a

**Video** (trích xuất audio bằng ffmpeg trước khi gửi): mp4, webm, mov, mkv, avi, flv, wmv, ts, mts, 3gp

## Xử lý lỗi thường gặp

| Lỗi                      | Nguyên nhân               | Cách xử lý                          |
| ------------------------ | ------------------------- | ----------------------------------- |
| `SONIOX_API_KEY not set` | Chưa set biến môi trường  | `export SONIOX_API_KEY=<key>`       |
| `File not found`         | Đường dẫn file sai        | Kiểm tra lại path                   |
| `Unsupported format`     | Format audio không hỗ trợ | Convert sang mp3/wav trước          |
| `ffmpeg chưa được cài`   | Video format cần ffmpeg   | `brew install ffmpeg`               |
| `API error 401`          | API key không hợp lệ      | Kiểm tra key tại console.soniox.com |
| `API error 429`          | Vượt rate limit           | Chờ vài giây rồi thử lại            |

## Tham khảo

Chi tiết API và các option nâng cao, đọc: `skills/speech-to-text/references/soniox-api.md`
