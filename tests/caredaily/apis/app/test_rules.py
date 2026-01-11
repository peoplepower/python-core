import unittest
from unittest.mock import MagicMock
from caredaily.apis.app import Rules

class TestRules(unittest.TestCase):
    def setUp(self):
        self.rules = Rules()
        self.mock_adapter = MagicMock()
        self.rules.adapter = self.mock_adapter

    def test_get_conditions_and_actions(self):
        self.mock_adapter.get.return_value = 'conditions-actions-result'
        result = self.rules.get_conditions_and_actions(location_id=1)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'conditions-actions-result')

    def test_create_update_rule(self):
        rule_data = {'rule': {'name': 'Test Rule'}}
        self.mock_adapter.post.return_value = 'create-update-rule-result'
        result = self.rules.create_update_rule(rule_data=rule_data)
        self.mock_adapter.post.assert_called_once()
        self.assertEqual(result, 'create-update-rule-result')

    def test_get_rules(self):
        location_id = 1
        self.mock_adapter.get.return_value = 'get-rules-result'
        result = self.rules.get_rules(location_id=location_id)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'get-rules-result')

    def test_delete_rules(self):
        location_id = 1
        rule_ids = [1, 2, 3]
        self.mock_adapter.delete.return_value = 'delete-rules-result'
        result = self.rules.delete_rules(location_id=location_id, rule_ids=rule_ids)
        self.mock_adapter.delete.assert_called_once()
        self.assertEqual(result, 'delete-rules-result')

    def test_get_conditions_and_actions_with_version(self):
        self.mock_adapter.get.return_value = {'conditions': []}
        result = self.rules.get_conditions_and_actions(location_id=1, version=2)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['version'], 2)

    def test_create_update_rule_create(self):
        rule_data = {'rule': {'name': 'Test Rule'}}
        self.mock_adapter.post.return_value = {'ruleId': 1}
        result = self.rules.create_update_rule(rule_data=rule_data, location_id=1)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/rules')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(result, {'ruleId': 1})

    def test_create_update_rule_update_by_rule_id_param(self):
        rule_data = {'rule': {'name': 'Updated Rule'}}
        self.mock_adapter.put.return_value = {'updated': True}
        result = self.rules.create_update_rule(
            rule_data=rule_data,
            location_id=1,
            rule_id=10
        )
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/rules/10')
        self.assertEqual(result, {'updated': True})

    def test_create_update_rule_update_by_rule_data_id(self):
        rule_data = {'rule': {'id': 10, 'name': 'Updated Rule'}}
        self.mock_adapter.put.return_value = {'updated': True}
        result = self.rules.create_update_rule(rule_data=rule_data, location_id=1)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/rules/10')

    def test_get_rules_with_all_filters(self):
        self.mock_adapter.get.return_value = {'rules': []}
        result = self.rules.get_rules(
            location_id=1,
            rule_id='10',
            device_id='dev1',
            details=True
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['ruleId'], '10')
        self.assertEqual(kwargs['ep_params']['deviceId'], 'dev1')
        self.assertEqual(kwargs['ep_params']['details'], True)

    def test_delete_rules_with_all_filters(self):
        self.mock_adapter.delete.return_value = {'deleted': True}
        result = self.rules.delete_rules(
            location_id=1,
            rule_ids=[1, 2, 3],
            status=1,
            device_type=10,
            device_id='dev1',
            default=True,
            hidden=False
        )
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(kwargs['ep_params']['ruleId'], [1, 2, 3])
        self.assertEqual(kwargs['ep_params']['status'], 1)
        self.assertEqual(kwargs['ep_params']['deviceType'], 10)
        self.assertEqual(kwargs['ep_params']['deviceId'], 'dev1')
        self.assertEqual(kwargs['ep_params']['default'], True)
        self.assertEqual(kwargs['ep_params']['hidden'], False)

    def test_update_rule_attrs(self):
        attrs = {'rule': {'name': 'New Name', 'status': 1}}
        self.mock_adapter.put.return_value = {'updated': True}
        result = self.rules.update_rule_attrs(
            rule_id=10,
            attrs=attrs,
            location_id=1
        )
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/rules/10/attrs')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(kwargs['ep_json'], attrs)
        self.assertEqual(result, {'updated': True})

    def test_delete_rule(self):
        self.mock_adapter.delete.return_value = {'deleted': True}
        result = self.rules.delete_rule(rule_id=10, location_id=1)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/rules/10')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(result, {'deleted': True})

    def test_update_rules_status(self):
        self.mock_adapter.put.return_value = {'updated': [1, 2, 3]}
        result = self.rules.update_rules_status(
            status=1,
            location_id=1
        )
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/rulesStatus/1')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(result, {'updated': [1, 2, 3]})

    def test_update_rules_status_with_all_filters(self):
        self.mock_adapter.put.return_value = {'updated': [1, 2, 3]}
        result = self.rules.update_rules_status(
            status=1,
            location_id=1,
            rule_ids=[1, 2, 3],
            device_type=10,
            device_id='dev1',
            default=True,
            hidden=False
        )
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_params']['ruleId'], [1, 2, 3])
        self.assertEqual(kwargs['ep_params']['deviceType'], 10)
        self.assertEqual(kwargs['ep_params']['deviceId'], 'dev1')
        self.assertEqual(kwargs['ep_params']['default'], True)
        self.assertEqual(kwargs['ep_params']['hidden'], False)

    def test_create_default_rules(self):
        self.mock_adapter.post.return_value = {'created': True}
        result = self.rules.create_default_rules(location_id=1)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/rulesCreateDefault')
        self.assertEqual(kwargs['ep_params']['locationId'], 1)
        self.assertEqual(result, {'created': True})

    def test_create_default_rules_with_device_id(self):
        self.mock_adapter.post.return_value = {'created': True}
        result = self.rules.create_default_rules(
            location_id=1,
            device_id='dev1'
        )
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['deviceId'], 'dev1')
