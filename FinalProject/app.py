import json

from flask import Flask, render_template, request
from FinalProject.db_utils import DBClient, FormHandler


app = Flask(__name__)
db_client = DBClient()


@app.route("/")
def index():
    return render_template("index.html", data=db_client.serialize_data())


@app.route("/search", methods=['GET', 'POST'])
def search():
    if not request.args:
        return render_template("search.html")

    query = FormHandler.compile_query(request.args)
    return render_template("search.html", data=db_client.serialize_data(query))


@app.route("/add", methods=['GET', 'POST'])
def add_value():
    if not request.args:
        return render_template("add.html")

    query = FormHandler.compile_query(request.args)
    FormHandler.update_query(query)
    db_client.data.insert_one(query)
    return render_template("add.html", data=query)


@app.route("/delete")
def delete_value():
    if not request.args:
        return render_template("delete.html")
    query = FormHandler.compile_query(request.args)
    db_client.data.remove(query)
    return render_template("delete.html", data=query)


@app.route("/modify")
def modify():
    if not request.args:
        return render_template("modify.html")
    try:
        fltr = json.loads(request.args["filter"])
        params = json.loads(request.args["params"])
        db_client.data.update_many(fltr, params)
        return render_template("modify.html", data=True)
    except Exception:
        return render_template("modify.html", error=True)


if __name__ == "__main__":
    app.run()
