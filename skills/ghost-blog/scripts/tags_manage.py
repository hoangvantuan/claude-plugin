#!/usr/bin/env python3
"""Manage Ghost blog tags.

Subcommands:
    list   - List all tags with optional post counts
    create - Create a new tag
    update - Update an existing tag
    delete - Delete a tag
"""

import argparse
import json
import sys

from ghost_core import api_request, format_error, GhostAPIError


def parse_args():
    """Parse command line arguments with subcommands."""
    parser = argparse.ArgumentParser(description='Manage Ghost blog tags')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # LIST subcommand
    list_p = subparsers.add_parser('list', help='List all tags')
    list_p.add_argument('--output', choices=['table', 'json'], default='table',
                        help='Output format')

    # CREATE subcommand
    create_p = subparsers.add_parser('create', help='Create a new tag')
    create_p.add_argument('--name', required=True, help='Tag name')
    create_p.add_argument('--slug', help='Custom slug (auto-generated if not set)')
    create_p.add_argument('--description', help='Tag description')

    # UPDATE subcommand
    update_p = subparsers.add_parser('update', help='Update a tag')
    update_p.add_argument('--id', help='Tag ID')
    update_p.add_argument('--slug', help='Tag slug (for lookup)')
    update_p.add_argument('--name', help='New tag name')
    update_p.add_argument('--description', help='New description')

    # DELETE subcommand
    delete_p = subparsers.add_parser('delete', help='Delete a tag')
    delete_p.add_argument('--id', help='Tag ID')
    delete_p.add_argument('--slug', help='Tag slug')
    delete_p.add_argument('--confirm', action='store_true',
                          help='Skip confirmation prompt')

    return parser.parse_args()


def handle_list(args):
    """List all tags."""
    params = {'limit': 'all'}

    response = api_request('GET', 'tags/', params=params)
    tags = response.get('tags', [])

    if args.output == 'json':
        print(json.dumps(tags, indent=2, ensure_ascii=False))
    else:
        print(f"{'NAME':<35} {'SLUG':<35}")
        print("-" * 70)
        for tag in tags:
            name = tag.get('name', '')[:33]
            slug = tag.get('slug', '')[:33]
            print(f"{name:<35} {slug:<35}")


def handle_create(args):
    """Create a new tag."""
    tag_data = {'name': args.name}
    if args.slug:
        tag_data['slug'] = args.slug
    if args.description:
        tag_data['description'] = args.description

    response = api_request('POST', 'tags/', data={'tags': [tag_data]})
    tag = response['tags'][0]

    print(f"Created tag: {tag['name']} ({tag['slug']})")


def handle_update(args):
    """Update an existing tag. Requires updated_at for collision prevention."""
    if not args.id and not args.slug:
        print("Error: Must provide --id or --slug for lookup", file=sys.stderr)
        sys.exit(1)

    # Get current tag
    identifier = args.id or f'slug/{args.slug}'
    response = api_request('GET', f'tags/{identifier}/')
    current = response['tags'][0]

    # Build update payload
    update_data = {
        'id': current['id'],
        'updated_at': current['updated_at']
    }

    if args.name:
        update_data['name'] = args.name
    if args.description:
        update_data['description'] = args.description

    response = api_request('PUT', f'tags/{current["id"]}/',
                           data={'tags': [update_data]})
    print(f"Updated tag: {response['tags'][0]['name']}")


def handle_delete(args):
    """Delete a tag with optional confirmation."""
    if not args.id and not args.slug:
        print("Error: Must provide --id or --slug", file=sys.stderr)
        sys.exit(1)

    identifier = args.id or f'slug/{args.slug}'

    if not args.confirm:
        response = api_request('GET', f'tags/{identifier}/')
        tag = response['tags'][0]

        print(f"About to delete tag: {tag['name']}")
        if input("Type 'yes' to confirm: ").lower() != 'yes':
            print("Cancelled.")
            return
        identifier = tag['id']

    api_request('DELETE', f'tags/{identifier}/')
    print("Tag deleted.")


def main():
    """Main entry point."""
    args = parse_args()

    handlers = {
        'list': handle_list,
        'create': handle_create,
        'update': handle_update,
        'delete': handle_delete
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
