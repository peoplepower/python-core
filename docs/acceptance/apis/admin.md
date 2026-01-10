# API Endpoint Inventory: admin.py

| Endpoint Name | HTTP Method | Path | Parameters (Query/Body) | Response (Sample) | Implementing Method | Status |
|---|---|---|---|---|---|---|
| Get Organizations | GET | /espapi/admin/json/organizations | organizationId, domainName, name | Organizations list | get_organizations | To Review |
| Delete Organization | DELETE | /espapi/admin/json/organizations | organizationId | JSON result | delete_organization | To Review |
| Create Organization | POST | /espapi/admin/json/organizations | organization info | JSON result | create_organization | To Review |
| Edit Organization | PUT | /espapi/admin/json/organizations | organizationId, organization info | JSON result | edit_organization | To Review |
| Get Organization Locations | GET | /espapi/admin/json/locations | organizationId, locationIds, searchBy, event, locationType, excludeType, searchTag, searchDeviceTag, deviceType, servicePlanId, stateId, countryId, priorityCategory, userRole, stateName, getTags, limit | Locations list | get_organization_locations | To Review |
| Create Organization Location | POST | /espapi/admin/json/locations | location info | JSON result | create_organization_location | To Review |
| Update Organization Location | PUT | /espapi/admin/json/locations | locationId, location info | JSON result | update_organization_location | To Review |
| Delete Organization Location | DELETE | /espapi/admin/json/locations | locationId | JSON result | delete_organization_location | To Review |
| Get Organization Devices | GET | /espapi/admin/json/devices | organizationId, groupId, userId, locationId, deviceId, deviceType, searchBy, searchTag, lessUpdateDate, moreUpdateDate, paramName, paramValue, limit, getTags | Devices list | get_organization_devices | To Review |
| Get Users | GET | /espapi/admin/json/users | filters | Users list | get_users | To Review |
| Get Roles | GET | /espapi/admin/json/roles | None | Roles list | get_roles | To Review |
| Grant User Role | POST | /espapi/admin/json/roles | userId, roleId | JSON result | grant_user_role | To Review |
| Revoke User Role | DELETE | /espapi/admin/json/roles | userId, roleId | JSON result | revoke_user_role | To Review |
| Get Organization Admins | GET | /espapi/admin/json/organizationAdmins | organizationId | Admins list | get_organization_admins | To Review |
| Add Organization Admin | POST | /espapi/admin/json/organizationAdmins | organizationId, userId | JSON result | add_organization_admin | To Review |
| Remove Organization Admin | DELETE | /espapi/admin/json/organizationAdmins | organizationId, userId | JSON result | remove_organization_admin | To Review |
| Get User Groups | GET | /espapi/admin/json/userGroups | filters | User groups list | get_user_groups | To Review |
| Create User Group | POST | /espapi/admin/json/userGroups | group info | JSON result | create_user_group | To Review |
| Update User Group | PUT | /espapi/admin/json/userGroups | groupId, group info | JSON result | update_user_group | To Review |
| Delete User Group | DELETE | /espapi/admin/json/userGroups | groupId | JSON result | delete_user_group | To Review |
| Add User Group Member | POST | /espapi/admin/json/userGroups/members | groupId, userId | JSON result | add_user_group_member | To Review |
| Remove User Group Member | DELETE | /espapi/admin/json/userGroups/members | groupId, userId | JSON result | remove_user_group_member | To Review |
| System Status | GET | /espapi/admin/json/systemStatus | None | System status | system_status | To Review |
| Upload Large Object | POST | /espapi/admin/json/objects | object data | JSON result | upload_large_object | To Review |
| Download Large Object | GET | /espapi/admin/json/objects/{objectId} | objectId | Object data | download_large_object | To Review |
| Delete Object | DELETE | /espapi/admin/json/objects/{objectId} | objectId | JSON result | delete_object | To Review |
| Get Objects and Properties | GET | /espapi/admin/json/objects/properties | filters | Objects/properties | get_objects_and_properties | To Review |
| Set Organization Properties | PUT | /espapi/admin/json/organizations/properties | organizationId, properties | JSON result | set_organization_properties | To Review |
| Organization Totals | GET | /espapi/admin/json/organizations/totals | organizationId | Totals | organization_totals | To Review |
| Get Bot Instances | GET | /espapi/admin/json/botInstances | filters | Bot instances | get_bot_instances | To Review |
| Create Organization Group | POST | /espapi/admin/json/organizationGroups | group info | JSON result | create_organization_group | To Review |
| Edit Organization Group | PUT | /espapi/admin/json/organizationGroups | groupId, group info | JSON result | edit_organization_group | To Review |
| Get Organization Groups | GET | /espapi/admin/json/organizationGroups | filters | Groups list | get_organization_groups | To Review |
| Remove Organization Group | DELETE | /espapi/admin/json/organizationGroups | groupId | JSON result | remove_organization_group | To Review |
| Test Camera Video Stream | POST | /espapi/admin/json/devices/cameraTest | deviceId, stream info | JSON result | test_camera_video_stream | To Review |
| Get Firmware Versions | GET | /espapi/admin/json/firmwareVersions | filters | Firmware versions | get_firmware_versions | To Review |
| Upload Firmware Version | POST | /espapi/admin/json/firmwareVersions | firmware info | JSON result | upload_firmware_version | To Review |
| Delete Firmware Version | DELETE | /espapi/admin/json/firmwareVersions | firmwareId | JSON result | delete_firmware_version | To Review |
| Update Device Firmware Group | PUT | /espapi/admin/json/devices/firmwareGroup | deviceId, group info | JSON result | update_device_firmware_group | To Review |
| Create Firmware Update Job | POST | /espapi/admin/json/firmwareUpdateJobs | job info | JSON result | create_firmware_update_job | To Review |
| Get Firmware Update Jobs | GET | /espapi/admin/json/firmwareUpdateJobs | filters | Jobs list | get_firmware_update_jobs | To Review |
| Delete Firmware Update Job | DELETE | /espapi/admin/json/firmwareUpdateJobs | jobId | JSON result | delete_firmware_update_job | To Review |
| Create Challenge | POST | /espapi/admin/json/challenges | challenge info | JSON result | create_challenge | To Review |
| Update Challenge | PUT | /espapi/admin/json/challenges | challengeId, challenge info | JSON result | update_challenge | To Review |
| Update Challenge Status | PUT | /espapi/admin/json/challenges/status | challengeId, status | JSON result | update_challenge_status | To Review |
| Get Challenges | GET | /espapi/admin/json/challenges | filters | Challenges list | get_challenges | To Review |
| Delete Challenge | DELETE | /espapi/admin/json/challenges | challengeId | JSON result | delete_challenge | To Review |
| Get Challenge Participants | GET | /espapi/admin/json/challenges/participants | challengeId | Participants | get_challenge_participants | To Review |
| Update Challenge Participant | PUT | /espapi/admin/json/challenges/participants | challengeId, participant info | JSON result | update_challenge_participant | To Review |
| Get Energy Usage | GET | /espapi/admin/json/energyUsage | filters | Usage data | get_energy_usage | To Review |
| Apply Tags | POST | /espapi/admin/json/tags | tag info | JSON result | apply_tags | To Review |
| Delete Tag | DELETE | /espapi/admin/json/tags | tagId | JSON result | delete_tag | To Review |
| Get Popular Tags | GET | /espapi/admin/json/tags/popular | filters | Tags list | get_popular_tags | To Review |
| Get Organization Narratives | GET | /espapi/admin/json/narratives | organizationId | Narratives | get_organization_narratives | To Review |
| Get Billing Items | GET | /espapi/admin/json/billing/items | filters | Billing items | get_billing_items | To Review |
| Create Billing Plan | POST | /espapi/admin/json/billing/plans | plan info | JSON result | create_billing_plan | To Review |
| Get Billing Plans | GET | /espapi/admin/json/billing/plans | filters | Plans list | get_billing_plans | To Review |
| Create Billing Plan Version | POST | /espapi/admin/json/billing/planVersions | version info | JSON result | create_billing_plan_version | To Review |
| Get Billing Plan Versions | GET | /espapi/admin/json/billing/planVersions | filters | Versions list | get_billing_plan_versions | To Review |
| Get Organization Billing Plans | GET | /espapi/admin/json/billing/organizationPlans | organizationId | Plans list | get_organization_billing_plans | To Review |
| Set Organization Billing Plan | PUT | /espapi/admin/json/billing/organizationPlans | organizationId, planId | JSON result | set_organization_billing_plan | To Review |
| Delete Organization Billing Plan | DELETE | /espapi/admin/json/billing/organizationPlans | organizationId, planId | JSON result | delete_organization_billing_plan | To Review |
| Generate Bill | POST | /espapi/admin/json/billing/bills | bill info | JSON result | generate_bill | To Review |
| Get Bills | GET | /espapi/admin/json/billing/bills | filters | Bills list | get_bills | To Review |
| Get Bill Content | GET | /espapi/admin/json/billing/bills/content | billId | Bill content | get_bill_content | To Review |

---

- Update the "Status" column as you review and implement each endpoint.
- Add more endpoints and details as needed.
- Use this file as a living document for API coverage tracking.
