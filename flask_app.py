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

@app.route('/')
def index():
    return render_template('index.html', people=people)

@app.route('/person/<int:person_id>')
def person(person_id):
    return render_template('user.html', person=people[person_id])

if __name__ == "__main__":
    app.run(debug=True)