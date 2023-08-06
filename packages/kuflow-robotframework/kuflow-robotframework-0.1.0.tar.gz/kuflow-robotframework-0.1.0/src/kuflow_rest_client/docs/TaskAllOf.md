# TaskAllOf

#### Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**state** | **object** |  | [optional] [readonly] 
**taskDefinition** | [**TasksDefinitionSummary**](TasksDefinitionSummary.md) |  | 
**processId** | **str** |  | 
**activityToken** | **str** | When create a Kuflow Task backed with a Temporal.io servers, this value is required and must be setted with the context task token of Temporal.io activity | [optional] 
**activityResponseVersion** | **str** | When create a Kuflow Task backed with a Temporal.io servers, this value is required and must be setted with the activity version response. | [optional] 
**elementValues** | **{str: (object,)}** | A ElementValueDocument or an array of ElementValueDocument is not allowed in any type of requests | [optional] 
**logs** | **[Log]** |  | [optional] [readonly] 
**owner** | **object** |  | [optional] [readonly] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

