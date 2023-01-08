import requests as requests
from faker import Faker
from flask import Flask, render_template, request

app = Flask(__name__)

if __name__ == "__main__":
    app.run()

@app.route("/space/")
def space():
    lsit_of_dict = requests.get('http://api.open-notify.org/astros.json').json()["people"]
    return f"People in Space: {len(lsit_of_dict)}, namely: {render_template('index.html', name_craft=lsit_of_dict)}"

@app.route("/mean/")
def mean():
    with open("hw.csv", "r") as r:
        Weight, Height = 0, 0
        for count, lines in enumerate(r.readlines()):
            number = lines.splitlines()[0].split(",")
            if len(number) > 1 and "Index" not in lines:
                Height += float(number[1])
                Weight += float(number[2])
    return f"Average weight: {round(Weight * 0.453592 / count)}kg. Average growth: {round(Height * 2.54 / count)}cm"


@app.route("/generate-users/", methods=["GET"])
def genetate():
    count = request.args.get('count', 100)
    fake = Faker()
    list_of_fake = [[fake.first_name(), fake.email()] for _ in range(int(count))]
    return render_template('index.html', list=list_of_fake)

@app.route("/requirements/")
def requirements():
    with open("requirements.txt", "r") as r:
        return render_template('index.html', list_of_requirements=r.read().split())
