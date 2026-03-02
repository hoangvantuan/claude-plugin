#!/usr/bin/env python3
"""OpenProject CLI - Single-command entry point for AI Agents.

Usage:
    uv run python op.py status
    uv run python op.py init <project_id>
    uv run python op.py config

    # Work Packages
    uv run python op.py wp list [--status open] [--assignee name] [--limit N]
    uv run python op.py wp get <id>
    uv run python op.py wp create --subject "..." [--type Task] [--assignee "Hung NB"]
    uv run python op.py wp update <id> [--status "In progress"] [--assignee "Tuan HV"]
    uv run python op.py wp delete <id>
    uv run python op.py wp comment <id> --message "..."
    uv run python op.py wp activities <id>
    uv run python op.py wp relations <id>
    uv run python op.py wp add-relation <from_id> <to_id> --type blocks
    uv run python op.py wp del-relation <relation_id>
    uv run python op.py wp schema [--type-id N]

    # Time
    uv run python op.py time log <wp_id> --hours N [--comment "..."] [--date YYYY-MM-DD]
    uv run python op.py time list [--wp N] [--user name] [--date YYYY-MM-DD]
    uv run python op.py time today
    uv run python op.py time get <id>
    uv run python op.py time update <id> [--hours N] [--comment "..."]
    uv run python op.py time delete <id>
    uv run python op.py time activities

    # Projects
    uv run python op.py project list
    uv run python op.py project get <id>
    uv run python op.py project create --name "..."
    uv run python op.py project update <id> [--name "..."]
    uv run python op.py project delete <id>
    uv run python op.py project versions [--id N]
    uv run python op.py project categories [--id N]

    # Notifications
    uv run python op.py notif list [--unread] [--reason mentioned]
    uv run python op.py notif count
    uv run python op.py notif read <id>
    uv run python op.py notif read-all

    # Users
    uv run python op.py user list
    uv run python op.py user get <id>
    uv run python op.py user me

    # Lookups
    uv run python op.py members
    uv run python op.py types
    uv run python op.py statuses
    uv run python op.py priorities
"""

import argparse
import json
import sys
import os

# Auto load .env before anything else
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def _json_out(data, compact=True):
    """Print data as JSON."""
    if compact:
        print(json.dumps(data, ensure_ascii=False, default=str))
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2, default=str))


def _resolve_name_to_id(resolver_fn, name, label="value"):
    """Resolve human name to ID using config helper, exit on failure."""
    result = resolver_fn(name)
    if result is None:
        print(json.dumps({"error": f"{label} not found: '{name}'"}))
        sys.exit(1)
    return result


def _clean_wp(wp):
    """Extract clean fields from a work package dict."""
    from openproject_core import extract_id_from_href
    links = wp.get("_links", {})
    return {
        "id": wp.get("id"),
        "subject": wp.get("subject"),
        "type": links.get("type", {}).get("title"),
        "status": links.get("status", {}).get("title"),
        "priority": links.get("priority", {}).get("title"),
        "assignee": links.get("assignee", {}).get("title"),
        "responsible": links.get("responsible", {}).get("title"),
        "version": links.get("version", {}).get("title"),
        "parent_id": extract_id_from_href(links.get("parent", {}).get("href", "")),
        "start_date": wp.get("startDate"),
        "due_date": wp.get("dueDate"),
        "done_ratio": wp.get("percentageDone"),
        "estimated_hours": wp.get("estimatedTime"),
        "spent_hours": wp.get("spentTime"),
        "created_at": wp.get("createdAt"),
        "updated_at": wp.get("updatedAt"),
        # Include custom fields
        **{k: v for k, v in wp.items() if k.startswith("customField")},
    }


def _clean_time_entry(entry):
    """Extract clean fields from a time entry dict."""
    from openproject_time import parse_duration
    links = entry.get("_links", {})
    return {
        "id": entry.get("id"),
        "hours": parse_duration(entry.get("hours", "")),
        "hours_raw": entry.get("hours"),
        "comment": entry.get("comment", {}).get("raw", ""),
        "spent_on": entry.get("spentOn"),
        "user": links.get("user", {}).get("title"),
        "work_package": links.get("workPackage", {}).get("title"),
        "work_package_id": _extract_wp_id_from_entry(entry),
        "activity": links.get("activity", {}).get("title"),
        "created_at": entry.get("createdAt"),
        "updated_at": entry.get("updatedAt"),
    }


def _extract_wp_id_from_entry(entry):
    """Extract work package ID from time entry."""
    from openproject_core import extract_id_from_href
    href = entry.get("_links", {}).get("workPackage", {}).get("href", "")
    return extract_id_from_href(href)


