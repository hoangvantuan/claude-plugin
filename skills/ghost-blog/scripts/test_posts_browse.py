#!/usr/bin/env python3
"""Comprehensive unit tests for posts_browse.py script."""

import argparse
import json
import sys
import unittest
from io import StringIO
from typing import Dict, Any, List
from unittest.mock import MagicMock, Mock, patch, call

import posts_browse
from ghost_core import GhostAPIError


class TestBuildFilter(unittest.TestCase):
    """Tests for build_filter() function."""

    def test_build_filter_empty_no_filters(self):
        """Empty filters return None."""
        args = argparse.Namespace(
            status='all',
            tag=None,
            featured=False
        )
        result = posts_browse.build_filter(args)
        self.assertIsNone(result)

    def test_build_filter_status_draft(self):
        """Single status filter returns correct string."""
        args = argparse.Namespace(
            status='draft',
            tag=None,
            featured=False
        )
        result = posts_browse.build_filter(args)
        self.assertEqual(result, 'status:draft')

    def test_build_filter_status_published(self):
        """Published status filter."""
        args = argparse.Namespace(
            status='published',
            tag=None,
            featured=False
        )
        result = posts_browse.build_filter(args)
        self.assertEqual(result, 'status:published')

    def test_build_filter_status_scheduled(self):
        """Scheduled status filter."""
        args = argparse.Namespace(
            status='scheduled',
            tag=None,
            featured=False
        )
        result = posts_browse.build_filter(args)
        self.assertEqual(result, 'status:scheduled')

    def test_build_filter_status_all_ignored(self):
        """status='all' is ignored."""
        args = argparse.Namespace(
            status='all',
            tag=None,
            featured=False
        )
        result = posts_browse.build_filter(args)
        self.assertIsNone(result)

    @patch('posts_browse.resolve_tag_slugs', side_effect=lambda x: x)
    def test_build_filter_single_tag(self, mock_resolve):
        """Single tag filter uses tag: format."""
        args = argparse.Namespace(
            status='all',
            tag=['news'],
            featured=False
        )
        result = posts_browse.build_filter(args)
        self.assertEqual(result, 'tag:news')

    @patch('posts_browse.resolve_tag_slugs', side_effect=lambda x: x)
    def test_build_filter_multiple_tags(self, mock_resolve):
        """Multiple tags filter uses tags:[] format."""
        args = argparse.Namespace(
            status='all',
            tag=['news', 'python', 'api'],
            featured=False
        )
        result = posts_browse.build_filter(args)
        self.assertEqual(result, 'tags:[news,python,api]')

    def test_build_filter_featured_only(self):
        """Featured filter only."""
        args = argparse.Namespace(
            status='all',
            tag=None,
            featured=True
        )
        result = posts_browse.build_filter(args)
        self.assertEqual(result, 'featured:true')

    def test_build_filter_status_and_featured(self):
        """Combined status and featured filters."""
        args = argparse.Namespace(
            status='draft',
            tag=None,
            featured=True
        )
        result = posts_browse.build_filter(args)
        self.assertEqual(result, 'status:draft+featured:true')

    @patch('posts_browse.resolve_tag_slugs', side_effect=lambda x: x)
    def test_build_filter_status_and_tags(self, mock_resolve):
        """Combined status and tags filters (single tag uses tag: format)."""
        args = argparse.Namespace(
            status='draft',
            tag=['news'],
            featured=False
        )
        result = posts_browse.build_filter(args)
        self.assertEqual(result, 'status:draft+tag:news')

    @patch('posts_browse.resolve_tag_slugs', side_effect=lambda x: x)
    def test_build_filter_all_three(self, mock_resolve):
        """Combined status, tags, and featured filters."""
        args = argparse.Namespace(
            status='draft',
            tag=['news', 'python'],
            featured=True
        )
        result = posts_browse.build_filter(args)
        self.assertEqual(result, 'status:draft+tags:[news,python]+featured:true')


