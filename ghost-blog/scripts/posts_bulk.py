#!/usr/bin/env python3
"""Bulk operations for Ghost blog posts.

Provides batch operations: publish, unpublish, add-tag, remove-tag, set-featured.
Safety: Preview mode by default, requires --execute to apply changes.

Usage:
    # Preview publish (default - no changes)
    python posts_bulk.py publish --filter "status:draft"

    # Execute publish
    python posts_bulk.py publish --filter "status:draft" --execute

    # Add tag to published posts
    python posts_bulk.py add-tag --filter "status:published" --tag "archive" --execute
"""

import argparse
import sys
import time
from typing import Callable, Dict, List

from ghost_core import api_request, format_error, GhostAPIError, paginate


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description='Bulk operations for Ghost blog posts',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s publish --filter "status:draft"
  %(prog)s publish --filter "status:draft" --execute
  %(prog)s add-tag --filter "status:published" --tag "archive" --execute
  %(prog)s remove-tag --ids "id1,id2,id3" --tag "old" --execute
        '''
    )
    parser.add_argument('--execute', action='store_true',
                        help='Apply changes (default: preview only)')
    parser.add_argument('--delay', type=int, default=100,
                        help='Delay between requests in ms (default: 100)')

    subparsers = parser.add_subparsers(dest='command', required=True)

    # PUBLISH subcommand
    pub_p = subparsers.add_parser('publish', help='Bulk publish drafts')
    pub_p.add_argument('--filter', help='NQL filter (e.g., "status:draft")')
    pub_p.add_argument('--ids', help='Comma-separated post IDs')

    # UNPUBLISH subcommand
    unpub_p = subparsers.add_parser('unpublish', help='Bulk unpublish posts')
    unpub_p.add_argument('--filter', help='NQL filter')
    unpub_p.add_argument('--ids', help='Comma-separated post IDs')

    # ADD-TAG subcommand
    add_tag_p = subparsers.add_parser('add-tag', help='Add tag to posts')
    add_tag_p.add_argument('--filter', help='NQL filter')
    add_tag_p.add_argument('--ids', help='Comma-separated post IDs')
    add_tag_p.add_argument('--tag', required=True, help='Tag to add')

    # REMOVE-TAG subcommand
    rm_tag_p = subparsers.add_parser('remove-tag', help='Remove tag from posts')
    rm_tag_p.add_argument('--filter', help='NQL filter')
    rm_tag_p.add_argument('--ids', help='Comma-separated post IDs')
    rm_tag_p.add_argument('--tag', required=True, help='Tag to remove')

    # SET-FEATURED subcommand
    feat_p = subparsers.add_parser('set-featured', help='Set featured status')
    feat_p.add_argument('--filter', help='NQL filter')
    feat_p.add_argument('--ids', help='Comma-separated post IDs')
    feat_p.add_argument('--featured', required=True, choices=['true', 'false'])

    return parser.parse_args()


def get_posts_by_filter(filter_str: str) -> List[Dict]:
    """Fetch all posts matching NQL filter."""
    posts = []
    params = {'filter': filter_str, 'include': 'tags', 'limit': 50}
    for response in paginate('posts/', params=params):
        posts.extend(response.get('posts', []))
    return posts


def get_posts_by_ids(ids_str: str) -> List[Dict]:
    """Fetch posts by comma-separated IDs."""
    ids = [id.strip() for id in ids_str.split(',') if id.strip()]
    posts = []
    for post_id in ids:
        try:
            response = api_request('GET', f'posts/{post_id}/', params={'include': 'tags'})
            posts.extend(response.get('posts', []))
        except GhostAPIError as e:
            print(f"Warning: Could not fetch {post_id}: {e.message}", file=sys.stderr)
    return posts


def get_target_posts(args: argparse.Namespace) -> List[Dict]:
    """Get posts based on --filter or --ids argument."""
    if not args.filter and not args.ids:
        print("Error: Must provide --filter or --ids", file=sys.stderr)
        sys.exit(1)
    if args.filter:
        return get_posts_by_filter(args.filter)
    return get_posts_by_ids(args.ids)


def preview_changes(posts: List[Dict], action: str, detail: str = '') -> None:
    """Display preview of changes without applying."""
    print(f"\n=== PREVIEW: {action} ===")
    print(f"Affected posts: {len(posts)}")
    if detail:
        print(f"Action: {detail}")
    print("\nPosts:")
    for post in posts[:20]:
        status = post.get('status', '')
        title = post.get('title', '')[:50]
        print(f"  [{status}] {title}")
    if len(posts) > 20:
        print(f"  ... and {len(posts) - 20} more")
    print("\nRun with --execute to apply changes.")


def execute_with_progress(posts: List[Dict], update_fn: Callable, delay_ms: int) -> Dict:
    """Execute updates with progress indicator."""
    total = len(posts)
    success = 0
    failed = 0
    errors = []

    for i, post in enumerate(posts):
        print(f"\rProcessing {i+1}/{total}...", end='', file=sys.stderr)
        try:
            update_fn(post)
            success += 1
        except GhostAPIError as e:
            failed += 1
            errors.append(f"{post['id']}: {e.message}")
        if delay_ms > 0 and i < total - 1:
            time.sleep(delay_ms / 1000)

    print(file=sys.stderr)  # Newline after progress
    return {'total': total, 'success': success, 'failed': failed, 'errors': errors}


def print_summary(result: Dict) -> None:
    """Print execution summary."""
    print(f"\n=== SUMMARY ===")
    print(f"Total: {result['total']}")
    print(f"Success: {result['success']}")
    print(f"Failed: {result['failed']}")
    if result['errors']:
        print("\nErrors:")
        for err in result['errors'][:10]:
            print(f"  {err}")
        if len(result['errors']) > 10:
            print(f"  ... and {len(result['errors']) - 10} more errors")


def update_post_status(post: Dict, new_status: str) -> None:
    """Update post status (publish/unpublish)."""
    update_data = {
        'id': post['id'],
        'updated_at': post['updated_at'],
        'status': new_status
    }
    api_request('PUT', f"posts/{post['id']}/", data={'posts': [update_data]})


def update_post_tags(post: Dict, tag_name: str, action: str) -> None:
    """Add or remove tag from post."""
    current_tags = [t['name'] for t in post.get('tags', [])]
    if action == 'add':
        if tag_name in current_tags:
            return  # Already has tag
        new_tags = current_tags + [tag_name]
    else:  # remove
        if tag_name not in current_tags:
            return  # Doesn't have tag
        new_tags = [t for t in current_tags if t != tag_name]

    update_data = {
        'id': post['id'],
        'updated_at': post['updated_at'],
        'tags': new_tags
    }
    api_request('PUT', f"posts/{post['id']}/", data={'posts': [update_data]})


def update_post_featured(post: Dict, featured: bool) -> None:
    """Update post featured status."""
    if post.get('featured') == featured:
        return  # Already correct
    update_data = {
        'id': post['id'],
        'updated_at': post['updated_at'],
        'featured': featured
    }
    api_request('PUT', f"posts/{post['id']}/", data={'posts': [update_data]})


def handle_publish(args: argparse.Namespace) -> None:
    """Bulk publish drafts."""
    posts = get_target_posts(args)
    posts = [p for p in posts if p.get('status') == 'draft']
    if not posts:
        print("No draft posts found matching criteria.")
        return
    if not args.execute:
        preview_changes(posts, "PUBLISH", "Change status to 'published'")
        return
    result = execute_with_progress(
        posts, lambda p: update_post_status(p, 'published'), args.delay
    )
    print_summary(result)


def handle_unpublish(args: argparse.Namespace) -> None:
    """Bulk unpublish posts."""
    posts = get_target_posts(args)
    posts = [p for p in posts if p.get('status') == 'published']
    if not posts:
        print("No published posts found matching criteria.")
        return
    if not args.execute:
        preview_changes(posts, "UNPUBLISH", "Change status to 'draft'")
        return
    result = execute_with_progress(
        posts, lambda p: update_post_status(p, 'draft'), args.delay
    )
    print_summary(result)


def handle_add_tag(args: argparse.Namespace) -> None:
    """Add tag to posts."""
    posts = get_target_posts(args)
    if not posts:
        print("No posts found matching criteria.")
        return
    if not args.execute:
        preview_changes(posts, f"ADD TAG '{args.tag}'")
        return
    result = execute_with_progress(
        posts, lambda p: update_post_tags(p, args.tag, 'add'), args.delay
    )
    print_summary(result)


def handle_remove_tag(args: argparse.Namespace) -> None:
    """Remove tag from posts."""
    posts = get_target_posts(args)
    posts = [p for p in posts if args.tag in [t['name'] for t in p.get('tags', [])]]
    if not posts:
        print(f"No posts found with tag '{args.tag}'.")
        return
    if not args.execute:
        preview_changes(posts, f"REMOVE TAG '{args.tag}'")
        return
    result = execute_with_progress(
        posts, lambda p: update_post_tags(p, args.tag, 'remove'), args.delay
    )
    print_summary(result)


def handle_set_featured(args: argparse.Namespace) -> None:
    """Set featured status on posts."""
    posts = get_target_posts(args)
    featured = args.featured == 'true'
    if not posts:
        print("No posts found matching criteria.")
        return
    if not args.execute:
        preview_changes(posts, f"SET FEATURED={featured}")
        return
    result = execute_with_progress(
        posts, lambda p: update_post_featured(p, featured), args.delay
    )
    print_summary(result)


def main() -> int:
    """Main entry point."""
    args = parse_args()
    handlers = {
        'publish': handle_publish,
        'unpublish': handle_unpublish,
        'add-tag': handle_add_tag,
        'remove-tag': handle_remove_tag,
        'set-featured': handle_set_featured
    }
    try:
        handlers[args.command](args)
        return 0
    except GhostAPIError as e:
        print(format_error(e), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