def _clean_notif(n):
    """Extract clean fields from a notification dict."""
    from openproject_core import extract_id_from_href
    links = n.get("_links", {})
    return {
        "id": n.get("id"),
        "reason": n.get("reason"),
        "read_at": n.get("readIAN"),
        "subject": links.get("resource", {}).get("title"),
        "project": links.get("project", {}).get("title"),
        "actor": links.get("actor", {}).get("title"),
        "resource_id": extract_id_from_href(links.get("resource", {}).get("href", "")),
        "created_at": n.get("createdAt"),
        "updated_at": n.get("updatedAt"),
    }


def _clean_project(p):
    """Extract clean fields from a project dict."""
    return {
        "id": p.get("id"),
        "name": p.get("name"),
        "identifier": p.get("identifier"),
        "description": p.get("description", {}).get("raw", "") if isinstance(p.get("description"), dict) else p.get("description", ""),
        "active": p.get("active"),
        "public": p.get("public"),
        "created_at": p.get("createdAt"),
        "updated_at": p.get("updatedAt"),
    }


def _clean_relation(r):
    """Extract clean fields from a relation dict."""
    from openproject_core import extract_id_from_href
    links = r.get("_links", {})
    return {
        "id": r.get("id"),
        "type": r.get("type"),
        "description": r.get("description"),
        "delay": r.get("lag"),
        "from_id": extract_id_from_href(links.get("from", {}).get("href", "")),
        "from_title": links.get("from", {}).get("title"),
        "to_id": extract_id_from_href(links.get("to", {}).get("href", "")),
        "to_title": links.get("to", {}).get("title"),
    }


def _ensure_config():
    """Ensure config is initialized, exit with helpful message if not."""
    from openproject_core import is_config_initialized
    if not is_config_initialized():
        print(json.dumps({
            "error": "Config not initialized",
            "fix": "Run: uv run python op.py init <project_id>"
        }))
        sys.exit(1)


# ──────────────────────────────────────────────
# Commands: System
# ──────────────────────────────────────────────

def cmd_status(args):
    """Check connection and session status."""
    from openproject_core import is_config_initialized, load_session_config, check_connection

    conn = check_connection()
    if not conn["ok"]:
        _json_out({"ok": False, "error": conn.get("error", "Connection failed")})
        sys.exit(1)

    result = {
        "ok": True,
        "connection": {
            "url": conn["url"],
            "user": conn["user"],
            "login": conn["login"],
            "admin": conn["admin"],
        }
    }

    if is_config_initialized():
        session = load_session_config()
        result["config"] = {
            "project": session.get("project"),
            "project_id": session.get("project_id"),
            "identifier": session.get("identifier"),
            "types_count": session.get("types_count"),
            "members_count": session.get("members_count"),
            "updated_at": session.get("updated_at"),
        }
    else:
        result["config"] = None
        result["hint"] = "Run: uv run python op.py init <project_id>"

    _json_out(result, compact=False)


def cmd_init(args):
    """Initialize or refresh config."""
    from openproject_core import init_config

    config = init_config(args.project_id)
    result = {
        "ok": True,
        "project": config["project"]["name"],
        "project_id": config["project"]["id"],
        "types": len(config.get("types", [])),
        "statuses": len(config.get("statuses", [])),
        "members": len(config.get("members", [])),
        "priorities": len(config.get("priorities", [])),
        "custom_fields": sum(len(v) for v in config.get("custom_fields", {}).values()),
    }
    _json_out(result, compact=False)


def cmd_config(args):
    """Show full config summary."""
    _ensure_config()
    from openproject_core import load_config

    config = load_config()
    summary = {
        "project": config.get("project"),
        "instance": {k: v for k, v in config.get("instance", {}).items() if k != "is_admin"},
        "types": [{"id": t["id"], "name": t["name"]} for t in config.get("types", [])],
        "statuses": [{"id": s["id"], "name": s["name"], "closed": s.get("is_closed")} for s in config.get("statuses", [])],
        "priorities": [{"id": p["id"], "name": p["name"]} for p in config.get("priorities", [])],
        "members": [{"user_id": m["user_id"], "name": m["principal_name"]} for m in config.get("members", [])],
        "custom_fields": config.get("custom_fields"),
        "updated_at": config.get("updated_at"),
    }
    _json_out(summary, compact=False)


# ──────────────────────────────────────────────
# Commands: Work Packages
# ──────────────────────────────────────────────

def cmd_wp_list(args):
    """List work packages."""
    _ensure_config()
    from openproject_core import get_project_id, get_status_id, get_type_id, get_member_id
    from openproject_work_packages import list_work_packages

    project_id = args.project or get_project_id()
    filters = []

    if args.status:
        status_lower = args.status.lower()
        if status_lower == "open":
            filters.append({"status": {"operator": "o", "values": []}})
        elif status_lower == "closed":
            filters.append({"status": {"operator": "c", "values": []}})
        elif status_lower != "all":
            sid = _resolve_name_to_id(get_status_id, args.status, "Status")
            filters.append({"status": {"operator": "=", "values": [str(sid)]}})

    if args.type:
        tid = _resolve_name_to_id(get_type_id, args.type, "Type")
        filters.append({"type": {"operator": "=", "values": [str(tid)]}})

    if args.assignee:
        uid = _resolve_name_to_id(get_member_id, args.assignee, "Assignee")
        filters.append({"assignee": {"operator": "=", "values": [str(uid)]}})

    if args.parent:
        filters.append({"parent": {"operator": "=", "values": [str(args.parent)]}})

    limit = args.limit or 50
    results = []
    for wp in list_work_packages(filters=filters or None, project_id=project_id):
        results.append(_clean_wp(wp))
        if len(results) >= limit:
            break

    _json_out({"count": len(results), "work_packages": results}, compact=False)


