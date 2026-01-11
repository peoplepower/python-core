import unittest
from unittest.mock import MagicMock
from caredaily.apis.app import DeviceTypesAndParameters

class TestDeviceTypesAndParameters(unittest.TestCase):
    def setUp(self):
        self.dtp = DeviceTypesAndParameters()
        self.mock_adapter = MagicMock()
        self.dtp.adapter = self.mock_adapter

    def test_get_device_types(self):
        self.mock_adapter.get.return_value = 'device-types-result'
        result = self.dtp.get_device_types()
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'device-types-result')

    def test_get_device_types_with_filters(self):
        self.mock_adapter.get.return_value = {'deviceTypes': []}
        result = self.dtp.get_device_types(
            device_type=1,
            attribute_name='test_attr',
            attribute_value='test_value',
            own=True,
            simple=False,
            organization_id=123
        )
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['deviceType'], 1)
        self.assertEqual(kwargs['ep_params']['attributeName'], 'test_attr')
        self.assertEqual(kwargs['ep_params']['organizationId'], 123)

    def test_get_device_type_attributes(self):
        device_type = 1
        self.mock_adapter.get.return_value = 'device-type-attributes-result'
        result = self.dtp.get_device_type_attributes(device_type=device_type)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'device-type-attributes-result')

    def test_get_device_type_attributes_without_type(self):
        self.mock_adapter.get.return_value = {'attributes': []}
        result = self.dtp.get_device_type_attributes()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertNotIn('deviceType', kwargs['ep_params'])

    def test_create_update_device_type_create(self):
        device_type_data = {'deviceType': {'name': 'Test Type'}}
        self.mock_adapter.post.return_value = 'create-update-device-type-result'
        result = self.dtp.create_update_device_type(device_type_data=device_type_data)
        self.mock_adapter.post.assert_called_once()
        self.assertEqual(result, 'create-update-device-type-result')

    def test_create_update_device_type_update(self):
        device_type_data = {'deviceType': {'id': 1, 'name': 'Test Type'}}
        self.mock_adapter.put.return_value = 'updated-result'
        result = self.dtp.create_update_device_type(device_type_data=device_type_data)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/deviceType/1')
        self.assertEqual(result, 'updated-result')

    def test_get_device_parameters(self):
        self.mock_adapter.get.return_value = 'device-parameters-result'
        result = self.dtp.get_device_parameters()
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'device-parameters-result')

    def test_get_device_parameters_with_name(self):
        self.mock_adapter.get.return_value = {'parameter': {}}
        result = self.dtp.get_device_parameters(param_name='test.param')
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['paramName'], 'test.param')

    def test_post_device_parameter(self):
        parameter_data = {'deviceParam': {'name': 'test.param'}}
        self.mock_adapter.post.return_value = {'created': True}
        result = self.dtp.post_device_parameter(parameter_data=parameter_data)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_json'], parameter_data)
        self.assertEqual(result, {'created': True})

    def test_post_device_parameter_none(self):
        self.mock_adapter.post.return_value = {'created': True}
        result = self.dtp.post_device_parameter(parameter_data=None)
        args, kwargs = self.mock_adapter.post.call_args
        self.assertIsNone(kwargs['ep_json'])

    def test_delete_device_parameter(self):
        self.mock_adapter.delete.return_value = {'deleted': True}
        result = self.dtp.delete_device_parameter(parameter_name='test.param')
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/deviceParameters/test.param')
        self.assertEqual(result, {'deleted': True})

    def test_put_device_parameter(self):
        parameter_data = {'deviceParam': {'name': 'test.param', 'value': 1}}
        self.mock_adapter.put.return_value = {'updated': True}
        result = self.dtp.put_device_parameter(
            parameter_name='test.param',
            parameter_data=parameter_data
        )
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/deviceParameters/test.param')
        self.assertEqual(kwargs['ep_json'], parameter_data)
        self.assertEqual(result, {'updated': True})

    def test_put_device_parameter_none(self):
        self.mock_adapter.put.return_value = {'updated': True}
        result = self.dtp.put_device_parameter(
            parameter_name='test.param',
            parameter_data=None
        )
        args, kwargs = self.mock_adapter.put.call_args
        self.assertIsNone(kwargs['ep_json'])

    def test_get_default_rules(self):
        self.mock_adapter.get.return_value = {'rules': []}
        result = self.dtp.get_default_rules(device_type=1)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/deviceType/1/rules')
        self.assertEqual(result, {'rules': []})

    def test_get_default_rules_with_details(self):
        self.mock_adapter.get.return_value = {'rules': []}
        result = self.dtp.get_default_rules(device_type=1, details=True)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['details'], True)

    def test_add_default_rule(self):
        self.mock_adapter.post.return_value = {'added': True}
        result = self.dtp.add_default_rule(device_type=1, rule_id=10)
        self.mock_adapter.post.assert_called_once()
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/deviceType/1/rules/10')
        self.assertEqual(result, {'added': True})

    def test_add_default_rule_with_hidden(self):
        self.mock_adapter.post.return_value = {'added': True}
        result = self.dtp.add_default_rule(device_type=1, rule_id=10, hidden=True)
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['hidden'], True)

    def test_delete_default_rule(self):
        self.mock_adapter.delete.return_value = {'deleted': True}
        result = self.dtp.delete_default_rule(device_type=1, rule_id=10)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/deviceType/1/rules/10')
        self.assertEqual(result, {'deleted': True})

    def test_get_device_goals_by_types_with_device_type(self):
        self.mock_adapter.get.return_value = {'goals': []}
        result = self.dtp.get_device_goals_by_types(device_type=1)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/deviceType/1/goals')
        self.assertEqual(result, {'goals': []})

    def test_get_device_goals_by_types_without_device_type(self):
        self.mock_adapter.get.return_value = {'goals': []}
        result = self.dtp.get_device_goals_by_types()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/deviceGoals')

    def test_get_device_goals_by_types_with_type_ids(self):
        self.mock_adapter.get.return_value = {'goals': []}
        result = self.dtp.get_device_goals_by_types(type_ids='1,2,3', app_name='test_app')
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['typeIds'], '1,2,3')
        self.assertEqual(kwargs['ep_params']['appName'], 'test_app')

    def test_get_device_goal_installation_instruction(self):
        self.mock_adapter.get.return_value = {'instructions': {}}
        result = self.dtp.get_device_goal_installation_instruction(goal_id=1)
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/goals/1/installation')
        self.assertEqual(result, {'instructions': {}})

    def test_put_device_media(self):
        media_data = {'media': {'deviceType': 1}}
        self.mock_adapter.put.return_value = {'updated': True}
        result = self.dtp.put_device_media(media_data=media_data)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/deviceMedia')
        self.assertEqual(kwargs['ep_json'], media_data)
        self.assertEqual(result, {'updated': True})

    def test_put_device_media_none(self):
        self.mock_adapter.put.return_value = {'updated': True}
        result = self.dtp.put_device_media(media_data=None)
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/deviceMedia')
        self.assertIsNone(kwargs['ep_json'])

    def test_get_media(self):
        self.mock_adapter.get.return_value = {'media': []}
        result = self.dtp.get_media()
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, {'media': []})

    def test_get_media_with_filters(self):
        self.mock_adapter.get.return_value = {'media': []}
        result = self.dtp.get_media(device_type=1, media_id=10)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['deviceType'], 1)
        self.assertEqual(kwargs['ep_params']['mediaId'], 10)

    def test_delete_media(self):
        self.mock_adapter.delete.return_value = {'deleted': True}
        result = self.dtp.delete_media(media_id=123)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/deviceMedia/123')
        self.assertEqual(result, {'deleted': True})

    def test_put_device_models(self):
        models_data = {'models': []}
        self.mock_adapter.put.return_value = {'updated': True}
        result = self.dtp.put_device_models(models_data=models_data)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_json'], models_data)
        self.assertEqual(result, {'updated': True})

    def test_put_device_models_none(self):
        self.mock_adapter.put.return_value = {'updated': True}
        result = self.dtp.put_device_models(models_data=None)
        args, kwargs = self.mock_adapter.put.call_args
        self.assertIsNone(kwargs['ep_json'])

    def test_get_device_models(self):
        self.mock_adapter.get.return_value = {'models': []}
        result = self.dtp.get_device_models()
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, {'models': []})

    def test_get_device_models_with_filters(self):
        self.mock_adapter.get.return_value = {'models': []}
        result = self.dtp.get_device_models(device_type=1, model_id='model1')
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['deviceType'], 1)
        self.assertEqual(kwargs['ep_params']['modelId'], 'model1')

    def test_delete_device_model_data(self):
        self.mock_adapter.delete.return_value = {'deleted': True}
        result = self.dtp.delete_device_model_data(model_id='model1')
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/deviceModels/model1')
        self.assertEqual(result, {'deleted': True})

    def test_get_stories(self):
        self.mock_adapter.get.return_value = {'stories': []}
        result = self.dtp.get_stories()
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, {'stories': []})

    def test_get_stories_with_filters(self):
        self.mock_adapter.get.return_value = {'stories': []}
        result = self.dtp.get_stories(device_type=1, story_id=10)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(kwargs['ep_params']['deviceType'], 1)
        self.assertEqual(kwargs['ep_params']['storyId'], 10)

    def test_put_stories(self):
        stories_data = {'stories': []}
        self.mock_adapter.put.return_value = {'updated': True}
        result = self.dtp.put_stories(stories_data=stories_data)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_json'], stories_data)
        self.assertEqual(result, {'updated': True})

    def test_put_stories_none(self):
        self.mock_adapter.put.return_value = {'updated': True}
        result = self.dtp.put_stories(stories_data=None)
        args, kwargs = self.mock_adapter.put.call_args
        self.assertIsNone(kwargs['ep_json'])

    def test_delete_story(self):
        self.mock_adapter.delete.return_value = {'deleted': True}
        result = self.dtp.delete_story(story_id=123)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/deviceStories/123')
        self.assertEqual(result, {'deleted': True})

    def test_get_stories_collection(self):
        """Test Case ID: TC-DeviceTypesAndParameters-001
        Title: Get Stories Collection
        Priority: P1
        """
        self.mock_adapter.get.return_value = {'stories': []}
        result = self.dtp.get_stories_collection(story_type=1, lang='en')
        self.mock_adapter.get.assert_called_once()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/stories')
        self.assertEqual(kwargs['ep_params']['storyType'], 1)
        self.assertEqual(kwargs['ep_params']['lang'], 'en')
        self.assertEqual(result, {'stories': []})

    def test_get_stories_collection_no_params(self):
        """Test Case ID: TC-DeviceTypesAndParameters-002
        Title: Get Stories Collection without Filters
        Priority: P1
        """
        self.mock_adapter.get.return_value = {'stories': []}
        result = self.dtp.get_stories_collection()
        args, kwargs = self.mock_adapter.get.call_args
        self.assertIsNone(kwargs.get('ep_params'))
        self.assertEqual(result, {'stories': []})

    def test_put_stories_collection(self):
        """Test Case ID: TC-DeviceTypesAndParameters-003
        Title: Put Stories Collection
        Priority: P1
        """
        stories_data = {'stories': [{'id': 'story1', 'storyType': 1}]}
        self.mock_adapter.put.return_value = {'resultCode': 0}
        result = self.dtp.put_stories_collection(stories_data=stories_data)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/stories')
        self.assertEqual(kwargs['ep_json'], stories_data)
        self.assertEqual(result, {'resultCode': 0})

    def test_delete_stories_collection(self):
        """Test Case ID: TC-DeviceTypesAndParameters-004
        Title: Delete Stories Collection
        Priority: P1
        """
        story_ids = [1, 2, 3]
        self.mock_adapter.delete.return_value = {'resultCode': 0}
        result = self.dtp.delete_stories_collection(story_ids=story_ids)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/stories')
        self.assertEqual(kwargs['ep_params']['storyId'], story_ids)
        self.assertEqual(result, {'resultCode': 0})

    def test_delete_stories_collection_all(self):
        """Test Case ID: TC-DeviceTypesAndParameters-005
        Title: Delete All Stories from Collection
        Priority: P2
        """
        self.mock_adapter.delete.return_value = {'resultCode': 0}
        result = self.dtp.delete_stories_collection()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertIsNone(kwargs.get('ep_params'))
        self.assertEqual(result, {'resultCode': 0})

    def test_put_media(self):
        """Test Case ID: TC-DeviceTypesAndParameters-006
        Title: Put Media
        Priority: P1
        """
        media_data = {'media': [{'id': 'media1', 'type': 1}]}
        self.mock_adapter.put.return_value = {'resultCode': 0}
        result = self.dtp.put_media(media_data=media_data)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/media')
        self.assertEqual(kwargs['ep_json'], media_data)
        self.assertEqual(result, {'resultCode': 0})

    def test_delete_media_collection(self):
        """Test Case ID: TC-DeviceTypesAndParameters-007
        Title: Delete Media Collection
        Priority: P1
        """
        media_ids = [1, 2, 3]
        self.mock_adapter.delete.return_value = {'resultCode': 0}
        result = self.dtp.delete_media_collection(media_ids=media_ids)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/media')
        self.assertEqual(kwargs['ep_params']['mediaId'], media_ids)
        self.assertEqual(result, {'resultCode': 0})

    def test_delete_media_collection_all(self):
        """Test Case ID: TC-DeviceTypesAndParameters-008
        Title: Delete All Media from Collection
        Priority: P2
        """
        self.mock_adapter.delete.return_value = {'resultCode': 0}
        result = self.dtp.delete_media_collection()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertIsNone(kwargs.get('ep_params'))
        self.assertEqual(result, {'resultCode': 0})
