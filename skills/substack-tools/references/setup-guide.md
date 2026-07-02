# Setup Guide — Cấu hình Substack Tools lần đầu

## Cách 1 — Environment variables (khuyến nghị)

Thêm vào `~/.zshrc` hoặc `~/.bashrc`:

```bash
export SUBSTACK_COOKIE="substack.sid=s%3A..."
export SUBSTACK_PUBLICATION_URL="https://yourname.substack.com"
```

## Cách 2 — File .env

Cài thêm `python-dotenv`:

```bash
uv pip install --python ~/.venv/claude/bin/python python-dotenv
```

Tạo `.env` trong thư mục skill (`skills/substack-tools/.env`) hoặc CWD:

```
SUBSTACK_COOKIE=substack.sid=s%3A...
SUBSTACK_PUBLICATION_URL=https://yourname.substack.com
```

## Lấy cookie

1. Mở Substack dashboard (đã login)
2. F12 → Application → Cookies → `substack.sid`
3. Copy toàn bộ value (bắt đầu `s%3A...`)
4. Cookie hết hạn sau 1-2 tuần — cần lấy lại khi gặp lỗi 400/401
