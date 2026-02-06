#!/usr/bin/env python3
"""Comprehensive unit tests for ghost_core.py module."""

import json
import os
import time
import unittest
from typing import Dict
from unittest.mock import MagicMock, Mock, patch, call
from binascii import hexlify
from io import StringIO

import jwt
import requests

import ghost_core


class TestLoadConfig(unittest.TestCase):
    """Tests for load_config() function."""

    @patch.dict(os.environ, {'GHOST_URL': 'https://blog.example.com',
                             'GHOST_ADMIN_KEY': 'abc123:def456',
                             'GHOST_API_VERSION': 'v5.0'})
    def test_load_config_with_all_env_vars(self):
        """Load config with all environment variables set."""
        config = ghost_core.load_config()
        self.assertEqual(config['ghost_url'], 'https://blog.example.com')
        self.assertEqual(config['admin_key'], 'abc123:def456')
        self.assertEqual(config['api_version'], 'v5.0')

    @patch.dict(os.environ, {}, clear=True)
    def test_load_config_with_defaults(self):
        """Load config uses defaults when env vars not set."""
        config = ghost_core.load_config()
        self.assertEqual(config['ghost_url'], '')
        self.assertEqual(config['admin_key'], '')
        self.assertEqual(config['api_version'], 'v5.0')

    @patch.dict(os.environ, {'GHOST_URL': 'https://blog.example.com/'}, clear=True)
    def test_load_config_strips_trailing_slash(self):
        """Load config removes trailing slash from GHOST_URL."""
        config = ghost_core.load_config()
        self.assertEqual(config['ghost_url'], 'https://blog.example.com')

    @patch.dict(os.environ, {'GHOST_URL': 'https://blog.example.com///'}, clear=True)
    def test_load_config_strips_multiple_trailing_slashes(self):
        """Load config removes multiple trailing slashes."""
        config = ghost_core.load_config()
        self.assertEqual(config['ghost_url'], 'https://blog.example.com')


class TestValidateConfig(unittest.TestCase):
    """Tests for validate_config() function."""

    def test_validate_config_valid(self):
        """Validate config accepts valid configuration."""
        config = {
            'ghost_url': 'https://blog.example.com',
            'admin_key': 'abc123:def456',
            'api_version': 'v5.0'
        }
        is_valid, error = ghost_core.validate_config(config)
        self.assertTrue(is_valid)
        self.assertEqual(error, '')

    def test_validate_config_missing_ghost_url(self):
        """Validate config fails when GHOST_URL missing."""
        config = {
            'ghost_url': '',
            'admin_key': 'abc123:def456',
            'api_version': 'v5.0'
        }
        is_valid, error = ghost_core.validate_config(config)
        self.assertFalse(is_valid)
        self.assertEqual(error, 'GHOST_URL not set')

    def test_validate_config_missing_admin_key(self):
        """Validate config fails when GHOST_ADMIN_KEY missing."""
        config = {
            'ghost_url': 'https://blog.example.com',
            'admin_key': '',
            'api_version': 'v5.0'
        }
        is_valid, error = ghost_core.validate_config(config)
        self.assertFalse(is_valid)
        self.assertEqual(error, 'GHOST_ADMIN_KEY not set')

    def test_validate_config_invalid_key_format(self):
        """Validate config fails when API key format invalid."""
        config = {
            'ghost_url': 'https://blog.example.com',
            'admin_key': 'no_colon_here',
            'api_version': 'v5.0'
        }
        is_valid, error = ghost_core.validate_config(config)
        self.assertFalse(is_valid)
        self.assertEqual(error, 'GHOST_ADMIN_KEY invalid format (expected id:secret)')


class TestGenerateToken(unittest.TestCase):
    """Tests for generate_token() function."""

    def test_generate_token_structure(self):
        """Generate token creates valid JWT with correct structure."""
        secret_bytes = b'\x00' * 32
        secret_hex = hexlify(secret_bytes).decode()
        api_key = f'test_id:{secret_hex}'

        token = ghost_core.generate_token(api_key)

        # Decode token without verification
        decoded = jwt.decode(token, options={"verify_signature": False})

        self.assertIn('iat', decoded)
        self.assertIn('exp', decoded)
        self.assertEqual(decoded['aud'], '/admin/')

    def test_generate_token_expiry_time(self):
        """Generate token sets expiry to 5 minutes (300 seconds)."""
        secret_bytes = b'\x00' * 32
        secret_hex = hexlify(secret_bytes).decode()
        api_key = f'test_id:{secret_hex}'

        token = ghost_core.generate_token(api_key)

        decoded = jwt.decode(token, options={"verify_signature": False})
        exp_time = decoded['exp']
        iat_time = decoded['iat']

        # Expiry should be TOKEN_EXPIRY_SECONDS after issue time
        self.assertEqual(exp_time - iat_time, ghost_core.TOKEN_EXPIRY_SECONDS)

    def test_generate_token_header_structure(self):
        """Generate token includes correct JWT headers."""
        secret_bytes = b'\x00' * 32
        secret_hex = hexlify(secret_bytes).decode()
        api_key = f'test_id:{secret_hex}'

        token = ghost_core.generate_token(api_key)

        # Decode header
        header = jwt.get_unverified_header(token)

        self.assertEqual(header['alg'], 'HS256')
        self.assertEqual(header['typ'], 'JWT')
        self.assertEqual(header['kid'], 'test_id')

    def test_generate_token_different_keys_produce_different_tokens(self):
        """Generate token produces different tokens for different API keys."""
        secret1 = hexlify(b'\x00' * 32).decode()
        secret2 = hexlify(b'\x01' * 32).decode()

        token1 = ghost_core.generate_token(f'id1:{secret1}')
        token2 = ghost_core.generate_token(f'id2:{secret2}')

        self.assertNotEqual(token1, token2)


