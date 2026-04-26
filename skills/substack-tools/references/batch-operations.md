# Batch Operations — Schedule nhiều bài

## Vấn đề

Chạy nhiều CLI call liên tiếp không delay → dính 429 sau ~7 call. Cooldown ~90s. Chạy có delay 6-8s + retry vẫn phải retry vài bài giữa chừng.

## Pattern khuyến nghị

```bash
#!/bin/bash
PY=~/.venv/claude/bin/python
SCRIPT=<path-to>/substack_cli.py

run_one() {
  local path="$1" cover="$2" at="$3" label="$4"
  for attempt in 1 2 3 4 5; do
    if $PY $SCRIPT schedule "$path" "$cover" --at "$at"; then
      return 0
    fi
    echo "[$label] retry $attempt sau 60s"
    sleep 60
  done
  echo "[$label] FAILED"
  return 1
}

run_one "bai-1.md" "cover-1.png" "2026-04-16T09:00:00+07:00" "1"
sleep 8
run_one "bai-2.md" "cover-2.png" "2026-04-17T09:00:00+07:00" "2"
sleep 8
# ... tiếp tục
```

## Lưu ý quan trọng

1. **Không sửa `substack_cli.py` khi batch đang chạy**: mỗi subprocess đọc file mới. Sửa dở giữa chừng → `AttributeError` fail hàng loạt.
2. **Log ra file**: `2>&1 | tee batch.log` — batch dài dễ mất output nếu terminal scroll.
3. **Verify sau batch**: `$PY $SCRIPT list --filter scheduled` — check đúng số lượng. 429 có thể khiến 1-2 bài rơi mà script không nhận ra.
4. **Delay tối thiểu 8s** giữa mỗi call để giảm xác suất 429.
5. **Retry tối đa 5 lần**, mỗi lần chờ 60s — đủ cho cooldown rate limit.
6. **`list --limit` tối đa 25**: Substack API reject limit > 25 với status 400.
