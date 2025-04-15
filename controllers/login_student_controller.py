from flask import Blueprint, render_template


login_bp = Blueprint('login_student', __name__)

@login_bp.route('/') #work in progress, changed to be index for login
def index():

    #render index with student data
    return render_template('index.html')