class TestTokenCache(unittest.TestCase):
    """Tests for _TokenCache class."""

    def setUp(self):
        """Reset token cache before each test."""
        ghost_core._token_cache.clear()

    def test_token_cache_initial_state(self):
        """Token cache starts with no token."""
        cache = ghost_core._TokenCache()
        self.assertIsNone(cache.token)
        self.assertEqual(cache.expiry, 0)

    def test_token_cache_get_generates_token(self):
        """Token cache generates token on first get."""
        secret_bytes = b'\x00' * 32
        secret_hex = hexlify(secret_bytes).decode()
        api_key = f'test_id:{secret_hex}'

        token = ghost_core._token_cache.get(api_key)

        self.assertIsNotNone(token)
        self.assertEqual(ghost_core._token_cache.token, token)

    def test_token_cache_returns_cached(self):
        """Token cache returns cached token if not expired."""
        secret_bytes = b'\x00' * 32
        secret_hex = hexlify(secret_bytes).decode()
        api_key = f'test_id:{secret_hex}'

        token1 = ghost_core._token_cache.get(api_key)
        token2 = ghost_core._token_cache.get(api_key)

        self.assertEqual(token1, token2)

    def test_token_cache_clear(self):
        """Token cache clear resets state."""
        secret_bytes = b'\x00' * 32
        secret_hex = hexlify(secret_bytes).decode()
        api_key = f'test_id:{secret_hex}'

        ghost_core._token_cache.get(api_key)
        ghost_core._token_cache.clear()

        self.assertIsNone(ghost_core._token_cache.token)
        self.assertEqual(ghost_core._token_cache.expiry, 0)

    def test_token_cache_regenerates_when_expired(self):
        """Token cache regenerates when expired."""
        secret_bytes = b'\x00' * 32
        secret_hex = hexlify(secret_bytes).decode()
        api_key = f'test_id:{secret_hex}'

        token1 = ghost_core._token_cache.get(api_key)

        # Force expiry
        ghost_core._token_cache.expiry = time.time() - 1

        # Wait to ensure different 'iat' timestamp
        time.sleep(1)

        token2 = ghost_core._token_cache.get(api_key)

        self.assertNotEqual(token1, token2)


class TestGetValidToken(unittest.TestCase):
    """Tests for get_valid_token() function."""

    def setUp(self):
        """Reset token cache before each test."""
        ghost_core._token_cache.clear()

    def test_get_valid_token_generates_new_when_empty(self):
        """Get valid token generates new token when cache empty."""
        secret_bytes = b'\x00' * 32
        secret_hex = hexlify(secret_bytes).decode()
        api_key = f'test_id:{secret_hex}'

        token = ghost_core.get_valid_token(api_key)

        self.assertIsNotNone(token)
        self.assertEqual(ghost_core._token_cache.token, token)

    def test_get_valid_token_returns_cached_when_valid(self):
        """Get valid token returns cached token if not expired."""
        secret_bytes = b'\x00' * 32
        secret_hex = hexlify(secret_bytes).decode()
        api_key = f'test_id:{secret_hex}'

        token1 = ghost_core.get_valid_token(api_key)
        token2 = ghost_core.get_valid_token(api_key)

        self.assertEqual(token1, token2)

    def test_get_valid_token_regenerates_when_expired(self):
        """Get valid token regenerates when cache expired."""
        secret_bytes = b'\x00' * 32
        secret_hex = hexlify(secret_bytes).decode()
        api_key = f'test_id:{secret_hex}'

        token1 = ghost_core.get_valid_token(api_key)

        # Force expiry
        ghost_core._token_cache.expiry = time.time() - 1

        # Wait to ensure different 'iat' timestamp
        time.sleep(1)

        token2 = ghost_core.get_valid_token(api_key)

        self.assertNotEqual(token1, token2)

    def test_get_valid_token_cache_duration(self):
        """Get valid token sets cache to expire in TOKEN_CACHE_SECONDS."""
        secret_bytes = b'\x00' * 32
        secret_hex = hexlify(secret_bytes).decode()
        api_key = f'test_id:{secret_hex}'

        before_time = time.time()
        ghost_core.get_valid_token(api_key)
        after_time = time.time()

        expiry = ghost_core._token_cache.expiry

        # Cache expiry should be roughly TOKEN_CACHE_SECONDS in future
        self.assertGreaterEqual(expiry - before_time, ghost_core.TOKEN_CACHE_SECONDS - 1)
        self.assertLessEqual(expiry - after_time, ghost_core.TOKEN_CACHE_SECONDS)


