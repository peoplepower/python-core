# API Endpoint Inventory: bot.py

| Endpoint Name | HTTP Method | Path | Parameters (Query/Body) | Response (Sample) | Implementing Method | Status |
|---|---|---|---|---|---|---|
| Create/Update Bot | PUT | /espapi/cloud/developer/apps | bundle, developerTeam, data (body) | JSON result | create_update_bot | To Review |
| Create/Update Bot Version | PUT | /espapi/cloud/developer/versions | bundle, status, version, data (body) | JSON result | create_update_bot_version | To Review |
| Upload Bot Code | POST | /espapi/cloud/developer/upload | bundle, runtime, source, async, memory, timeout, data (body), content-type (header) | JSON result | upload_bot_code | To Review |
| Get Upload Bot Code Result | GET | /espapi/cloud/developer/upload/{requestId} | requestId | JSON result | get_upload_bot_code_result | To Review |
| Update Bot Parameters | PUT | /espapi/cloud/developer/botParams/{bundle} | bundle, memory, timeout, development | JSON result | update_bot_parameters | To Review |
| Set Bot Version Status | PUT | /espapi/cloud/developer/versionStatus | bundle, status | JSON result | set_bot_version_status | To Review |
| Get Bots | GET | /espapi/cloud/developer/apps | bundle | Bots list | get_bots | To Review |
| Get Bot Versions | GET | /espapi/cloud/developer/versions | bundle, status, version | Versions list | get_bot_versions | To Review |
| Get Bot Statistics | GET | /espapi/cloud/developer/stats | bundle | Statistics | get_bot_statistics | To Review |
| Upload Bot Object | PUT | /espapi/cloud/developer/apps/objects/{name} | name, bundle, data (body), content-type (header) | JSON result | upload_bot_object | To Review |
| Set Message Topics | PUT | /espapi/cloud/developer/messageTopics | bundle, topics (body) | JSON result | set_message_topics | To Review |
| Get Execution History | GET | /espapi/cloud/developer/executionHistory | startDate, endDate, bundle, developer, appInstanceId, flow, trigger, errorsOnly, rowCount, sortOrder | Execution history | get_execution_history | To Review |
| Get Execution Info | GET | /espapi/cloud/developer/executionInfo | appInstanceId, flow, requestDate | Execution info | get_execution_info | To Review |
| Manage Bot Instance Logging | PUT | /espapi/cloud/developer/cloudwatchlog | appInstanceId, flow, status, endDate | JSON result | manage_bot_instance_logging | To Review |
| Describe Bot Instance Logging | GET | /espapi/cloud/developer/cloudwatchlog | appInstanceId, flow | Logging info | describe_bot_instance_logging | To Review |
| Export Bot Instance Log | POST | /espapi/cloud/developer/cloudwatchlog/export | appInstanceId, flow, startDate, endDate | JSON result | export_bot_instance_log | To Review |
| Get Exported Bot Instance Log | GET | /espapi/cloud/developer/cloudwatchlog/export | taskId | Log export result | get_exported_bot_instance_log | To Review |
| Create Team | POST | /espapi/cloud/developer/teams | name, description (body) | JSON result | create_team | To Review |
| Add Team Member | POST | /espapi/cloud/developer/teams/members | teamName, userId, username, tester | JSON result | add_member | To Review |
| Remove Team Member | DELETE | /espapi/cloud/developer/teams/members | teamName, userId, username | JSON result | remove_member | To Review |
| Get Teams | GET | /espapi/cloud/developer/teams | teamName, userId, bundle | Teams list | get_teams | To Review |
| Add Bot to Organization | POST | /espapi/cloud/appstore/organizations/{organizationId} | bundle | JSON result | add_bot_to_organization | To Review |
| Remove Bot from Organization | DELETE | /espapi/cloud/appstore/organizations/{organizationId} | bundle | JSON result | remove_bot_from_organization | To Review |
| Approve Bot for Organization | PUT | /espapi/cloud/appstore/organizations/{organizationId} | bundle, status, development | JSON result | approve_bot_for_organization | To Review |
| Get Bot Organizations | GET | /espapi/cloud/appstore/organizations | bundle | Organizations list | get_bot_organizations | To Review |
| Search Bots | GET | /espapi/cloud/appstore/search | searchBy, categories, compatible, lang, core, locationId, organizationId, objectNames, limit | Bots list | search_bots | To Review |
| Get Bot Info | GET | /espapi/cloud/appstore/appinfo | bundle, lang, lastNVersion, objectName | Bot info | get_bot_info | To Review |
| Purchase Bot | POST | /espapi/cloud/appstore/appInstance | bundle, locationId, organizationId | JSON result | purchase_bot | To Review |
| Configure My Bot | PUT | /espapi/cloud/appstore/appInstance | appInstanceId, status, data (body) | JSON result | configure_my_bot | To Review |
| Get My Bots | GET | /espapi/cloud/appstore/appInstance | appInstanceId, bundle, locationId, organizationId, userId, objectNames | Bots list | get_my_bots | To Review |
| Remove from My Bots | DELETE | /espapi/cloud/appstore/appInstance | appInstanceId | JSON result | remove_from_my_bots | To Review |
| Send Data Stream Message | POST | /espapi/cloud/appstore/stream | scope, address, data (body), locationId, organizationId | JSON result | send_data_stream_message | To Review |
| Get Summary | GET | /espapi/cloud/appstore/summary | locationId, organizationId | Summary | get_summary | To Review |

---

- Update the "Status" column as you review and implement each endpoint.
- Add more endpoints and details as needed.
- Use this file as a living document for API coverage tracking.
