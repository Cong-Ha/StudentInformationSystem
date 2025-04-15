from flask import Blueprint, render_template
from models.student_model import get_all_students

read_bp = Blueprint('read_student', __name__)

@read_bp.route('/students')
def index():
    #fetch all customers from db
    students = get_all_students()

    #render index with student data
    return render_template('students.html', students=students)