class TestFormatTable(unittest.TestCase):
    """Tests for format_table() function."""

    def test_format_table_empty_list(self):
        """Empty list returns 'No posts found.'"""
        result = posts_browse.format_table([])
        self.assertEqual(result, "No posts found.")

    def test_format_table_single_post(self):
        """Single post formats correctly."""
        posts = [
            {
                'id': 'post123',
                'status': 'published',
                'title': 'Test Post',
                'tags': []
            }
        ]
        result = posts_browse.format_table(posts)
        lines = result.split('\n')
        self.assertEqual(len(lines), 3)  # header, separator, post
        self.assertIn('post123', lines[2])
        self.assertIn('published', lines[2])
        self.assertIn('Test Post', lines[2])

    def test_format_table_truncates_long_title(self):
        """Long title truncates at 38 chars."""
        posts = [
            {
                'id': 'post123',
                'status': 'published',
                'title': 'This is a very long title that exceeds the limit',
                'tags': []
            }
        ]
        result = posts_browse.format_table(posts)
        # Check that title is truncated (max 38 chars in display)
        self.assertIn('This is a very long title that exceed', result)

    def test_format_table_no_tags(self):
        """Post with no tags shows empty tags column."""
        posts = [
            {
                'id': 'post123',
                'status': 'published',
                'title': 'Test',
                'tags': []
            }
        ]
        result = posts_browse.format_table(posts)
        lines = result.split('\n')
        # Should have header, separator, and post
        self.assertEqual(len(lines), 3)

    def test_format_table_one_tag(self):
        """Post with one tag displays correctly."""
        posts = [
            {
                'id': 'post123',
                'status': 'published',
                'title': 'Test',
                'tags': [{'name': 'news'}]
            }
        ]
        result = posts_browse.format_table(posts)
        self.assertIn('news', result)

    def test_format_table_two_tags(self):
        """Post with two tags displays both."""
        posts = [
            {
                'id': 'post123',
                'status': 'published',
                'title': 'Test',
                'tags': [{'name': 'news'}, {'name': 'python'}]
            }
        ]
        result = posts_browse.format_table(posts)
        self.assertIn('news', result)
        self.assertIn('python', result)
        self.assertNotIn('...', result)

    def test_format_table_three_tags_shows_ellipsis(self):
        """Post with 3+ tags shows first 2 and '...'"""
        posts = [
            {
                'id': 'post123',
                'status': 'published',
                'title': 'Test',
                'tags': [
                    {'name': 'news'},
                    {'name': 'python'},
                    {'name': 'api'}
                ]
            }
        ]
        result = posts_browse.format_table(posts)
        self.assertIn('news', result)
        self.assertIn('python', result)
        self.assertNotIn('api', result)  # Third tag shouldn't be shown
        self.assertIn('...', result)

    def test_format_table_multiple_posts(self):
        """Multiple posts format with proper alignment."""
        posts = [
            {
                'id': 'post1',
                'status': 'published',
                'title': 'First Post',
                'tags': []
            },
            {
                'id': 'post2',
                'status': 'draft',
                'title': 'Second Post',
                'tags': [{'name': 'draft'}]
            }
        ]
        result = posts_browse.format_table(posts)
        lines = result.split('\n')
        self.assertEqual(len(lines), 4)  # header, separator, post1, post2

    def test_format_table_missing_fields(self):
        """Posts missing some fields still format correctly."""
        posts = [
            {
                'id': 'post123'
                # Missing status, title, tags
            }
        ]
        result = posts_browse.format_table(posts)
        lines = result.split('\n')
        self.assertEqual(len(lines), 3)
        # Should not crash, just use empty strings


class TestFormatJson(unittest.TestCase):
    """Tests for format_json() function."""

    def test_format_json_empty_list(self):
        """Empty list returns valid JSON array."""
        result = posts_browse.format_json([])
        parsed = json.loads(result)
        self.assertEqual(parsed, [])

    def test_format_json_single_post(self):
        """Single post returns valid JSON."""
        posts = [{'id': 'post123', 'title': 'Test'}]
        result = posts_browse.format_json(posts)
        parsed = json.loads(result)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]['id'], 'post123')
        self.assertEqual(parsed[0]['title'], 'Test')

    def test_format_json_multiple_posts(self):
        """Multiple posts return valid JSON array."""
        posts = [
            {'id': 'post1', 'title': 'Post 1'},
            {'id': 'post2', 'title': 'Post 2'}
        ]
        result = posts_browse.format_json(posts)
        parsed = json.loads(result)
        self.assertEqual(len(parsed), 2)

    def test_format_json_preserves_unicode(self):
        """JSON preserves unicode characters."""
        posts = [{'id': 'post123', 'title': 'Python 编程'}]
        result = posts_browse.format_json(posts)
        self.assertIn('Python', result)
        self.assertIn('编程', result)
        # Verify it's valid JSON
        parsed = json.loads(result)
        self.assertEqual(parsed[0]['title'], 'Python 编程')

    def test_format_json_is_valid_json(self):
        """Output is always valid JSON."""
        posts = [
            {'id': '1', 'title': 'Post', 'status': 'published'},
            {'id': '2', 'title': 'Draft', 'status': 'draft'}
        ]
        result = posts_browse.format_json(posts)
        # Should not raise an exception
        parsed = json.loads(result)
        self.assertIsInstance(parsed, list)


