# PowerView http api.

---
## Get user data.

### method
```http
method: GET
api/userdata/
```

### response example
```javascript
{"userData":{"serialNumber":"392550D370D40032","rfID":"0x207B","rfIDInt":8315,"rfStatus":0,"hubName":"RHVldHRlIFRTQlUgdGVzdA==","macAddress":"00:26:74:84:ea:67","roomCount":2,"shadeCount":2,"groupCount":2,"sceneCount":6,"sceneMemberCount":6,"multiSceneCount":0,"multiSceneMemberCount":0,"scheduledEventCount":3,"sceneControllerCount":0,"sceneControllerMemberCount":0,"localTimeDataSet":true,"enableScheduledEvents":true,"remoteConnectEnabled":true,"editingEnabled":true,"_isEnableFirmwareDownload":true,"_isEnableRemoteActionServer":false,"unassignedShadeCount":0,"undefinedShadeCount":0}}
```

---
## Get all rooms.

### method
```http
method: GET
api/rooms/
```

### response example
```javascript
{
  "roomIds":[64902],
  "roomData":[
    {
      "id":64902,
      "name":"S2FudG9vcg==",
      "order":0,
      "colorId":6,
      "iconId":0,
      "order":0
    }
  ]
}
```

---
## Get all shades

### method
```http
method: GET
api/shades
```

### response example
```javascript
{
  "shadeIds":[36933,52214,59580,29938,33595,41123],
  "shadeData":[
    {
      "id":36933,
      "name":"VHdpc3QgdmVyZ2FkZXJydWltdGU=",
      "roomId":64902,
      "groupId":52218,
      "order":0,
      "type":5,
      "batteryStrength":0,
      "batteryStatus":0,
      "batteryIsLow":false
    },
    {
      "id":52214,
      "name":"UGxpc3PDqSBCVSBrYW50b29y",
      "roomId":64902,
      "groupId":34104,
      "order":1,
      "type":17,
      "batteryStrength":186,
      "batteryStatus":3,
      "batteryIsLow":false
    },
    {
      "id":59580,
      "name":"U2lsaG91ZXR0ZSBiYXR0ZXJ5IHRlc3Q=",
      "roomId":64902,
      "groupId":62463,
      "order":2,
      "type":23,
      "batteryStrength":173,
      "batteryStatus":3,
      "batteryIsLow":false
    },
    {
      "id":29938,
      "name":"U2lsaG91ZXR0ZSBrYW50b29y",
      "roomId":64902,
      "groupId":62463,
      "order":3,
      "type":23,
      "batteryStrength":176,
      "batteryStatus":3,
      "batteryIsLow":false
    },
    {
      "id":33595,
      "name":"Um9sbG8gdGVzdCBCZXJ0",
      "roomId":64902,
      "groupId":52218,
      "order":4,
      "type":5,
      "batteryStrength":0,
      "batteryStatus":0,
      "batteryIsLow":false
    },
    {
      "id":41123,"name":"Um9sbG8gYmxhY2sgZGlzcGxheQ==","roomId":64902,"groupId":52218,"order":5,"type":5,"batteryStrength":0,"batteryStatus":0,"batteryIsLow":false}]}
```

---

### method
```http
method: GET
api/scenes/
```

### response example
```javascript
{
  "sceneIds":[7214,64073,15890,42747],
  "sceneData":[
    {
      "id":7214,
      "name":"QWxsIGRvd24=",
      "roomId":64902,
      "order":0,
      "colorId":2,
      "iconId":0
    },
    {
      "id":64073,
      "name":"UGxpc3NlIDE=",
      "roomId":64902,
      "order":1,
      "colorId":5,
      "iconId":0
    },
    {
      "id":15890,
      "name":"QWxsIHVw",
      "roomId":64902,
      "order":2,
      "colorId":0,
      "iconId":0
    },
    {
      "id":42747,
      "name":"UGxpc3NlIDI=",
      "roomId":64902,
      "order":3,
      "colorId":7,
      "iconId":0
    }
  ]
}
```

---

### method
```http
/api/scenecollections/
```

### response example
```javascript
{
  "sceneCollectionIds": [],
  "sceneCollectionData":[]
}
```

---

### method
```http
/api/scenecollectionmembers/
```

### response example
```javascript
{
  "sceneCollectionMemberIds": [],
  "sceneCollectionMemberData":[]
}
```

---

### method
```http
method: GET
/api/scheduledevents/
```

### response example
```javascript
{
  "scheduledEventIds":[2471,24559],
  "scheduledEventData":[
    {
      "id":2471,
      "enabled":true,
      "sceneId":64073,
      "daySunday":true,
      "dayMonday":true,
      "dayTuesday":true,
      "dayWednesday":true,
      "dayThursday":true,
      "dayFriday":true,
      "daySaturday":true,
      "eventType":0,
      "hour":15,
      "minute":58
    },
    {
      "id":24559,
      "enabled":true,
      "sceneId":42747,
      "daySunday":false,
      "dayMonday":true,
      "dayTuesday":false,
      "dayWednesday":false,
      "dayThursday":false,
      "dayFriday":false,
      "daySaturday":false,
      "eventType":0,
      "hour":16,
      "minute":3
    }
  ]
}
```

---
Move a shade to a certain position

### method
```http
method: PUT
/api/shades/<shadeid>
```


### body example
```javascript
{
  "shade":{
    "id":52214,
    "positions":{
      "posKind1":1,
      "position1":34181 //range between 0 and 65535
    }
  }
}
```


### response example
```javascript
{
  "shade":{
    "id":52214,
    "name":"UGxpc3PDqSBCVSBrYW50b29y", //encoded in base64
    "roomId":64902,
    "groupId":34104,
    "order":1,
    "type":17,
    "batteryStrength":186,
    "batteryStatus":3,
    "batteryIsLow":false,
    "positions":{
      "position1":34181,
      "posKind1":1
    }
  }
}
```

---
Activate a scene

### method
```http
method: GET
/api/scenes?sceneid=<sceneid>
```

### response example
```javascript
{
  "scene":{"shadeIds":[35523]}
}
```

---
Get battery level.

### method
```http
method: GET
/api/shades/<shadeId>?updateBatteryLevel=true
```

### body example
```
/api/shades/494?updateBatteryLevel=true
```

### response example
```javascript
{
  "shade": {
    "id": 494,
    "name": "U2hhZGUgMTE=",
    "roomId": 22215,
    "groupId": 15903,
    "order": 9,
    "type": 8,
    "timedOut": false,
    "batteryStrength": 185,
    "batteryStatus": 3,
    "positions": {
      "position1": 43189,
      "posKind1": 1,
      "position2": 8653,
      "posKind2": 2
    }
  }
}
```

