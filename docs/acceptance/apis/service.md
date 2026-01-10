# API Endpoint Inventory: service.py

| Endpoint Name | HTTP Method | Path | Parameters (Query/Body) | Response (Sample) | Implementing Method | Status |
|---|---|---|---|---|---|---|
| Get Bot Key | GET | /espapi/analytic/appkey | app_instance_id | API key | get_bot_key | To Review |
| Location Scenes History | GET | /espapi/cloud/json/location/{locationId}/events | locationId, startDate, endDate | Events | location_scenes_history | To Review |
| Get Parameters | GET | /espapi/cloud/json/parameters | locationId, deviceId, paramName | Parameters | get_parameters | To Review |
| Send Commands | PUT | /espapi/cloud/json/devices/{deviceId}/parameters | deviceId, locationId, command, skipProspects | JSON result | send_commands | To Review |
| Inject Parameters | POST | /espapi/cloud/json/devices/{deviceId}/parameters | deviceId, locationId, parameters | JSON result | inject_parameters | To Review |
| Send a Notification | POST | /espapi/cloud/json/notifications | userId, locationId, ... | JSON result | send_a_notification | To Review |
| Send Location Notification | POST | /espapi/cloud/json/locationNotification | locationId, message, ... | JSON result | send_location_notification | To Review |
| Post Zendesk Ticket | POST | /espapi/cloud/json/support | appName, firstName, ... | JSON result | post_zendesk_ticket | To Review |
| Send Message | POST | /espapi/cloud/json/messages | messages, locationId | JSON result | send_message | To Review |
| Update Messages | PUT | /espapi/cloud/json/messages | messages | JSON result | update_messages | To Review |
| Send MMS | POST | /espapi/cloud/json/mms | mms info | JSON result | send_mms | To Review |
| Get Call Center | GET | /espapi/cloud/json/callcenter | callCenterId | Call center info | get_call_center | To Review |
| Update Call Center | PUT | /espapi/cloud/json/callcenter | callCenterId, data | JSON result | update_call_center | To Review |
| Get Call Center Alerts | GET | /espapi/cloud/json/callcenter/alerts | callCenterId | Alerts | get_call_center_alerts | To Review |
| Test Execution | POST | /espapi/cloud/json/execution/test | execution info | JSON result | test_execution | To Review |
| Execute Again | POST | /espapi/cloud/json/execution/again | executionId | JSON result | execute_again | To Review |
| Get Challenge Participants | GET | /espapi/cloud/json/challenge/participants | challengeId | Participants | get_challenge_participants | To Review |
| Start Execution | POST | /espapi/cloud/json/execution/start | execution info | JSON result | start_execution | To Review |
| Submit Data Request | POST | /espapi/cloud/json/dataRequests | locationId, brand, ... | JSON result | submit_data_request | To Review |
| Send Fall Event Feedback | POST | /espapi/cloud/json/fallEventFeedback | feedback info | JSON result | send_fall_event_feedback | To Review |
| Ask Question | POST | /espapi/cloud/json/questions | question info | JSON result | ask_question | To Review |
| Delete Question | DELETE | /espapi/cloud/json/questions | questionId | JSON result | delete_question | To Review |
| Update Response | PUT | /espapi/cloud/json/questions/response | response info | JSON result | update_response | To Review |
| Get Responses | GET | /espapi/cloud/json/questions/response | questionId | Responses | get_responses | To Review |
| Define Question Collection | POST | /espapi/cloud/json/questions/collections | collection info | JSON result | define_question_collection | To Review |
| Get Question Collections | GET | /espapi/cloud/json/questions/collections | None | Collections | get_question_collections | To Review |
| Clear Question Collection | DELETE | /espapi/cloud/json/questions/collections | collectionId | JSON result | clear_question_collection | To Review |
| Apply Tags | PUT | /espapi/cloud/json/usertags/{tag} | tag | JSON result | apply_tags | To Review |
| Delete Tag | DELETE | /espapi/cloud/json/usertags/{tag} | tag | JSON result | delete_tag | To Review |
| Get Tags | GET | /espapi/cloud/json/usertags | None | Tags | get_tags | To Review |
| Load Variable | GET | /espapi/cloud/json/variables/{name} | name | Variable | load_variable | To Review |
| Save Variable | PUT | /espapi/cloud/json/variables/{name} | name, value | JSON result | save_variable | To Review |
| Delete Variable | DELETE | /espapi/cloud/json/variables/{name} | name | JSON result | delete_variable | To Review |
| Make Voice Call | POST | /espapi/cloud/json/voicecall | call info | JSON result | make_voice_call | To Review |
| Set Answer Voice Call | PUT | /espapi/cloud/json/voicecall/answer | answer info | JSON result | set_answer_voice_call | To Review |
| Delete Answer Voice Call | DELETE | /espapi/cloud/json/voicecall/answer | answerId | JSON result | delete_answer_voice_call | To Review |
| Call AI | POST | /espapi/cloud/json/ai | ai info | AI result | call_ai | To Review |


---

- Update the "Status" column as you review and implement each endpoint.
- Add more endpoints and details as needed.
- Use this file as a living document for API coverage tracking.
