from flask import Flask, render_template, request
import pandas as pd
import requests as req
import json as js

app = Flask(__name__)

API = "https://swapi.dev/api/"
PERSON_API = API + "people/{}"
DEBUGGING = True

if DEBUGGING:
    print("Debugging is enabled")
    from colorama import Fore, init
    init(autoreset=True)

@app.errorhandler(404)
def page_not_found(e):
    return "Whooopsiezzzz, I did a whoopsies, or this page hasn't been birthed yet.", 404

@app.route('/')
def index():
    people = []
    current_page = 0
    all_people_gathered = False
    
    while not all_people_gathered:
        current_page += 1
        print("iteration ran")    
        api_url = PERSON_API.format("?page={}".format(current_page))
        
        response = req.get(api_url)
        if response.status_code == 200:
            response = response.json()
            returned_people = response["results"]
            
            for person in returned_people:
                people.append(person)
                print(person["name"])
            
            if DEBUGGING:
                print("[WARN]", Fore.YELLOW, "Saving JSON Request's Response to output.json") 
                with open("output.json", 'w') as f:
                    js.dump(response, f, indent=4)
                    print("[WARN]", Fore.GREEN, "Successfully Saved JSON Request")
        elif response.status_code == 404:
            print(response.content)
            all_people_gathered = True
    print(people)
    return "Homepage", 200

if __name__ == "__main__":
    app.run(debug=True)