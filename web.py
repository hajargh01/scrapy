import csv

from flask import Flask, render_template
from ai import Domaine

app = Flask(__name__)


@app.route("/")
def index():
    ls = []

    with open("consultations.csv", newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            ls.append(row)

    return render_template("index.html", domaines=Domaine.values(), consultations=ls)


if __name__ == "__main__":
    app.run(port=8080)
