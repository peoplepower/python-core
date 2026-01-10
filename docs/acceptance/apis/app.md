# API Endpoint Inventory: app.py

| Endpoint Name | HTTP Method | Path | Parameters (Query/Body) | Response (Sample) | Implementing Method | Status |
|---|---|---|---|---|---|---|
| Check Availability | GET | /espapi/watch | None | 200 OK (text/plain) | check_availability | To Review |
| Get Version | GET | /espapi/version | version (bool), json (bool) | JSON version info | get_version | To Review |
| Get Cloud Settings | GET | /espapi/cloud/json/settings | device_id, connected, version | JSON cloud info | get_cloud_settings | To Review |
| Get Server Settings | GET | /espapi/cloud/json/settingsServer/{type} | crtTag, deviceId, connected, brand, appName | JSON server info | get_server_settings | To Review |
| Get Server Settings URL | GET | /espapi/cloud/json/settingsServer | type, deviceId, connected, ssl, brand, appName | Plain text URL | get_server_settings_url | To Review |
| Get Cloud Instances | GET | /espapi/cloud/json/settingsCloud | deviceId | JSON cloud instance | get_cloud_instances | To Review |
| Login by Username | GET | /espapi/cloud/json/login | username, password, passcode, expiry, keyType, appName, brand, clientId, prefDeliveryType, smsPrefix, appHash, totp, sign, signAlgorithm | API key | login_by_username | To Review |
| Send Passcode | GET | /espapi/cloud/json/passcode | username, prefDeliveryType, brand, prefix, appHash | JSON result | send_passcode | To Review |
| Login by Key | GET | /espapi/cloud/json/loginByKey | key, passcode, keyType, expiry, prefDeliveryType, brand, clientId | API key | login_by_key | To Review |
| Logout | GET | /espapi/cloud/json/logout | API key (header) | JSON result | logout | To Review |
| Create TOTP Secret | POST | /espapi/cloud/json/totp | name, issuer | TOTP secret and URL | create_totp_factor | To Review |
| Confirm TOTP Secret | PUT | /espapi/cloud/json/totp | name, code | JSON result | confirm_totp_factor | To Review |
| Get TOTP Factors | GET | /espapi/cloud/json/totp | None | TOTP factors | get_totp_factors | To Review |
| Delete TOTP Factor | DELETE | /espapi/cloud/json/totp | name | JSON result | delete_totp_factor | To Review |
| Get Private Key | GET | /espapi/cloud/json/signatureKey | appName | Private key | get_private_key | To Review |
| Put Public Key | PUT | /espapi/cloud/json/signatureKey | appName, publicKey | JSON result | get_public_key | To Review |
| Get Operation Token | GET | /espapi/cloud/json/token | type | Operation token | get_operation_token | To Review |
| Create User Account | POST | /espapi/cloud/json/user | user info | JSON result | create_user_account | To Review |
| Get User Information | GET | /espapi/cloud/json/user | userId, organizationId | User info | get_user_information | To Review |
| Update User | PUT | /espapi/cloud/json/user | userId, user info | JSON result | update_user | To Review |
| Delete User | DELETE | /espapi/cloud/json/user | userId | JSON result | delete_user | To Review |
| Get Pronouns | GET | /espapi/cloud/json/pronouns | None | Pronouns | get_pronouns | To Review |
| Send Verification Message | GET | /espapi/cloud/json/emailVerificationMessage | type, brand | JSON result | send_verification_message | To Review |
| Provide Verification Code | PUT | /espapi/cloud/json/emailVerificationMessage | code, type | JSON result | provide_verification_code | To Review |
| Update Password | PUT | /espapi/cloud/json/userPassword | password info | JSON result | put_new_password | To Review |
| Recover Password | POST | /espapi/cloud/json/recoverPassword | email | JSON result | recover_password | To Review |
| Reset User Badges | PUT | /espapi/cloud/json/userBadges | userId | JSON result | reset_user_badges | To Review |
| Get Terms of Service | GET | /espapi/cloud/json/termsOfServices | signatureId | Terms of Service | get_terms_of_service | To Review |
| Sign Terms of Service | PUT | /espapi/cloud/json/termsOfServices/{signatureId} | signatureId | JSON result | put_terms_of_service | To Review |
| Apply Tag | PUT | /espapi/cloud/json/usertags/{tag} | tag | JSON result | put_user_tag | To Review |
| Delete User Tag | DELETE | /espapi/cloud/json/usertags/{tag} | tag | JSON result | delete_user_tag | To Review |
| Put User Code | PUT | /espapi/cloud/json/userCodes | name, locationId, type, code, deviceId, setExpiry, verify | JSON result | put_user_code | To Review |
| Get User Codes | GET | /espapi/cloud/json/userCodes | None | Codes | get_user_codes | To Review |
| Delete User Code | DELETE | /espapi/cloud/json/userCodes | name, locationId | JSON result | delete_user_code | To Review |
| Create Location | POST | /espapi/cloud/json/location | location info | JSON result | create_location | To Review |
| Update Location | PUT | /espapi/cloud/json/location/{locationId} | locationId, data | JSON result | update_location | To Review |
| Delete Location | DELETE | /espapi/cloud/json/location/{locationId} | locationId | JSON result | delete_location | To Review |
| Move Location to Organization | PUT | /espapi/cloud/json/location/{locationId}/organization/{domainName} | locationId, domainName | JSON result | put_location_to_organization | To Review |
| Change Scene at Location | POST | /espapi/cloud/json/location/{locationId}/event/{eventName} | locationId, eventName, comment | JSON result | post_location_event | To Review |
| Location Scenes History | GET | /espapi/cloud/json/location/{locationId}/events | locationId, startDate, endDate | Events | get_location_events_history | To Review |
| Location Priorities History | GET | /espapi/cloud/json/location/{locationId}/priorities | locationId, startDate, endDate, priority | Priorities | get_location_priorities_history | To Review |
| Get Countries | GET | /espapi/cloud/json/countries | organizationId, countryCode, lang | Countries | get_countries | To Review |
| Get Location Users | GET | /espapi/cloud/json/location/{locationId}/users | locationId | Users | get_location_users | To Review |
| Add Location Users | PUT | /espapi/cloud/json/location/{locationId}/users | locationId, users | JSON result | add_location_users | To Review |
| Update Location User | PUT | /espapi/cloud/json/location/{locationId}/users | locationId, user info | JSON result | update_location_user | To Review |
| Delete Location User | DELETE | /espapi/cloud/json/location/{locationId}/users | locationId, userId | JSON result | delete_location_user | To Review |
| Add Sub-Location | PUT | /espapi/cloud/json/location/{locationId}/subs | locationId, subLocationId, startDate | JSON result | add_sub_location | To Review |
| Delete Sub-Location | DELETE | /espapi/cloud/json/location/{locationId}/subs | locationId, subLocationId | JSON result | delete_sub_location | To Review |
| Get Location Spaces | GET | /espapi/cloud/json/location/{locationId}/spaces | locationId | Spaces | get_location_spaces | To Review |
| Delete Location Space | DELETE | /espapi/cloud/json/location/{locationId}/spaces | locationId, spaceId | JSON result | delete_location_space | To Review |
| Get Narratives | GET | /espapi/cloud/json/locations/{locationId}/narratives | locationId, filters | Narratives | get_narratives | To Review |
| Put Narrative | PUT | /espapi/cloud/json/locations/{locationId}/narratives | locationId, narrative info | JSON result | put_narrative | To Review |
| Delete a Narrative | DELETE | /espapi/cloud/json/locations/{locationId}/narratives | locationId, narrativeId, narrativeTime | JSON result | delete_a_narrative | To Review |
| Stream Message | POST | /espapi/cloud/appstore/stream | scope, address, feed, locationId, organizationId, locations, bots | JSON result | stream_message | To Review |
| Get Summary | GET | /espapi/cloud/appstore/summary | locationId, organizationId | Summary | get_summary | To Review |
| Put State | PUT | /espapi/cloud/json/locations/{locationId}/state | locationId, name, state, overwrite, publish, upd, del | JSON result | put_state | To Review |
| Get State | GET | /espapi/cloud/json/locations/{locationId}/state | locationId, name | State | get_state | To Review |
| Delete States | DELETE | /espapi/cloud/json/states | locationId | JSON result | delete_states | To Review |
| Put Time State | PUT | /espapi/cloud/json/locations/{locationId}/timeStates | locationId, name, timestampMs, state, overwrite, publish, upd, del | JSON result | put_time_state | To Review |
| Get Time State | GET | /espapi/cloud/json/locations/{locationId}/timeStates | locationId, startDate, endDate, name, field, keepParent, aggregation | Time-series States | get_time_state | To Review |
| Get Location Totals | GET | /espapi/cloud/json/locationTotals | locationId, devices, files, rules | Totals | get_location_totals | To Review |
| Get Presence IDs | GET | /espapi/cloud/json/presence | paramsMap | JSON result | get_presence_ids | To Review |
| Add Location Presence | POST | /espapi/cloud/json/presence | paramsMap | JSON result | add_location_presence | To Review |
| Register a Device | POST | /espapi/cloud/json/devices | device info | JSON result | register_a_device | To Review |
| Get Devices | GET | /espapi/cloud/json/devices | locationId, userId, checkPersistent, spaceId, getTags, prospect | Devices | get_devices | To Review |
| Delete Multiple Devices | DELETE | /espapi/cloud/json/devices | deviceId(s), locationId, keepOnAccount, keepSlave, keepSlaveOnGateway, clear | JSON result | delete_multiple_devices | To Review |
| Get Single Device | GET | /espapi/cloud/json/devices/{deviceId} | deviceId, locationId, checkConnected | Device info | get_device | To Review |
| Get Device Services | GET | /espapi/cloud/json/devices/{deviceId}/services | deviceId | Services | get_device_services | To Review |
| Update Device Attributes | PUT | /espapi/cloud/json/devices/{deviceId} | deviceId, attributes | JSON result | update_device_attributes | To Review |
| Remove Device at Location | DELETE | /espapi/cloud/json/locations/{locationId}/devices/{deviceId} | locationId, deviceId, keepOnAccount, keepSlave, keepSlaveOnGateway, clear | JSON result | remove_device_at_a_specific_location | To Review |
| Device SIM Card | PUT | /espapi/cloud/json/locations/{locationId}/devices/{deviceId}/simCard | locationId, deviceId, status, simId | JSON result | device_sim_card | To Review |
| Device Copy Simulator | POST | /espapi/cloud/json/locations/{locationId}/devices/{deviceId}/copySimulator | locationId, deviceId, simulatedLocationId | JSON result | device_copy_simulator | To Review |
| Get Device Activation Info | GET | /espapi/cloud/json/locations/{locationId}/deviceActivation/{deviceType} | locationId, deviceType, sendEmail | Activation info | get_device_activation_information | To Review |
| Get Device Properties | GET | /espapi/cloud/json/devices/{deviceId}/properties | deviceId, locationId, name, index | Properties | get_device_properties | To Review |
| Set Device Properties | PUT | /espapi/cloud/json/devices/{deviceId}/properties | deviceId, locationId, properties | JSON result | set_device_properties | To Review |
| Delete Device Property | DELETE | /espapi/cloud/json/devices/{deviceId}/properties | deviceId, locationId, name | JSON result | delete_device_property | To Review |
| Link Device to Space | PUT | /espapi/cloud/json/locations/{locationId}/devices/{deviceId}/spaces/{spaceId} | locationId, deviceId, spaceId | JSON result | link_device_to_space | To Review |
| Unlink Device from Space | DELETE | /espapi/cloud/json/locations/{locationId}/devices/{deviceId}/spaces/{spaceId} | locationId, deviceId, spaceId | JSON result | unlink_device_from_space | To Review |
| Get Firmware Update Jobs | GET | /espapi/cloud/json/fwupdate | deviceId, locationId | Jobs | get_firmware_update_jobs | To Review |
| Set Firmware Update Status | PUT | /espapi/cloud/json/fwupdate | deviceId, status, index, startDate, userId | JSON result | set_firmware_update_status | To Review |
| Get Device Logs | GET | /espapi/cloud/json/deviceLogs | locationId, deviceId, startDate, endDate | Logs | get_device_logs | To Review |
| Get Device Log Content | GET | /espapi/cloud/json/deviceLogContent | locationId, deviceId, logDate | Log content URL | get_device_log_content | To Review |
| Test Video Players | GET | /espapi/cloud/json/testVideoPlayers | deviceId | JSON result | test_video_players | To Review |
| Upload Sensitivity Map | POST | /espapi/cloud/json/devices/{deviceId}/sensitivityMap | deviceId | JSON result | upload_sensitivity_map | To Review |
| Delete Sensitivity Map | DELETE | /espapi/cloud/json/devices/{deviceId}/sensitivityMap | deviceId | JSON result | delete_sensitivity_map | To Review |
| Get Specific Device Parameters | GET | /espapi/cloud/json/devices/{deviceId}/parameters | deviceId, locationId, paramName | Parameters | get_specific_device_parameters | To Review |
| Get Multiple Device Parameters | GET | /espapi/cloud/json/parameters | locationId, deviceId, paramName | Parameters | get_multiple_device_parameters | To Review |
| Send Device Command | PUT | /espapi/cloud/json/devices/{deviceId}/parameters | deviceId, locationId, command, skipProspects | JSON result | send_device_command | To Review |
| Device Readings History | GET | /espapi/cloud/json/devices/{deviceId}/parametersByDate/{startDate} | deviceId, startDate, locationId, endDate, parameterNames, parameterIndex, rangeOnly, reduceNoise, interval, aggregation, sortOrder | Readings | device_readings_history | To Review |
| Last Device Readings | GET | /espapi/cloud/json/devices/{deviceId}/parametersByCount/{rowCount} | deviceId, rowCount, locationId, startDate, endDate, paramName, index, reduceNoise | Readings | last_device_readings | To Review |
| Get Device Alerts | GET | /espapi/cloud/json/deviceAlerts | deviceId, locationId, startDate, endDate | Alerts | get_device_alerts | To Review |
| Submit Data Request | POST | /espapi/cloud/json/dataRequests | locationId, brand, byEmail, dataRequests | JSON result | submit_data_request | To Review |
| Get Data Requests | GET | /espapi/cloud/json/dataRequests | locationId, organizationId, requestKey | Data requests | get_data_requests | To Review |
| Get Units of Measurement | GET | /espapi/cloud/json/units | None | Units | get_units_of_measurement | To Review |
| Get Notification Subscriptions | GET | /espapi/cloud/json/notificationSubscriptions | userId | Subscriptions | get_notification_subscriptions | To Review |
| Set Notification Subscriptions | PUT | /espapi/cloud/json/notificationSubscriptions | userId, subscriptions | JSON result | set_notification_subscriptions | To Review |
| Post Push Notification Token | PUT | /espapi/cloud/json/notificationToken/{appName}/{token} | appName, token, badge, brand | JSON result | post_push_notification_token | To Review |
| Delete Push Notification Token | DELETE | /espapi/cloud/json/notificationToken/{token} | token | JSON result | delete_push_notification_token | To Review |
| Send Notification | POST | /espapi/cloud/json/notifications | userId, locationId, organizationId, brand, userCategories, users, language, pushMessage, emailMessage, smsMessage, deviceMessage | JSON result | send_notification | To Review |
| Get Notifications | GET | /espapi/cloud/json/notifications | userId, startDate, endDate, locationId, sourceType, deliveryType, notificationType | Notifications | get_notifications | To Review |
| Post Support Ticket | POST | /espapi/cloud/json/support | appName, firstName, lastName, email, subject, text, subscribe | JSON result | post_support_ticket | To Review |
| Post Feedback | POST | /espapi/cloud/json/feedback | feedback | JSON result | post_feedback | To Review |
| Get Feedback by Search | GET | /espapi/cloud/json/feedback/{appName}/{type} | appName, type, startPos, length, productId, productCategory, disabled | Feedbacks | get_feedback_by_search | To Review |
| Get Specific Feedback | GET | /espapi/cloud/json/feedback/{feedbackId} | feedbackId | Feedback | get_specific_feedback | To Review |
| Vote for Feedback | PUT | /espapi/cloud/json/feedback/{feedbackId}/{rank} | feedbackId, rank | JSON result | vote_for_feedback | To Review |
| Support | POST | /espapi/cloud/json/support | support info | JSON result | support | To Review |
| Get Questions | GET | /espapi/cloud/json/questions | locationId, answerStatus, editable, collectionName, questionId, appInstanceId, lang, limit | Questions | get_questions | To Review |
| Answer Questions | PUT | /espapi/cloud/json/questions | locationId, answers, checkIfValid | JSON result | answer_questions | To Review |
| Get Survey Questions | GET | /espapi/cloud/json/surveys | brand | Questions | get_survey_questions | To Review |
| Answer Survey Question | PUT | /espapi/cloud/json/surveys | question | JSON result | answer_survey_question | To Review |
| Get Message Topics | GET | /espapi/cloud/json/messageTopics | appId, language | Topics | get_message_topics | To Review |
| Create Messages | POST | /espapi/cloud/json/messages | messages, locationId | JSON result | create_messages | To Review |
| Get Messages | GET | /espapi/cloud/json/messages | locationId, startDateMs, endDateMs, instance, topicId, readStatus | Messages | get_messages | To Review |
| Update Message Read Status | PUT | /espapi/cloud/json/messages | locationId, messageId, readStatus | JSON result | update_message_read_status | To Review |
| Get Property | GET | /espapi/cloud/json/systemProperty/{propertyName} | propertyName | Property value | get_property | To Review |
| Get User Properties | GET | /espapi/cloud/json/userProperty/{name} | name, userId | Property value | get_user_properties | To Review |
| Set User Property | PUT | /espapi/cloud/json/userProperty/{name} | name, value, userId | JSON result | set_user_property | To Review |
| Set User Properties | PUT | /espapi/cloud/json/userProperties | properties | JSON result | set_user_properties | To Review |
| Upload Device File | POST | /espapi/cloud/json/files | file info | JSON result | upload_file | To Review |
| Upload Device File Fragment | POST | /espapi/cloud/json/files/{fileId} | fileId, proxyId, thumbnail, incomplete, index | JSON result | upload_a_binary_files_parts_or_thumbnail | To Review |
| Get Device Files | GET | /espapi/cloud/json/files | locationId, type, owners, ownerId, deviceId, deviceDescription, startDate, endDate | Files | get_files | To Review |
| Delete All Device Files | DELETE | /espapi/cloud/json/files | locationId | JSON result | delete_all_files | To Review |
| Get Last Device Files | GET | /espapi/cloud/json/filesByCount/{count} | count, locationId, startDate, endDate, type, deviceId, deviceDescription | Files | get_last_n_files | To Review |
| Get Device File Download URLs | GET | /espapi/cloud/json/files/{fileId}/url | fileId, locationId, content, thumbnail, expiration | URLs | get_file_download_urls | To Review |
| Download Device File | GET | /espapi/cloud/json/files/{fileId} | fileId, userId, locationId, attach, Range | File content | download_file | To Review |
| Update Device File | PUT | /espapi/cloud/json/files/{fileId} | fileId, attributes | JSON result | update_file | To Review |
| Delete Single Device File | DELETE | /espapi/cloud/json/files/{fileId} | fileId, locationId | JSON result | delete_single_file | To Review |
| Get Files Summary | GET | /espapi/cloud/json/filesSummary/{aggregation} | aggregation, locationId, startDate, endDate | Summary | get_files_summary | To Review |
| Get File Info | GET | /espapi/cloud/json/filesInfo/{fileId} | fileId, locationId | File info | get_file_info | To Review |
| Get File Devices | GET | /espapi/cloud/json/fileDevices | locationId | Devices | get_file_devices | To Review |
| Apply File Tags | PUT | /espapi/cloud/json/files/{fileId}/tags | fileId, tags | JSON result | apply_file_tags | To Review |
| Delete File Tags | DELETE | /espapi/cloud/json/files/{fileId}/tags | fileId, tags | JSON result | delete_file_tags | To Review |
| Report File | POST | /espapi/cloud/json/files/{fileId}/report | fileId, report | JSON result | report_file | To Review |
| Upload App File Content | POST | /espapi/cloud/json/appfiles | file info | JSON result | upload_file_content | To Review |
| Get App Files | GET | /espapi/cloud/json/appfiles | fileId, type, userId, locationId, deviceId, name | Files | get_files | To Review |
| Download App File | GET | /espapi/cloud/json/appfiles/{fileId} | fileId, userId, locationId, attach, Range | File content | download_file | To Review |
| Delete App File | DELETE | /espapi/cloud/json/appfiles/{fileId} | fileId, userId, locationId | JSON result | delete_file | To Review |
| Get Rule Conditions and Actions | GET | /espapi/cloud/json/rules/conditions |  | List of conditions/actions | get_conditions_and_actions | To Review |
| Create or Update Rule | PUT | /espapi/cloud/json/rules | rule | Rule result | create_update_rule | To Review |
| Get Rules | GET | /espapi/cloud/json/rules | filters | List of rules | get_rules | To Review |
| Delete Rules | DELETE | /espapi/cloud/json/rules | ruleIds | Deletion result | delete_rules | To Review |
| Update Rule Attributes | PUT | /espapi/cloud/json/rules/attrs | attrs | Update result | update_rule_attrs | To Review |
| Delete Rule | DELETE | /espapi/cloud/json/rules/{ruleId} | ruleId | Deletion result | delete_rule | To Review |
| Update Rules Status | PUT | /espapi/cloud/json/rules/status | status | Update result | update_rules_status | To Review |
| Create Default Rules | POST | /espapi/cloud/json/rules/default | params | Default rules result | create_default_rules | To Review |
| Get Service Plans | GET | /espapi/cloud/json/servicePlans | filters | List of plans | get_service_plans | To Review |
| Post Apple Purchase Receipt | POST | /espapi/cloud/json/purchase/apple | receipt | Purchase result | post_an_apple_purchase_receipt | To Review |
| Get Payment Profiles | GET | /espapi/cloud/json/paymentProfiles | filters | List of profiles | get_payment_profiles | To Review |
| Post Purchase Info | POST | /espapi/cloud/json/purchase | info | Purchase result | post_purchase_info | To Review |
| Update Purchase Info | PUT | /espapi/cloud/json/purchase | info | Update result | update_purchase_info | To Review |
| Upgrade Purchased Plan | POST | /espapi/cloud/json/purchase/upgrade | planId | Upgrade result | upgrade_purchased_plan | To Review |
| Get Location Service Plans | GET | /espapi/cloud/json/locationServicePlans | locationId | List of plans | get_location_service_plans | To Review |
| Get Transactions | GET | /espapi/cloud/json/transactions | filters | List of transactions | get_transactions | To Review |
| Assign Services to Location | POST | /espapi/cloud/json/locationServicePlans/assign | params | Assignment result | assign_services_to_location | To Review |
| Assign Services to Group of Users | POST | /espapi/cloud/json/userServicePlans/assign | params | Assignment result | assign_services_to_group_of_users | To Review |
| Cancel User Service Plan | POST | /espapi/cloud/json/userServicePlans/cancel | params | Cancel result | cancel_user_service_plan | To Review |
| Get Market Products | GET | /espapi/cloud/json/marketProducts | filters | List of products | get_market_products | To Review |
| Get Chargify Token | GET | /espapi/cloud/json/chargifyToken | userId | Token | get_chargify_token | To Review |
| Get Call Center Settings | GET | /espapi/cloud/json/callCenter/settings | userId, locationId | Settings | get_call_center_settings | To Review |
| Provide Call Center Settings | POST | /espapi/cloud/json/callCenter/settings | settings | Result | provide_call_center_settings | To Review |
| Cancel Call Center | POST | /espapi/cloud/json/callCenter/cancel | params | Cancel result | cancel_call_center | To Review |
| Create Call Center Test | POST | /espapi/cloud/json/callCenter/test | params | Test result | create_call_center_test | To Review |
| Cancel Call Center Test | POST | /espapi/cloud/json/callCenter/test/cancel | params | Cancel result | cancel_call_center_test | To Review |
| Get Call Center Alerts | GET | /espapi/cloud/json/callCenter/alerts | filters | List of alerts | get_call_center_alerts | To Review |
| Get Location Energy Usage | GET | /espapi/cloud/json/energy/location | locationId | Usage data | get_location_energy_usage | To Review |
| Get Current Device Energy Usage | GET | /espapi/cloud/json/energy/device/current | deviceId | Usage data | get_current_device_energy_usage | To Review |
| Get Aggregated Device Energy Usage | GET | /espapi/cloud/json/energy/device/aggregated | deviceId | Aggregated usage | get_aggregated_device_energy_usage | To Review |
| Get Billing Setting | GET | /espapi/cloud/json/energy/billing | userId | Billing setting | get_billing_setting | To Review |
| Put Billing Setting | PUT | /espapi/cloud/json/energy/billing | settings | Update result | put_billing_setting | To Review |
| Get Weather | GET | /espapi/cloud/json/weather | locationId | Weather data | get_weather | To Review |
| Get Device Types | GET | /espapi/cloud/json/deviceTypes | filters | List of types | get_device_types | To Review |
| Get Device Type Attributes | GET | /espapi/cloud/json/deviceTypeAttributes | typeId | Attributes | get_device_type_attributes | To Review |
| Create or Update Device Type | PUT | /espapi/cloud/json/deviceTypes | type | Update result | create_update_device_type | To Review |
| Get Device Parameters | GET | /espapi/cloud/json/deviceParameters | paramName | List of parameters | get_device_parameters | To Review |
| Post Device Parameter | POST | /espapi/cloud/json/deviceParameters | param | Result | post_device_parameter | To Review |
| Delete Device Parameter | DELETE | /espapi/cloud/json/deviceParameters/{paramId} | paramId | Deletion result | delete_device_parameter | To Review |
| Put Device Parameter | PUT | /espapi/cloud/json/deviceParameters/{paramId} | param | Update result | put_device_parameter | To Review |
| Get Default Rules | GET | /espapi/cloud/json/deviceDefaultRules | deviceType | List of rules | get_default_rules | To Review |
| Add Default Rule | POST | /espapi/cloud/json/deviceDefaultRules | rule | Result | add_default_rule | To Review |
| Delete Default Rule | DELETE | /espapi/cloud/json/deviceDefaultRules/{ruleId} | ruleId | Deletion result | delete_default_rule | To Review |
| Get Device Goals by Types | GET | /espapi/cloud/json/deviceGoals | typeIds | List of goals | get_device_goals_by_types | To Review |
| Get Device Goal Installation Instruction | GET | /espapi/cloud/json/deviceGoalInstructions | goalId | Instructions | get_device_goal_installation_instruction | To Review |
| Put Media | PUT | /espapi/cloud/json/deviceMedia | media | Update result | put_media | To Review |
| Get Media | GET | /espapi/cloud/json/deviceMedia | filters | List of media | get_media | To Review |
| Delete Media | DELETE | /espapi/cloud/json/deviceMedia/{mediaId} | mediaId | Deletion result | delete_media | To Review |
| Put Device Models | PUT | /espapi/cloud/json/deviceModels | models | Update result | put_device_models | To Review |
| Get Device Models | GET | /espapi/cloud/json/deviceModels | filters | List of models | get_device_models | To Review |
| Delete Device Model Data | DELETE | /espapi/cloud/json/deviceModels/{modelId} | modelId | Deletion result | delete_device_model_data | To Review |
| Get Stories | GET | /espapi/cloud/json/deviceStories | filters | List of stories | get_stories | To Review |
| Put Stories | PUT | /espapi/cloud/json/deviceStories | stories | Update result | put_stories | To Review |
| Delete Story | DELETE | /espapi/cloud/json/deviceStories/{storyId} | storyId | Deletion result | delete_story | To Review |
| Get 3rd Party Clouds | GET | /espapi/cloud/json/3rdPartyClouds | filters | List of clouds | get_3rd_party_clouds | To Review |
| Access 3rd Party Cloud | POST | /espapi/cloud/json/3rdPartyClouds/access | params | Access result | access_3rd_party_cloud | To Review |
| Revoke Access to 3rd Party Cloud | POST | /espapi/cloud/json/3rdPartyClouds/revoke | params | Revoke result | revoke_access_to_3rd_party_cloud | To Review |
| Authorize 3rd Party Client | POST | /espapi/cloud/json/3rdPartyClouds/authorize | params | Auth result | authorize_3rd_party_client | To Review |
| Approve or Deny Client Authorization | POST | /espapi/cloud/json/3rdPartyClouds/approve | params | Approve result | approve_or_deny_client_authorization | To Review |
| Get Access Token | GET | /espapi/cloud/json/3rdPartyClouds/token | params | Token | get_access_token | To Review |
| Update OAuth Client | PUT | /espapi/cloud/json/3rdPartyClouds/oauth | params | Update result | update_oauth_client | To Review |
| Revoke OAuth Client | POST | /espapi/cloud/json/3rdPartyClouds/oauth/revoke | params | Revoke result | revoke_oauth_client | To Review |
| Upload RAG Document | POST | /espapi/cloud/json/rag/documents | document | Upload result | upload_document | To Review |
| Get RAG Documents | GET | /espapi/cloud/json/rag/documents | filters | List of documents | get_documents | To Review |
| Update RAG Document | PUT | /espapi/cloud/json/rag/documents/{docId} | docId, document | Update result | update_document | To Review |
| Delete RAG Document | DELETE | /espapi/cloud/json/rag/documents/{docId} | docId | Deletion result | delete_document | To Review |
| Post RAG Questions | POST | /espapi/cloud/json/rag/questions | questions | Result | post_questions | To Review |
| Get RAG Questions | GET | /espapi/cloud/json/rag/questions | filters | List of questions | get_questions | To Review |
| Update RAG Questions | PUT | /espapi/cloud/json/rag/questions | questions | Update result | update_questions | To Review |
| Get Community Posts | GET | /espapi/cloud/json/community/posts | filters | List of posts | get_community_posts | To Review |
| Create Community Post | POST | /espapi/cloud/json/community/posts | post | Post result | create_a_community_post | To Review |
| Update Community Post | PUT | /espapi/cloud/json/community/posts/{postId} | postId, post | Update result | update_a_community_post | To Review |
| Delete Community Post | DELETE | /espapi/cloud/json/community/posts/{postId} | postId | Deletion result | delete_a_community_post | To Review |
| Comment on Community Post | POST | /espapi/cloud/json/community/posts/{postId}/comments | postId, comment | Comment result | comment_community_post | To Review |
| Delete Community Comment | DELETE | /espapi/cloud/json/community/posts/{postId}/comments/{commentId} | postId, commentId | Deletion result | delete_a_comment | To Review |
| Community Post Reaction | POST | /espapi/cloud/json/community/posts/{postId}/reactions | postId, reaction | Reaction result | community_post_reaction | To Review |
| Create Community File | POST | /espapi/cloud/json/community/files | file | File result | create_a_file | To Review |
| Complete Community File | POST | /espapi/cloud/json/community/files/{fileId}/complete | fileId | Complete result | complete_a_file | To Review |
| Delete Community File | DELETE | /espapi/cloud/json/community/files/{fileId} | fileId | Deletion result | delete_a_file | To Review |
| Get Community File URLs | GET | /espapi/cloud/json/community/files/{fileId}/urls | fileId | URLs | get_file_urls | To Review |
| Websocket | WS | /espapi/cloud/json/websocket | params | Websocket connection | websocket | To Review |

---

- Update the "Status" column as you review and implement each endpoint.
- Add more endpoints and details as needed.
- Use this file as a living document for API coverage tracking.