def cmd_wp_get(args):
    """Get single work package."""
    from openproject_work_packages import get_work_package
    wp = get_work_package(args.id)
    _json_out(_clean_wp(wp), compact=False)


def cmd_wp_create(args):
    """Create work package."""
    _ensure_config()
    from openproject_core import get_project_id, get_type_id, get_status_id, get_priority_id, get_member_id
    from openproject_work_packages import create_work_package

    project_id = args.project or get_project_id()
    kwargs = {"project_id": project_id, "subject": args.subject}

    if args.type:
        kwargs["type_id"] = _resolve_name_to_id(get_type_id, args.type, "Type")
    if args.status:
        kwargs["status_id"] = _resolve_name_to_id(get_status_id, args.status, "Status")
    if args.priority:
        kwargs["priority_id"] = _resolve_name_to_id(get_priority_id, args.priority, "Priority")
    if args.assignee:
        kwargs["assignee_id"] = _resolve_name_to_id(get_member_id, args.assignee, "Assignee")
    if args.responsible:
        kwargs["responsible_id"] = _resolve_name_to_id(get_member_id, args.responsible, "Responsible")
    if args.description:
        kwargs["description"] = args.description
    if args.parent:
        kwargs["parent_id"] = args.parent
    if args.version:
        kwargs["version_id"] = args.version
    if args.start_date:
        kwargs["start_date"] = args.start_date
    if args.due_date:
        kwargs["due_date"] = args.due_date
    if args.estimated_hours:
        kwargs["estimated_hours"] = args.estimated_hours

    if args.cf:
        for cf_str in args.cf:
            key, val = cf_str.split("=", 1)
            try:
                kwargs[key] = float(val)
            except ValueError:
                kwargs[key] = val

    wp = create_work_package(**kwargs)
    _json_out({"ok": True, "created": _clean_wp(wp)}, compact=False)


def cmd_wp_update(args):
    """Update work package."""
    _ensure_config()
    from openproject_core import get_status_id, get_priority_id, get_member_id, get_type_id
    from openproject_work_packages import update_work_package

    updates = {}

    if args.subject:
        updates["subject"] = args.subject
    if args.status:
        updates["status_id"] = _resolve_name_to_id(get_status_id, args.status, "Status")
    if args.priority:
        updates["priority_id"] = _resolve_name_to_id(get_priority_id, args.priority, "Priority")
    if args.assignee:
        updates["assignee_id"] = _resolve_name_to_id(get_member_id, args.assignee, "Assignee")
    if args.responsible:
        updates["responsible_id"] = _resolve_name_to_id(get_member_id, args.responsible, "Responsible")
    if args.type:
        updates["type_id"] = _resolve_name_to_id(get_type_id, args.type, "Type")
    if args.description:
        updates["description"] = args.description
    if args.parent is not None:
        updates["parent_id"] = args.parent if args.parent != 0 else None
    if args.version is not None:
        updates["version_id"] = args.version if args.version != 0 else None
    if args.start_date:
        updates["start_date"] = args.start_date
    if args.due_date:
        updates["due_date"] = args.due_date
    if args.estimated_hours is not None:
        updates["estimated_hours"] = args.estimated_hours
    if args.done is not None:
        updates["done_ratio"] = args.done

    if args.cf:
        for cf_str in args.cf:
            key, val = cf_str.split("=", 1)
            try:
                updates[key] = float(val)
            except ValueError:
                updates[key] = val

    if not updates:
        print(json.dumps({"error": "No updates specified"}))
        sys.exit(1)

    wp = update_work_package(args.id, **updates)
    _json_out({"ok": True, "updated": _clean_wp(wp)}, compact=False)


def cmd_wp_delete(args):
    """Delete work package."""
    from openproject_work_packages import delete_work_package
    delete_work_package(args.id)
    _json_out({"ok": True, "deleted_id": args.id})


def cmd_wp_comment(args):
    """Add comment to work package."""
    from openproject_work_packages import add_comment
    result = add_comment(args.id, args.message)
    _json_out({"ok": True, "work_package_id": args.id, "comment_id": result.get("id")})


