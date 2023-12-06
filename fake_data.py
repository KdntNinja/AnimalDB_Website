import sqlite3 as sql
from faker import Faker
import random



def get_db_connection():
    con = sql.connect(DATABASE)
    return con


def execute_db_query(query, params):
    con = get_db_connection()
    cur = con.cursor()
    cur.execute(query, params)
    con.commit()
    con.close()


# Function to generate random dummy data
def generate_dummy_data():
    return (
        fake.name(),
        fake.random_element(elements=("Dog", "Cat", "Bird")),
        fake.random_element(elements=("Small", "Medium", "Large")),
        fake.random_element(elements=("Male", "Female")),
        fake.word(),
        str(random.uniform(1, 10)), "kg",
        str(random.uniform(0.1, 1.5)), "m",
        str(random.randint(1, 10)),
    )


# Function to insert dummy data into the database
def insert_dummy_data(num_records):
    for _ in range(num_records):
        animal_data = generate_dummy_data()
        query = "INSERT INTO animals (animal_name, animal_type, animal_size, animal_gender, animal_breed, animal_weight, weight_unit, animal_height, height_unit, animal_age) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        execute_db_query(query, animal_data)


if __name__ == "__main__":
    DATABASE = "data/Data.sqlite3"

    fake = Faker()

    insert_dummy_data(100)
