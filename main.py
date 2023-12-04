from werkzeug.utils import secure_filename
import sqlite3 as sql
from flask import *
import os


app = Flask(__name__)

DATABASE = "data/Data.sqlite3"


@app.route("/")
def home():
    create_table()
    return render_template("home.html")


def get_db_connection():
    con = sql.connect(DATABASE)
    return con


def execute_db_query(query, params):
    con = get_db_connection()
    cur = con.cursor()
    cur.execute(query, params)
    con.commit()
    con.close()


def create_table():
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS animals (
            id INTEGER PRIMARY KEY,
            animal_name TEXT NOT NULL,
            animal_type TEXT NOT NULL,
            animal_size TEXT NOT NULL,
            animal_gender TEXT NOT NULL,
            animal_breed TEXT NOT NULL,
            animal_weight TEXT NOT NULL,
            weight_unit TEXT NOT NULL,
            animal_height TEXT NOT NULL,
            height_unit TEXT NOT NULL,
            animal_age TEXT NOT NULL,
            animal_description TEXT NOT NULL
        )
    """)
    con.commit()
    con.close()


@app.route("/add-animal", methods=["GET", "POST"])
def add_animal():
    if request.method == "POST":
        try:
            animal_data = (
                request.form["animal_name"],
                request.form["animal_type"],
                request.form["animal_size"],
                request.form["animal_gender"],
                request.form["animal_breed"],
                request.form["animal_weight"],
                request.form["weight_unit"],
                request.form["animal_height"],
                request.form["height_unit"],
                request.form["animal_age"],
                request.form["animal_description"]
            )
            query = "INSERT INTO animals (animal_name, animal_type, animal_size, animal_gender, animal_breed, animal_weight, weight_unit, animal_height, height_unit, animal_age, animal_description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            execute_db_query(query, animal_data)
            msg = "Record successfully added"
        except sql.Error as e:
            msg = f"Error in insert operation: {e}"
        finally:
            return redirect(url_for("loading", msg=msg))
    else:
        return render_template("add_animal.html")


@app.route("/add-animal-loading")
def loading():
    return render_template("loading.html")


@app.route("/result-search")
def search():
    query = request.args.get("q", "")
    search_option = request.args.get("search_option", "animal_name")
    con = get_db_connection()
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute(f"SELECT * FROM animals WHERE {search_option} LIKE ?", ("%" + query + "%",))
    animals = cur.fetchall()
    con.close()
    return render_template("search_result.html", animals=animals)


@app.route("/get-breeds")
def get_breeds():
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT DISTINCT animal_breed FROM animals")
    breeds = [row[0] for row in cur.fetchall()]
    con.close()
    return jsonify(breeds)


@app.route("/view-animals")
def view_animals():
    con = get_db_connection()
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM animals")
    rows = cur.fetchall()
    con.close()
    return render_template("view_animals.html", rows=rows)


@app.route("/delete-animal/<int:animal_id>", methods=["DELETE"])
def delete_animal(animal_id):
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM animals WHERE id = ?", (animal_id,))
    con.commit()
    con.close()
    return '', 204


if __name__ == "__main__":
    app.run(debug=True)
