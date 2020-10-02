# Risk Profile Engine API #
Risk Profile Engine is exposed as an API endpoint that other application components/ services could consume easily.

## API Details ##
* API endpoint is available <a href="https://api-xxx.example.com/risk/classification">here</a>
* API method: POST
* Features
  * **Temperature**: Body temperature submitted by the user
  * **SpO2**: SpO2 reading submitted by the user
  * **Travel History**: An aggregate information to capture if the user has traveled to any country during the last 14 days
  * **Positive Contact**: Has the user come in contact with any potentially infected person during the last 14 days 
  * **Symptoms**: Symptom(s) that the user could select from the available list
  * **Overall Health Status**: To enable the user to indicate the overall health status progression
* Invoking components (like Workflow) could use the below table as a guidance for capturing information from the user and to invoke the API. For sample JSON payload request and response format, click [here](#sample-json)

|Feature Group|Control Type|UI Display Value|JSON Payload Key|JSON Payload Value|
|:---------------|:---------------|:---------------|:---------------|:----------|
|Temperature|Single select|Normal|temperature|Normal|
|||High||High|
|||Severe||Severe|
|SpO2|Single select|\> 93|spo2|\> 93|
|||90 to 93||90 to 93|
|||< 90||< 90|
|Travel History|Single select|Have you traveled to any country in the last 14 days? No|travelHistory|No|
|||Yes||Yes|
|Positive Contact|Single select|Have you come in contact with any potentially infected person in the last 14 days? No|positiveContact|No|
|||Yes||Yes|
|Symptoms|Multi select|Dry Cough|symptoms|Dry Cough|
|||Sore Throat||Sore Throat|
|||Shortness of Breath||Shortness of Breath|
|||Chest Pain/ pressure||Chest Pain/ pressure|
|||Confusion/ problems thinking||Confusion/ problems thinking|
|||Bluish lips/ face||Bluish lips/ face|
|||Fatigue||Fatigue|
|||Aches and Pain||Aches and Pain|
|||Headache||Headache|
|||Stuffy/ runny Nose||Stuffy/ runny Nose|
|||Sneezing||Sneezing|
|||Loss of appetite/ smell||Loss of appetite/ smell|
|||Vomiting||Vomiting|
|||Diarrhea||Diarrhea|
|Overall Health Status|Single select|No Change|overallHealthStatus|No Change|
|||Improved||Improved|
|||Declined||Declined|

## Sample JSON ##
### Scenario - with symptoms ###
* Request
```
  {
    "instances": [
      {
        "features": [
          {
            "temperature": "High",
            "spo2": "> 93",
            "travelHistory": "Yes",
            "positiveContact": "No",
            "symptoms": [
              "Chest Pain/ pressure",
              "Confusion/ problems thinking",
              "Fatigue",
              "Aches and pain",
              "Headache",
              "Stuffy/ runny Nose",
              "Vomiting",
              "Diarrhea",
              "Sneezing"
            ],
            "overallHealthStatus": "Improved"
          }
        ]
      }
    ]
  }
```
* Response
```
  {
    "statusCode": 200,
    "body": [
        "green"
    ]
  }
```
### Scenario - with no symptoms ###
* Request
```
  {
    "instances": [
      {
        "features": [
          {
            "temperature": "Normal",
            "spo2": "> 93",
            "travelHistory": "Yes",
            "positiveContact": "No",
            "symptoms": [],
            "overallHealthStatus": "No Change"
          }
        ]
      }
    ]
  }
```
* Response
```
  {
    "statusCode": 200,
    "body": [
        "green"
    ]
  }
```  
 
[<img src="./diagrams/top.png" height="24" width="24"></img>](#risk-profile-engine-api)

<a href="../README.md"><img src="./diagrams/back.png" height="24" width="24"></img></a>