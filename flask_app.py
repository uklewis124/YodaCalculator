from flask import Flask, render_template, request
import get_yoda_heights as yoda
import json

app = Flask(__name__)

DEBUGGING = json.load(open("config.json"))["DEBUGGING"]

if DEBUGGING:
    print("Debugging is enabled")
    from colorama import Fore, init
    init(autoreset=True)

people = yoda.setup_people()

@app.errorhandler(404)
def page_not_found(e):
    return "Whooopsiezzzz, I did a whoopsies, or this page hasn't been birthed yet.", 404

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name_to_search = request.form.get("name")
        results = []
        for person in people:
            if name_to_search.lower() in person["name"].lower():
                results.append(person)
        return render_template('index.html', people=results)
    else:
        return render_template('index.html', people=people)

@app.route('/person/<int:person_id>')
def person(person_id):
    return render_template('user.html', person=people[person_id])

if __name__ == "__main__":
    app.run(debug=True)