class TestFormatMinimal(unittest.TestCase):
    """Tests for format_minimal() function."""

    def test_format_minimal_empty_list(self):
        """Empty list returns 'No posts found.'"""
        result = posts_browse.format_minimal([])
        self.assertEqual(result, "No posts found.")

    def test_format_minimal_single_post(self):
        """Single post returns 'id: title' format."""
        posts = [{'id': 'post123', 'title': 'Test Post'}]
        result = posts_browse.format_minimal(posts)
        self.assertEqual(result, 'post123: Test Post')

    def test_format_minimal_multiple_posts(self):
        """Multiple posts, one per line."""
        posts = [
            {'id': 'post1', 'title': 'First'},
            {'id': 'post2', 'title': 'Second'},
            {'id': 'post3', 'title': 'Third'}
        ]
        result = posts_browse.format_minimal(posts)
        lines = result.split('\n')
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[0], 'post1: First')
        self.assertEqual(lines[1], 'post2: Second')
        self.assertEqual(lines[2], 'post3: Third')

    def test_format_minimal_missing_title(self):
        """Post without title shows 'Untitled'."""
        posts = [{'id': 'post123'}]
        result = posts_browse.format_minimal(posts)
        self.assertEqual(result, 'post123: Untitled')

    def test_format_minimal_empty_title(self):
        """Post with empty title shows empty string (not 'Untitled')."""
        posts = [{'id': 'post123', 'title': ''}]
        result = posts_browse.format_minimal(posts)
        # .get() only provides default for missing keys, not empty values
        self.assertEqual(result, 'post123: ')


class TestParseArgs(unittest.TestCase):
    """Tests for parse_args() function."""

    def test_parse_args_defaults(self):
        """Default values are set correctly."""
        with patch('sys.argv', ['prog']):
            args = posts_browse.parse_args()
            self.assertEqual(args.status, 'all')
            self.assertIsNone(args.tag)
            self.assertFalse(args.featured)
            self.assertIsNone(args.search)
            self.assertEqual(args.order, 'published_at desc')
            self.assertEqual(args.limit, 15)
            self.assertEqual(args.page, 1)
            self.assertFalse(args.fetch_all)
            self.assertEqual(args.output, 'table')

    def test_parse_args_status_choices(self):
        """Status argument accepts valid choices."""
        for status in ['draft', 'published', 'scheduled', 'all']:
            with patch('sys.argv', ['prog', '--status', status]):
                args = posts_browse.parse_args()
                self.assertEqual(args.status, status)

    def test_parse_args_output_choices(self):
        """Output argument accepts valid choices."""
        for output in ['table', 'json', 'minimal']:
            with patch('sys.argv', ['prog', '--output', output]):
                args = posts_browse.parse_args()
                self.assertEqual(args.output, output)

    def test_parse_args_single_tag(self):
        """Single tag argument."""
        with patch('sys.argv', ['prog', '--tag', 'news']):
            args = posts_browse.parse_args()
            self.assertEqual(args.tag, ['news'])

    def test_parse_args_multiple_tags(self):
        """Multiple tag arguments can be repeated."""
        with patch('sys.argv', ['prog', '--tag', 'news', '--tag', 'python']):
            args = posts_browse.parse_args()
            self.assertEqual(args.tag, ['news', 'python'])

    def test_parse_args_featured_flag(self):
        """Featured flag sets to True."""
        with patch('sys.argv', ['prog', '--featured']):
            args = posts_browse.parse_args()
            self.assertTrue(args.featured)

    def test_parse_args_search(self):
        """Search argument."""
        with patch('sys.argv', ['prog', '--search', 'python']):
            args = posts_browse.parse_args()
            self.assertEqual(args.search, 'python')

    def test_parse_args_order(self):
        """Custom order argument."""
        with patch('sys.argv', ['prog', '--order', 'title:asc']):
            args = posts_browse.parse_args()
            self.assertEqual(args.order, 'title:asc')

    def test_parse_args_limit(self):
        """Limit argument as integer."""
        with patch('sys.argv', ['prog', '--limit', '50']):
            args = posts_browse.parse_args()
            self.assertEqual(args.limit, 50)

    def test_parse_args_page(self):
        """Page argument as integer."""
        with patch('sys.argv', ['prog', '--page', '2']):
            args = posts_browse.parse_args()
            self.assertEqual(args.page, 2)

    def test_parse_args_fetch_all(self):
        """Fetch all flag."""
        with patch('sys.argv', ['prog', '--all']):
            args = posts_browse.parse_args()
            self.assertTrue(args.fetch_all)

    def test_parse_args_combined(self):
        """Multiple arguments together."""
        with patch('sys.argv', [
            'prog',
            '--status', 'draft',
            '--tag', 'news',
            '--featured',
            '--output', 'json',
            '--limit', '30'
        ]):
            args = posts_browse.parse_args()
            self.assertEqual(args.status, 'draft')
            self.assertEqual(args.tag, ['news'])
            self.assertTrue(args.featured)
            self.assertEqual(args.output, 'json')
            self.assertEqual(args.limit, 30)

    def test_parse_args_max_results_default(self):
        """Max-results defaults to 1000."""
        with patch('sys.argv', ['prog']):
            args = posts_browse.parse_args()
            self.assertEqual(args.max_results, 1000)

    def test_parse_args_max_results_custom(self):
        """Max-results can be set to custom value."""
        with patch('sys.argv', ['prog', '--max-results', '500']):
            args = posts_browse.parse_args()
            self.assertEqual(args.max_results, 500)