def cmd_wp_activities(args):
    """List work package activities (comments, history)."""
    from openproject_work_packages import list_activities
    results = []
    for a in list_activities(args.id):
        results.append({
            "id": a.get("id"),
            "type": a.get("_type"),
            "comment": a.get("comment", {}).get("raw", "") if isinstance(a.get("comment"), dict) else "",
            "user": a.get("_links", {}).get("user", {}).get("title"),
            "created_at": a.get("createdAt"),
        })
    _json_out({"count": len(results), "work_package_id": args.id, "activities": results}, compact=False)


def cmd_wp_relations(args):
    """List work package relations."""
    from openproject_work_packages import list_relations
    results = [_clean_relation(r) for r in list_relations(args.id)]
    _json_out({"count": len(results), "work_package_id": args.id, "relations": results}, compact=False)


def cmd_wp_add_relation(args):
    """Create relation between work packages."""
    from openproject_work_packages import create_relation
    kwargs = {"from_id": args.from_id, "to_id": args.to_id, "relation_type": args.type}
    if args.description:
        kwargs["description"] = args.description
    if args.delay:
        kwargs["delay"] = args.delay
    result = create_relation(**kwargs)
    _json_out({"ok": True, "created": _clean_relation(result)}, compact=False)


def cmd_wp_del_relation(args):
    """Delete a relation."""
    from openproject_work_packages import delete_relation
    delete_relation(args.relation_id)
    _json_out({"ok": True, "deleted_relation_id": args.relation_id})


def cmd_wp_schema(args):
    """Get work package schema (custom fields, allowed values)."""
    _ensure_config()
    from openproject_core import get_project_id
    from openproject_work_packages import get_schema

    project_id = args.project or get_project_id()
    schema = get_schema(project_id=project_id, type_id=args.type_id)

    # Extract useful info
    fields = {}
    for key, val in schema.items():
        if isinstance(val, dict) and "name" in val:
            fields[key] = {
                "name": val.get("name"),
                "type": val.get("type"),
                "required": val.get("required", False),
                "writable": val.get("writable", True),
            }

    _json_out({"project_id": project_id, "type_id": args.type_id, "fields": fields}, compact=False)


# ──────────────────────────────────────────────
# Commands: Time Tracking
# ──────────────────────────────────────────────

def cmd_time_log(args):
    """Log time entry."""
    from openproject_time import create_time_entry

    kwargs = {"work_package_id": args.wp_id, "hours": args.hours}
    if args.comment:
        kwargs["comment"] = args.comment
    if args.date:
        kwargs["spent_on"] = args.date
    if args.activity:
        kwargs["activity_id"] = args.activity

    entry = create_time_entry(**kwargs)
    _json_out({"ok": True, "created": _clean_time_entry(entry)}, compact=False)


def cmd_time_list(args):
    """List time entries."""
    from openproject_time import list_time_entries, parse_duration
    from openproject_core import get_member_id

    filters = []

    if args.wp:
        filters.append({"entity_type": {"operator": "=", "values": ["WorkPackage"]}})
        filters.append({"entity_id": {"operator": "=", "values": [str(args.wp)]}})

    if args.user:
        uid = _resolve_name_to_id(get_member_id, args.user, "User")
        filters.append({"user": {"operator": "=", "values": [str(uid)]}})

    if args.date:
        filters.append({"spent_on": {"operator": "=", "values": [args.date]}})

    if args.from_date:
        filters.append({"spent_on": {"operator": ">=d", "values": [args.from_date]}})

    if args.to_date:
        filters.append({"spent_on": {"operator": "<=d", "values": [args.to_date]}})

    limit = args.limit or 50
    results = []
    total_hours = 0.0

    for entry in list_time_entries(filters=filters or None):
        cleaned = _clean_time_entry(entry)
        results.append(cleaned)
        total_hours += cleaned["hours"]
        if len(results) >= limit:
            break

    _json_out({
        "count": len(results),
        "total_hours": round(total_hours, 2),
        "entries": results
    }, compact=False)


def cmd_time_today(args):
    """Get today's time entries."""
    from openproject_time import get_user_time_today

    entries = get_user_time_today()
    results = [_clean_time_entry(e) for e in entries]
    total = round(sum(r["hours"] for r in results), 2)

    _json_out({"count": len(results), "total_hours": total, "entries": results}, compact=False)


def cmd_time_get(args):
    """Get single time entry."""
    from openproject_time import get_time_entry
    entry = get_time_entry(args.id)
    _json_out(_clean_time_entry(entry), compact=False)


def cmd_time_update(args):
    """Update time entry."""
    from openproject_time import update_time_entry

    updates = {}
    if args.hours is not None:
        updates["hours"] = args.hours
    if args.comment:
        updates["comment"] = args.comment
    if args.date:
        updates["spent_on"] = args.date
    if args.wp:
        updates["work_package_id"] = args.wp
    if args.activity:
        updates["activity_id"] = args.activity

    if not updates:
        print(json.dumps({"error": "No updates specified"}))
        sys.exit(1)

    entry = update_time_entry(args.id, **updates)
    _json_out({"ok": True, "updated": _clean_time_entry(entry)}, compact=False)


