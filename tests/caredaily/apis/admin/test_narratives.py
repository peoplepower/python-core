import unittest
from unittest.mock import MagicMock

from caredaily.apis.admin import Narratives


class TestNarratives(unittest.TestCase):
    def setUp(self):
        self.narratives = Narratives()
        self.mock_adapter = MagicMock()
        self.narratives.adapter = self.mock_adapter
        self.mock_adapter._headers = {'ADMIN_KEY': 'admin_key'}
        self.mock_adapter._get_headers = MagicMock(return_value={'API_KEY': 'admin_key'})

    def test_get_organization_narratives_success(self):
        self.mock_adapter.get.return_value = {'narratives': []}
        result = self.narratives.get_organization_narratives(
            organization_id=123,
            row_count=50
        )
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['rowCount'], 50)
        self.assertEqual(result, {'narratives': []})

    def test_get_organization_narratives_with_all_filters(self):
        self.mock_adapter.get.return_value = {'narratives': []}
        self.narratives.get_organization_narratives(
            organization_id=123,
            row_count=50,
            search_tag='tag1',
            location_id=10,
            narrative_time=1234567890,
            narrative_id=5,
            parent_id=3,
            narrative_type=1,
            priority=2,
            to_priority=5,
            status=1,
            event_type='test_event',
            search_by='test*',
            start_date='2024-01-01',
            end_date='2024-12-31',
            page_marker='marker123'
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['rowCount'], 50)
        self.assertEqual(kwargs['ep_params']['searchTag'], 'tag1')
        self.assertEqual(kwargs['ep_params']['locationId'], 10)
        self.assertEqual(kwargs['ep_params']['narrativeTime'], 1234567890)
        self.assertEqual(kwargs['ep_params']['narrativeId'], 5)
        self.assertEqual(kwargs['ep_params']['parentId'], 3)
        self.assertEqual(kwargs['ep_params']['narrativeType'], 1)
        self.assertEqual(kwargs['ep_params']['priority'], 2)
        self.assertEqual(kwargs['ep_params']['toPriority'], 5)
        self.assertEqual(kwargs['ep_params']['status'], 1)
        self.assertEqual(kwargs['ep_params']['eventType'], 'test_event')
        self.assertEqual(kwargs['ep_params']['searchBy'], 'test*')
        self.assertEqual(kwargs['ep_params']['startDate'], '2024-01-01')
        self.assertEqual(kwargs['ep_params']['endDate'], '2024-12-31')
        self.assertEqual(kwargs['ep_params']['pageMarker'], 'marker123')

    def test_get_organization_narratives_minimal_params(self):
        self.mock_adapter.get.return_value = {'narratives': []}
        self.narratives.get_organization_narratives(
            organization_id=123,
            row_count=50
        )
        args, kwargs = self.mock_adapter.get.call_args
        # Only rowCount should be present, other None params filtered out
        self.assertEqual(kwargs['ep_params']['rowCount'], 50)
        self.assertNotIn('searchTag', kwargs['ep_params'])
        self.assertNotIn('locationId', kwargs['ep_params'])
        self.assertNotIn('pageMarker', kwargs['ep_params'])
