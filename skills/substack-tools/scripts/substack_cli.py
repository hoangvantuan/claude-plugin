#!/usr/bin/env python3
"""CLI test đăng bài Substack kèm ảnh.

Đăng bài lên Substack (draft / schedule / publish), liệt kê draft/scheduled,
publish bài đã có sẵn. Dùng python-substack (reverse-engineered client).

Chạy:
    ~/.venv/claude/bin/python substack_cli.py <subcommand> [args]

Xem help:
    ~/.venv/claude/bin/python substack_cli.py --help
"""

import sys
sys.dont_write_bytecode = True

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from substack import Api
from substack.post import Post


ENV_COOKIE = "SUBSTACK_COOKIE"
ENV_PUBLICATION = "SUBSTACK_PUBLICATION_URL"

SKILL_DIR = Path(__file__).resolve().parent.parent  # thư mục chứa SKILL.md


def _try_load_dotenv() -> None:
    """Fallback: load .env từ thư mục skill → CWD (chỉ khi env vars chưa có)."""
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    for candidate in [SKILL_DIR / ".env", Path.cwd() / ".env"]:
        if candidate.is_file():
            load_dotenv(candidate, override=False)
            return


def load_env() -> tuple[str, str]:
    cookie = os.getenv(ENV_COOKIE)
    publication = os.getenv(ENV_PUBLICATION)
    if not cookie or not publication:
        _try_load_dotenv()
        cookie = cookie or os.getenv(ENV_COOKIE)
        publication = publication or os.getenv(ENV_PUBLICATION)
    if not cookie:
        sys.exit(f"Thiếu {ENV_COOKIE} — set env var hoặc tạo .env trong thư mục skill/CWD")
    if not publication:
        sys.exit(f"Thiếu {ENV_PUBLICATION} — set env var hoặc tạo .env trong thư mục skill/CWD")
    return cookie, publication.rstrip("/")


def read_article(path: Path) -> tuple[str, str]:
    """Dòng đầu = title, phần còn lại = body markdown."""
    if not path.exists():
        sys.exit(f"Không tìm thấy file bài viết: {path}")
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines:
        sys.exit(f"File bài viết rỗng: {path}")
    title = lines[0].lstrip("#").strip()
    body = "\n".join(lines[1:]).strip()
    if not title:
        sys.exit("Dòng đầu tiên (title) không được rỗng")
    return title, body


def make_api(dry_run: bool) -> Api | None:
    if dry_run:
        return None
    cookie, publication = load_env()
    return Api(cookies_string=cookie, publication_url=publication)


def _fix_prosemirror_nodes(node) -> None:
    """Patch bug của python-substack.Post.from_markdown().

    parse_inline() trả về dict dạng {"content": "...", "marks": [...]} — không
    phải ProseMirror node. Khi dùng cho paragraph thường nó được convert qua
    add_complex_text(), nhưng với bullet_list thì đi thẳng → JSON sai, Substack
    web báo `RangeError: Invalid input for Fragment.fromJSON`.

    Walk toàn bộ cây, convert dict `{"content": str}` không có `type`
    thành text node `{"type": "text", "text": str, ...}`.
    """
    if isinstance(node, dict):
        children = node.get("content")
        if isinstance(children, list):
            for i, child in enumerate(children):
                if (
                    isinstance(child, dict)
                    and "type" not in child
                    and isinstance(child.get("content"), str)
                ):
                    fixed = {"type": "text", "text": child["content"]}
                    marks = child.get("marks")
                    if marks:
                        fixed["marks"] = marks
                    children[i] = fixed
                else:
                    _fix_prosemirror_nodes(child)
    elif isinstance(node, list):
        for child in node:
            _fix_prosemirror_nodes(child)


def fetch_sections(api: Api) -> list[dict]:
    """Lấy danh sách sections của publication hiện tại.

    python-substack.get_sections() gọi `/subscriptions` rồi lọc theo hostname —
    broken: (1) sections trả về [] cho owner, (2) crash khi publication trong
    list có hostname=None. Endpoint đúng là `/api/v1/publication/sections/`
    (capture từ DevTools), trả thẳng list section của publication hiện tại.
    """
    resp = api._session.get(f"{api.publication_url}/publication/sections/")
    if resp.status_code != 200:
        sys.exit(
            f"GET /publication/sections/ lỗi {resp.status_code}: {resp.text[:300]}"
        )
    data = resp.json()
    return data if isinstance(data, list) else []