def cmd_time_delete(args):
    """Delete time entry."""
    from openproject_time import delete_time_entry
    delete_time_entry(args.id)
    _json_out({"ok": True, "deleted_id": args.id})


def cmd_time_activities(args):
    """List available time entry activity types."""
    from openproject_time import list_activities
    results = list(list_activities())
    _json_out({"count": len(results), "activities": results}, compact=False)


# ──────────────────────────────────────────────
# Commands: Projects
# ──────────────────────────────────────────────

def cmd_project_list(args):
    """List all projects."""
    from openproject_projects import list_projects

    results = []
    for p in list_projects():
        results.append(_clean_project(p))

    _json_out({"count": len(results), "projects": results}, compact=False)


def cmd_project_get(args):
    """Get single project."""
    from openproject_projects import get_project
    p = get_project(args.id)
    _json_out(_clean_project(p), compact=False)


def cmd_project_create(args):
    """Create project."""
    from openproject_projects import create_project

    kwargs = {"name": args.name}
    if args.identifier:
        kwargs["identifier"] = args.identifier
    if args.description:
        kwargs["description"] = args.description
    if args.parent:
        kwargs["parent_id"] = args.parent
    if args.public:
        kwargs["public"] = True

    p = create_project(**kwargs)
    _json_out({"ok": True, "created": _clean_project(p)}, compact=False)


def cmd_project_update(args):
    """Update project."""
    from openproject_projects import update_project

    updates = {}
    if args.name:
        updates["name"] = args.name
    if args.description:
        updates["description"] = args.description
    if args.active is not None:
        updates["active"] = args.active

    if not updates:
        print(json.dumps({"error": "No updates specified"}))
        sys.exit(1)

    p = update_project(args.id, **updates)
    _json_out({"ok": True, "updated": _clean_project(p)}, compact=False)


def cmd_project_delete(args):
    """Delete project."""
    from openproject_projects import delete_project
    delete_project(args.id)
    _json_out({"ok": True, "deleted_id": args.id})


def cmd_project_versions(args):
    """List project versions."""
    _ensure_config()
    from openproject_core import get_project_id
    from openproject_projects import get_versions

    project_id = args.id or get_project_id()
    results = []
    for v in get_versions(project_id):
        results.append({
            "id": v.get("id"),
            "name": v.get("name"),
            "status": v.get("status"),
            "start_date": v.get("startDate"),
            "end_date": v.get("endDate"),
        })

    _json_out({"count": len(results), "versions": results}, compact=False)


def cmd_project_categories(args):
    """List project categories."""
    _ensure_config()
    from openproject_core import get_project_id
    from openproject_projects import get_categories

    project_id = args.id or get_project_id()
    results = [{"id": c.get("id"), "name": c.get("name")} for c in get_categories(project_id)]
    _json_out({"count": len(results), "categories": results}, compact=False)


# ──────────────────────────────────────────────
# Commands: Notifications
# ──────────────────────────────────────────────

def cmd_notif_list(args):
    """List notifications."""
    from openproject_notifications import list_notifications

    kwargs = {}
    if args.unread:
        kwargs["read_status"] = False
    if args.reason:
        kwargs["reason"] = args.reason

    limit = args.limit or 20
    results = []
    for n in list_notifications(**kwargs):
        results.append(_clean_notif(n))
        if len(results) >= limit:
            break

    _json_out({"count": len(results), "notifications": results}, compact=False)


def cmd_notif_count(args):
    """Get unread notification count."""
    from openproject_notifications import get_unread_count
    count = get_unread_count()
    _json_out({"unread_count": count})


def cmd_notif_read(args):
    """Mark notification as read."""
    from openproject_notifications import mark_read
    mark_read(args.id)
    _json_out({"ok": True, "marked_read": args.id})


def cmd_notif_unread(args):
    """Mark notification as unread."""
    from openproject_notifications import mark_unread
    mark_unread(args.id)
    _json_out({"ok": True, "marked_unread": args.id})


def cmd_notif_read_all(args):
    """Mark all notifications as read."""
    from openproject_notifications import mark_all_read
    mark_all_read()
    _json_out({"ok": True, "all_marked_read": True})


# ──────────────────────────────────────────────
# Commands: Users
# ──────────────────────────────────────────────

def cmd_user_list(args):
    """List users."""
    from openproject_users import list_users

    results = []
    limit = args.limit or 50
    for u in list_users():
        results.append({
            "id": u.get("id"),
            "login": u.get("login"),
            "name": f"{u.get('firstName', '')} {u.get('lastName', '')}".strip(),
            "email": u.get("email"),
            "admin": u.get("admin"),
            "status": u.get("status"),
        })
        if len(results) >= limit:
            break

    _json_out({"count": len(results), "users": results}, compact=False)


