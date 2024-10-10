import pandas as pd
import requests as req
import json
from colorama import Fore, init

DEBUGGING = json.load(open("config.json"))["DEBUGGING"]
API = "https://swapi.dev/api/"
PERSON_API = API + "people/{}"

init(autoreset=True)

def run(people):
    print("[INFO]", Fore.GREEN, "Calculating Yoda Heights")
    """
    Calculate the height of each person in terms of Yoda's height and add it to the person's dictionary.
    Args:
        people (list): A list of dictionaries, where each dictionary represents a person and contains a "height" key.
    Returns:
        list: A new list of dictionaries, where each dictionary includes an additional "yoda_height" key representing the height of the person in terms of Yoda's height (66 cm).
    """
    new_people = []
    
    for person in people:
        yoda_height = 66 # 66cm
        try:
            person_height = float(person["height"])
            
        except ValueError:
            person_height = 0
        finally:
            compared_height = person_height / yoda_height  # Find out how many yodas make up that person's height
            person["yoda_height"] = compared_height
            new_people.append(person)
    
    print("[SUCCESS]", Fore.GREEN, "Yoda Heights Calculated")
    return new_people

def setup_people():
    print("[INFO]", Fore.GREEN, "Setting Up People")
    
    people = []
    current_page = 0
    all_people_gathered = False
    
    
    while not all_people_gathered:
        current_page += 1
        api_url = PERSON_API.format("?page={}".format(current_page))
        
        response = req.get(api_url)
        
        if response.status_code == 200:
            response = response.json()
            returned_people = response["results"]
            
            for person in returned_people:
                people.append(person)
            
            if DEBUGGING:
                print("[WARN]", Fore.YELLOW, "Saving JSON Request's Response to output.json") 
                with open("output.json", 'w') as f:
                    json.dump(response, f, indent=4)
                    print("[WARN]", Fore.GREEN, "Successfully Saved JSON Request")
        
        elif response.status_code == 404:
            all_people_gathered = True
    
    
    new_people = run(people)
    
    print("[SUCCESS]", Fore.GREEN, "People Set Up")
    
    return new_people