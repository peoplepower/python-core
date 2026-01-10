# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///

from typing import List

from .api import API

from ..models import (
    APIKeyType,
)

class System(API):
    def system_status(): ...


class Organizations(API):
    def create_organization(): ...
    def edit_organization(): ...
    def get_organizations(
        self,
        organization_id: int = None,
        domain_name: str = None,
        name: str = None,
    ):
        params = {
            "organizationId": organization_id,
            "domainName": domain_name,
            "name": name,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            "/espapi/admin/json/organizations",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                self.adapter._headers.get("ADMIN_KEY"), 
                key_type=APIKeyType.USER
            )
        )
            

    def delete_organization(): ...
    def upload_large_object(): ...
    def download_large_object(): ...
    def delete_object(): ...
    def get_objects_and_properties(): ...
    def set_organization_properties(): ...
    def organization_totals(): ...
    def get_bot_instances(): ...


class Groups(API):
    def create_organization_group(): ...
    def edit_organization_group(): ...
    def get_organization_groups(): ...
    def remove_organization_group(): ...


class Users(API):
    def get_users(): ...
    def get_roles(): ...
    def grant_user_role(): ...
    def revoke_user_role(): ...
    def get_organization_admins(): ...
    def add_organization_admin(): ...
    def remove_organization_admin(): ...
    def get_notification_users(): ...
    def update_notification_user(): ...


class UserGroups(API):
    def create_user_group(): ...
    def update_user_group(): ...
    def get_user_groups(): ...
    def delete_user_group(): ...
    def add_user_group_member(): ...
    def remove_user_group_member(): ...


class Locations(API):
    def get_organization_locations(
        self,
        organization_id: int = None,
        location_ids: List[int] = None,
        search_by: str = None,
        event: str = None,
        location_type: List[int] = None,
        exclude_type: List[int] = None,
        search_tag: List[str] = None,
        search_device_tag: List[str] = None,
        device_type: List[int] = None,
        service_plan_id: int = None,
        state_id: int = None,
        country_id: int = None,
        priority_category: List[int] = None,
        user_role: int = None,
        state_name: str = None,
        get_tags: bool = None,
        limit: int = None,
    ):
        params = {
            "organizationId": organization_id,
            "locationIds": location_ids,
            "searchBy": search_by,
            "event": event,
            "locationType": location_type,
            "excludeType": exclude_type,
            "searchTag": search_tag,
            "searchDeviceTag": search_device_tag,
            "deviceType": device_type,
            "servicePlanId": service_plan_id,
            "stateId": state_id,
            "countryId": country_id,
            "priorityCategory": priority_category,
            "userRole": user_role,
            "stateName": state_name,
            "getTags": get_tags,
            "limit": limit,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result = self.adapter.get(
            "/espapi/admin/json/locations",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                self.adapter._headers.get("ADMIN_KEY"), 
                key_type=APIKeyType.USER
            ),
        )
        return result

    def create_organization_location(): ...
    def update_organization_location(): ...
    def delete_organization_location(): ...
    def add_update_delete_organization_locations(): ...


class Devices(API):
    def get_organization_devices(
            self,
            organization_id: int,
            group_id: int = None,
            user_id: int = None,
            location_id: int = None,
            device_id: str = None,
            device_type: int = None,
            searchBy: str = None,
            search_tag: str = None,
            less_update_date: str = None,
            more_update_date: str = None,
            param_name: str = None,
            param_value: str = None,
            limit: int = None,
            get_tags: bool = None,
    ):
        params = {
            "organizationId": organization_id,
            "groupId": group_id,
            "userId": user_id,
            "locationId": location_id,
            "deviceId": device_id,
            "deviceType": device_type,
            "searchBy": searchBy,
            "searchTag": search_tag,
            "lessUpdateDate": less_update_date,
            "moreUpdateDate": more_update_date,
            "paramName": param_name,
            "paramValue": param_value,
            "limit": limit,
            "getTags": get_tags,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result = self.adapter.get(
            "/espapi/admin/json/devices",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                # Uses API_KEY with admin key type
                {"API_KEY": self.adapter._headers.get("ADMIN_KEY")}
            ),
        )
        return result
    def test_camera_video_stream(): ...
    def get_firmware_versions(): ...
    def upload_firmware_version(): ...
    def delete_firmware_version(): ...
    def update_device_firmware_group(): ...
    def create_firmware_update_job(): ...
    def get_firmware_update_jobs(): ...
    def delete_firmware_update_job(): ...


class Challenges(API):
    def create_challenge(): ...
    def update_challenge(): ...
    def update_challenge_status(): ...
    def get_challenges(): ...
    def delete_challenge(): ...
    def get_challenge_participants(): ...
    def update_challenge_participant(): ...
    def get_energy_usage(): ...


class Tags(API):
    def apply_tags(): ...
    def delete_tag(): ...
    def get_popular_tags(): ...


class Narratives(API):
    def get_organization_narratives(): ...


class Billing(API):
    def get_billing_items(): ...
    def create_billing_plan(): ...
    def get_billing_plans(): ...
    def create_billing_plan_version(): ...
    def get_billing_plan_versions(): ...
    def get_organization_billing_plans(): ...
    def set_organization_billing_plan(): ...
    def delete_organization_billing_plan(): ...
    def generate_bill(): ...
    def get_bills(): ...
    def get_bill_content(): ...