def resolve_section_id(api: Api, section_name: str) -> int:
    """Match section theo name (case-sensitive), return id."""
    sections = fetch_sections(api)
    for s in sections:
        if s.get("name") == section_name:
            return int(s["id"])
    available = ", ".join(repr(s.get("name")) for s in sections) or "(rỗng)"
    sys.exit(f"Không tìm thấy section {section_name!r}. Có sẵn: {available}")


def apply_section(post: Post, api: Api | None, section_name: str | None) -> None:
    """Gán section cho post nếu có `--section`.

    Dry-run: fake draft_section_id để payload có field này khi in ra.
    Real: match name → id qua endpoint /publication/sections/.
    """
    if not section_name:
        return
    if api is None:
        post.draft_section_id = f"<dry-run:{section_name}>"
        return
    post.draft_section_id = resolve_section_id(api, section_name)


def build_post(
    title: str,
    body: str,
    image_path: Path,
    api: Api | None,
    user_id: int,
    subtitle: str = "",
) -> Post:
    """Tạo Post với ảnh ở đầu (vừa làm cover, vừa inline)."""
    post = Post(title=title, subtitle=subtitle or "", user_id=user_id)

    if not image_path.exists():
        sys.exit(f"Không tìm thấy ảnh: {image_path}")

    image_src: str
    if api is not None:
        uploaded = api.get_image(str(image_path))
        image_src = uploaded.get("url", "")
        if not image_src:
            sys.exit(f"Upload ảnh thất bại: {uploaded}")
    else:
        image_src = f"file://{image_path.resolve()}"

    post.add(
        {
            "type": "captionedImage",
            "src": image_src,
            "alt": image_path.stem,
        }
    )
    post.from_markdown(body, api=api)
    _fix_prosemirror_nodes(post.draft_body)
    return post


def dry_run_user_id() -> int:
    return 0


def print_payload(label: str, payload: dict) -> None:
    print(f"=== [DRY-RUN] {label} ===")
    # draft_body là JSON string -> parse lại để in đẹp
    if "draft_body" in payload and isinstance(payload["draft_body"], str):
        try:
            payload = {**payload, "draft_body": json.loads(payload["draft_body"])}
        except json.JSONDecodeError:
            pass
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def cmd_draft(args: argparse.Namespace) -> None:
    api = make_api(args.dry_run)
    title, body = read_article(Path(args.file))
    user_id = api.get_user_id() if api else dry_run_user_id()
    post = build_post(title, body, Path(args.image), api, user_id, args.subtitle)
    apply_section(post, api, args.section)
    payload = post.get_draft()

    if args.dry_run:
        print_payload("post_draft payload", payload)
        return

    result = api.post_draft(payload)
    print(f"Đã tạo draft id={result.get('id')} title={result.get('draft_title')!r}")


def _format_trigger_at(dt: datetime) -> str:
    """Substack format: 2026-04-23T13:53:00.000Z"""
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def _schedule_draft_raw(api: Api, draft_id: int, dt: datetime, audience: str) -> dict:
    """Gọi endpoint nội bộ /drafts/{id}/scheduled_release (reverse-engineered).

    python-substack.schedule_draft() dùng endpoint cũ /schedule → 404.
    """
    trigger_at = _format_trigger_at(dt)
    resp = api._session.post(
        f"{api.publication_url}/drafts/{draft_id}/scheduled_release",
        json={
            "trigger_at": trigger_at,
            "post_audience": audience,
            "email_audience": audience,
        },
    )
    if resp.status_code != 200:
        sys.exit(f"scheduled_release lỗi {resp.status_code}: {resp.text[:300]}")
    return resp.json()


def _unschedule_draft_raw(api: Api, draft_id: int) -> None:
    resp = api._session.delete(
        f"{api.publication_url}/drafts/{draft_id}/scheduled_release"
    )
    if resp.status_code != 200:
        sys.exit(f"DELETE scheduled_release lỗi {resp.status_code}: {resp.text[:300]}")


def cmd_schedule(args: argparse.Namespace) -> None:
    api = make_api(args.dry_run)
    title, body = read_article(Path(args.file))
    user_id = api.get_user_id() if api else dry_run_user_id()
    post = build_post(title, body, Path(args.image), api, user_id, args.subtitle)
    apply_section(post, api, args.section)
    payload = post.get_draft()

    try:
        dt = datetime.fromisoformat(args.at)
    except ValueError:
        sys.exit("Flag --at cần ISO 8601, ví dụ 2026-04-20T09:00:00")
    if dt.tzinfo is None:
        dt = dt.astimezone()

    if args.dry_run:
        print_payload("post_draft payload (schedule)", payload)
        print(
            f"[DRY-RUN] POST /drafts/<id>/scheduled_release "
            f"trigger_at={_format_trigger_at(dt)} audience={args.audience}"
        )
        return

    draft = api.post_draft(payload)
    draft_id = draft["id"]
    _schedule_draft_raw(api, draft_id, dt, args.audience)
    print(f"Đã schedule draft id={draft_id} tại {_format_trigger_at(dt)}")