class TestValidateArgs(unittest.TestCase):
    """Tests for validate_args() function."""

    def test_validate_args_valid_defaults(self):
        """Valid default arguments return None."""
        args = argparse.Namespace(
            limit=15,
            page=1,
            max_results=1000
        )
        result = posts_browse.validate_args(args)
        self.assertIsNone(result)

    def test_validate_args_valid_custom_values(self):
        """Valid custom arguments return None."""
        args = argparse.Namespace(
            limit=50,
            page=5,
            max_results=500
        )
        result = posts_browse.validate_args(args)
        self.assertIsNone(result)

    def test_validate_args_limit_zero(self):
        """Limit of 0 returns error message."""
        args = argparse.Namespace(
            limit=0,
            page=1,
            max_results=1000
        )
        result = posts_browse.validate_args(args)
        self.assertIsNotNone(result)
        self.assertIn('limit', result)
        self.assertIn('1 and 100', result)

    def test_validate_args_limit_negative(self):
        """Negative limit returns error message."""
        args = argparse.Namespace(
            limit=-5,
            page=1,
            max_results=1000
        )
        result = posts_browse.validate_args(args)
        self.assertIsNotNone(result)
        self.assertIn('limit', result)

    def test_validate_args_limit_too_high(self):
        """Limit over 100 returns error message."""
        args = argparse.Namespace(
            limit=101,
            page=1,
            max_results=1000
        )
        result = posts_browse.validate_args(args)
        self.assertIsNotNone(result)
        self.assertIn('limit', result)
        self.assertIn('1 and 100', result)

    def test_validate_args_limit_boundary_1(self):
        """Limit of 1 is valid."""
        args = argparse.Namespace(
            limit=1,
            page=1,
            max_results=1000
        )
        result = posts_browse.validate_args(args)
        self.assertIsNone(result)

    def test_validate_args_limit_boundary_100(self):
        """Limit of 100 is valid."""
        args = argparse.Namespace(
            limit=100,
            page=1,
            max_results=1000
        )
        result = posts_browse.validate_args(args)
        self.assertIsNone(result)

    def test_validate_args_page_zero(self):
        """Page of 0 returns error message."""
        args = argparse.Namespace(
            limit=15,
            page=0,
            max_results=1000
        )
        result = posts_browse.validate_args(args)
        self.assertIsNotNone(result)
        self.assertIn('page', result)
        self.assertIn('at least 1', result)

    def test_validate_args_page_negative(self):
        """Negative page returns error message."""
        args = argparse.Namespace(
            limit=15,
            page=-1,
            max_results=1000
        )
        result = posts_browse.validate_args(args)
        self.assertIsNotNone(result)
        self.assertIn('page', result)

    def test_validate_args_page_boundary_1(self):
        """Page of 1 is valid."""
        args = argparse.Namespace(
            limit=15,
            page=1,
            max_results=1000
        )
        result = posts_browse.validate_args(args)
        self.assertIsNone(result)

    def test_validate_args_page_large_number(self):
        """Large page numbers are valid."""
        args = argparse.Namespace(
            limit=15,
            page=999,
            max_results=1000
        )
        result = posts_browse.validate_args(args)
        self.assertIsNone(result)

    def test_validate_args_max_results_zero(self):
        """Max-results of 0 returns error message."""
        args = argparse.Namespace(
            limit=15,
            page=1,
            max_results=0
        )
        result = posts_browse.validate_args(args)
        self.assertIsNotNone(result)
        self.assertIn('max-results', result)
        self.assertIn('at least 1', result)

    def test_validate_args_max_results_negative(self):
        """Negative max-results returns error message."""
        args = argparse.Namespace(
            limit=15,
            page=1,
            max_results=-100
        )
        result = posts_browse.validate_args(args)
        self.assertIsNotNone(result)
        self.assertIn('max-results', result)

    def test_validate_args_max_results_boundary_1(self):
        """Max-results of 1 is valid."""
        args = argparse.Namespace(
            limit=15,
            page=1,
            max_results=1
        )
        result = posts_browse.validate_args(args)
        self.assertIsNone(result)

    def test_validate_args_max_results_large(self):
        """Large max-results values are valid."""
        args = argparse.Namespace(
            limit=15,
            page=1,
            max_results=100000
        )
        result = posts_browse.validate_args(args)
        self.assertIsNone(result)


