import os
import json

from sources.mapping import getMappingEvents

def getChrome(service, config, ipsExport):
    # Official documentation : https://support.google.com/a/answer/9393909?hl=en

    # ----------------------------------------
    # Define users
    # ----------------------------------------
    if config['users'][0] == 'all':
        userKeyList = 'all'
    else:
        userKeyList = config['users'][0]

    
    logsExport = []

    # Get mapping events
    eventsList = getMappingEvents()

    nextPage = False

    while True:
        

        # ----------------------------------------
        # Call the Admin SDK Reports API for chrome application
        # ----------------------------------------
        if nextPage == False:
            results = service.activities().list(userKey=userKeyList, applicationName='chrome',startTime=config['start'], endTime=config['end'],
                                                maxResults=1000).execute()
        else:
            results = service.activities().list(userKey=userKeyList, applicationName='chrome',startTime=config['start'], endTime=config['end'],
                                                maxResults=1000, pageToken=str(nextPage)).execute()

        # Get results            
        activities = results.get('items', [])

        attributesList = {"base": ["kind", "time", "uniqueQualifier", "applicationName", "email", "callerType", "profileId", "ipAddress", "eventsType", "eventsName"], "params": []}
        attributesList["mitre"] = ["tactics", "technique", "mitre_id"]
        
        if not activities:
            return logsExport, ipsExport, attributesList
        else:
            # Check if there is other page to request
            try:
                nextPage = results["nextPageToken"]
            except:
                # No nextPageToken
                nextPage = False

            # ----------------------------------------
            # Logs
            # ----------------------------------------

            
            for activity in activities:
                #print(u'{0}: {1} ({2})'.format(activity['id']['time'], activity['actor']['email'], activity['events'][0]['name']))
                #print(activity)
                #print(json.dumps(activity, indent=4))
                # Example :
                # kind / id (time/ uniqueQualifier/applicationName/customerId) / etag / actor (email/profilId) / ipAddress / events (type/name/parameters))
                try:
                    for param in activity['events'][0]['parameters']:
                        attributesList["params"].append(param["name"])
                except:
                    pass

                line = {}
                try:
                    line["kind"] = activity['kind']
                except:
                    line["kind"] = "/"
                try:
                    line["time"] = activity['id']['time']
                except:
                    line["time"] = "/"
                try:
                    line["uniqueQualifier"] = activity['id']['uniqueQualifier']
                except:
                    line["uniqueQualifier"] = "/"
                try:
                    line["applicationName"] = activity['id']['applicationName']
                except:
                    line["applicationName"] = "/"
                try:
                    line["email"] = activity['actor']['email']
                except:
                    line["email"] = "/"
                try:
                    line["callerType"] = activity['actor']['callerType']
                except:
                    line["callerType"] = "/"
                try:
                    line["profileId"] = activity['actor']['profileId']
                except:
                    line["profileId"] = "/"
                try:
                    line["ipAddress"] = activity['ipAddress']
                    currentData = {}
                    currentData['time'] = line["time"]
                    currentData['ipAddress'] = activity['ipAddress']
                    currentData['email'] = line["email"]
                    currentData['applicationName'] = line["applicationName"]
                    ipsExport.append(currentData)
                except:
                    line["ipAddress"] = "/"
                try:
                    line["eventsType"] = activity['events'][0]['type']
                except:
                    line["eventsType"] = "/"
                try:
                    line["eventsName"] = activity['events'][0]['name']
                except:
                    line["eventsName"] = "/"
                try:
                    for param in activity['events'][0]['parameters']:
                        try:
                            try:
                                line[param["name"]] = param["value"]
                            except:
                                line[param["name"]] = param["boolValue"]
                        except:
                            continue
                except Exception as e:
                    print(e)

                if line["eventsName"] in eventsList.keys():
                    line["tactics"]  = eventsList[line["eventsName"]]["mitre"]["tactics"]
                    line["technique"]  = eventsList[line["eventsName"]]["mitre"]["technique"]
                    line["mitre_id"]  = eventsList[line["eventsName"]]["mitre"]["id"]

                logsExport.append(line)
                #print(line)

        if nextPage == False:
            break

    # ----------------------------------------
    # Return all logs found
    # ----------------------------------------
    attributesList["params"] = list(dict.fromkeys(attributesList["params"]))

    return logsExport, ipsExport, attributesList