# APIs about schedules

## Get list schedules

```
GET /schedules
```

## Add a schedule

```
POST /schedules
```

Normal Response Codes: 200

Response

Name | Type | Description
--- | --- | ---
name | string | Schedule name
time | string | Time to call worker, follow cron syntax
method | string | HTTP verb
uri | string | The endpoint URI
parameters | object | (Optional) Parameters to call endpoint
comment | string | (Optional) Comment about this schedule

## Remove a schedule
 
```
DELETE /schedules/<schedule_id>
```
 
```
DELETE /schedules/name/<schedule_name>
``` 
 
## Update a schedule

```
PUT /schedules/<schedule_id>
```

```
PUT /schedules/name/<schedule_name>
```
 