class TestFetchPosts(unittest.TestCase):
    """Tests for fetch_posts() function."""

    @patch('posts_browse.api_request')
    def test_fetch_posts_basic(self, mock_api):
        """Basic fetch returns posts and pagination."""
        mock_api.return_value = {
            'posts': [
                {'id': '1', 'title': 'Post 1', 'status': 'published'},
                {'id': '2', 'title': 'Post 2', 'status': 'published'}
            ],
            'meta': {
                'pagination': {
                    'page': 1,
                    'pages': 2,
                    'total': 15
                }
            }
        }
        args = argparse.Namespace(
            status='all',
            tag=None,
            featured=False,
            search=None,
            order='created_at:desc',
            limit=15,
            page=1,
            fetch_all=False,
            max_results=1000
        )
        posts, pagination = posts_browse.fetch_posts(args)
        self.assertEqual(len(posts), 2)
        self.assertEqual(pagination['page'], 1)
        self.assertEqual(pagination['total'], 15)

    @patch('posts_browse.api_request')
    def test_fetch_posts_with_filter(self, mock_api):
        """Fetch with filter includes filter param."""
        mock_api.return_value = {
            'posts': [{'id': '1', 'title': 'Draft'}],
            'meta': {'pagination': {}}
        }
        args = argparse.Namespace(
            status='draft',
            tag=None,
            featured=False,
            search=None,
            order='created_at:desc',
            limit=15,
            page=1,
            fetch_all=False,
            max_results=1000
        )
        posts, _ = posts_browse.fetch_posts(args)
        # Check that api_request was called with filter
        call_kwargs = mock_api.call_args[1]
        self.assertIn('filter', call_kwargs['params'])
        self.assertEqual(call_kwargs['params']['filter'], 'status:draft')

    @patch('posts_browse.paginate')
    def test_fetch_posts_fetch_all(self, mock_paginate):
        """Fetch all iterates through pages."""
        mock_paginate.return_value = [
            {
                'posts': [{'id': '1'}, {'id': '2'}],
                'meta': {'pagination': {'next': 2}}
            },
            {
                'posts': [{'id': '3'}],
                'meta': {'pagination': {}}
            }
        ]
        args = argparse.Namespace(
            status='all',
            tag=None,
            featured=False,
            search=None,
            order='created_at:desc',
            limit=15,
            page=1,
            fetch_all=True,
            max_results=1000
        )
        with patch('sys.stderr', new_callable=StringIO):
            posts, pagination = posts_browse.fetch_posts(args)
        self.assertEqual(len(posts), 3)

    @patch('posts_browse.api_request')
    def test_fetch_posts_search_filters_results(self, mock_api):
        """Search parameter filters by title and content."""
        mock_api.return_value = {
            'posts': [
                {'id': '1', 'title': 'Python Guide', 'html': '<p>Content about Python</p>'},
                {'id': '2', 'title': 'Other Post', 'html': '<p>No match here</p>'},
                {'id': '3', 'title': 'More Info', 'html': '<p>Python is great</p>'}
            ],
            'meta': {'pagination': {}}
        }
        args = argparse.Namespace(
            status='all',
            tag=None,
            featured=False,
            search='python',
            order='created_at:desc',
            limit=15,
            page=1,
            fetch_all=False,
            max_results=1000
        )
        posts, _ = posts_browse.fetch_posts(args)
        # Should only return posts with 'python' in title or html
        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0]['id'], '1')
        self.assertEqual(posts[1]['id'], '3')

    @patch('posts_browse.api_request')
    def test_fetch_posts_search_case_insensitive(self, mock_api):
        """Search is case-insensitive."""
        mock_api.return_value = {
            'posts': [
                {'id': '1', 'title': 'Python Guide', 'html': ''},
                {'id': '2', 'title': 'PYTHON TIPS', 'html': ''},
            ],
            'meta': {'pagination': {}}
        }
        args = argparse.Namespace(
            status='all',
            tag=None,
            featured=False,
            search='PYTHON',
            order='created_at:desc',
            limit=15,
            page=1,
            fetch_all=False,
            max_results=1000
        )
        posts, _ = posts_browse.fetch_posts(args)
        self.assertEqual(len(posts), 2)

    @patch('posts_browse.api_request')
    def test_fetch_posts_includes_tags_and_authors(self, mock_api):
        """API request includes tags and authors."""
        mock_api.return_value = {
            'posts': [],
            'meta': {'pagination': {}}
        }
        args = argparse.Namespace(
            status='all',
            tag=None,
            featured=False,
            search=None,
            order='created_at:desc',
            limit=15,
            page=1,
            fetch_all=False,
            max_results=1000
        )
        posts_browse.fetch_posts(args)
        call_kwargs = mock_api.call_args[1]
        self.assertEqual(call_kwargs['params']['include'], 'tags,authors')

    @patch('posts_browse.paginate')
    def test_fetch_posts_respects_max_results_cap(self, mock_paginate):
        """Fetch all breaks when max-results limit is reached."""
        # Create mock pages with enough posts to exceed max_results
        mock_paginate.return_value = [
            {
                'posts': [{'id': str(i)} for i in range(1, 51)],  # 50 posts
                'meta': {'pagination': {'next': 2}}
            },
            {
                'posts': [{'id': str(i)} for i in range(51, 101)],  # 50 posts
                'meta': {'pagination': {'next': 3}}
            },
            {
                'posts': [{'id': str(i)} for i in range(101, 151)],  # 50 posts
                'meta': {'pagination': {}}
            }
        ]
        args = argparse.Namespace(
            status='all',
            tag=None,
            featured=False,
            search=None,
            order='created_at:desc',
            limit=15,
            page=1,
            fetch_all=True,
            max_results=75  # Stop after 75 posts
        )
        with patch('sys.stderr', new_callable=StringIO):
            posts, pagination = posts_browse.fetch_posts(args)
        # Should have exactly 75 posts (max_results), not 150
        self.assertEqual(len(posts), 75)

    @patch('posts_browse.paginate')
    def test_fetch_posts_prints_max_results_message(self, mock_paginate):
        """Fetch all prints message when max-results reached."""
        mock_paginate.return_value = [
            {
                'posts': [{'id': str(i)} for i in range(1, 101)],
                'meta': {'pagination': {'next': 2}}
            },
            {
                'posts': [{'id': str(i)} for i in range(101, 201)],
                'meta': {'pagination': {}}
            }
        ]
        args = argparse.Namespace(
            status='all',
            tag=None,
            featured=False,
            search=None,
            order='created_at:desc',
            limit=15,
            page=1,
            fetch_all=True,
            max_results=50
        )
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            posts, pagination = posts_browse.fetch_posts(args)
        stderr_output = mock_stderr.getvalue()
        self.assertIn('Reached max-results limit', stderr_output)
        self.assertIn('50', stderr_output)

    @patch('posts_browse.paginate')
    def test_fetch_posts_does_not_break_before_max_results(self, mock_paginate):
        """Fetch all fetches all pages if less than max-results."""
        mock_paginate.return_value = [
            {
                'posts': [{'id': str(i)} for i in range(1, 26)],  # 25 posts
                'meta': {'pagination': {'next': 2}}
            },
            {
                'posts': [{'id': str(i)} for i in range(26, 51)],  # 25 posts
                'meta': {'pagination': {}}
            }
        ]
        args = argparse.Namespace(
            status='all',
            tag=None,
            featured=False,
            search=None,
            order='created_at:desc',
            limit=15,
            page=1,
            fetch_all=True,
            max_results=100  # Higher than total
        )
        with patch('sys.stderr', new_callable=StringIO):
            posts, pagination = posts_browse.fetch_posts(args)
        # Should have all 50 posts since we didn't hit max-results
        self.assertEqual(len(posts), 50)