class TestApiRequest(unittest.TestCase):
    """Tests for api_request() function."""

    def setUp(self):
        """Reset token cache before each test."""
        ghost_core._token_cache.clear()

    @patch('ghost_core.requests.request')
    def test_api_request_get_success(self, mock_request):
        """API request makes GET request with correct headers."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'posts': []}
        mock_request.return_value = mock_response

        config = {
            'ghost_url': 'https://blog.example.com',
            'admin_key': f'keyid:{hexlify(b"x" * 32).decode()}',
            'api_version': 'v5.0'
        }

        result = ghost_core.api_request('GET', 'posts/', config=config)

        mock_request.assert_called_once()
        call_args = mock_request.call_args
        self.assertEqual(call_args[0][0], 'GET')
        self.assertIn('https://blog.example.com/ghost/api/admin/posts/', call_args[0][1])

    @patch('ghost_core.requests.request')
    def test_api_request_includes_auth_header(self, mock_request):
        """API request includes Authorization header."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_request.return_value = mock_response

        config = {
            'ghost_url': 'https://blog.example.com',
            'admin_key': f'keyid:{hexlify(b"x" * 32).decode()}',
            'api_version': 'v5.0'
        }

        ghost_core.api_request('GET', 'posts/', config=config)

        call_kwargs = mock_request.call_args[1]
        headers = call_kwargs['headers']

        self.assertIn('Authorization', headers)
        self.assertTrue(headers['Authorization'].startswith('Ghost '))

    @patch('ghost_core.requests.request')
    def test_api_request_includes_timeout(self, mock_request):
        """API request includes timeout parameter."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_request.return_value = mock_response

        config = {
            'ghost_url': 'https://blog.example.com',
            'admin_key': f'keyid:{hexlify(b"x" * 32).decode()}',
            'api_version': 'v5.0'
        }

        ghost_core.api_request('GET', 'posts/', config=config)

        call_kwargs = mock_request.call_args[1]
        self.assertEqual(call_kwargs['timeout'], ghost_core.REQUEST_TIMEOUT)

    @patch('ghost_core.requests.request')
    def test_api_request_custom_timeout(self, mock_request):
        """API request uses custom timeout when provided."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_request.return_value = mock_response

        config = {
            'ghost_url': 'https://blog.example.com',
            'admin_key': f'keyid:{hexlify(b"x" * 32).decode()}',
            'api_version': 'v5.0'
        }

        ghost_core.api_request('GET', 'posts/', config=config, timeout=60)

        call_kwargs = mock_request.call_args[1]
        self.assertEqual(call_kwargs['timeout'], 60)

    @patch('ghost_core.requests.request')
    def test_api_request_includes_accept_version_header(self, mock_request):
        """API request includes Accept-Version header."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_request.return_value = mock_response

        config = {
            'ghost_url': 'https://blog.example.com',
            'admin_key': f'keyid:{hexlify(b"x" * 32).decode()}',
            'api_version': 'v5.0'
        }

        ghost_core.api_request('GET', 'posts/', config=config)

        call_kwargs = mock_request.call_args[1]
        headers = call_kwargs['headers']

        self.assertEqual(headers['Accept-Version'], 'v5.0')

    @patch('ghost_core.requests.request')
    def test_api_request_with_json_data(self, mock_request):
        """API request passes JSON data for POST requests."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_request.return_value = mock_response

        config = {
            'ghost_url': 'https://blog.example.com',
            'admin_key': f'keyid:{hexlify(b"x" * 32).decode()}',
            'api_version': 'v5.0'
        }

        data = {'posts': [{'title': 'Test'}]}
        ghost_core.api_request('POST', 'posts/', data=data, config=config)

        call_kwargs = mock_request.call_args[1]
        self.assertEqual(call_kwargs['json'], data)

    @patch('ghost_core.requests.request')
    def test_api_request_with_query_params(self, mock_request):
        """API request passes query parameters."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_request.return_value = mock_response

        config = {
            'ghost_url': 'https://blog.example.com',
            'admin_key': f'keyid:{hexlify(b"x" * 32).decode()}',
            'api_version': 'v5.0'
        }

        params = {'limit': 10, 'page': 2}
        ghost_core.api_request('GET', 'posts/', params=params, config=config)

        call_kwargs = mock_request.call_args[1]
        self.assertEqual(call_kwargs['params'], params)

    def test_api_request_invalid_config_raises_error(self):
        """API request raises error with invalid configuration."""
        config = {
            'ghost_url': '',
            'admin_key': 'invalid',
            'api_version': 'v5.0'
        }

        with self.assertRaises(ghost_core.GhostAPIError) as context:
            ghost_core.api_request('GET', 'posts/', config=config)

        self.assertEqual(context.exception.error_type, 'ConfigurationError')

    @patch('ghost_core.requests.request')
    def test_api_request_endpoint_leading_slash(self, mock_request):
        """API request handles endpoint with leading slash."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_request.return_value = mock_response

        config = {
            'ghost_url': 'https://blog.example.com',
            'admin_key': f'keyid:{hexlify(b"x" * 32).decode()}',
            'api_version': 'v5.0'
        }

        ghost_core.api_request('GET', '/posts/', config=config)

        call_args = mock_request.call_args
        self.assertIn('/ghost/api/admin/posts/', call_args[0][1])


