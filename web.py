import csv

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    items = []

    with open("consultations.csv", newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            items.append(row)
    return render_template("index.html", items=items)


if __name__ == "__main__":
    app.run(port=8080)
