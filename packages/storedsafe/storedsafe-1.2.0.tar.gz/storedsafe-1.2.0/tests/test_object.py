"""
Test that /object endpoints use the correct format.
"""
import unittest
from unittest.mock import patch
from storedsafe import StoredSafe
# pylint: disable=unused-wildcard-import,wildcard-import
from mocks import *


class Object(unittest.TestCase):
    """Test /object endpoint"""

    def setUp(self):
        self.api = StoredSafe(
            host=MOCK_HOST,
            token=MOCK_TOKEN,
            **MOCK_DEFAULT_OPTIONS)

    @patch('requests.get', get_object)
    def test_get_object(self):
        """Successfully get object"""
        res = self.api.get_object(
            MOCK_OBJECT_ID, requests_options=MOCK_OVERRIDE_OPTIONS)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(has_merged_options(res.options), True)

    @patch('requests.get', get_object_children)
    def test_get_object_children(self):
        """Successfully get object with children"""
        res = self.api.get_object(
            MOCK_OBJECT_ID, True, requests_options=MOCK_OVERRIDE_OPTIONS)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(has_merged_options(res.options), True)

    @patch('requests.get', decrypt_object)
    def test_decrypt_object(self):
        """Successfully decrypt object"""
        res = self.api.decrypt_object(
            MOCK_OBJECT_ID, requests_options=MOCK_OVERRIDE_OPTIONS)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(has_merged_options(res.options), True)

    @patch('requests.get', get_file)
    def test_get_file(self):
        """Successfully get file"""
        res = self.api.get_file(
            MOCK_OBJECT_ID, requests_options=MOCK_OVERRIDE_OPTIONS)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(has_merged_options(res.options), True)

    @patch('requests.post', create_object)
    def test_create_object(self):
        """Successful create object"""
        res = self.api.create_object(
            **MOCK_PARAMS, requests_options=MOCK_OVERRIDE_OPTIONS)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(has_merged_options(res.options), True)

    @patch('requests.put', edit_object)
    def test_edit_object(self):
        """Successful edit object"""
        res = self.api.edit_object(
            MOCK_OBJECT_ID, **MOCK_PARAMS, requests_options=MOCK_OVERRIDE_OPTIONS)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(has_merged_options(res.options), True)

    @patch('requests.delete', delete_object)
    def test_delete_object(self):
        """Successful delete object"""
        res = self.api.delete_object(
            MOCK_OBJECT_ID, requests_options=MOCK_OVERRIDE_OPTIONS)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(has_merged_options(res.options), True)

    @patch('requests.get', find)
    def test_find(self):
        """Successfully request find"""
        res = self.api.find(
            MOCK_NEEDLE, requests_options=MOCK_OVERRIDE_OPTIONS)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(has_merged_options(res.options), True)