class TestApiRequestRetry(unittest.TestCase):
    """Tests for api_request() retry logic."""

    def setUp(self):
        """Reset token cache before each test."""
        ghost_core._token_cache.clear()

    @patch('ghost_core.time.sleep')
    @patch('ghost_core.requests.request')
    def test_api_request_retries_on_429(self, mock_request, mock_sleep):
        """API request retries on 429 rate limit."""
        mock_response_429 = Mock()
        mock_response_429.status_code = 429

        mock_response_200 = Mock()
        mock_response_200.status_code = 200
        mock_response_200.json.return_value = {'posts': []}

        mock_request.side_effect = [mock_response_429, mock_response_200]

        config = {
            'ghost_url': 'https://blog.example.com',
            'admin_key': f'keyid:{hexlify(b"x" * 32).decode()}',
            'api_version': 'v5.0'
        }

        result = ghost_core.api_request('GET', 'posts/', config=config)

        self.assertEqual(mock_request.call_count, 2)
        mock_sleep.assert_called()
        self.assertEqual(result, {'posts': []})

    @patch('ghost_core.time.sleep')
    @patch('ghost_core.requests.request')
    def test_api_request_retries_on_500(self, mock_request, mock_sleep):
        """API request retries on 500 server error."""
        mock_response_500 = Mock()
        mock_response_500.status_code = 500

        mock_response_200 = Mock()
        mock_response_200.status_code = 200
        mock_response_200.json.return_value = {'posts': []}

        mock_request.side_effect = [mock_response_500, mock_response_200]

        config = {
            'ghost_url': 'https://blog.example.com',
            'admin_key': f'keyid:{hexlify(b"x" * 32).decode()}',
            'api_version': 'v5.0'
        }

        result = ghost_core.api_request('GET', 'posts/', config=config)

        self.assertEqual(mock_request.call_count, 2)
        mock_sleep.assert_called()

    @patch('ghost_core.time.sleep')
    @patch('ghost_core.requests.request')
    def test_api_request_retries_on_network_error(self, mock_request, mock_sleep):
        """API request retries on network error."""
        mock_response_200 = Mock()
        mock_response_200.status_code = 200
        mock_response_200.json.return_value = {'posts': []}

        mock_request.side_effect = [
            requests.RequestException("Network error"),
            mock_response_200
        ]

        config = {
            'ghost_url': 'https://blog.example.com',
            'admin_key': f'keyid:{hexlify(b"x" * 32).decode()}',
            'api_version': 'v5.0'
        }

        result = ghost_core.api_request('GET', 'posts/', config=config)

        self.assertEqual(mock_request.call_count, 2)
        mock_sleep.assert_called()

    @patch('ghost_core.time.sleep')
    @patch('ghost_core.requests.request')
    def test_api_request_max_retries_exceeded(self, mock_request, mock_sleep):
        """API request raises error after max retries."""
        mock_request.side_effect = requests.RequestException("Network error")

        config = {
            'ghost_url': 'https://blog.example.com',
            'admin_key': f'keyid:{hexlify(b"x" * 32).decode()}',
            'api_version': 'v5.0'
        }

        with self.assertRaises(ghost_core.GhostAPIError) as context:
            ghost_core.api_request('GET', 'posts/', config=config)

        self.assertEqual(context.exception.error_type, 'NetworkError')
        self.assertEqual(mock_request.call_count, ghost_core.MAX_RETRIES)

    @patch('ghost_core.time.sleep')
    @patch('ghost_core.requests.request')
    def test_api_request_exponential_backoff(self, mock_request, mock_sleep):
        """API request uses exponential backoff for retries."""
        mock_response_500 = Mock()
        mock_response_500.status_code = 500

        mock_response_200 = Mock()
        mock_response_200.status_code = 200
        mock_response_200.json.return_value = {'posts': []}

        mock_request.side_effect = [mock_response_500, mock_response_500, mock_response_200]

        config = {
            'ghost_url': 'https://blog.example.com',
            'admin_key': f'keyid:{hexlify(b"x" * 32).decode()}',
            'api_version': 'v5.0'
        }

        ghost_core.api_request('GET', 'posts/', config=config)

        # Check exponential backoff: 1.0 * 2^0, 1.0 * 2^1
        sleep_calls = mock_sleep.call_args_list
        self.assertEqual(sleep_calls[0][0][0], ghost_core.RETRY_BACKOFF * 1)
        self.assertEqual(sleep_calls[1][0][0], ghost_core.RETRY_BACKOFF * 2)


