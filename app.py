from flask import Flask

#import blueprints
from controllers.read_student_controller import read_bp
from controllers.create_student_controller import create_bp
from controllers.login_student_controller import login_bp

#initialize the Flask application
app = Flask(__name__)


#register blueprints
app.register_blueprint(read_bp)
app.register_blueprint(create_bp)
app.register_blueprint(login_bp)




app.secret_key="your_secret_key"

if __name__ == '__main__':
    app.run(debug=True)


