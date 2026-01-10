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
    Runtime,
)
from .api import API


class BotDeveloper(API):
    def create_update_bot(
        self,
        bundle: str,
        data: Dict,
        developer_team: str = None,
    ):
        params = {"bundle": bundle, "developerTeam": developer_team}
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.put(
            "/espapi/cloud/developer/apps",
            ep_json=data,
            ep_params=params,
        )

    def create_update_bot_version(
        self,
        bundle: str,
        status: int = None,
        version: str = None,
        data: Dict = None,
    ):
        params = {"bundle": bundle, "status": status, "version": version}
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.put(
            "/espapi/cloud/developer/versions",
            ep_json=data,
            ep_params=params,
        )

    def upload_bot_code(
        self,
        data,
        content_type: str,
        bundle: str = None,
        runtime: int = None,
        source: bool = True,
        a_sync: bool = True,
        memory: int = None,
        timeout: int = None,
    ):
        params = {
            "bundle": bundle,
            "runtime": runtime,
            "source": source,
            "async": a_sync,
            "memory": memory,
            "timeout": timeout,
        }
        params = {k: v for k, v in params.items() if v is not None}
        headers = {"Content-Type": content_type}
        return self.adapter.post(
            "/espapi/cloud/developer/upload",
            ep_data=data,
            ep_params=params,
            ep_headers=headers,
        )

    def get_upload_bot_code_result(
        self,
        request_id: str,
    ):
        return self.adapter.get(
            f"/espapi/cloud/developer/upload/{request_id}",
        )

    def update_bot_parameters(
        self,
        bundle: str,
        memory: int,
        timeout: int,
        development: bool = None,
    ):
        params = {
            "memory": memory,
            "timeout": timeout,
            "development": development,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.put(
            "/espapi/cloud/developer/botParams/{}".format(bundle),
            ep_params=params,
        )

    def set_bot_version_status(
        self,
        bundle: str,
        status: int,
    ):
        params = {"bundle": bundle, "status": status}
        return self.adapter.put(
            "/espapi/cloud/developer/versionStatus",
            ep_params=params,
        )

    def get_bots(
        self,
        bundle: str = None
    ):
        params = {"bundle": bundle}
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get("/espapi/cloud/developer/apps", ep_params=params)

    def get_bot_versions(
        self,
        bundle: str,
        statuses: List[str] = None,
        version: str = None,
    ):
        params = {"bundle": bundle, "status": statuses, "version": version}
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get("/espapi/cloud/developer/versions", ep_params=params)

    def get_bot_statistics(
        self,
        bundle: str,
    ):
        params = {"bundle": bundle}
        return self.adapter.get(
            "/espapi/cloud/developer/stats",
            ep_params=params,
        )

    def upload_bot_object(
        self,
        name: str,
        bundle: str,
        data,
        content_type: str = "image/png",
    ):
        params = {"name": name, "bundle": bundle}
        headers = {"Content-Type": content_type}
        return self.adapter.put(
            f"/espapi/cloud/developer/apps/objects/{name}",
            ep_data=data,
            ep_params=params,
            ep_headers=headers,
        )

    def set_message_topics(
        self,
        bundle: str,
        topics: Dict,
    ):
        params = {"bundle": bundle}
        return self.adapter.put(
            "/espapi/cloud/developer/messageTopics",
            ep_json=json.dumps(topics),
            ep_params=params,
        )

    def get_execution_history(
        self,
        start_date_ms: int,
        end_date_ms: int,
        bundle: str = None,
        developer: bool = None,
        app_instance_id: int = None,
        flow: int = None,
        trigger: int = None,
        errors_only: bool = None,
        row_count: int = None,
        sort_order: str = None,
    ):
        params = {
            "startDate": start_date_ms,
            "endDate": end_date_ms,
            "bundle": bundle,
            "developer": developer,
            "appInstanceId": app_instance_id,
            "flow": flow,
            "trigger": trigger,
            "errorsOnly": errors_only,
            "rowCount": row_count,
            "sortOrder": sort_order,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            "/espapi/cloud/developer/executionHistory",
            ep_params=params,
        )

    def get_execution_info(
        self,
        app_instance_id: int,
        flow: int,
        request_date_ms: int,
    ):
        params = {
            "appInstanceId": app_instance_id,
            "flow": flow,
            "requestDate": request_date_ms,
        }
        return self.adapter.get(
            "/espapi/cloud/developer/executionInfo",
            ep_params=params,
        )

    def manage_bot_instance_logging(
        self,
        app_instance_id: int,
        flow: int,
        status: int,
        end_date_ms: int = None,
    ):
        params = {
            "appInstanceId": app_instance_id,
            "flow": flow,
            "status": status,
            "endDate": end_date_ms,  # TODO:  ISO 8601
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.put(
            "/espapi/cloud/developer/cloudwatchlog",
            ep_params=params,
        )

    def describe_bot_instance_logging(
        self,
        app_instance_id: int,
        flow: int,
    ):
        params = {"appInstanceId": app_instance_id, "flow": flow}
        return self.adapter.get(
            "/espapi/cloud/developer/cloudwatchlog",
            ep_params=params,
        )

    def export_bot_instance_log(
        self,
        app_instance_id: int,
        flow: int,
        start_date_ms: int,
        end_date_ms: int = None,
    ):
        params = {
            "appInstanceId": app_instance_id,
            "flow": flow,
            "startDate": start_date_ms,
            "endDate": end_date_ms,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.post(
            "/espapi/cloud/developer/cloudwatchlog/export",
            ep_params=params,
        )

    def get_exported_bot_instance_log(
        self,
        task_id: str,
    ):
        params = {"taskId": task_id}
        return self.adapter.get(
            "/espapi/cloud/developer/cloudwatchlog/export",
            ep_params=params,
        )


class DeveloperTeams(API):
    def create_team(
        self,
        team_name: str,
        description: str = None,
    ):
        data = {
            "name": team_name,
            "description": description,
        }
        data = {k: v for k, v in data.items() if v is not None}
        return self.adapter.post(
            "/espapi/cloud/developer/teams",
            ep_json=data,
        )

    def add_member(
        self,
        team_name: str,
        user_id: int = None,
        username: str = None,
        tester: bool = None,
    ):
        params = {
            "teamName": team_name,
            "userId": user_id,
            "username": username,
            "tester": tester,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.post(
            "/espapi/cloud/developer/teams/members",
            ep_params=params,
        )

    def remove_member(
        self,
        team_name: str,
        user_id: int = None,
        username: str = None,
    ):
        params = {
            "teamName": team_name,
            "userId": user_id,
            "username": username,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.delete(
            "/espapi/cloud/developer/teams/members",
            ep_params=params,
        )

    def get_teams(
        self,
        team_name: str = None,
        user_id: int = None,
        bundle: str = None,
    ):
        params = {
            "teamName": team_name,
            "userId": user_id,
            "bundle": bundle,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            "/espapi/cloud/developer/teams",
            ep_params=params,
        )

    def attach_teams(): ...


class BotStore(API):
    def add_bot_to_organization(
        self,
        bundle: str,
        organization_id: int,
    ):
        params = {"bundle": bundle}
        return self.adapter.post(
            f"/espapi/cloud/appstore/organizations/{organization_id}",
            ep_params=params,
        )

    def remove_bot_from_organization(
        self,
        bundle: str,
        organization_id: int,
    ):
        params = {"bundle": bundle}
        return self.adapter.delete(
            f"/espapi/cloud/appstore/organizations/{organization_id}",
            ep_params=params,
        )

    def approve_bot_for_organization(
        self,
        bundle: str,
        organization_id: int,
        status: int,
        development: bool = None,
    ):
        params = {
            "bundle": bundle,
            "status": status,
            "development": development,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.put(
            f"/espapi/cloud/appstore/organizations/{organization_id}",
            ep_params=params,
            ep_headers=self.adapter._get_headers(
                # Uses API_KEY with admin key type
                self.adapter._headers.get("ADMIN_KEY"),
                APIKeyType.USER,
            ),
        )

    def get_bot_organizations(
        self,
        bundle: str,
    ):
        params = {"bundle": bundle}
        return self.adapter.get(
            "/espapi/cloud/appstore/organizations",
            ep_params=params,
        )

    def search_bots(
        self,
        search_by: str = None,
        categories: List[str] = None,
        compatible: bool = None,
        lang: str = None,
        core: int = None,
        location_id: int = None,
        organization_id: int = None,
        object_names: List[str] = None,
        limit: int = None,
    ):
        params = {
            "searchBy": search_by,
            "categories": categories,
            "compatible": compatible,
            "lang": lang,
            "core": core,
            "locationId": location_id,
            "organizationId": organization_id,
            "objectNames": object_names,
            "limit": limit,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            "/espapi/cloud/appstore/search",
            ep_params=params,
        )

    def get_bot_info(
        self,
        bundle: str,
        lang: str = None,
        last_n_version: int = None,
        object_name: str = None,
    ):
        params = {
            "bundle": bundle,
            "lang": lang,
            "lastNVersion": last_n_version,
            "objectName": object_name,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            "/espapi/cloud/appstore/appinfo",
            ep_params=params,
        )

    def get_bot_object(): ...
    def purchase_bot(
        self,
        bundle: str,
        location_id: int = None,
        organization_id: int = None,
    ):
        params = {
            "bundle": bundle,
            "locationId": location_id,
            "organizationId": organization_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.post(
            "/espapi/cloud/appstore/appInstance",
            ep_params=params,
        )

    def configure_my_bot(
        self,
        app_instance_id: int,
        status: int = None,
        data: Dict = None,
    ):
        params = {"appInstanceId": app_instance_id, "status": status}
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.put(
            "/espapi/cloud/appstore/appInstance",
            ep_json=json.dumps(data),
            ep_params=params,
        )

    def get_my_bots(
        self,
        app_instance_id: int = None,
        bundle: str = None,
        location_id: int = None,
        organization_id: int = None,
        user_id: int = None,
        object_names: List[str] = None,
    ):
        params = {
            "appInstanceId": app_instance_id,
            "bundle": bundle,
            "locationId": location_id,
            "organizationId": organization_id,
            "userId": user_id,
            "objectNames": object_names,
        }
        params = {k: v for k, v in params.items() if v is not None}
        headers = self.adapter._get_headers()
        if "ADMIN_KEY" in self.adapter._headers:
            headers = self.adapter._get_headers(
                self.adapter._headers.get("ADMIN_KEY"), 
                key_type=APIKeyType.USER
            )
        return self.adapter.get(
            "/espapi/cloud/appstore/appInstance",
            ep_params=params,
            ep_headers=headers,
        )

    def remove_from_my_bots(
        self,
        app_instance_id: int,
    ):
        params = {"appInstanceId": app_instance_id}
        return self.adapter.delete(
            "/espapi/cloud/appstore/appInstance",
            ep_params=params,
        )

    def send_data_stream_message(
        self,
        scope: int,
        address: str,
        data: Dict,
        location_id: int = None,
        organization_id: int = None,
    ):
        params = {
            "scope": scope,
            "address": address,
            "locationId": location_id,
            "organizationId": organization_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.post(
            "/espapi/cloud/appstore/stream",
            ep_json=json.dumps(data),
            ep_params=params,
        )

    def get_summary(
        self,
        location_id: int = None,
        organization_id: int = None,
    ):
        params = {"locationId": location_id, "organizationId": organization_id}
        params = {k: v for k, v in params.items() if v is not None}
        return self.adapter.get(
            "/espapi/cloud/appstore/summary",
            ep_params=params,
        )
