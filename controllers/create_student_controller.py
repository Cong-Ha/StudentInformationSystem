from flask import Blueprint, render_template, request, url_for, flash, redirect
from models.student_model import add_student, get_all_students
import re

create_bp = Blueprint("create_student", __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

    image_file = request.files.get("image")
    if image_file and image_file.filename != "":
        if not allowed_file(image_file.filename):
            errors.append("Invalid image format. only png, jpg, jpeg, gif are allowed.")
    else:
        image_file = None

    #rerender if errors
    if errors:
        students = get_all_students()
        return render_template('students.html', students=students, errors=errors, student=student_data)

    #if no errors add to db
    add_student(student_data, image_file)
    flash('Student added successfully!', 'success')

    return redirect(url_for("read_student.index"))