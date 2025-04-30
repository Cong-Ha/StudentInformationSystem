from flask import Blueprint, request, url_for, render_template, redirect, flash
from models.student_model import update_student, get_all_students
from controllers.create_student_controller import validate_input, allowed_file
from datetime import datetime
import re

update_bp = Blueprint('update_student', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def validate_input_with_date(data, date):
    errors = validate_input(data)
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
        errors.append("Enrollment date must be in the format YYYY-MM-DD.")
    return errors

@update_bp.route("/update/<id>", methods=["POST"])
def update_student_route(id):
    raw_date = request.form['enrollment_date']
    current_time = datetime.now().strftime("%H:%M:%S")

    errors = validate_input_with_date(request.form, raw_date)

    image_file = request.files.get("image")
    if image_file and image_file.filename != "":
        if not allowed_file(image_file.filename):
            errors.append("Invalid image format. ONLY png, jpg, jpeg, gif are allowed.")
    else:
        image_file = None

    if errors:
        students = get_all_students()
        update_data = dict(request.form)
        update_data['_id'] = id
        return render_template("students.html", students=students, errors=errors, student=update_data, validation_target_id=id)

    # Safe to parse now
    full_datetime = f"{raw_date} {current_time}"
    parsed_date = datetime.strptime(full_datetime, "%Y-%m-%d %H:%M:%S")
    db_date = parsed_date.strftime("%Y-%m-%d %H:%M:%S")

    update_data = {
        'name': request.form.get('name'),
        'email': request.form.get('email'),
        'phone': request.form.get('phone'),
        'program': request.form.get('program'),
        'enrollment_date': db_date
    }

    update_student(id, update_data, image_file)
    flash('Student updated successfully!', 'success')
    return redirect(url_for("read_student.index"))