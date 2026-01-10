# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///

import json
from typing import Dict, List

from ..models import (
    APIKeyType,
    Cloud,
    MQTT,
    Result,
    Server,
    ServerType,
    SignatureAlgorithm,
)
from .api import API


class CloudConnectivity(API):
    def check_availability(self):
        result = self.adapter.get(
            "/espapi/watch", ep_headers={"Content-Type": "text/plain"}
        )
        return result

    def get_version(self, version: bool = None, json: bool = None):
        endpoint = "/espapi/version"
        headers = {}
        if version:
            endpoint += "?version=true"
            headers["Content-Type"] = "text/html"
        elif json:
            endpoint += "?json=true"
        else:
            headers["Content-Type"] = "application/xml"
        result = self.adapter.get(endpoint, ep_headers=headers)
        return result

    def get_cloud_settings(
        self, device_id: str = None, connected: bool = None, version: str = None
    ):
        params = {
            "device_id": device_id,
            "connected": connected,
            "version": version,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/espapi/cloud/json/settings", ep_params=params
        )
        return result
        clouds = result.data.get("clouds", [])
        return [Cloud(**cloud) for cloud in clouds]

    def get_server_settings(
        self,
        server_type: ServerType = ServerType.RESTFUL,
        crtTag: bool = None,
        deviceId: str = None,
        connected: bool = None,
        brand: str = None,
        appName: str = None,
    ):
        params = {
            "crtTag": crtTag,
            "deviceId": deviceId,
            "connected": connected,
            "brand": brand,
            "appName": appName,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            f"/espapi/cloud/json/settingsServer/{server_type.value}", ep_params=params
        )
        return result
        server = result.data.get("server", {})
        mqtt = result.data.get("mqtt", {})
        return Server(**server), MQTT(**mqtt)

    def get_server_settings_url(
        self,
        server_type: ServerType = ServerType.RESTFUL,
        device_id: str = None,
        connected: bool = None,
        ssl: bool = None,
        brand: str = None,
        appName: str = None,
    ):
        params = {
            "type": server_type.value,
            "deviceId": device_id,
            "connected": connected,
            "ssl": ssl,
            "brand": brand,
            "appName": appName,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/espapi/cloud/json/settingsServer", ep_params=params
        )
        return result
    
    def get_cloud_instances(
            self, 
            device_id: str
        ):
        params = {
            "deviceId": device_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/espapi/cloud/json/settingsCloud", ep_params=params
        )
        return result