class TestHandleResponse(unittest.TestCase):
    """Tests for _handle_response() function."""

    def test_handle_response_204_no_content(self):
        """Handle response returns success for 204 No Content."""
        response = Mock()
        response.status_code = 204

        result = ghost_core._handle_response(response)

        self.assertEqual(result, {'success': True})

    def test_handle_response_200_with_json(self):
        """Handle response returns JSON data for 200 OK."""
        response = Mock()
        response.status_code = 200
        response.json.return_value = {'posts': [{'id': 1, 'title': 'Test'}]}

        result = ghost_core._handle_response(response)

        self.assertEqual(result, {'posts': [{'id': 1, 'title': 'Test'}]})

    def test_handle_response_invalid_json_raises_error(self):
        """Handle response raises error for invalid JSON."""
        response = Mock()
        response.status_code = 200
        response.json.side_effect = ValueError("Invalid JSON")
        response.text = "Invalid JSON content"

        with self.assertRaises(ghost_core.GhostAPIError) as context:
            ghost_core._handle_response(response)

        self.assertIn('Invalid JSON', context.exception.message)
        self.assertEqual(context.exception.error_type, 'ParseError')
        self.assertEqual(context.exception.status_code, 200)

    def test_handle_response_truncates_long_error_text(self):
        """Handle response truncates long error text with ellipsis."""
        response = Mock()
        response.status_code = 200
        response.json.side_effect = ValueError("Invalid JSON")
        response.text = "x" * 300  # Longer than ERROR_TRUNCATE_LENGTH

        with self.assertRaises(ghost_core.GhostAPIError) as context:
            ghost_core._handle_response(response)

        # Should be truncated and end with ...
        self.assertTrue(context.exception.message.endswith('...'))
        # Message should be shorter than original
        self.assertLess(len(context.exception.message), 300)

    def test_handle_response_api_error_in_response(self):
        """Handle response raises error when errors in response."""
        response = Mock()
        response.status_code = 400
        response.json.return_value = {
            'errors': [{
                'message': 'Invalid request',
                'errorType': 'ValidationError'
            }]
        }

        with self.assertRaises(ghost_core.GhostAPIError) as context:
            ghost_core._handle_response(response)

        self.assertEqual(context.exception.message, 'Invalid request')
        self.assertEqual(context.exception.error_type, 'ValidationError')
        self.assertEqual(context.exception.status_code, 400)

    def test_handle_response_error_without_type(self):
        """Handle response handles error without errorType field."""
        response = Mock()
        response.status_code = 500
        response.json.return_value = {
            'errors': [{
                'message': 'Server error'
            }]
        }

        with self.assertRaises(ghost_core.GhostAPIError) as context:
            ghost_core._handle_response(response)

        self.assertEqual(context.exception.message, 'Server error')
        self.assertIsNone(context.exception.error_type)

    def test_handle_response_error_without_message(self):
        """Handle response uses default message when missing."""
        response = Mock()
        response.status_code = 500
        response.json.return_value = {
            'errors': [{
                'errorType': 'InternalError'
            }]
        }

        with self.assertRaises(ghost_core.GhostAPIError) as context:
            ghost_core._handle_response(response)

        self.assertEqual(context.exception.message, 'Unknown error')


