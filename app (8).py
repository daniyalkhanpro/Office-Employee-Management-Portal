import streamlit as st
import pickle
import os
from datetime import date

# Pickle file
DATA_FILE = "employee_data.pkl"


# Load employee data
def load_employees():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "rb") as file:
                return pickle.load(file)
        except Exception:
            return []
    return []


# Save employee data
def save_employees(employees):
    with open(DATA_FILE, "wb") as file:
        pickle.dump(employees, file)


# App configuration
st.set_page_config(
    page_title="Office Employee Management Portal",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 Office Employee Management Portal")

employees = load_employees()


# Add employee form
st.subheader("Add New Employee")

with st.form("employee_form"):

    name = st.text_input("Employee Name")
    designation = st.text_input("Designation")
    doj = st.date_input("Date of Joining", date.today())
    experience = st.text_input("Experience")
    phone = st.text_input("Phone Number")
    address = st.text_area("Address")

    submit = st.form_submit_button("Add Employee")


if submit:

    if name and designation and phone:

        new_employee = {
            "id": len(employees) + 1,
            "name": name,
            "designation": designation,
            "doj": str(doj),
            "experience": experience,
            "phone": phone,
            "address": address
        }

        employees.append(new_employee)
        save_employees(employees)

        st.success("Employee added successfully!")
        st.rerun()

    else:
        st.warning("Please fill Name, Designation and Phone Number")


# Display employees
st.subheader("Employee Records")

if employees:

    for emp in employees:

        with st.expander(f"{emp['name']} - {emp['designation']}"):

            st.write("**Employee ID:**", emp["id"])
            st.write("**Name:**", emp["name"])
            st.write("**Designation:**", emp["designation"])
            st.write("**Date of Joining:**", emp["doj"])
            st.write("**Experience:**", emp["experience"])
            st.write("**Phone:**", emp["phone"])
            st.write("**Address:**", emp["address"])

else:
    st.info("No employee records found.")
