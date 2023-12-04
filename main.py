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


def execute_db_query(query, params):
    with sql.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute(query, params)
        con.commit()


def create_table():
    with sql.connect(DATABASE) as con:
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
                animal_description TEXT NOT NULL,
                animal_image TEXT NOT NULL
            )
        """)
        con.commit()


@app.route("/add-animal", methods=["GET", "POST"])
def add_animal():
    if request.method == "POST":
        msg = ""
        try:
            image = request.files["animal_image"]
            if image.filename != "":
                filename = secure_filename(image.filename)
                image.save(os.path.join("data/img", filename))
                animal_image = "/data/img/" + filename
            else:
                animal_image = None

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
                request.form["animal_description"],
                animal_image
            )
            query = "INSERT INTO animals (animal_name, animal_type, animal_size, animal_gender, animal_breed, animal_color, animal_weight, weight_unit, animal_height, height_unit, animal_age, animal_description, animal_image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
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


@app.route("/search")
def search():
    query = request.args.get("q", "")
    with sql.connect(DATABASE) as con:
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM animals WHERE animal_name LIKE ?", ("%" + query + "%",))
        animals = cur.fetchall()
    return render_template("result.html", animals=animals)


@app.route("/view-animals")
def view_animals():
    with sql.connect(DATABASE) as con:
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM animals")
        rows = cur.fetchall()
    return render_template("view_animals.html", rows=rows)


if __name__ == "__main__":
    app.run(debug=True)
