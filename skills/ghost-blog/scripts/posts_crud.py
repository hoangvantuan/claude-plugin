#!/usr/bin/env python3
"""CRUD operations for Ghost blog posts.

Subcommands:
    get       - Get a post by ID or slug
    create    - Create a new post
    update    - Update an existing post
    delete    - Delete a post
    publish   - Publish a draft (or schedule)
    unpublish - Revert post to draft
"""

import argparse
import json
import sys
from typing import Optional

from ghost_core import api_request, format_error, GhostAPIError


def parse_args():
    """Parse command line arguments with subcommands."""
    parser = argparse.ArgumentParser(description='Manage Ghost blog posts')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # GET subcommand
    get_p = subparsers.add_parser('get', help='Get a post by ID or slug')
    get_p.add_argument('--id', help='Post ID')
    get_p.add_argument('--slug', help='Post slug')
    get_p.add_argument('--format', choices=['html', 'json'], default='json',
                       help='Output format')

    # CREATE subcommand
    create_p = subparsers.add_parser('create', help='Create a new post')
    create_p.add_argument('--title', required=True, help='Post title')
    create_p.add_argument('--html', help='Post content as HTML')
    create_p.add_argument('--file', help='Read content from file')
    create_p.add_argument('--status', choices=['draft', 'published'],
                          default='draft', help='Post status')
    create_p.add_argument('--tags', help='Comma-separated tag names')
    create_p.add_argument('--featured', action='store_true',
                          help='Mark as featured')
    create_p.add_argument('--newsletter', help='Newsletter slug to send post via email (requires --status published)')
    create_p.add_argument('--email-segment', dest='email_segment',
                          choices=['all', 'status:free', 'status:-free'],
                          help='Email recipient segment')

    # UPDATE subcommand
    update_p = subparsers.add_parser('update', help='Update a post')
    update_p.add_argument('--id', required=True, help='Post ID')
    update_p.add_argument('--title', help='New title')
    update_p.add_argument('--html', help='New content')
    update_p.add_argument('--featured', choices=['true', 'false'],
                          help='Set featured status')
    update_p.add_argument('--meta-title', dest='meta_title',
                          help='SEO meta title')
    update_p.add_argument('--meta-description', dest='meta_description',
                          help='SEO meta description')

    # DELETE subcommand
    delete_p = subparsers.add_parser('delete', help='Delete a post')
    delete_p.add_argument('--id', required=True, help='Post ID')
    delete_p.add_argument('--confirm', action='store_true',
                          help='Skip confirmation prompt')

    # PUBLISH subcommand
    publish_p = subparsers.add_parser('publish', help='Publish a draft')
    publish_p.add_argument('--id', required=True, help='Post ID')
    publish_p.add_argument('--scheduled', help='Schedule for future (ISO datetime)')
    publish_p.add_argument('--newsletter', help='Newsletter slug to send post via email')
    publish_p.add_argument('--email-segment', dest='email_segment',
                          choices=['all', 'status:free', 'status:-free'],
                          help='Email recipient segment (all, free only, paid only)')

    # UNPUBLISH subcommand
    unpublish_p = subparsers.add_parser('unpublish', help='Revert post to draft')
    unpublish_p.add_argument('--id', required=True, help='Post ID')

    return parser.parse_args()


def handle_get(args):
    """Get a single post by ID or slug."""
    if not args.id and not args.slug:
        print("Error: Must provide --id or --slug", file=sys.stderr)
        sys.exit(1)

    identifier = args.id or f'slug/{args.slug}'
    params = {'include': 'tags,authors', 'formats': 'html'}

    response = api_request('GET', f'posts/{identifier}/', params=params)
    post = response['posts'][0]

    if args.format == 'html':
        print(f"# {post['title']}\n")
        print(post.get('html', ''))
    else:
        print(json.dumps(post, indent=2, ensure_ascii=False))


