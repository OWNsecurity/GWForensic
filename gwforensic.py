import os
import sys
import argparse
import os.path
import csv  
import json
import datetime
from yaml import safe_load, YAMLError
from opensearchpy import OpenSearch

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from pathlib import Path

from timesketch_api_client import config
from timesketch_import_client import importer
from datetime import datetime

# Google Workspace Sources
from sources.login import getLogin
from sources.admin import getAdmin
from sources.drive import getDrive
from sources.token import getToken
from sources.chat import getChat
from sources.meet import getMeet
from sources.calendar import getCalendar
from sources.groups import getGroups
from sources.groups_enterprise import getGroupsEnterprise
from sources.chrome import getChrome
from sources.context_aware_access import getContextAwareAccess
from sources.gcp import getGcp
from sources.rules import getRules
from sources.saml import getSaml
from sources.users_accounts import getUsersAccounts
from sources.data_studio import getDatastudio
from sources.mobile import getMobile
from sources.keep import getKeep
from sources.jamboard import getJamboard
from sources.access_transparency import getAccessTransparency
from sources.currents import getCurrents

# Variables
SCOPES = ['https://www.googleapis.com/auth/admin.reports.audit.readonly']
TOKEN_PATH = "token.json"
OFFICIAL_SOURCES = ['all', 'login', 'admin','drive','token','chat','meet','calendar','groups','groups_enterprise','chrome','context_aware_access','gcp','rules','saml','user_accounts','data_studio','mobile','keep','jamboard','access_transparency','currents']
OFFICIAL_EXPORT_METHOD = ['csv', 'json', 'timesketch', 'opensearch']

# Parse configuration file function
def parseConfigFile(config_path):

    # Loading global configuration file
    with open(config_path, "r") as fd:
        try:
            configFile = safe_load(fd)

            # Get sources list
            sources = configFile.get("sources")

            if sources == None or sources == [""]:
                print("ERROR : No source is specified. Check and try again.")
                sys.exit(1)
            if "all" in sources:
                sources = OFFICIAL_SOURCES
                sources.pop(0) # Remove first element : "all"
            else:
                for source in sources:
                    if source not in OFFICIAL_SOURCES:
                        print("ERROR : source "+str(source)+" does not exist. Check and try again.")
                        sys.exit(1)

            # Get user list
            users = configFile.get("users")
            if users == None or users == [""]:
                print("ERROR : No user is specified. Check and try again.")
                sys.exit(1)

            # Get current date
            currentDate = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+"Z"
            obj_currentDate = datetime.strptime(currentDate[:-1], "%Y-%m-%dT%H:%M:%S.%f")

            startDate = configFile.get("date").get("start")
            endDate = configFile.get("date").get("end")

            if startDate == "":
                # By default: All events
                startDate = None
                endDate = None
            else:
                obj_startDate = datetime.strptime(startDate[:-1], "%Y-%m-%dT%H:%M:%S.%f")
                if endDate == "":
                    obj_endDate = obj_currentDate
                    endDate = None
                else:
                    obj_endDate = datetime.strptime(endDate[:-1], "%Y-%m-%dT%H:%M:%S.%f")
                
                if obj_startDate > obj_endDate:
                    print("ERROR : Dates are incorrect.")
                    sys.exit(1)
                if obj_startDate >= obj_currentDate:
                    print("ERROR : Dates are incorrect.")
                    sys.exit(1)

            exportMethod = configFile.get("export")
            if exportMethod not in OFFICIAL_EXPORT_METHOD:
                print("ERROR : export method "+str(exportMethod)+" does not exist. Check and try again.")
                sys.exit(1)

            
            # Get export folder
            exportFolder = configFile.get("exportFolder")
            if exportFolder == None or exportFolder == "":
                print("ERROR : No folder is specified. Check and try again.")
                sys.exit(1)
            
            exportFolder_path = Path(exportFolder)    

            if not exportFolder_path.exists():
                print("ERROR : no export folder path exists. Check and try again.")
                sys.exit(1)
            
            if exportMethod == "timesketch":
                # Get sketch_number
                sketch_number = configFile.get("timesketch").get("sketch")
                if sketch_number != None:
                    sketch_number = int(sketch_number)
                else:
                    print("ERROR : No sketch number is defined. Check and try again.")
                    sys.exit(1)

                timestamp_description = configFile.get("timesketch").get("timestamp_description")
                if timestamp_description == None:
                    print("ERROR : No timestamp description is defined. Check and try again.")
                    sys.exit(1)

                timeline_name = configFile.get("timesketch").get("timeline_name")
                if timeline_name == None:
                    print("ERROR : No timeline name is defined. Check and try again.")
                    sys.exit(1)
            else:
                timeline_name = None
                sketch_number = None
                timestamp_description = None

            if exportMethod == "opensearch":

                opensearch_url = configFile.get("opensearch").get("url")
                if opensearch_url != None:
                    opensearch_url = str(opensearch_url)
                else:
                    print("ERROR : No URL for opensearch is defined. Check and try again.")
                    sys.exit(1)

                opensearch_user = configFile.get("opensearch").get("user")
                if opensearch_user == None:
                    print("ERROR : No user is defined. Check and try again.")
                    sys.exit(1)

                opensearch_password = configFile.get("opensearch").get("password")
                if opensearch_password == None:
                    print("ERROR : No password is defined. Check and try again.")
                    sys.exit(1)
                
                opensearch_indexname = configFile.get("opensearch").get("index_name")
                if opensearch_indexname == None:
                    print("ERROR : No index name is defined. Check and try again.")
                    sys.exit(1)
                opensearch_port = configFile.get("opensearch").get("port")
                if opensearch_port == None:
                    print("ERROR : No port is defined. Check and try again.")
                    sys.exit(1)
            else:
                opensearch_url = None
                opensearch_user = None
                opensearch_password = None
                opensearch_indexname = None
                opensearch_port = None

            
            # Return configuration information
            configuration = {'sources': sources, 'users': users, 'start': startDate, 'end': endDate, 'exportMethod': exportMethod, 'exportFolder': exportFolder, "timeline_name": timeline_name, "sketch_number": sketch_number, "timestamp_description": timestamp_description, "opensearch_url": opensearch_url, "opensearch_user": opensearch_user, "opensearch_password": opensearch_password, "opensearch_indexname": opensearch_indexname, "opensearch_port": opensearch_port}
            return configuration
   

        except YAMLError as err:
            print(f"ERROR : Can not load configuration file: {err}")
            sys.exit(1)


