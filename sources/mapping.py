from yaml import safe_load, YAMLError

def getMappingEvents():

    # Chargement du fichier de configuration globale
    with open("mapping_event/events.yml", "r") as fd:
        try:
            eventsFile = safe_load(fd)

            # Charger les evenements
            eventsList = eventsFile.get("eventsList")
        except Exception as e:
            print(e)
            return {}
    
    return eventsList