def cmd_user_get(args):
    """Get single user."""
    from openproject_users import get_user
    u = get_user(args.id)
    _json_out({
        "id": u.get("id"),
        "login": u.get("login"),
        "name": f"{u.get('firstName', '')} {u.get('lastName', '')}".strip(),
        "email": u.get("email"),
        "admin": u.get("admin"),
        "status": u.get("status"),
        "created_at": u.get("createdAt"),
        "updated_at": u.get("updatedAt"),
    }, compact=False)


def cmd_user_me(args):
    """Get current user."""
    from openproject_users import get_current_user
    u = get_current_user()
    _json_out({
        "id": u.get("id"),
        "login": u.get("login"),
        "name": f"{u.get('firstName', '')} {u.get('lastName', '')}".strip(),
        "email": u.get("email"),
        "admin": u.get("admin"),
    }, compact=False)


# ──────────────────────────────────────────────
# Commands: Lookups (from config cache)
# ──────────────────────────────────────────────

def cmd_members(args):
    """List project members."""
    _ensure_config()
    from openproject_core import load_config

    config = load_config()
    members = [{
        "user_id": m.get("user_id"),
        "name": m.get("principal_name"),
        "roles": [r.get("title") for r in m.get("roles", [])],
    } for m in config.get("members", [])]

    _json_out({"count": len(members), "members": members}, compact=False)


def cmd_types(args):
    """List work package types."""
    _ensure_config()
    from openproject_core import load_config

    config = load_config()
    types = [{"id": t["id"], "name": t["name"], "color": t.get("color"), "is_milestone": t.get("is_milestone")}
             for t in config.get("types", [])]

    _json_out({"count": len(types), "types": types}, compact=False)


def cmd_statuses(args):
    """List statuses."""
    _ensure_config()
    from openproject_core import load_config

    config = load_config()
    statuses = [{"id": s["id"], "name": s["name"], "is_closed": s.get("is_closed"), "is_default": s.get("is_default")}
                for s in config.get("statuses", [])]

    _json_out({"count": len(statuses), "statuses": statuses}, compact=False)


def cmd_priorities(args):
    """List priorities."""
    _ensure_config()
    from openproject_core import load_config

    config = load_config()
    priorities = [{"id": p["id"], "name": p["name"], "is_default": p.get("is_default")}
                  for p in config.get("priorities", [])]

    _json_out({"count": len(priorities), "priorities": priorities}, compact=False)


# ──────────────────────────────────────────────
# Argument Parser
# ──────────────────────────────────────────────

