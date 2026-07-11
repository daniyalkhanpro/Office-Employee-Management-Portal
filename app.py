from flask import Flask, render_template, request, redirect
import pickle
import os

app = Flask(__name__)

PICKLE_FILE = "employee_data.pkl"


# Load employee data
def load_employees():

    if os.path.exists(PICKLE_FILE):

        with open(PICKLE_FILE, "rb") as file:
            return pickle.load(file)

    return []


# Save employee data
def save_employees(employees):

    with open(PICKLE_FILE, "wb") as file:
        pickle.dump(employees, file)


# Home page
@app.route("/")
def home():

    employees = load_employees()

    return render_template(
        "employees.html",
        employees=employees
    )


# Add employee
@app.route("/add", methods=["POST"])
def add_employee():

    employees = load_employees()

    new_employee = {
        "id": len(employees) + 1,
        "name": request.form["name"],
        "designation": request.form["designation"],
        "doj": request.form["doj"],
        "experience": request.form["experience"],
        "phone": request.form["phone"],
        "address": request.form["address"]
    }

    employees.append(new_employee)

    save_employees(employees)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
