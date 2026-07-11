from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)


def connect_db():
   return sqlite3.connect("database.db")


# Create table
with connect_db() as con:
   con.execute("""
   CREATE TABLE IF NOT EXISTS employees(
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       name TEXT,
       designation TEXT,
       doj TEXT,
       experience TEXT,
       phone TEXT,
       address TEXT
   )
   """)


@app.route("/")
def home():
   return render_template("add_employee.html")


@app.route("/add", methods=["POST"])
def add_employee():

   name = request.form["name"]
   designation = request.form["designation"]
   doj = request.form["doj"]
   phone = request.form["phone"]
   address = request.form["address"]

   joining = datetime.strptime(doj, "%Y-%m-%d")
   today = datetime.today()

   experience = today.year - joining.year

   if (today.month, today.day) < (joining.month, joining.day):
       experience -= 1

   with connect_db() as con:
       con.execute(
           """
           INSERT INTO employees
           (name,designation,doj,experience,phone,address)
           VALUES(?,?,?,?,?,?)
           """,
           (
               name,
               designation,
               doj,
               f"{experience} Years",
               phone,
               address
           )
       )

   return redirect("/employees")


@app.route("/employees")
def employees():

   with connect_db() as con:
       data = con.execute(
           "SELECT * FROM employees"
       ).fetchall()

   return render_template(
       "employee_list.html",
       employees=data
   )


if __name__ == "__main__":
   app.run(debug=True)