def BuildCredentials(tokenPath):

    creds = None


    if os.path.exists(tokenPath):
        creds = Credentials.from_authorized_user_file(tokenPath, SCOPES)
    # No valid credentials? Ask to user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=9090)
        # Save the credentials for the next run
        with open(tokenPath, 'w') as token:
            token.write(creds.to_json())

    service = build('admin', 'reports_v1', credentials=creds)
    
    return service

def ExportCSVFile(name, logsExport, exportFolder, header):
    # Export data in CSV file
    # Open the file in the write mode
    print("Writing "+str(name)+ " logs in CSV file...")
    with open(exportFolder+str(name), 'w', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        # write header
        headerList = header["base"]+header["params"]+header["mitre"]
        writer.writerow(headerList)
        # write a row to the csv file
        for line in logsExport:
            temp_line = []
            for attr in headerList:
                try:
                    # Available
                    temp_line.append(line[attr])
                except:
                    # Not available
                    temp_line.append("")

            writer.writerow(temp_line)
    print("Writing "+str(len(logsExport))+" "+str(name)+ " logs in CSV file : OK\n")

def ExportJSONFile(name, logsExport, exportFolder):
    # Export data in JSON file
    print("Writing "+str(name)+ " logs in JSON file...")
    #logsExport.pop(0)
    json_object = json.dumps(logsExport, indent=4)
    with open(exportFolder+str(name), "w", encoding='UTF8') as outfile:
        outfile.write(json_object)

    print("Writing "+str(len(logsExport))+" "+str(name)+ " logs in JSON file : OK\n")


def ExportCSVFileIp(name, ipsExport, exportFolder):
    # Export data (IPs) in CSV file
    # open the file in the write mode
    print("Writing "+str(name)+ " logs in CSV file...")
    with open(exportFolder+str(name), 'w', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        # write a row to the csv file
        for line in ipsExport:
            resultList = list(line.values())
            writer.writerow(resultList)
    print("Writing "+str(name)+ " logs in CSV file : OK")


def ExportTimesketch(name, logsExport, configuration):
    # Export data in Timesketch
    print("Writing "+str(name)+ " logs to Timesketch...")
    logsExport.pop(0)

    with importer.ImportStreamer() as streamer:
        try:
            ts_client = config.get_client()
            my_sketch = ts_client.get_sketch(configuration["sketch_number"])
            streamer.set_sketch(my_sketch)
            streamer.set_timestamp_description(configuration["timestamp_description"])
            streamer.set_timeline_name(configuration["timeline_name"]+str(name))
        except:
            print("ERROR : unable to access to Timesketch. Check your configuration and client and try again.")
            sys.exit(1)


        for elem in logsExport:
            timesketch_message = str(elem['eventsType'])+" - "+str(elem['eventsName'])
            streamer.set_message_format_string('{eventsType:s} - {eventsName:s} - {eventsParameters:s}')

            streamer.add_dict({
                'time': elem['time'],
                'kind': elem['kind'],
                'uniqueQualifier': elem['uniqueQualifier'],
                'applicationName': elem['applicationName'],
                'email': elem['email'],
                'callerType': elem['callerType'],
                'profileId': elem['profileId'],
                'ipAddress': elem['ipAddress'],
                'eventsType': str(elem['eventsType']),
                'eventsName': str(elem['eventsName']),
                'eventsParameters': str(elem['eventsParameters'])
                })

    print("Writing "+str(name)+ " logs to Timesketch : OK")

def ExportOpenSearch(name, logsExport, configuration, client):
    print("Writing "+str(name)+ " logs in OpenSearch...")
    
    # Add each document
    for line in logsExport:
        response = client.index(
            index = configuration["opensearch_indexname"],
            body = line,
            refresh = True
        )

    print("Writing "+str(len(logsExport))+" "+str(name)+ " logs in OpenSearch : OK\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GWForensic - Get & analyze Google Workspace logs")

    parser.add_argument("config", help="Path of the config file")
    
    args = parser.parse_args()
    config_path = Path(args.config)
    

    if not config_path.exists():
        print("ERROR : no config path exists. Check and try again.")
        sys.exit(1)

    if not config_path.is_absolute():
        config_path = config_path.resolve()

    print("   ______        __  _____ ___  ____  _____ _   _ ____ ___ ____ ")
    print("  / ___\ \      / / |  ___/ _ \|  _ \| ____| \ | / ___|_ _/ ___|")
    print(" | |  _ \ \ /\ / /  | |_ | | | | |_) |  _| |  \| \___ \| | |    ")
    print(" | |_| | \ V  V /   |  _|| |_| |  _ <| |___| |\  |___) | | |___ ")
    print("  \____|  \_/\_/    |_|   \___/|_| \_\_____|_| \_|____/___\____|")
    print("")
    print("     Collect, parse and analyze all Google Workspace logs!\n")
    print("                https://github.com/OWNsecurity\n\n")



    # Parse config file
    configuration = parseConfigFile(config_path)

    sourcesList = "all" if configuration["sources"] == "all" else configuration["sources"]
    usersList = "all users" if configuration["users"] == "all" else configuration["users"]
    print("  __________________________________________________________ ")
    print(" |                                                          |")
    print(" |   Configuration                                          |")
    print(" |__________________________________________________________|\n")
    print("Logs sources          : "+', '.join(sourcesList))
    print("Users                 : "+', '.join(usersList))
    if configuration["start"] == None and configuration["end"] == None:
        print("Date                  : no limitation")
    else:
        if configuration["end"] == None:
            print("Date                  : From "+str(configuration["start"])+" to now")
        else:
            print("Date                  : From "+str(configuration["start"])+" to "+str(configuration["end"]))

    print("Export format         : "+str(configuration["exportMethod"]))
    print("Export folder         : "+str(configuration["exportFolder"]))

    
    print("\n  __________________________________________________________ ")
    print(" |                                                          |")
    print(" |   Get (or generate) credentials                          |")
    print(" |__________________________________________________________|\n")
    # Get token file
    service = BuildCredentials(TOKEN_PATH)
    print("OK")

    print("\n\n  __________________________________________________________ ")
    print(" |                                                          |")
    print(" |   Collect & export logs                                  |")
    print(" |__________________________________________________________|\n")


    if configuration["exportMethod"] == "opensearch":

        auth = (configuration["opensearch_user"], configuration["opensearch_password"])
        client = OpenSearch(
            hosts = [{'host': configuration["opensearch_url"], 'port': configuration["opensearch_port"]}],
            http_compress = True,
            http_auth = auth,
            use_ssl = True,
            verify_certs = False,
            ssl_assert_hostname = False,
            ssl_show_warn = False
        )
        # Index creation
        index_body = {
            'settings': {
                'index': {
                'number_of_shards': 4
                }
            }
        }
        response = client.indices.create(configuration["opensearch_indexname"], body=index_body)

    
    # IP addresses observed in logs
    ipsExport = [{"date": "date", "ipAddress": "ipAddress", "user": "user", "applicationName": "applicationName"}]
    
    activityList = {}
    # Get Source
    for source in configuration["sources"]:
        print("Collecting "+str(source)+" logs...")
        if source == "login":
            # Get sourceLogin
            activityList[source], ipsExport, header = getLogin(service, configuration, ipsExport)
        elif source == "admin":
            # Get SourceAdmin
            activityList[source], ipsExport, header = getAdmin(service, configuration, ipsExport)
        elif source == "drive":
            # Get SourceDrive
            activityList[source], ipsExport, header = getDrive(service, configuration, ipsExport)
        elif source == "token":
            # Get SourceToken
            activityList[source], ipsExport, header = getToken(service, configuration, ipsExport)
        elif source == "chat":
            # Get SourceChat
            activityList[source], ipsExport, header = getChat(service, configuration, ipsExport)
        elif source == "meet":
            # Get SourceMeet
            activityList[source], ipsExport, header = getMeet(service, configuration, ipsExport)
        elif source == "calendar":
            # Get SourceCalendar
            activityList[source], ipsExport, header = getCalendar(service, configuration, ipsExport)
        elif source == "groups":
            # Get SourceGroups
            activityList[source], ipsExport, header = getGroups(service, configuration, ipsExport)
        elif source == "groups_enterprise":
            # Get SourceGroupsEnterprise
            activityList[source], ipsExport, header = getGroupsEnterprise(service, configuration, ipsExport)
        elif source == "chrome":
            # Get SourceGroupsChrome
            activityList[source], ipsExport, header = getChrome(service, configuration, ipsExport)
        elif source == "context_aware_access":
            # Get SourceGroupsContextAwareAccess
            activityList[source], ipsExport, header = getContextAwareAccess(service, configuration, ipsExport)
        elif source == "gcp":
            # Get SourceGcp
            activityList[source], ipsExport, header = getGcp(service, configuration, ipsExport)
        elif source == "rules":
            # Get SourceRules
            activityList[source], ipsExport, header = getRules(service, configuration, ipsExport)
        elif source == "saml":
            # Get SourceSaml
            activityList[source], ipsExport, header = getSaml(service, configuration, ipsExport)
        elif source == "user_accounts":
            # Get SourceUsersAccounts
            activityList[source], ipsExport, header = getUsersAccounts(service, configuration, ipsExport)
        elif source == "data_studio":
            # Get SourceDataStudio
            activityList[source], ipsExport, header = getDatastudio(service, configuration, ipsExport)
        elif source == "mobile":
            # Get SourceMobile
            activityList[source], ipsExport, header = getMobile(service, configuration, ipsExport)
        elif source == "keep":
            # Get SourceKeep
            activityList[source], ipsExport, header = getKeep(service, configuration, ipsExport)
        elif source == "jamboard":
            # Get SourceJamboard
            activityList[source], ipsExport, header = getJamboard(service, configuration, ipsExport)
        elif source == "access_transparency":
            # Get SourceAccessTransparency
            activityList[source], ipsExport, header = getAccessTransparency(service, configuration, ipsExport)
        elif source == "currents":
            # Get SourceCurrents
            activityList[source], ipsExport, header = getCurrents(service, configuration, ipsExport)
        else:
            print("ERROR : source "+str(source)+" does not exist. Check and try again.")
            sys.exit(1)

        if len(activityList[source]) == 1:
            print("Collecting "+str(source)+" logs : No logs found")
        else:
            print("Collecting "+str(source)+" logs : OK")

        if configuration["exportMethod"] == "csv":
            ExportCSVFile(source+".csv", activityList[source], configuration["exportFolder"], header)
    
        elif configuration["exportMethod"] == "json":
            ExportJSONFile(source+".json", activityList[source], configuration["exportFolder"])
        
        elif configuration["exportMethod"] == "timesketch":
            ExportTimesketch(source, activityList[source], configuration)
        
        elif configuration["exportMethod"] == "opensearch":
            # Ajout des logs
            if len(activityList[source]) == 1:
                print("There is no logs found for "+str(source)+".\n")
            ExportOpenSearch(source, activityList[source], configuration, client)
        else:
            print("ERROR : An error is triggered during export. Check and try again.")
            sys.exit(1)


    print("\n\n  __________________________________________________________ ")
    print(" |                                                          |")
    print(" |   Export IPs list                                        |")
    print(" |__________________________________________________________|\n")

    ExportCSVFileIp("ips_list.csv", ipsExport, configuration["exportFolder"])

    print("\n\n  __________________________________________________________ ")
    print(" |                                                          |")
    print(" |   Result                                                 |")
    print(" |__________________________________________________________|\n")
    print("All logs have been collected and exported!")
    