class TestPaginate(unittest.TestCase):
    """Tests for paginate() generator function."""

    def setUp(self):
        """Reset token cache before each test."""
        ghost_core._token_cache.clear()

    @patch('ghost_core.api_request')
    def test_paginate_single_page(self, mock_api_request):
        """Paginate stops after first page when no next page."""
        mock_api_request.return_value = {
            'posts': [{'id': 1}],
            'meta': {
                'pagination': {
                    'page': 1,
                    'limit': 50,
                    'pages': 1,
                    'total': 1,
                    'next': None
                }
            }
        }

        config = {
            'ghost_url': 'https://blog.example.com',
            'admin_key': f'keyid:{hexlify(b"x" * 32).decode()}',
            'api_version': 'v5.0'
        }

        results = list(ghost_core.paginate('posts/', config=config))

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['posts'], [{'id': 1}])

    @patch('ghost_core.api_request')
    def test_paginate_multiple_pages(self, mock_api_request):
        """Paginate continues through multiple pages."""
        mock_api_request.side_effect = [
            {
                'posts': [{'id': 1}],
                'meta': {
                    'pagination': {
                        'page': 1,
                        'limit': 1,
                        'pages': 2,
                        'total': 2,
                        'next': 2
                    }
                }
            },
            {
                'posts': [{'id': 2}],
                'meta': {
                    'pagination': {
                        'page': 2,
                        'limit': 1,
                        'pages': 2,
                        'total': 2,
                        'next': None
                    }
                }
            }
        ]

        config = {
            'ghost_url': 'https://blog.example.com',
            'admin_key': f'keyid:{hexlify(b"x" * 32).decode()}',
            'api_version': 'v5.0'
        }

        results = list(ghost_core.paginate('posts/', config=config))

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['posts'], [{'id': 1}])
        self.assertEqual(results[1]['posts'], [{'id': 2}])

    @patch('ghost_core.api_request')
    def test_paginate_with_initial_params(self, mock_api_request):
        """Paginate preserves initial parameters across pages."""
        mock_api_request.side_effect = [
            {
                'posts': [{'id': 1}],
                'meta': {
                    'pagination': {
                        'page': 1,
                        'next': 2
                    }
                }
            },
            {
                'posts': [{'id': 2}],
                'meta': {
                    'pagination': {
                        'page': 2,
                        'next': None
                    }
                }
            }
        ]

        config = {
            'ghost_url': 'https://blog.example.com',
            'admin_key': f'keyid:{hexlify(b"x" * 32).decode()}',
            'api_version': 'v5.0'
        }

        list(ghost_core.paginate('posts/', params={'limit': 10}, config=config))

        # First call should have limit: 10
        first_call_params = mock_api_request.call_args_list[0][1]['params']
        self.assertEqual(first_call_params['limit'], 10)

        # Second call should preserve limit: 10
        second_call_params = mock_api_request.call_args_list[1][1]['params']
        self.assertEqual(second_call_params['limit'], 10)

    @patch('ghost_core.api_request')
    def test_paginate_default_params(self, mock_api_request):
        """Paginate sets default page and limit."""
        mock_api_request.return_value = {
            'posts': [],
            'meta': {
                'pagination': {
                    'next': None
                }
            }
        }

        config = {
            'ghost_url': 'https://blog.example.com',
            'admin_key': f'keyid:{hexlify(b"x" * 32).decode()}',
            'api_version': 'v5.0'
        }

        list(ghost_core.paginate('posts/', config=config))

        call_params = mock_api_request.call_args[1]['params']
        self.assertEqual(call_params['page'], 1)
        self.assertEqual(call_params['limit'], 50)

    @patch('ghost_core.api_request')
    def test_paginate_does_not_mutate_original_params(self, mock_api_request):
        """Paginate does not mutate original params dict."""
        mock_api_request.side_effect = [
            {
                'posts': [{'id': 1}],
                'meta': {'pagination': {'next': 2}}
            },
            {
                'posts': [{'id': 2}],
                'meta': {'pagination': {'next': None}}
            }
        ]

        config = {
            'ghost_url': 'https://blog.example.com',
            'admin_key': f'keyid:{hexlify(b"x" * 32).decode()}',
            'api_version': 'v5.0'
        }

        original_params = {'filter': 'status:published'}
        list(ghost_core.paginate('posts/', params=original_params, config=config))

        # Original params should not have page/limit added
        self.assertNotIn('page', original_params)
        self.assertNotIn('limit', original_params)


class TestFormatError(unittest.TestCase):
    """Tests for format_error() function."""

    def test_format_error_message_only(self):
        """Format error returns message when no type or status."""
        error = ghost_core.GhostAPIError("Test error message")
        result = ghost_core.format_error(error)
        self.assertEqual(result, "Error: Test error message")

    def test_format_error_with_type(self):
        """Format error includes error type when provided."""
        error = ghost_core.GhostAPIError("Test error", error_type="ValidationError")
        result = ghost_core.format_error(error)
        self.assertEqual(result, "[ValidationError] Error: Test error")

    def test_format_error_with_status_code(self):
        """Format error includes HTTP status code when provided."""
        error = ghost_core.GhostAPIError("Test error", status_code=400)
        result = ghost_core.format_error(error)
        self.assertEqual(result, "Error: Test error (HTTP 400)")

    def test_format_error_with_all_fields(self):
        """Format error includes type, message, and status code."""
        error = ghost_core.GhostAPIError("Test error",
                                         error_type="ValidationError",
                                         status_code=400)
        result = ghost_core.format_error(error)
        self.assertEqual(result, "[ValidationError] Error: Test error (HTTP 400)")

    def test_format_error_verbose_mode(self):
        """Format error verbose mode shows all details."""
        error = ghost_core.GhostAPIError("Test error",
                                         error_type="ValidationError",
                                         status_code=400)
        result = ghost_core.format_error(error, verbose=True)
        self.assertIn("Type: ValidationError", result)
        self.assertIn("Message: Test error", result)
        self.assertIn("HTTP Status: 400", result)

    def test_format_error_verbose_without_type(self):
        """Format error verbose works without error type."""
        error = ghost_core.GhostAPIError("Test error", status_code=500)
        result = ghost_core.format_error(error, verbose=True)
        self.assertIn("Message: Test error", result)
        self.assertIn("HTTP Status: 500", result)
        self.assertNotIn("Type:", result)


