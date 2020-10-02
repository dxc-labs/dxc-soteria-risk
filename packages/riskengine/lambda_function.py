import os
import boto3
import json

# grab environment variables
ENDPOINT_NAME = os.environ['RISK_CLASSIFICATION_ENDPOINT']
client = boto3.client(service_name='sagemaker-runtime')

def getEncodedRisk(risk):
    return {
        '0.0': 'green',
        '1.0': 'amber',
        '2.0': 'red'
    }.get(risk, "Invalid Risk Category")

def trnsdata(data):
    try:
        features=data.copy()
        return ','.join([str(feature) for feature in features[0:]])

    except Exception as err:
        print('Error transforming data: {0},{1}'.format(data, err))
        raise Exception('Error transforming data: {0},{1}'.format(data, err))

def getTemperature(temperature):
    return {
        'normal': 0,
        'high': 1,
        'severe': 2
    }.get(temperature)

def getSpO2Range(spo2):
    return {
        '> 93': 0,
        '90 to 93': 1,
        '< 90': 2
    }.get(spo2)

def getTravelHistory(travelHistory):
    return {
        'no': 0,
        'yes': 1
    }.get(travelHistory)

def getPositiveContact(positiveContact):
    return {
        'no': 0,
        'yes': 1
    }.get(positiveContact)

def getOverallHealthStatus(overallHealthStatus):
    return {
        'no change': 0,
        'improved': 1,
        'declined': 2
    }.get(overallHealthStatus)

validKeys=['temperature', 'spo2', 'travelhistory', 'positivecontact', 'symptoms', 'overallhealthstatus']
validTemperatures=['normal', 'high', 'severe']
validSpO2=['> 93', '90 to 93', '< 90']
validTravelHistory=['no', 'yes']
validPositiveContact=['no', 'yes']
validSymptoms=['dry cough', 'shortness of breath', 'chest pain/ pressure', 'confusion/ problems thinking', 'bluish lips/ face', 'sore throat', 'fatigue', 'aches and pain', 'loss of appetite/ smell', 'headache', 'stuffy/ runny nose', 'vomiting', 'diarrhea', 'sneezing']
validHealthStatusProgress=['no change', 'improved', 'declined']
allowedTemperatures=['Normal', 'High', 'or Severe']
allowedTravelHistory=['No', 'Yes']
allowedPositiveContact=['No', 'Yes']
allowedSymptoms=['Dry Cough', 'Shortness of Breath', 'Chest pain/ pressure', 'Confusion/ problems thinking', 'Bluish lips/ face', 'Sore Throat', 'Fatigue', 'Aches and pain', 'Loss of appetite/ smell', 'Headache', 'Stuffy/ runny nose', 'Vomiting', 'Diarrhea', 'and Sneezing']
allowedHealthStatusProgress=['No Change', 'Improved', 'or Declined']

def checkParameters(type, keyVal):
    keyVal=keyVal.lower()
    if (type == 'TEMPERATURE'):
        if validTemperatures.count(keyVal) > 0:
            return True
        else:
            return False
    elif (type == 'SPO2'):
        if validSpO2.count(keyVal) > 0:
            return True
        else:
            return False
    elif (type == 'TRAVEL_HISTORY'):
        if validTravelHistory.count(keyVal) > 0:
            return True
        else:
            return False
    elif (type == 'POSITIVE_CONTACT'):
        if validPositiveContact.count(keyVal) > 0:
            return True
        else:
            return False
    elif (type == 'SYMPTOMS'):
        if validSymptoms.count(keyVal) > 0:
            return True
        else:
            return False
    elif (type == 'OVERALL_HEALTH_STATUS'):
        if validHealthStatusProgress.count(keyVal) > 0:
            return True
        else:
            return False

def isValidJSON(inputjson):
  try:
    objJSON = json.dumps(inputjson)
  except ValueError as e:
    return False
  return True

def lowerDict(obj):
    if isinstance(obj, dict):
        return {k.lower():lowerDict(v) for k, v in obj.items()}
    elif isinstance(obj, (list, set, tuple)):
        t = type(obj)
        return t(lowerDict(o) for o in obj)
    elif isinstance(obj, str):
        return obj.lower()
    else:
        return obj