def handle_create(args):
    """Create a new post. Optionally publish and send via newsletter."""
    html_content = args.html
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            html_content = f.read()

    if not html_content:
        print("Error: Must provide --html or --file", file=sys.stderr)
        sys.exit(1)

    # Validate newsletter requires published status
    if args.newsletter and args.status != 'published':
        print("Error: --newsletter requires --status published", file=sys.stderr)
        sys.exit(1)

    post_data = {
        'title': args.title,
        'html': html_content,
        'status': args.status,
        'featured': args.featured
    }

    if args.tags:
        post_data['tags'] = [t.strip() for t in args.tags.split(',')]

    # Build query params - source=html tells Ghost to convert HTML to Lexical
    params = {'source': 'html'}
    if args.newsletter:
        params['newsletter'] = args.newsletter
        if args.email_segment:
            params['email_segment'] = args.email_segment

    response = api_request('POST', 'posts/', data={'posts': [post_data]}, params=params)
    post = response['posts'][0]

    print(f"Created post: {post['id']}")
    print(f"  Title: {post['title']}")
    print(f"  Status: {post['status']}")
    print(f"  Slug: {post['slug']}")
    if args.newsletter:
        print(f"  Newsletter: {args.newsletter}")
        if post.get('email'):
            print(f"  Email status: {post['email'].get('status', 'pending')}")


def handle_update(args):
    """Update an existing post. Requires updated_at for collision prevention."""
    # Get current post to retrieve updated_at
    response = api_request('GET', f'posts/{args.id}/')
    current = response['posts'][0]

    # Build update payload with required fields
    update_data = {
        'id': args.id,
        'updated_at': current['updated_at']
    }

    if args.title:
        update_data['title'] = args.title
    if args.html:
        update_data['html'] = args.html
    if args.featured is not None:
        update_data['featured'] = args.featured == 'true'
    if args.meta_title:
        update_data['meta_title'] = args.meta_title
    if args.meta_description:
        update_data['meta_description'] = args.meta_description

    # Add source=html if updating HTML content (Ghost 5.0+ uses Lexical format)
    params = {'source': 'html'} if args.html else {}
    response = api_request('PUT', f'posts/{args.id}/', data={'posts': [update_data]}, params=params)
    post = response['posts'][0]

    print(f"Updated post: {post['id']}")
    print(f"  Title: {post['title']}")


def handle_delete(args):
    """Delete a post with optional confirmation."""
    if not args.confirm:
        response = api_request('GET', f'posts/{args.id}/')
        post = response['posts'][0]

        print(f"About to delete: {post['title']}")
        confirm = input("Type 'yes' to confirm: ")
        if confirm.lower() != 'yes':
            print("Cancelled.")
            return

    api_request('DELETE', f'posts/{args.id}/')
    print(f"Deleted post: {args.id}")


def handle_publish(args):
    """Publish a draft or schedule for future. Optionally send via newsletter."""
    response = api_request('GET', f'posts/{args.id}/')
    current = response['posts'][0]

    update_data = {
        'id': args.id,
        'updated_at': current['updated_at'],
        'status': 'scheduled' if args.scheduled else 'published'
    }

    if args.scheduled:
        update_data['published_at'] = args.scheduled

    # Build query params for newsletter sending
    params = {}
    if args.newsletter:
        params['newsletter'] = args.newsletter
        if args.email_segment:
            params['email_segment'] = args.email_segment

    response = api_request('PUT', f'posts/{args.id}/', data={'posts': [update_data]}, params=params)
    post = response['posts'][0]

    print(f"Published: {post['title']}")
    print(f"  Status: {post['status']}")
    if post.get('published_at'):
        print(f"  Published at: {post['published_at']}")
    if args.newsletter:
        print(f"  Newsletter: {args.newsletter}")
        if post.get('email'):
            print(f"  Email status: {post['email'].get('status', 'pending')}")


def handle_unpublish(args):
    """Revert a published post to draft."""
    response = api_request('GET', f'posts/{args.id}/')
    current = response['posts'][0]

    update_data = {
        'id': args.id,
        'updated_at': current['updated_at'],
        'status': 'draft'
    }

    response = api_request('PUT', f'posts/{args.id}/', data={'posts': [update_data]})
    print(f"Unpublished: {response['posts'][0]['title']}")


def main():
    """Main entry point."""
    args = parse_args()

    handlers = {
        'get': handle_get,
        'create': handle_create,
        'update': handle_update,
        'delete': handle_delete,
        'publish': handle_publish,
        'unpublish': handle_unpublish
    }

    try:
        handlers[args.command](args)
    except GhostAPIError as e:
        print(format_error(e), file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nAborted.", file=sys.stderr)
        sys.exit(130)


if __name__ == '__main__':
    main()