def build_parser():
    parser = argparse.ArgumentParser(prog="op", description="OpenProject CLI for AI Agents")
    sub = parser.add_subparsers(dest="command", help="Available commands")

    # ── System ──
    sub.add_parser("status", help="Check connection and session status")

    p_init = sub.add_parser("init", help="Initialize config for a project")
    p_init.add_argument("project_id", type=int, help="Project ID (numeric)")

    sub.add_parser("config", help="Show full config summary")

    # ── wp ──
    p_wp = sub.add_parser("wp", help="Work package operations")
    wp_sub = p_wp.add_subparsers(dest="wp_command", help="WP sub-commands")

    # wp list
    p = wp_sub.add_parser("list", help="List work packages")
    p.add_argument("--project", type=int, help="Project ID (default: configured)")
    p.add_argument("--status", help="Filter: status name or 'open'/'closed'/'all'")
    p.add_argument("--type", help="Filter: type name (Task, Bug, etc.)")
    p.add_argument("--assignee", help="Filter: assignee name")
    p.add_argument("--parent", type=int, help="Filter: parent WP ID")
    p.add_argument("--limit", type=int, default=50, help="Max results (default: 50)")

    # wp get
    p = wp_sub.add_parser("get", help="Get work package by ID")
    p.add_argument("id", type=int)

    # wp create
    p = wp_sub.add_parser("create", help="Create work package")
    p.add_argument("--subject", required=True, help="Title (required)")
    p.add_argument("--project", type=int, help="Project ID")
    p.add_argument("--type", help="Type name")
    p.add_argument("--status", help="Status name")
    p.add_argument("--priority", help="Priority name")
    p.add_argument("--assignee", help="Assignee name")
    p.add_argument("--responsible", help="Responsible person name")
    p.add_argument("--description", help="Description")
    p.add_argument("--parent", type=int, help="Parent WP ID")
    p.add_argument("--version", type=int, help="Version/sprint ID")
    p.add_argument("--start-date", help="Start date (YYYY-MM-DD)")
    p.add_argument("--due-date", help="Due date (YYYY-MM-DD)")
    p.add_argument("--estimated-hours", type=float, help="Estimated hours")
    p.add_argument("--cf", action="append", help="Custom field: key=value")

    # wp update
    p = wp_sub.add_parser("update", help="Update work package")
    p.add_argument("id", type=int)
    p.add_argument("--subject", help="New subject")
    p.add_argument("--status", help="New status name")
    p.add_argument("--priority", help="New priority name")
    p.add_argument("--type", help="New type name")
    p.add_argument("--assignee", help="New assignee name")
    p.add_argument("--responsible", help="New responsible name")
    p.add_argument("--description", help="New description")
    p.add_argument("--parent", type=int, help="Parent WP ID (0 to unset)")
    p.add_argument("--version", type=int, help="Version ID (0 to unset)")
    p.add_argument("--start-date", help="Start date")
    p.add_argument("--due-date", help="Due date")
    p.add_argument("--estimated-hours", type=float, help="Estimated hours")
    p.add_argument("--done", type=int, help="Percentage done (0-100)")
    p.add_argument("--cf", action="append", help="Custom field: key=value")

    # wp delete
    p = wp_sub.add_parser("delete", help="Delete work package")
    p.add_argument("id", type=int)

    # wp comment
    p = wp_sub.add_parser("comment", help="Add comment to work package")
    p.add_argument("id", type=int)
    p.add_argument("--message", required=True, help="Comment text")

    # wp activities
    p = wp_sub.add_parser("activities", help="List WP activities (comments, history)")
    p.add_argument("id", type=int)

    # wp relations
    p = wp_sub.add_parser("relations", help="List WP relations")
    p.add_argument("id", type=int)

    # wp add-relation
    p = wp_sub.add_parser("add-relation", help="Create relation between WPs")
    p.add_argument("from_id", type=int, help="Source WP ID")
    p.add_argument("to_id", type=int, help="Target WP ID")
    p.add_argument("--type", required=True, help="Relation type: relates|blocks|blocked|precedes|follows|duplicates|includes|partof|requires")
    p.add_argument("--description", help="Description")
    p.add_argument("--delay", type=int, help="Days delay (for precedes/follows)")

    # wp del-relation
    p = wp_sub.add_parser("del-relation", help="Delete a relation")
    p.add_argument("relation_id", type=int)

    # wp schema
    p = wp_sub.add_parser("schema", help="Get form schema (custom fields, allowed values)")
    p.add_argument("--type-id", type=int, required=True, help="Type ID")
    p.add_argument("--project", type=int, help="Project ID")

    # ── time ──
    p_time = sub.add_parser("time", help="Time entry operations")
    time_sub = p_time.add_subparsers(dest="time_command", help="Time sub-commands")

    # time log
    p = time_sub.add_parser("log", help="Log time entry")
    p.add_argument("wp_id", type=int, help="Work package ID")
    p.add_argument("--hours", type=float, required=True, help="Hours spent")
    p.add_argument("--comment", help="Description of work")
    p.add_argument("--date", help="Date (YYYY-MM-DD, default: today)")
    p.add_argument("--activity", type=int, help="Activity type ID")

    # time list
    p = time_sub.add_parser("list", help="List time entries")
    p.add_argument("--wp", type=int, help="Filter: work package ID")
    p.add_argument("--user", help="Filter: user name")
    p.add_argument("--date", help="Filter: exact date (YYYY-MM-DD)")
    p.add_argument("--from-date", help="Filter: from date")
    p.add_argument("--to-date", help="Filter: to date")
    p.add_argument("--limit", type=int, default=50, help="Max results")

    # time today
    time_sub.add_parser("today", help="Today's time entries for current user")

    # time get
    p = time_sub.add_parser("get", help="Get time entry by ID")
    p.add_argument("id", type=int)

    # time update
    p = time_sub.add_parser("update", help="Update time entry")
    p.add_argument("id", type=int)
    p.add_argument("--hours", type=float, help="New hours")
    p.add_argument("--comment", help="New comment")
    p.add_argument("--date", help="New date")
    p.add_argument("--wp", type=int, help="Move to different WP")
    p.add_argument("--activity", type=int, help="New activity type ID")

    # time delete
    p = time_sub.add_parser("delete", help="Delete time entry")
    p.add_argument("id", type=int)

    # time activities
    time_sub.add_parser("activities", help="List available activity types")

    # ── project ──
    p_proj = sub.add_parser("project", help="Project operations")
    proj_sub = p_proj.add_subparsers(dest="project_command", help="Project sub-commands")

    # project list
    proj_sub.add_parser("list", help="List all projects")

    # project get
    p = proj_sub.add_parser("get", help="Get project by ID")
    p.add_argument("id", type=int)

    # project create
    p = proj_sub.add_parser("create", help="Create project")
    p.add_argument("--name", required=True, help="Project name")
    p.add_argument("--identifier", help="URL-friendly identifier")
    p.add_argument("--description", help="Description")
    p.add_argument("--parent", type=int, help="Parent project ID")
    p.add_argument("--public", action="store_true", help="Make public")

    # project update
    p = proj_sub.add_parser("update", help="Update project")
    p.add_argument("id", type=int)
    p.add_argument("--name", help="New name")
    p.add_argument("--description", help="New description")
    p.add_argument("--active", type=bool, help="Active status")

    # project delete
    p = proj_sub.add_parser("delete", help="Delete project")
    p.add_argument("id", type=int)

    # project versions
    p = proj_sub.add_parser("versions", help="List project versions")
    p.add_argument("--id", type=int, help="Project ID (default: configured)")

    # project categories
    p = proj_sub.add_parser("categories", help="List project categories")
    p.add_argument("--id", type=int, help="Project ID (default: configured)")

    # ── notif ──
    p_notif = sub.add_parser("notif", help="Notification operations")
    notif_sub = p_notif.add_subparsers(dest="notif_command", help="Notification sub-commands")

    # notif list
    p = notif_sub.add_parser("list", help="List notifications")
    p.add_argument("--unread", action="store_true", help="Only unread")
    p.add_argument("--reason", help="Filter: mentioned|assigned|watched|responsible|commented|created")
    p.add_argument("--limit", type=int, default=20, help="Max results")

    # notif count
    notif_sub.add_parser("count", help="Get unread notification count")

    # notif read
    p = notif_sub.add_parser("read", help="Mark notification as read")
    p.add_argument("id", type=int)

    # notif unread
    p = notif_sub.add_parser("unread", help="Mark notification as unread")
    p.add_argument("id", type=int)

    # notif read-all
    notif_sub.add_parser("read-all", help="Mark all notifications as read")

    # ── user ──
    p_user = sub.add_parser("user", help="User operations")
    user_sub = p_user.add_subparsers(dest="user_command", help="User sub-commands")

    # user list
    p = user_sub.add_parser("list", help="List users")
    p.add_argument("--limit", type=int, default=50, help="Max results")

    # user get
    p = user_sub.add_parser("get", help="Get user by ID")
    p.add_argument("id", type=int)

    # user me
    user_sub.add_parser("me", help="Get current user info")

    # ── Lookup commands (shortcuts) ──
    sub.add_parser("members", help="List project members (from config)")
    sub.add_parser("types", help="List work package types (from config)")
    sub.add_parser("statuses", help="List all statuses (from config)")
    sub.add_parser("priorities", help="List all priorities (from config)")

    return parser


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        cmd_map = {
            "status": cmd_status,
            "init": cmd_init,
            "config": cmd_config,
            "members": cmd_members,
            "types": cmd_types,
            "statuses": cmd_statuses,
            "priorities": cmd_priorities,
        }

        if args.command in cmd_map:
            cmd_map[args.command](args)

        elif args.command == "wp":
            wp_map = {
                "list": cmd_wp_list,
                "get": cmd_wp_get,
                "create": cmd_wp_create,
                "update": cmd_wp_update,
                "delete": cmd_wp_delete,
                "comment": cmd_wp_comment,
                "activities": cmd_wp_activities,
                "relations": cmd_wp_relations,
                "add-relation": cmd_wp_add_relation,
                "del-relation": cmd_wp_del_relation,
                "schema": cmd_wp_schema,
            }
            if not args.wp_command:
                print(json.dumps({"error": "Specify wp sub-command: " + "|".join(wp_map.keys())}))
                sys.exit(1)
            wp_map[args.wp_command](args)

        elif args.command == "time":
            time_map = {
                "log": cmd_time_log,
                "list": cmd_time_list,
                "today": cmd_time_today,
                "get": cmd_time_get,
                "update": cmd_time_update,
                "delete": cmd_time_delete,
                "activities": cmd_time_activities,
            }
            if not args.time_command:
                print(json.dumps({"error": "Specify time sub-command: " + "|".join(time_map.keys())}))
                sys.exit(1)
            time_map[args.time_command](args)

        elif args.command == "project":
            proj_map = {
                "list": cmd_project_list,
                "get": cmd_project_get,
                "create": cmd_project_create,
                "update": cmd_project_update,
                "delete": cmd_project_delete,
                "versions": cmd_project_versions,
                "categories": cmd_project_categories,
            }
            if not args.project_command:
                print(json.dumps({"error": "Specify project sub-command: " + "|".join(proj_map.keys())}))
                sys.exit(1)
            proj_map[args.project_command](args)

        elif args.command == "notif":
            notif_map = {
                "list": cmd_notif_list,
                "count": cmd_notif_count,
                "read": cmd_notif_read,
                "unread": cmd_notif_unread,
                "read-all": cmd_notif_read_all,
            }
            if not args.notif_command:
                print(json.dumps({"error": "Specify notif sub-command: " + "|".join(notif_map.keys())}))
                sys.exit(1)
            notif_map[args.notif_command](args)

        elif args.command == "user":
            user_map = {
                "list": cmd_user_list,
                "get": cmd_user_get,
                "me": cmd_user_me,
            }
            if not args.user_command:
                print(json.dumps({"error": "Specify user sub-command: " + "|".join(user_map.keys())}))
                sys.exit(1)
            user_map[args.user_command](args)

        else:
            parser.print_help()
            sys.exit(1)

    except Exception as e:
        error_type = type(e).__name__
        _json_out({"error": str(e), "type": error_type})
        sys.exit(1)


if __name__ == "__main__":
    main()