class TestMaskApiKey(unittest.TestCase):
    """Tests for mask_api_key() function."""

    def test_mask_api_key_with_colon(self):
        """Mask API key formats key with colon-separated format."""
        api_key = "keyid:abcdefgh1234567890abcdefgh1234567890"
        result = ghost_core.mask_api_key(api_key)

        self.assertTrue(result.startswith("keyid:"))
        self.assertIn("abcd", result)
        self.assertIn("7890", result)
        self.assertIn("...", result)

    def test_mask_api_key_short_secret(self):
        """Mask API key shows *** for short secrets."""
        api_key = "keyid:short"
        result = ghost_core.mask_api_key(api_key)

        self.assertEqual(result, "keyid:***")

    def test_mask_api_key_without_colon(self):
        """Mask API key masks simple keys without colon."""
        api_key = "verylongapikeywithoutcolon1234567890"
        result = ghost_core.mask_api_key(api_key)

        self.assertTrue(result.startswith("verylong"))
        self.assertTrue(result.endswith("..."))
        self.assertIn("...", result)

    def test_mask_api_key_short_without_colon(self):
        """Mask API key shows *** for short keys without colon."""
        api_key = "short"
        result = ghost_core.mask_api_key(api_key)

        self.assertEqual(result, "***")

    def test_mask_api_key_preserves_key_id(self):
        """Mask API key preserves the key ID part."""
        api_key = "my_key_id:secret_hex_string_long_enough"
        result = ghost_core.mask_api_key(api_key)

        self.assertTrue(result.startswith("my_key_id:"))


class TestGhostAPIError(unittest.TestCase):
    """Tests for GhostAPIError exception class."""

    def test_ghost_api_error_basic(self):
        """GhostAPIError creates exception with message."""
        error = ghost_core.GhostAPIError("Test error")
        self.assertEqual(error.message, "Test error")
        self.assertIsNone(error.error_type)
        self.assertIsNone(error.status_code)

    def test_ghost_api_error_with_type(self):
        """GhostAPIError stores error type."""
        error = ghost_core.GhostAPIError("Test error", error_type="ValidationError")
        self.assertEqual(error.error_type, "ValidationError")

    def test_ghost_api_error_with_status_code(self):
        """GhostAPIError stores HTTP status code."""
        error = ghost_core.GhostAPIError("Test error", status_code=400)
        self.assertEqual(error.status_code, 400)

    def test_ghost_api_error_is_exception(self):
        """GhostAPIError is an Exception subclass."""
        error = ghost_core.GhostAPIError("Test error")
        self.assertIsInstance(error, Exception)

    def test_ghost_api_error_with_all_fields(self):
        """GhostAPIError stores all fields."""
        error = ghost_core.GhostAPIError("Test error",
                                         error_type="ValidationError",
                                         status_code=400)
        self.assertEqual(error.message, "Test error")
        self.assertEqual(error.error_type, "ValidationError")
        self.assertEqual(error.status_code, 400)


class TestMain(unittest.TestCase):
    """Tests for main() CLI entrypoint function."""

    def setUp(self):
        """Reset token cache before each test."""
        ghost_core._token_cache.clear()

    @patch('ghost_core.api_request')
    @patch.dict(os.environ, {'GHOST_URL': 'https://blog.example.com',
                             'GHOST_ADMIN_KEY': f'keyid:{hexlify(b"x" * 32).decode()}',
                             'GHOST_API_VERSION': 'v5.0'})
    @patch('builtins.print')
    def test_main_success(self, mock_print, mock_api_request):
        """Main returns 0 on successful connection."""
        mock_api_request.return_value = {
            'meta': {'pagination': {'total': 42}}
        }

        result = ghost_core.main()

        self.assertEqual(result, 0)
        # Check that success message was printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('successful' in call.lower() for call in print_calls))

    @patch.dict(os.environ, {'GHOST_URL': '', 'GHOST_ADMIN_KEY': ''}, clear=True)
    @patch('builtins.print')
    def test_main_invalid_config(self, mock_print):
        """Main returns 1 on invalid configuration."""
        result = ghost_core.main()

        self.assertEqual(result, 1)
        # Check that error message was printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('error' in call.lower() for call in print_calls))

    @patch('ghost_core.api_request')
    @patch.dict(os.environ, {'GHOST_URL': 'https://blog.example.com',
                             'GHOST_ADMIN_KEY': f'keyid:{hexlify(b"x" * 32).decode()}',
                             'GHOST_API_VERSION': 'v5.0'})
    @patch('builtins.print')
    def test_main_api_error(self, mock_print, mock_api_request):
        """Main returns 1 on API error."""
        mock_api_request.side_effect = ghost_core.GhostAPIError(
            "Connection failed", "NetworkError", 500
        )

        result = ghost_core.main()

        self.assertEqual(result, 1)

    @patch('ghost_core.api_request')
    @patch.dict(os.environ, {'GHOST_URL': 'https://blog.example.com',
                             'GHOST_ADMIN_KEY': f'keyid:{hexlify(b"x" * 32).decode()}',
                             'GHOST_API_VERSION': 'v5.0'})
    @patch('builtins.print')
    def test_main_prints_masked_key(self, mock_print, mock_api_request):
        """Main prints masked API key."""
        mock_api_request.return_value = {
            'meta': {'pagination': {'total': 0}}
        }

        ghost_core.main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        # API key should be masked (contain ...)
        self.assertTrue(any('...' in call for call in print_calls))


