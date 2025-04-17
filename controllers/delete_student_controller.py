from flask import Blueprint, request, redirect, url_for, flash
from models.student_model import delete_student

delete_bp = Blueprint('delete_student', __name__)

@delete_bp.route("/delete/<id>", methods=["POST"])
def delete_customer_route(id):
    delete_student(id)
    flash('Student deleted successfully!', 'success')
    return redirect(url_for("read_student.index"))