def cmd_unschedule(args: argparse.Namespace) -> None:
    if args.dry_run:
        print(f"[DRY-RUN] DELETE /drafts/{args.draft_id}/scheduled_release")
        return
    api = make_api(False)
    _unschedule_draft_raw(api, args.draft_id)
    print(f"Đã huỷ schedule draft id={args.draft_id} (chuyển về draft)")


def safe_prepublish(api: Api, draft_id: int) -> None:
    """prepublish endpoint của Substack flaky (500 random).
    Best-effort, log warning nếu fail, không raise.
    """
    try:
        api.prepublish_draft(draft_id)
    except Exception as e:
        print(f"[warn] prepublish_draft({draft_id}) lỗi, bỏ qua: {e}")


def cmd_publish(args: argparse.Namespace) -> None:
    api = make_api(args.dry_run)
    title, body = read_article(Path(args.file))
    user_id = api.get_user_id() if api else dry_run_user_id()
    post = build_post(title, body, Path(args.image), api, user_id, args.subtitle)
    apply_section(post, api, args.section)
    payload = post.get_draft()

    if args.dry_run:
        print_payload("post_draft payload (publish)", payload)
        print("[DRY-RUN] publish_draft")
        return

    draft = api.post_draft(payload)
    draft_id = draft["id"]
    safe_prepublish(api, draft_id)
    api.publish_draft(draft_id, send=args.send, share_automatically=False)
    print(f"Đã publish draft id={draft_id}")


def cmd_list(args: argparse.Namespace) -> None:
    if args.dry_run:
        print(f"[DRY-RUN] get_drafts(filter={args.filter!r}, limit={args.limit})")
        return

    api = make_api(False)
    # Substack hỗ trợ filter server-side: draft | scheduled | published | None
    server_filter = None if args.filter == "all" else args.filter
    drafts = api.get_drafts(filter=server_filter, offset=0, limit=args.limit)
    items = drafts if isinstance(drafts, list) else drafts.get("drafts", drafts)

    if not items:
        print(f"Không có bài nào với filter={args.filter}")
        return

    for d in items:
        schedules = d.get("postSchedules") or []
        # /drafts list không trả postSchedules — phải fetch detail khi cần
        if not schedules and args.filter == "scheduled" and not d.get("is_published"):
            try:
                full = api.get_draft(d["id"])
                schedules = full.get("postSchedules") or []
            except Exception:
                pass

        if d.get("is_published"):
            status = "published"
            when = d.get("post_date") or "-"
        elif schedules:
            status = "scheduled"
            when = schedules[0].get("trigger_at", "-")
        else:
            status = "draft"
            when = "-"
        title = d.get("draft_title") or d.get("title") or "(no title)"
        print(f"id={d.get('id')}  [{status:9}]  title={title!r}  when={when}")
    print(f"\nTổng: {len(items)} (filter={args.filter})")


def cmd_publish_existing(args: argparse.Namespace) -> None:
    if args.dry_run:
        print(f"[DRY-RUN] publish_draft id={args.draft_id}")
        return

    api = make_api(False)
    safe_prepublish(api, args.draft_id)
    api.publish_draft(args.draft_id, send=args.send, share_automatically=False)
    print(f"Đã publish draft id={args.draft_id}")


def cmd_sections(args: argparse.Namespace) -> None:
    if args.dry_run:
        print("[DRY-RUN] GET /publication/sections/")
        return
    api = make_api(False)
    sections = fetch_sections(api)
    if not sections:
        print("Publication không có section nào.")
        return
    for s in sections:
        sid = s.get("id")
        name = s.get("name") or "(no name)"
        slug = s.get("slug") or "-"
        print(f"id={sid}  name={name!r}  slug={slug}")
    print(f"\nTổng: {len(sections)} section")


