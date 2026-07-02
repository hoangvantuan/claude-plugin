#!/usr/bin/env python3
"""List and filter Ghost blog posts with pagination and multiple output formats."""

import argparse
import json
import sys
from typing import Any, Dict, List, Optional, Tuple

from ghost_core import GhostAPIError, api_request, format_error, paginate


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description='List and filter Ghost blog posts',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''Examples:
  %(prog)s --status draft
  %(prog)s --tag news --featured
  %(prog)s --search "python" --order published_at:desc
  %(prog)s --all --output json > posts.json'''
    )
    parser.add_argument('--status', choices=['draft', 'published', 'scheduled', 'all'],
                        default='all', help='Filter by post status')
    parser.add_argument('--tag', action='append', help='Filter by tag (can repeat)')
    parser.add_argument('--featured', action='store_true', help='Only featured posts')
    parser.add_argument('--search', help='Search in title/content')
    parser.add_argument('--order', default='published_at desc',
                        help='Sort order (e.g., title asc, published_at desc)')
    parser.add_argument('--limit', type=int, default=15,
                        help='Posts per page (1-100)', metavar='N')
    parser.add_argument('--page', type=int, default=1, help='Page number')
    parser.add_argument('--all', action='store_true', dest='fetch_all',
                        help='Fetch all pages')
    parser.add_argument('--max-results', type=int, default=1000, dest='max_results',
                        help='Max posts when using --all (safety cap, default 1000)')
    parser.add_argument('--output', choices=['table', 'json', 'minimal'],
                        default='table', help='Output format')
    return parser.parse_args()


def resolve_tag_slugs(tag_inputs: List[str]) -> List[str]:
    """Resolve tag names/slugs to actual slugs by looking up from API."""
    # Fetch all tags once
    response = api_request('GET', 'tags/', params={'limit': 'all'})
    all_tags = response.get('tags', [])

    # Build lookup maps
    name_to_slug = {t['name'].lower(): t['slug'] for t in all_tags}
    slug_set = {t['slug'] for t in all_tags}

    resolved = []
    for tag_input in tag_inputs:
        tag_lower = tag_input.lower()
        # Check if input is already a valid slug
        if tag_input in slug_set:
            resolved.append(tag_input)
        # Check if input matches a tag name (case-insensitive)
        elif tag_lower in name_to_slug:
            resolved.append(name_to_slug[tag_lower])
        else:
            # Keep as-is, let API handle error
            resolved.append(tag_input)
    return resolved


def build_filter(args: argparse.Namespace) -> Optional[str]:
    """Build NQL filter string from arguments."""
    filters = []
    if args.status and args.status != 'all':
        filters.append(f'status:{args.status}')
    if args.tag:
        # Resolve tag names to slugs
        slugs = resolve_tag_slugs(args.tag)
        # Use tag:slug format for single, tags:[slug1,slug2] for multiple
        if len(slugs) == 1:
            filters.append(f'tag:{slugs[0]}')
        else:
            filters.append(f'tags:[{",".join(slugs)}]')
    if args.featured:
        filters.append('featured:true')
    return '+'.join(filters) if filters else None


def format_table(posts: List[Dict[str, Any]]) -> str:
    """Format posts as ASCII table."""
    if not posts:
        return "No posts found."
    lines = [
        f"{'ID':<26} {'STATUS':<10} {'TITLE':<40} {'TAGS':<20}",
        "-" * 100
    ]
    for post in posts:
        post_id = post.get('id', '')[:24]
        status = post.get('status', '')[:10]
        title = post.get('title', '')[:38]
        tags = ','.join(t.get('name', '')[:10] for t in post.get('tags', [])[:2])
        if len(post.get('tags', [])) > 2:
            tags += '...'
        lines.append(f"{post_id:<26} {status:<10} {title:<40} {tags:<20}")
    return '\n'.join(lines)


def format_json(posts: List[Dict[str, Any]]) -> str:
    """Format posts as JSON."""
    return json.dumps(posts, indent=2, ensure_ascii=False)


def format_minimal(posts: List[Dict[str, Any]]) -> str:
    """Format as minimal list (id: title)."""
    if not posts:
        return "No posts found."
    return '\n'.join(f"{p['id']}: {p.get('title', 'Untitled')}" for p in posts)


def fetch_posts(args: argparse.Namespace) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Fetch posts based on arguments, return (posts, pagination)."""
    params: Dict[str, Any] = {
        'limit': args.limit,
        'page': args.page,
        'order': args.order,
        'include': 'tags,authors'
    }
    filter_str = build_filter(args)
    if filter_str:
        params['filter'] = filter_str

    all_posts: List[Dict[str, Any]] = []
    pagination: Dict[str, Any] = {}

    if args.fetch_all:
        for response in paginate('posts/', params=params):
            all_posts.extend(response.get('posts', []))
            pagination = response.get('meta', {}).get('pagination', {})
            print(f"\rFetching... {len(all_posts)} posts", end='', file=sys.stderr)
            if len(all_posts) >= args.max_results:
                all_posts = all_posts[:args.max_results]
                print(f"\nReached max-results limit ({args.max_results})", file=sys.stderr)
                break
        else:
            print(file=sys.stderr)
    else:
        response = api_request('GET', 'posts/', params=params)
        all_posts = response.get('posts', [])
        pagination = response.get('meta', {}).get('pagination', {})

    if args.search:
        keyword = args.search.lower()
        all_posts = [p for p in all_posts if keyword in p.get('title', '').lower()
                     or keyword in p.get('html', '').lower()]
    return all_posts, pagination


def validate_args(args: argparse.Namespace) -> Optional[str]:
    """Validate arguments, return error message if invalid."""
    if args.limit < 1 or args.limit > 100:
        return "Error: --limit must be between 1 and 100"
    if args.page < 1:
        return "Error: --page must be at least 1"
    if args.max_results < 1:
        return "Error: --max-results must be at least 1"
    return None


def main() -> int:
    """Main entry point."""
    args = parse_args()
    error = validate_args(args)
    if error:
        print(error, file=sys.stderr)
        return 1
    if args.fetch_all and args.search:
        print("Warning: --search with --all fetches all posts then filters locally",
              file=sys.stderr)
    try:
        posts, pagination = fetch_posts(args)
        if args.output == 'json':
            print(format_json(posts))
        elif args.output == 'minimal':
            print(format_minimal(posts))
        else:
            print(format_table(posts))
            if not args.fetch_all and pagination:
                total = pagination.get('total', 0)
                pages = pagination.get('pages', 1)
                current = pagination.get('page', 1)
                print(f"\nPage {current}/{pages} (Total: {total} posts)")
        return 0
    except GhostAPIError as e:
        print(format_error(e), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