def lambda_handler(event, context):

    if (not isValidJSON(event)):
        return {
            'statusCode': 400,
            'body': 'Invalid payload received...'
        }

    theFeatures=[]
    theInstance={}
    receivedKeys=[]
    try:
        for record in event['instances']:
            for item in record['features']:

                for k, v in item.items():
                    receivedKeys.append(k)
                
                receivedKeys=lowerDict(receivedKeys)
                allKeysPresent = all(elem in receivedKeys  for elem in validKeys)
                if not allKeysPresent:
                    t=set(validKeys).difference(receivedKeys)
                    a = ', '.join(str(i) for i in t)
                    err='Payload is missing some of the required keys... please check your invocation parameters for proper key value pairs that need to be supplied... you have not supplied the key(s): ['+ a +']'
                    return {
                        'statusCode': 400,
                        'body': err
                    }

                for k, v in item.items():
                    err = ""
                    if (k.lower() == 'temperature'):
                        if (not checkParameters('TEMPERATURE', v)) :
                            err = 'Invalid value (' + v + ') passed for temperature... please check the value passed for temperature...valid values are: ' + ', '.join(allowedTemperatures)
                    elif (k.lower() == 'spo2'):
                        if (not checkParameters('SPO2', v)) :
                            err = 'Invalid value (' + v + ') passed for SpO2... please check the value passed for SpO2...valid values are: ' + ', '.join(validSpO2)
                    elif (k.lower() == 'travelhistory'):
                        if (not checkParameters('TRAVEL_HISTORY', v)) :
                            err = 'Invalid value (' + v + ') passed for travel history... please check the value passed for travel history...valid values are: ' + ' or '.join(allowedTravelHistory)
                    elif (k.lower() == 'positivecontact'):
                        if (not checkParameters('POSITIVE_CONTACT', v)) :
                            err = 'Invalid value (' + v + ') passed for positive contact... please check the value passed for positive contact...valid values are: ' + ' or '.join(allowedPositiveContact)
                    elif (k.lower() == 'symptoms'):
                        passedSymptoms=item[k]
                        for s in passedSymptoms:
                            if (not checkParameters('SYMPTOMS', s)) :
                                err = 'Invalid symptom (' + s + ') passed... please check your symptoms that you have passed...valid values are: ' + ', '.join(allowedSymptoms)
                    elif (k == 'overallHealthStatus'):
                        if (not checkParameters('OVERALL_HEALTH_STATUS', v)) :
                            err = 'Invalid value (' + v + ') passed for health status progress... please check the value passed for health status progress...valid values are: ' + ', '.join(allowedHealthStatusProgress)
                    if (not err == ""):
                        return {
                            'statusCode': 400,
                            'body': err
                        }

                item=lowerDict(item)

                featureValue=[]
                riskDict ={}

                temperature=item['temperature']
                temperature=getTemperature(temperature)
                featureValue.append(temperature)

                spo2=item['spo2']
                spo2=getSpO2Range(spo2)
                featureValue.append(spo2)

                travelHistory=item['travelhistory']
                travelHistory=getTravelHistory(travelHistory)
                featureValue.append(travelHistory)

                positiveContact=item['positivecontact']
                positiveContact=getPositiveContact(positiveContact)
                featureValue.append(positiveContact)
                
                symptoms=item['symptoms']
                symptomCount=len(symptoms)
                if symptomCount==0:
                    featureValue.append(1) # No Symptoms
                    featureValue.append(0) # No Dry Cough
                    featureValue.append(0) # No Shortness of Breath
                    featureValue.append(0) # No Chest Pain/ pressure
                    featureValue.append(0) # No Confusion/ problems thinking
                    featureValue.append(0) # No Bluish lips/ face
                    featureValue.append(0) # No Sore Throat
                    featureValue.append(0) # No Fatigue
                    featureValue.append(0) # No Aches and Pain
                    featureValue.append(0) # No Loss of appetite/ smell
                    featureValue.append(0) # No Headache
                    featureValue.append(0) # No Stuffy/ runny Nose
                    featureValue.append(0) # No Vomiting
                    featureValue.append(0) # No Diarrhea
                    featureValue.append(0) # No Sneezing
                else:
                    featureValue.append(0) # No Symptoms is false
                    if 'dry cough' in symptoms:
                        featureValue.append(1)
                    else:
                        featureValue.append(0)
                    if 'shortness of breath' in symptoms:
                        featureValue.append(1)
                    else:
                        featureValue.append(0)                        
                    if 'chest pain/ pressure' in symptoms:
                        featureValue.append(1)
                    else:
                        featureValue.append(0)                        
                    if 'confusion/ problems thinking' in symptoms:
                        featureValue.append(1)
                    else:
                        featureValue.append(0)
                    if 'bluish lips/ face' in symptoms:
                        featureValue.append(1)
                    else:
                        featureValue.append(0)
                    if 'sore throat' in symptoms:
                        featureValue.append(1)
                    else:
                        featureValue.append(0)
                    if 'fatigue' in symptoms:
                        featureValue.append(1)
                    else:
                        featureValue.append(0)
                    if 'aches and pain' in symptoms:
                        featureValue.append(1)
                    else:
                        featureValue.append(0)
                    if 'loss of appetite/ smell' in symptoms:
                        featureValue.append(1)
                    else:
                        featureValue.append(0)
                    if 'headache' in symptoms:
                        featureValue.append(1)
                    else:
                        featureValue.append(0)
                    if 'stuffy/ runny nose' in symptoms:
                        featureValue.append(1)
                    else:
                        featureValue.append(0)
                    if 'vomiting' in symptoms:
                        featureValue.append(1)
                    else:
                        featureValue.append(0)
                    if 'diarrhea' in symptoms:
                        featureValue.append(1)
                    else:
                        featureValue.append(0)
                    if 'sneezing' in symptoms:
                        featureValue.append(1)
                    else:
                        featureValue.append(0)

                overallHealthStatus=item['overallhealthstatus']
                overallHealthStatus=getOverallHealthStatus(overallHealthStatus)
                featureValue.append(overallHealthStatus)

                riskDict['features'] = featureValue
                theFeatures.append(riskDict)
                riskDict ={}
            
        theInstance['instances']= theFeatures
        request = theInstance
        
        tdata=[trnsdata(instance['features']) for instance in request['instances']]
        result = client.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                              ContentType='text/csv',
                              Body=('\n'.join(tdata).encode('utf-8')))
        result = result['Body'].read().decode('utf-8')
        result=result.split(',')
        prediction=[]
        prediction += [getEncodedRisk(r) for r in result]

        return {
            'statusCode': 200,
            'body': (prediction)
        }

    except Exception as err:
        return {
            'statusCode': 400,
            'body': 'Error - call failed {0}'.format(err)
        }
