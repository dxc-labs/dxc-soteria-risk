## Mapping of features to code ##
For training the model, the text categorical features were mapped to numerical categorical variables.

|Feature Group|Value|Code|Comments|
|:----------|:-----|:---|:-------|
|Temperature|Normal|0||
||High|1||
||Severe|2||
|SpO2|> 93|0||
||90 to 93|1||
||< 90|2||
|Travel History|No|0||
||Yes|1||
|Positive Contact|No|0||
||Yes|1||
|Symptoms|None|1/ 0|1 if none of the individual symptoms are present, 0 if otherwise|
||Dry Cough|1/ 0|1 if symptom present, 0 if not|
||Shortness of Breath|1/ 0|1 if symptom present, 0 if not|
||Chest Pain/ pressure|1/ 0|1 if symptom present, 0 if not|
||Confusion/ problems thinking|1/ 0|1 if symptom present, 0 if not|
||Bluish lips/ face|1/ 0|1 if symptom present, 0 if not|
||Sore Throat|1/ 0|1 if symptom present, 0 if not|
||Fatigue|1/ 0|1 if symptom present, 0 if not|
||Aches and Pain|1/ 0|1 if symptom present, 0 if not|
||Loss of appetite/ smell|1/ 0|1 if symptom present, 0 if not|
||Headache|1/ 0|1 if symptom present, 0 if not|
||Stuffy/ runny Nose|1/ 0|1 if symptom present, 0 if not|
||Vomiting|1/ 0|1 if symptom present, 0 if not|
||Diarrhea|1/ 0|1 if symptom present, 0 if not|
||Sneezing|1/ 0|1 if symptom present, 0 if not|
|Health Status Progress|No Change|0||
||Improved|1||
||Declined|2||

<a href="../README.md"><img src="./diagrams/back.png" height="24" width="24"></img></a>