class Authentication(API):
    def login_by_username(
        self,
        username: str,
        password: str = None,
        passcode: str = None,
        expiry: int = None,
        key_type: APIKeyType = None,
        app_name: str = None,
        brand: str = None,
        client_id: str = None,
        pref_delivery_type: int = None,
        sms_prefix: str = None,
        app_hash: str = None,
        totp: bool = None,
        sign: bool = None,
        sign_algorithm: SignatureAlgorithm = None,
    ):
        params = {
            "username": username,
            "expiry": expiry,
            "keyType": key_type.value if key_type else None,
            "appName": app_name,
            "brand": brand,
            "clientId": client_id,
            "prefDeliveryType": pref_delivery_type,
            "smsPrefix": sms_prefix,
            "appHash": app_hash,
            "totp": totp,
            "sign": sign,
            "signAlgorithm": sign_algorithm.value if sign_algorithm else None,
        }
        params = {k: v for k, v in params.items() if v is not None}
        headers = {
            "PASSWORD": password,
            "passcode": passcode,
        }
        headers = {k: v for k, v in headers.items() if v is not None}
        result: Result = self.adapter.get(
            "/espapi/cloud/json/login", ep_params=params, ep_headers=headers
        )
        return result

    def send_passcode(): ...

    def login_by_key(
        self,
        key: str,
        passcode: str = None,
        key_type: APIKeyType = None,
        expiry: int = None,
        pref_delivery_type: int = None,
        brand: str = None,
        client_id: str = None,
    ):
        params = {
            "keyType": key_type.value if key_type else None,
            "expiry": expiry,
            "prefDeliveryType": pref_delivery_type,
            "brand": brand,
            "clientId": client_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        headers = {
            "API_KEY": key,
            "passcode": passcode,
        }
        headers = {k: v for k, v in headers.items() if v is not None}
        result: Result = self.adapter.get(
            "/espapi/cloud/json/loginByKey", ep_params=params, ep_headers=headers
        )
        return result

    def logout(): ...

    def create_totp_factor(): ...

    def confirm_totp_factor(): ...

    def get_totp_factors(): ...

    def delete_totp_factor(): ...

    def get_private_key(): ...

    def get_public_key(): ...

    def get_operation_token(): ...


class UserAccounts(API):
    def create_user_account(): ...

    def get_user_information(
        self,
        user_id: int = None,
        organization_id: int = None,
    ):
        params = {
            "userId": user_id,
            "organizationId": organization_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result = self.adapter.get(
            "/espapi/cloud/json/user", ep_params=params
        )
        return result

    def update_user(): ...

    def delete_user(): ...

    def get_pronouns(): ...

    def send_verification_message(): ...

    def provide_verification_code(): ...

    def put_new_password(): ...

    def recover_password(): ...

    def reset_user_badges(): ...

    def get_terms_of_service(): ...

    def put_terms_of_service(): ...

    def put_user_tag(): ...

    def delete_user_tag(): ...

    def put_user_code(): ...

    def get_user_codes(): ...

    def delete_user_code(): ...


class Locations(API):
    def create_location(): ...

    def update_location(
        self,
        location_id: int,
        data: Dict,
        analytic_key: str = None,
    ):
        headers = None
        if analytic_key:
            headers = self.adapter._get_headers(analytic_key, APIKeyType.ANALYTIC)
        return self.adapter.put(
            f"/espapi/cloud/json/location/{location_id}",
            ep_json=json.dumps(data),
            ep_headers=headers,
        )

    def delete_location(): ...

    def put_location_to_organization(): ...

    def post_location_event(): ...

    def get_location_events_history(
            self,
            location_id: int,
            start_date_ms: int = None,
            end_date_ms: int = None,
    ):
        params = {
            "startDate": start_date_ms,
            "endDate": end_date_ms,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            f"/espapi/cloud/json/location/{location_id}/events",
            ep_params=params,
        )

    def get_location_priorities_history(): ...

    def get_countries(): ...

    def get_location_users(): ...

    def add_location_users(): ...

    def update_location_user(): ...

    def delete_location_user(): ...

    def add_sub_location(): ...

    def delete_sub_location(): ...

    def get_location_spaces(): ...

    def create_update_location_space(): ...

    def delete_location_space(): ...

    def get_narratives(
            self,
            location_id: int,
            row_count: int,
narrative_id: int = None,
narrative_time: int = None,
narrative_type: int = None,
scope: int = None,
priority: int = None,
to_priority: int = None,
status: int = None,
event_type: str = None,
search_by: str = None,
start_date_ms: int = None,
end_date_ms: int = None,
page_marker: str = None,
analytic_key: str = None,
    ):
        params = {
            "rowCount": row_count,
            "narrativeId": narrative_id,
            "narrativeTime": narrative_time,
            "narrativeType": narrative_type,
            "scope": scope,
            "priority": priority,
            "toPriority": to_priority,
            "status": status,
            "eventType": event_type,
            "searchBy": search_by,
            "startDate": start_date_ms,
            "endDate": end_date_ms,
            "pageMarker": page_marker,
        }
        params = {k: v for k, v in params.items() if v is not None}
        headers = None
        if analytic_key:
            headers = self.adapter._get_headers(analytic_key, APIKeyType.ANALYTIC)
        return self.adapter.get(
            f"/espapi/cloud/json/locations/{location_id}/narratives",
            ep_params=params,
            ep_headers=headers,
        )

    def put_narrative(
        self,
        location_id: int,
        scope: int,
        narrative: Dict,
        publish: bool = None,
        narrative_id: int = None,
        narrative_time_ms: int = None,
        analytic_key: str = None,
    ):
        params = {
            "scope": scope,
            "narrativeId": narrative_id,
            "narrativeTime": narrative_time_ms,
            "publish": publish,
        }
        params = {k: v for k, v in params.items() if v is not None}
        headers = None
        if analytic_key:
            headers = self.adapter._get_headers(analytic_key, APIKeyType.ANALYTIC)
        return self.adapter.put(
            f"/espapi/cloud/json/locations/{location_id}/narratives",
            ep_json=json.dumps(narrative),
            ep_params=params,
            ep_headers=headers,
        )

    def delete_a_narrative(
            self,
            location_id: int,
            scope: int,
            narrative_id: int,
            narrative_time_ms: int,
            publish: bool = None,
            event_type: str = None,
            analytic_key: str = None,
    ):
        params = {
            "scope": scope,
            "narrativeId": narrative_id,
            "narrativeTime": narrative_time_ms,
            "publish": publish,
            "eventType": event_type,
        }
        params = {k: v for k, v in params.items() if v is not None}
        headers = None
        if analytic_key:
            headers = self.adapter._get_headers(analytic_key, APIKeyType.ANALYTIC)
        return self.adapter.delete(
            f"/espapi/cloud/json/locations/{location_id}/narratives",
            ep_params=params,
            ep_headers=headers,
        )
    
    def stream_message(
        self,
        scope: str,
        address: str,
        feed: dict,
        location_id: int = None,
        organization_id: int = None,
        locations: List[int] = None,
        bots: List[int] = None,
    ):
        params = {
            "scope": scope,
            "address": address,
            "locationId": location_id,
            "organizationId": organization_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        body = {
            "locations": locations,
            "bots": bots,
            "feed": feed,
        }
        body = {k: v for k, v in body.items() if v is not None}
        headers = self.adapter._get_headers()
        if "ADMIN_KEY" in self.adapter._headers:
            headers = self.adapter._get_headers(
                self.adapter._headers.get("ADMIN_KEY"), 
                key_type=APIKeyType.USER
            )
        return self.adapter.post(
            "/espapi/cloud/appstore/stream",
            ep_json=body,
            ep_params=params,
            ep_headers=headers,
        )
    
    def get_summary(
        self,
        location_id: int,
        organization_id: int = None,
    ):
        params = {
            "locationId": location_id,
            "organizationId": organization_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        headers = self.adapter._get_headers()
        if "ADMIN_KEY" in self.adapter._headers:
            headers = self.adapter._get_headers(
                self.adapter._headers.get("ADMIN_KEY"), 
                key_type=APIKeyType.USER
            )
        return self.adapter.get(
            "/espapi/cloud/appstore/summary",
            ep_params=params,
            ep_headers=headers,
        )

    def put_state(
        self,
        location_id: int,
        name: str,
        state: Dict,
        overwrite: bool = None,
        publish: bool = None,
        updated: str = None,
        deleted: str = None,
    ):
        params = {
            "name": name,
            "overwrite": overwrite,
            "publish": publish,
            "upd": updated,
            "del": deleted,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.put(
            f"/espapi/cloud/json/locations/{location_id}/state",
            ep_json=json.dumps(state),
            ep_params=params,
        )


    def get_state(
        self,
        location_id: int,
        name: List[str] | str = None,
    ):
        params = {
            "name": name,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            f"/espapi/cloud/json/locations/{location_id}/state",
            ep_params=params,
        )

    def delete_states(
        self,
        location_id: int,
    ):
        params = {
            "locationId": location_id,
        }
        return self.adapter.delete(
            "/espapi/cloud/json/states",
            ep_params=params,
        )

    def put_time_state(
        self,
        location_id: int,
        name: str,
        timestamp_ms: int,
        state: Dict,
        overwrite: bool = None,
        publish: bool = None,
        updated: str = None,
        deleted: str = None,
    ):
        params = {
            "name": name,
            "timestampMs": timestamp_ms,
            "overwrite": overwrite,
            "publish": publish,
            "upd": updated,
            "del": deleted,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.put(
            f"/espapi/cloud/json/locations/{location_id}/timeStates",
            ep_json=json.dumps(state),
            ep_params=params,
        )

    def get_time_state(
            self,
            location_id: int,
            start_date_ms: int,
            end_date_ms: int = None,
            name: List[str] | str = None,
            field: List[str] | str = None,
            keep_parent: bool = None,
            aggregation: int = None,
    ):
        params = {
            "startDate": start_date_ms,
            "endDate": end_date_ms,
            "name": name,
            "field": field,
            "keepParent": keep_parent,
            "aggregation": aggregation,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            f"/espapi/cloud/json/locations/{location_id}/timeStates",
            ep_params=params,
        )

    def get_location_totals(): ...

    def get_presence_ids(): ...

    def add_location_presence(): ...


class Devices(API):
    def register_a_device(): ...

    def get_devices(
        self,
        location_id: int,
        user_id: int = None,
        check_persistent: bool = None,
        space_id: int = None,
        get_tags: bool = None,
        prospect: bool = None,
    ):
        params = {
            "locationId": location_id,
            "userId": user_id,
            "checkPersistent": check_persistent,
            "spaceId": space_id,
            "getTags": get_tags,
            "prospect": prospect,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            "/espapi/cloud/json/devices",
            ep_params=params,
        )


    def delete_multiple_devices(): ...

    def get_single_device(
        self,
        device_id: str,
        location_id: int,
        check_connected: bool = None,
    ):
        params = {
            "locationId": location_id,
            "checkConnected": check_connected,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            f"/espapi/cloud/json/devices/{device_id}",
            ep_params=params,
        )

    def get_device_services(): ...

    def update_device_attributes(): ...

    def remove_device_at_a_specific_location(): ...

    def device_sim_card(): ...

    def device_copy_simulator(): ...

    def get_device_activation_information(): ...

    def get_device_properties(
            self,
            device_id: str,
            location_id: int,
            name: str = None,
            index: str = None,
    ):
        params = {
            "locationId": location_id,
            "name": name,
            "index": index,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            f"/espapi/cloud/json/devices/{device_id}/properties",
            ep_params=params,
        )
        

    def set_device_properties(): ...

    def delete_device_property(): ...

    def link_device_to_space(): ...

    def unlink_device_from_space(): ...

    def get_firmware_update_jobs(): ...

    def set_firmware_update_status(): ...

    def get_device_logs(): ...

    def get_device_log_content(): ...

    def test_video_players(): ...

    def upload_sensitivity_map(): ...

    def delete_sensitivity_map(): ...


class DeviceMeasurements(API):
    def get_specific_device_parameters(
        self,
        device_id: str,
        location_id: int,   
        param_name: List[str] = None,
    ):
        params = {
            "locationId": location_id,
            "paramName": param_name,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            f"/espapi/cloud/json/devices/{device_id}/parameters",
            ep_params=params,
        )

    def get_multiple_device_parameters(): ...

    def send_device_command(
            self,
            device_id: str,
            location_id: int,
            command: Dict,
            skip_prospects: bool = None,
    ):
        params = {"locationId": location_id, "skipProspects": skip_prospects}
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.put(
            f"/espapi/cloud/json/devices/{device_id}/parameters",
            ep_json=json.dumps(command),
            ep_params=params,
        )

    def device_readings_history(
            self,
            device_id: str,
start_date_ms: int,
location_id: int,
end_date_ms: int = None,
parameter_names: List[str] = None,
parameter_index: str = None,
range_only: bool = None,
reduice_noise: bool = None,
interval: int = None,
aggregation: int = None,
sort_order: str = None,
    ):
        params = {
            "endDate": end_date_ms,
            "locationId": location_id,
            "parameterNames": parameter_names,
            "parameterIndex": parameter_index,
            "rangeOnly": range_only,
            "reduceNoise": reduice_noise,
            "interval": interval,
            "aggregation": aggregation,
            "sortOrder": sort_order,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            f"/espapi/cloud/json/devices/{device_id}/parametersByDate/{start_date_ms}",
            ep_params=params,
        )

    def last_device_readings(
            self,
            device_id: str,
            row_count: int,
            location_id: int,
            start_date_ms: int,
            end_date_ms: int = None,
            param_name: str = None,
            index: str = None,
            reduce_noise: bool = None,
    ):
        params = {
            "locationId": location_id,
            "startDate": start_date_ms,
            "endDate": end_date_ms,
            "paramName": param_name,
            "index": index,
            "reduceNoise": reduce_noise,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            f"/espapi/cloud/json/devices/{device_id}/parametersByCount/{row_count}",
            ep_params=params,
        )

    def get_device_alerts(): ...

    def submit_data_request(): ...

    def get_data_requests(): ...

    def get_units_of_measurement(): ...


class UserCommunication(API):
    def get_notification_subscriptions(): ...

    def set_notification_subscriptions(): ...

    def post_push_notification_token(): ...

    def delete_push_notification_token(): ...

    def send_notification(): ...

    def get_notifications(): ...

    def post_support_ticket(): ...

    def post_feedback(): ...

    def get_feedback_by_search(): ...

    def get_specific_feedback(): ...

    def vote_for_feedback(): ...

    def support(): ...

    def get_questions(
            self,
            location_id: int,
    answer_statuses: List[int] = None,
    editable: bool = None,
collection_name: str = None,
question_id: int = None,
appInstance_id: int = None,
lang: str = None,
limit: int = None,
    ):
        params = {
            "locationId": location_id,
            "answerStatus": answer_statuses,
            "editable": editable,
            "collectionName": collection_name,
            "questionId": question_id,
            "appInstanceId": appInstance_id,
            "lang": lang,
            "limit": limit,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            "/espapi/cloud/json/questions",
            ep_params=params,
        )

    def answer_questions(
            self,
            location_id: int,
            answers: Dict,
            check_if_valid: bool = None,
    ):
        params = {"locationId": location_id, "checkIfValid": check_if_valid}
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.put(
            "/espapi/cloud/json/questions",
            ep_json=json.dumps(answers),
            ep_params=params,
            ep_headers={"Content-Type": "application/json"} if check_if_valid else None,
        )

    def get_survey_questions(): ...

    def answer_survey_question(): ...

    def get_message_topics(
        self,
        app_id: int,
        language: str = None,
        analytic_key: str = None,
    ):
        params = {"appId": app_id, "language": language}
        params = {k: v for k, v in params.items() if v is not None}
        headers = None
        if analytic_key:
            headers = self.adapter._get_headers(analytic_key, APIKeyType.ANALYTIC)
        return self.adapter.get(
            "/espapi/cloud/json/messageTopics",
            ep_params=params,
            ep_headers=headers,
        )

    def create_messages(
            self,
            messages: Dict,
            location_id: int = None,
            analytic_key: str = None,
    ):
        params = {"locationId": location_id}
        params = {k: v for k, v in params.items() if v is not None}
        headers = None
        if analytic_key:
            headers = self.adapter._get_headers(analytic_key, APIKeyType.ANALYTIC)
        return self.adapter.post(
            "/espapi/cloud/json/messages",
            ep_json=json.dumps(messages),
            ep_params=params,
            ep_headers=headers,
        )

    def get_messages(
            self,
            location_id: int, 
            start_date_ms: int, 
            end_date_ms: int = None, 
            instance: int = None, 
            topic_id: int = None, 
            read_status: bool = None,
    ):
        params = {
            "locationId": location_id,
            "startDateMs": start_date_ms,
            "endDateMs": end_date_ms,
            "instance": instance,
            "topicId": topic_id,
            "readStatus": read_status,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            "/espapi/cloud/json/messages",
            ep_params=params,
        )
            

    def update_message_read_status(
            self,
            location_id: int,
            message_id: int,
            read_status: bool,
    ):
        params = {
            "locationId": location_id,
            "messageId": message_id,
            "readStatus": read_status,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.put(
            "/espapi/cloud/json/messages",
            ep_params=params,
        )


class SystemAndUserProperties(API):
    def get_property(): ...

    def get_user_properties(): ...

    def set_user_property(): ...

    def set_user_properties(): ...


class DeviceFiles(API):
    def upload_file(): ...

    def upload_a_binary_files_parts_or_thumbnail(): ...

    def get_files(): ...

    def delete_all_files(): ...

    def get_last_n_files(): ...

    def get_file_download_urls(): ...

    def download_file(): ...

    def update_file(): ...

    def delete_single_file(): ...

    def get_files_summary(): ...

    def get_file_info(): ...

    def get_file_devices(): ...

    def apply_file_tags(): ...

    def delete_file_tags(): ...

    def report_file(): ...


class AppFiles(API):
    def upload_file_content(): ...

    def get_files(): ...

    def download_file(): ...

    def delete_file(): ...


class Rules(API):
    def get_conditions_and_actions(): ...

    def create_update_rule(): ...

    def get_rules(): ...

    def delete_rules(): ...

    def update_rule_attrs(): ...

    def delete_rule(): ...

    def update_rules_status(): ...

    def create_default_rules(): ...


class PaidServices(API):
    def get_service_plans(): ...

    def post_an_apple_purchase_receipt(): ...

    def get_payment_profiles(): ...

    def post_purchase_info(): ...

    def update_purchase_info(): ...

    def upgrade_purchased_plan(): ...

    def get_location_service_plans(): ...

    def get_transactions(): ...

    def assign_services_to_location(): ...

    def assign_services_to_group_of_users(): ...

    def cancel_user_service_plan(): ...

    def get_market_products(): ...

    def get_chargify_token(): ...


class ProfessionalMonitoring(API):
    def get_call_center_settings(): ...

    def provide_call_center_settings(): ...

    def cancel_call_center(): ...

    def create_call_center_test(): ...

    def cancel_call_center_test(): ...

    def get_call_center_alerts(): ...


class EnergyManagement(API):
    def get_location_energy_usage(): ...

    def get_current_device_energy_usage(): ...

    def get_aggregated_device_energy_usage(): ...

    def get_billing_setting(): ...

    def put_billing_setting(): ...


class Weather(API):
    def get_weather(): ...


class DeviceTypesAndParameters(API):
    def get_device_types(
        self,
        device_type: int = None,
        attribute_name: str = None,
        attribute_value: str = None,
        own: bool = None,
        simple: bool = None,
        organization_id: int = None,
    ):
        params = {
            "deviceType": device_type,
            "attributeName": attribute_name,
            "attributeValue": attribute_value,
            "own": own,
            "simple": simple,
            "organizationId": organization_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            "/espapi/cloud/json/deviceTypes",
            ep_params=params,
        )

    def get_device_type_attributes(): ...

    def create_update_device_type(): ...

    def get_device_parameters(
            self,
            param_name: str = None,
    ):
        params = {
            "paramName": param_name,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            "/espapi/cloud/json/deviceParameters",
            ep_params=params,
        )

    def post_device_parameter(): ...

    def delete_device_parameter(): ...

    def put_device_parameter(): ...

    def get_default_rules(): ...

    def add_default_rule(): ...

    def delete_default_rule(): ...

    def get_device_goals_by_types(): ...

    def get_device_goal_installation_instruction(): ...

    def put_media(): ...

    def get_media(): ...

    def delete_media(): ...

    def put_device_models(): ...

    def get_device_models(): ...

    def delete_device_model_data(): ...

    def get_stories(): ...

    def put_stories(): ...

    def delete_story(): ...


class CloudsIntegration(API):
    def get_3rd_party_clouds(): ...

    def access_3rd_party_cloud(): ...

    def revoke_access_to_3rd_party_cloud(): ...

    def authorize_3rd_party_client(): ...

    def approve_or_deny_client_authorization(): ...

    def get_access_token(): ...

    def update_oauth_client(): ...

    def revoke_oauth_client(): ...


class RAG(API):
    def upload_document(): ...

    def get_documents(): ...

    def update_document(): ...

    def delete_document(): ...

    def post_questions(): ...

    def get_questions(): ...

    def update_questions(): ...


class Community(API):
    def get_community_posts(): ...

    def create_a_community_post(): ...

    def update_a_community_post(): ...

    def delete_a_community_post(): ...

    def comment_community_post(): ...

    def delete_a_comment(): ...

    def community_post_reaction(): ...

    def create_a_file(): ...

    def complete_a_file(): ...

    def delete_a_file(): ...

    def get_file_urls(): ...


class Websocket(API):
    def websocket(): ...