class TestIntegration(unittest.TestCase):
    """Integration tests for combined functionality."""

    def setUp(self):
        """Reset token cache before each test."""
        ghost_core._token_cache.clear()

    @patch('ghost_core.requests.request')
    @patch.dict(os.environ, {'GHOST_URL': 'https://blog.example.com',
                             'GHOST_ADMIN_KEY': f'keyid:{hexlify(b"x" * 32).decode()}',
                             'GHOST_API_VERSION': 'v5.0'})
    def test_full_api_request_flow(self, mock_request):
        """Full flow: config load, validation, token generation, API request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'posts': [{'id': 1, 'title': 'Test'}]}
        mock_request.return_value = mock_response

        config = ghost_core.load_config()
        is_valid, error = ghost_core.validate_config(config)

        self.assertTrue(is_valid)

        result = ghost_core.api_request('GET', 'posts/', config=config)

        self.assertIn('posts', result)
        self.assertEqual(len(result['posts']), 1)

    @patch('ghost_core.api_request')
    def test_pagination_with_error_handling(self, mock_api_request):
        """Pagination with error in middle page."""
        mock_api_request.side_effect = [
            {
                'posts': [{'id': 1}],
                'meta': {'pagination': {'next': 2}}
            },
            ghost_core.GhostAPIError("API Error", status_code=500)
        ]

        config = {
            'ghost_url': 'https://blog.example.com',
            'admin_key': f'keyid:{hexlify(b"x" * 32).decode()}',
            'api_version': 'v5.0'
        }

        results = []
        with self.assertRaises(ghost_core.GhostAPIError):
            for page in ghost_core.paginate('posts/', config=config):
                results.append(page)

        self.assertEqual(len(results), 1)

    @patch('ghost_core.requests.request')
    @patch.dict(os.environ, {'GHOST_URL': 'https://blog.example.com',
                             'GHOST_ADMIN_KEY': f'keyid:{hexlify(b"x" * 32).decode()}',
                             'GHOST_API_VERSION': 'v5.0'})
    def test_api_request_loads_config_from_env_when_none(self, mock_request):
        """API request loads config from env when config param is None."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'posts': []}
        mock_request.return_value = mock_response

        # Call without config parameter
        result = ghost_core.api_request('GET', 'posts/')

        # Should have made request without raising config error
        mock_request.assert_called_once()
        self.assertEqual(result, {'posts': []})

    @patch('ghost_core.api_request')
    def test_paginate_loads_config_from_env_when_none(self, mock_api_request):
        """Paginate loads config from env when config param is None."""
        mock_api_request.return_value = {
            'posts': [{'id': 1}],
            'meta': {'pagination': {'next': None}}
        }

        # Call without config parameter
        results = list(ghost_core.paginate('posts/'))

        self.assertEqual(len(results), 1)
        # Verify api_request was called
        mock_api_request.assert_called_once()

    @patch('ghost_core.requests.request')
    def test_api_request_post_with_delete_method(self, mock_request):
        """API request handles DELETE method."""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_request.return_value = mock_response

        config = {
            'ghost_url': 'https://blog.example.com',
            'admin_key': f'keyid:{hexlify(b"x" * 32).decode()}',
            'api_version': 'v5.0'
        }

        result = ghost_core.api_request('DELETE', 'posts/1/', config=config)

        self.assertEqual(result['success'], True)
        self.assertEqual(mock_request.call_args[0][0], 'DELETE')

    @patch('ghost_core.requests.request')
    def test_api_request_put_method(self, mock_request):
        """API request handles PUT method."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'posts': [{'id': 1, 'title': 'Updated'}]}
        mock_request.return_value = mock_response

        config = {
            'ghost_url': 'https://blog.example.com',
            'admin_key': f'keyid:{hexlify(b"x" * 32).decode()}',
            'api_version': 'v5.0'
        }

        result = ghost_core.api_request('PUT', 'posts/1/', config=config)

        self.assertEqual(mock_request.call_args[0][0], 'PUT')
        self.assertIn('posts', result)


if __name__ == '__main__':
    unittest.main()
