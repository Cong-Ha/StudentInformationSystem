from flask import Blueprint, render_template, request, url_for, flash, redirect
from models.student_model import add_student, get_all_students
import re

create_bp = Blueprint("create_student", __name__)

def validate_input(data):
    errors = []
    if not  data.get("name") or not re.match(r'^[A-Za-z ]+$', data["name"]):
        errors.append("Name must only contain letters and spaces.")
    if not  data.get("email") or not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', data['email']):
        errors.append("Invalid email address.")
    if not  data.get("program") or not re.match(r'^[A-Za-z ]+$', data["program"]):
        errors.append("Program must only contain letters and spaces.")
    return  errors

@create_bp.route("/add_student", methods=["POST"])
def add_student_route():
    student_data = {
        'name': request.form.get('name'),
        'email': request.form.get('email'),
        'program': request.form.get('program')
    }

    errors = validate_input(student_data)

    #rerender if errors
    if errors:
        students = get_all_students()
        return render_template('students.html', students=students, errors=errors)

    #if no errors add to db
    add_student(student_data)
    flash('Student added successfully!', 'success')

    return redirect(url_for("read_student.index"))