class TestMain(unittest.TestCase):
    """Tests for main() function."""

    @patch('posts_browse.fetch_posts')
    @patch('posts_browse.parse_args')
    def test_main_search_with_all_shows_warning(self, mock_parse, mock_fetch):
        """Main prints warning when --all and --search combined."""
        mock_parse.return_value = argparse.Namespace(
            status='all',
            tag=None,
            featured=False,
            search='python',  # Search is set
            order='created_at:desc',
            limit=15,
            page=1,
            fetch_all=True,  # Fetch all is set
            output='table',
            max_results=1000
        )
        mock_fetch.return_value = (
            [{'id': '1', 'title': 'Post', 'status': 'published', 'tags': []}],
            {}
        )
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            result = posts_browse.main()
        stderr_output = mock_stderr.getvalue()
        self.assertIn('Warning', stderr_output)
        self.assertIn('search', stderr_output)
        self.assertIn('all', stderr_output)

    @patch('posts_browse.fetch_posts')
    @patch('posts_browse.parse_args')
    def test_main_no_warning_without_search(self, mock_parse, mock_fetch):
        """Main does not warn when only --all without --search."""
        mock_parse.return_value = argparse.Namespace(
            status='all',
            tag=None,
            featured=False,
            search=None,  # No search
            order='created_at:desc',
            limit=15,
            page=1,
            fetch_all=True,
            output='table',
            max_results=1000
        )
        mock_fetch.return_value = (
            [{'id': '1', 'title': 'Post', 'status': 'published', 'tags': []}],
            {}
        )
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            result = posts_browse.main()
        stderr_output = mock_stderr.getvalue()
        self.assertNotIn('Warning', stderr_output)

    @patch('posts_browse.fetch_posts')
    @patch('posts_browse.parse_args')
    def test_main_validation_error_returns_1(self, mock_parse, mock_fetch):
        """Main returns 1 on validation error."""
        mock_parse.return_value = argparse.Namespace(
            status='all',
            tag=None,
            featured=False,
            search=None,
            order='created_at:desc',
            limit=101,  # Invalid: > 100
            page=1,
            fetch_all=False,
            output='table',
            max_results=1000
        )
        with patch('sys.stderr', new_callable=StringIO):
            result = posts_browse.main()
        self.assertEqual(result, 1)

    @patch('posts_browse.fetch_posts')
    @patch('posts_browse.parse_args')
    def test_main_table_output(self, mock_parse, mock_fetch):
        """Main returns 0 and prints table output."""
        mock_parse.return_value = argparse.Namespace(
            status='all',
            tag=None,
            featured=False,
            search=None,
            order='created_at:desc',
            limit=15,
            page=1,
            fetch_all=False,
            output='table',
            max_results=1000
        )
        mock_fetch.return_value = (
            [{'id': '1', 'title': 'Post', 'status': 'published', 'tags': []}],
            {'page': 1, 'pages': 1, 'total': 1}
        )
        with patch('builtins.print') as mock_print:
            result = posts_browse.main()
        self.assertEqual(result, 0)
        mock_print.assert_called()

    @patch('posts_browse.fetch_posts')
    @patch('posts_browse.parse_args')
    def test_main_json_output(self, mock_parse, mock_fetch):
        """Main prints JSON output."""
        mock_parse.return_value = argparse.Namespace(
            status='all',
            tag=None,
            featured=False,
            search=None,
            order='created_at:desc',
            limit=15,
            page=1,
            fetch_all=False,
            output='json',
            max_results=1000
        )
        mock_fetch.return_value = (
            [{'id': '1', 'title': 'Post'}],
            {}
        )
        with patch('builtins.print') as mock_print:
            result = posts_browse.main()
        self.assertEqual(result, 0)
        # Verify JSON was printed
        call_args = mock_print.call_args[0][0]
        parsed = json.loads(call_args)
        self.assertEqual(len(parsed), 1)

    @patch('posts_browse.fetch_posts')
    @patch('posts_browse.parse_args')
    def test_main_minimal_output(self, mock_parse, mock_fetch):
        """Main prints minimal output."""
        mock_parse.return_value = argparse.Namespace(
            status='all',
            tag=None,
            featured=False,
            search=None,
            order='created_at:desc',
            limit=15,
            page=1,
            fetch_all=False,
            output='minimal',
            max_results=1000
        )
        mock_fetch.return_value = (
            [{'id': '1', 'title': 'Post'}],
            {}
        )
        with patch('builtins.print') as mock_print:
            result = posts_browse.main()
        self.assertEqual(result, 0)
        mock_print.assert_called()

    @patch('posts_browse.parse_args')
    def test_main_handles_api_error(self, mock_parse):
        """Main returns 1 on GhostAPIError."""
        mock_parse.return_value = argparse.Namespace(
            status='all',
            tag=None,
            featured=False,
            search=None,
            order='created_at:desc',
            limit=15,
            page=1,
            fetch_all=False,
            output='table',
            max_results=1000
        )
        with patch('posts_browse.fetch_posts') as mock_fetch:
            mock_fetch.side_effect = GhostAPIError('Test error', 'TestError', 400)
            with patch('builtins.print'):
                result = posts_browse.main()
        self.assertEqual(result, 1)

    @patch('posts_browse.fetch_posts')
    @patch('posts_browse.parse_args')
    def test_main_pagination_info_table_output(self, mock_parse, mock_fetch):
        """Main prints pagination info for table output when not fetch_all."""
        mock_parse.return_value = argparse.Namespace(
            status='all',
            tag=None,
            featured=False,
            search=None,
            order='created_at:desc',
            limit=15,
            page=1,
            fetch_all=False,
            output='table',
            max_results=1000
        )
        mock_fetch.return_value = (
            [{'id': '1', 'title': 'Post', 'status': 'published', 'tags': []}],
            {'page': 1, 'pages': 3, 'total': 45}
        )
        with patch('builtins.print') as mock_print:
            posts_browse.main()
        # Check that pagination was printed
        calls = mock_print.call_args_list
        pagination_call = None
        for call_obj in calls:
            if call_obj[0] and 'Page 1/3' in str(call_obj[0][0]):
                pagination_call = call_obj
                break
        self.assertIsNotNone(pagination_call)

    @patch('posts_browse.fetch_posts')
    @patch('posts_browse.parse_args')
    def test_main_no_pagination_for_fetch_all(self, mock_parse, mock_fetch):
        """Main does not print pagination when fetch_all=True."""
        mock_parse.return_value = argparse.Namespace(
            status='all',
            tag=None,
            featured=False,
            search=None,
            order='created_at:desc',
            limit=15,
            page=1,
            fetch_all=True,
            output='table',
            max_results=1000
        )
        mock_fetch.return_value = (
            [{'id': '1', 'title': 'Post', 'status': 'published', 'tags': []}],
            {}  # Empty pagination for fetch_all
        )
        with patch('builtins.print') as mock_print:
            posts_browse.main()
        # Verify pagination info not printed
        calls = mock_print.call_args_list
        pagination_printed = any(
            'Page' in str(call_obj[0][0]) if call_obj[0] else False
            for call_obj in calls
        )
        # With empty pagination dict, pagination shouldn't be printed
        self.assertFalse(pagination_printed)


if __name__ == '__main__':
    unittest.main()