def cmd_set_section(args: argparse.Namespace) -> None:
    """Gán section cho nhiều draft có sẵn (kể cả scheduled).

    PUT /drafts/{id} với body {"draft_section_id": <id>} — partial update,
    không đụng body / schedule / metadata khác (verified).
    """
    if args.dry_run:
        print(
            f"[DRY-RUN] resolve section={args.section!r} -> id; "
            f"PUT /drafts/{{id}} draft_section_id=<id> cho {len(args.draft_ids)} bài"
        )
        return

    api = make_api(False)
    section_id = resolve_section_id(api, args.section)
    print(f"Section {args.section!r} → id={section_id}")

    ok, fail = 0, 0
    for did in args.draft_ids:
        resp = api._session.put(
            f"{api.publication_url}/drafts/{did}",
            json={"draft_section_id": section_id},
        )
        if resp.status_code == 200:
            body = resp.json() if "json" in resp.headers.get("content-type", "") else {}
            if body.get("draft_section_id") == section_id:
                print(f"OK  id={did}")
                ok += 1
                continue
        print(f"ERR id={did} status={resp.status_code} body={resp.text[:200]}")
        fail += 1
    print(f"\nTổng: ok={ok} fail={fail}")


def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--dry-run",
        action="store_true",
        help="In payload ra console, không gọi API thật.",
    )

    parser = argparse.ArgumentParser(
        description="CLI test đăng bài Substack kèm ảnh (dùng python-substack).",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    def add_content_args(p: argparse.ArgumentParser) -> None:
        p.add_argument("file", help="Path file markdown (dòng đầu = title)")
        p.add_argument("image", help="Path ảnh dùng làm cover + chèn đầu bài")
        p.add_argument(
            "--section",
            default=None,
            help=(
                "Tên section (newsletter section) để gán bài vào. "
                "Dùng `sections` subcommand để xem danh sách."
            ),
        )
        p.add_argument(
            "--subtitle",
            default="",
            help="Subtitle của bài (hiển thị dưới title trên Substack).",
        )

    p_draft = sub.add_parser("draft", parents=[common], help="Tạo draft từ file")
    add_content_args(p_draft)
    p_draft.set_defaults(func=cmd_draft)

    p_sched = sub.add_parser("schedule", parents=[common], help="Tạo draft + schedule")
    add_content_args(p_sched)
    p_sched.add_argument(
        "--at",
        required=True,
        help="Thời điểm đăng (ISO 8601, ví dụ 2026-04-20T09:00:00)",
    )
    p_sched.add_argument(
        "--audience",
        default="everyone",
        choices=["everyone", "only_paid", "only_free", "founding"],
        help="Đối tượng nhận bài (mặc định everyone)",
    )
    p_sched.set_defaults(func=cmd_schedule)

    p_unsched = sub.add_parser(
        "unschedule", parents=[common], help="Huỷ schedule, chuyển về draft"
    )
    p_unsched.add_argument("draft_id", type=int)
    p_unsched.set_defaults(func=cmd_unschedule)

    p_pub = sub.add_parser("publish", parents=[common], help="Tạo draft + publish ngay")
    add_content_args(p_pub)
    p_pub.add_argument(
        "--no-send",
        dest="send",
        action="store_false",
        help="Không gửi email tới subscriber",
    )
    p_pub.set_defaults(func=cmd_publish, send=True)

    p_list = sub.add_parser("list", parents=[common], help="Liệt kê draft và scheduled")
    p_list.add_argument(
        "--filter",
        choices=["all", "draft", "scheduled", "published"],
        default="draft",
        help="draft (default) | scheduled | published | all",
    )
    p_list.add_argument("--limit", type=int, default=25)
    p_list.set_defaults(func=cmd_list)

    p_pe = sub.add_parser(
        "publish-existing", parents=[common], help="Publish một draft có sẵn"
    )
    p_pe.add_argument("draft_id", type=int, help="Draft id")
    p_pe.add_argument(
        "--no-send",
        dest="send",
        action="store_false",
        help="Không gửi email tới subscriber",
    )
    p_pe.set_defaults(func=cmd_publish_existing, send=True)

    p_sec = sub.add_parser(
        "sections", parents=[common], help="Liệt kê newsletter sections của publication"
    )
    p_sec.set_defaults(func=cmd_sections)

    p_set = sub.add_parser(
        "set-section",
        parents=[common],
        help="Gán section cho 1 hoặc nhiều draft/scheduled có sẵn",
    )
    p_set.add_argument("section", help="Tên section (match chính xác)")
    p_set.add_argument(
        "draft_ids",
        nargs="+",
        type=int,
        help="Một hoặc nhiều draft id",
    )
    p_set.set_defaults(func=cmd_set_section)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
