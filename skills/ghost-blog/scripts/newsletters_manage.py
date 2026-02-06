#!/usr/bin/env python3
"""Ghost Admin API newsletters management - list, read, create, update newsletters.

Usage:
    python newsletters_manage.py list [--include-count]
    python newsletters_manage.py get --id NEWSLETTER_ID
    python newsletters_manage.py get --slug NEWSLETTER_SLUG
"""

import argparse
import json
import sys
from typing import Any, Dict, List, Optional

from ghost_core import GhostAPIError, api_request, format_error


def list_newsletters(include_count: bool = False) -> List[Dict[str, Any]]:
    """List all newsletters.

    Args:
        include_count: Include subscriber count in response

    Returns:
        List of newsletter dicts
    """
    params: Dict[str, Any] = {'limit': 'all'}
    if include_count:
        params['include'] = 'count.active_members,count.posts'

    response = api_request('GET', 'newsletters/', params=params)
    return response.get('newsletters', [])


def get_newsletter(newsletter_id: Optional[str] = None,
                   slug: Optional[str] = None) -> Dict[str, Any]:
    """Get a single newsletter by ID or slug.

    Args:
        newsletter_id: Newsletter ID
        slug: Newsletter slug

    Returns:
        Newsletter dict

    Raises:
        GhostAPIError: If newsletter not found or invalid params
    """
    if not newsletter_id and not slug:
        raise GhostAPIError("Must provide either --id or --slug", "ValidationError")

    if newsletter_id:
        endpoint = f'newsletters/{newsletter_id}/'
    else:
        endpoint = f'newsletters/slug/{slug}/'

    response = api_request('GET', endpoint)
    newsletters = response.get('newsletters', [])
    if not newsletters:
        raise GhostAPIError("Newsletter not found", "NotFoundError", 404)
    return newsletters[0]


def format_newsletter_row(newsletter: Dict[str, Any], include_count: bool = False) -> str:
    """Format a newsletter for table display.

    Args:
        newsletter: Newsletter dict
        include_count: Include subscriber/post counts

    Returns:
        Formatted string row
    """
    name = newsletter.get('name', 'Untitled')[:30]
    slug = newsletter.get('slug', '')[:20]
    status = newsletter.get('status', 'unknown')
    visibility = newsletter.get('visibility', 'members')
    subscribe_on_signup = 'Yes' if newsletter.get('subscribe_on_signup') else 'No'

    if include_count:
        count = newsletter.get('count', {})
        active_members = count.get('active_members', 0)
        posts = count.get('posts', 0)
        return f"{name:<30} {slug:<20} {status:<10} {visibility:<10} {subscribe_on_signup:<8} {active_members:>8} {posts:>6}"
    return f"{name:<30} {slug:<20} {status:<10} {visibility:<10} {subscribe_on_signup:<8}"


def format_newsletter_detail(newsletter: Dict[str, Any]) -> str:
    """Format newsletter details for display.

    Args:
        newsletter: Newsletter dict

    Returns:
        Formatted multi-line string
    """
    lines = [
        f"ID: {newsletter.get('id', 'N/A')}",
        f"Name: {newsletter.get('name', 'Untitled')}",
        f"Slug: {newsletter.get('slug', 'N/A')}",
        f"Status: {newsletter.get('status', 'unknown')}",
        f"Visibility: {newsletter.get('visibility', 'members')}",
        f"Subscribe on Signup: {'Yes' if newsletter.get('subscribe_on_signup') else 'No'}",
        f"Sender Name: {newsletter.get('sender_name', 'N/A')}",
        f"Sender Email: {newsletter.get('sender_email', 'N/A')}",
        f"Sender Reply-To: {newsletter.get('sender_reply_to', 'N/A')}",
        f"Sort Order: {newsletter.get('sort_order', 0)}",
    ]

    # Include counts if available
    count = newsletter.get('count', {})
    if count:
        lines.append(f"Active Members: {count.get('active_members', 0)}")
        lines.append(f"Posts: {count.get('posts', 0)}")

    # Timestamps
    if newsletter.get('created_at'):
        lines.append(f"Created: {newsletter['created_at'][:10]}")
    if newsletter.get('updated_at'):
        lines.append(f"Updated: {newsletter['updated_at'][:10]}")

    return "\n".join(lines)


def cmd_list(args: argparse.Namespace) -> int:
    """Handle list command."""
    try:
        newsletters = list_newsletters(include_count=args.include_count)

        if args.json:
            print(json.dumps(newsletters, indent=2))
            return 0

        if not newsletters:
            print("No newsletters found.")
            return 0

        # Print header
        if args.include_count:
            print(f"{'NAME':<30} {'SLUG':<20} {'STATUS':<10} {'VISIBILITY':<10} {'SIGNUP':<8} {'MEMBERS':>8} {'POSTS':>6}")
            print("-" * 102)
        else:
            print(f"{'NAME':<30} {'SLUG':<20} {'STATUS':<10} {'VISIBILITY':<10} {'SIGNUP':<8}")
            print("-" * 88)

        for newsletter in newsletters:
            print(format_newsletter_row(newsletter, include_count=args.include_count))

        print(f"\nTotal: {len(newsletters)} newsletter(s)")
        return 0

    except GhostAPIError as e:
        print(format_error(e), file=sys.stderr)
        return 1


def cmd_get(args: argparse.Namespace) -> int:
    """Handle get command."""
    try:
        newsletter = get_newsletter(newsletter_id=args.id, slug=args.slug)

        if args.json:
            print(json.dumps(newsletter, indent=2))
        else:
            print(format_newsletter_detail(newsletter))
        return 0

    except GhostAPIError as e:
        print(format_error(e), file=sys.stderr)
        return 1


def main() -> int:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(
        description='Manage Ghost newsletters',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python newsletters_manage.py list
  python newsletters_manage.py list --include-count
  python newsletters_manage.py get --id 64f1a2b3c4d5e6f7a8b9c0d1
  python newsletters_manage.py get --slug default-newsletter
'''
    )
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    subparsers = parser.add_subparsers(dest='command', required=True)

    # List command
    list_parser = subparsers.add_parser('list', help='List all newsletters')
    list_parser.add_argument('--include-count', action='store_true',
                             help='Include subscriber and post counts')
    list_parser.set_defaults(func=cmd_list)

    # Get command
    get_parser = subparsers.add_parser('get', help='Get newsletter details')
    get_parser.add_argument('--id', help='Newsletter ID')
    get_parser.add_argument('--slug', help='Newsletter slug')
    get_parser.set_defaults(func=cmd_get)

    args = parser.parse_args()
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
