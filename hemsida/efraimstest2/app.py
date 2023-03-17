import os
import cv2
from calibration_module import calibrate_cross
from flask import Flask, render_template, request, redirect, url_for, flash, session, get_flashed_messages, current_app
from werkzeug.utils import secure_filename
from velocity_module import velocity
from accuracy_module import accuracy
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_current_user():
    return dict(current_user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    messages = get_flashed_messages()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()

        if existing_user is None:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('You have successfully registered! Please log in.')
            return redirect(url_for('login'))
        else:
            flash('A user with that username already exists. Please choose a different username.')
            return redirect(url_for('register'))

    return render_template('register.html', messages=messages)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query the user from the database
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('measure'))

        flash('Invalid username or password.')

    return render_template('login.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calibrate', methods=['POST'])
def calibrate():
    file1 = request.files['file1']
    file2 = request.files['file2']
    filename1 = secure_filename(file1.filename)
    filename2 = secure_filename(file2.filename)
    file_path1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
    file_path2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
    file1.save(file_path1)
    file2.save(file_path2)

    cross_position_x_side, cross_position_y_side, ball_radius_side = calibrate_cross(file_path1)  # Run the calibration function for the first file
    cross_position_x_floor, cross_position_y_floor, ball_radius_floor = calibrate_cross(file_path2)  # Run the calibration function for the second file

    # Check if both results are valid (you can customize the condition as needed)
    if cross_position_x_side is not None and cross_position_x_floor is not None:
        # Store the calibration results in the session
        session['calibration_results'] = {'x_side': cross_position_x_side, 'y_side': cross_position_y_side, 'bollradie_side': ball_radius_side, 'x_floor': cross_position_x_floor, 'y_floor': cross_position_y_floor, 'bollradie_floor': ball_radius_floor}

        # Display a success message
        flash('Calibration successful!')
    else:
        flash('The ball could not be detected. Proceed with a new calibration video!')

    return redirect(url_for('calibration'))



@app.route('/calibration', methods=['GET'])
def calibration():
    messages = get_flashed_messages()
    return render_template('calibration.html', messages=messages)


@app.route('/measure', methods=['GET', 'POST'])
@login_required
def measure():
    throw_info = session.get('throw_info', {'velocity': None, 'accuracy_x': None, 'accuracy_y': None, 'total_distance': None})
    messages = get_flashed_messages()
    if request.method == 'POST':
        file1 = request.files['file1']
        file2 = request.files['file2']
        filename1 = secure_filename(file1.filename)
        filename2 = secure_filename(file2.filename)
        file_path1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
        file_path2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
        file1.save(file_path1)
        file2.save(file_path2)

        calibration_results = session.get('calibration_results', None)

        if calibration_results:
            # Import the measure function from measure_module.py
            from measure_module import measure_throw

            # Get ball_radius_side and ball_radius_floor from calibration results
            ball_radius_side = calibration_results['bollradie_side']
            ball_radius_floor = calibration_results['bollradie_floor']
            cal_x_side = calibration_results['x_side']
            cal_y_side = calibration_results['y_side']
            cal_x_floor = calibration_results['x_side']
            cal_y_floor = calibration_results['y_floor']

            # Run the measure function with the calibration results and the file paths
            x_list_side, y_list_side = measure_throw(file_path1, ball_radius_side, 'side')
            x_list_floor, y_list_floor = measure_throw(file_path2, ball_radius_floor, 'floor')

            if len(x_list_side) and len(x_list_floor) > 3:
                throw_velocity = velocity(x_list_side, y_list_side, x_list_floor, y_list_floor, ball_radius_side, ball_radius_floor, 240)
                accuracy_x, accuracy_y, total_distance = accuracy(x_list_floor, y_list_side, ball_radius_side, ball_radius_floor, cal_x_floor, cal_y_floor, cal_x_side, cal_y_side)
                flash('Throw successfully measured')
                session['measure_results'] = {'x_list_side': x_list_side, 'y_list_side': y_list_side, 'x_list_floor': x_list_floor, 'y_list_floor': y_list_floor}
                session['throw_info'] = {'velocity': throw_velocity, 'accuracy_x': accuracy_x, 'accuracy_y': accuracy_y, 'total_distance': total_distance}
                return render_template('measure.html', messages=messages, throw_info=session['throw_info'])
            
            else:
                flash('Throw could not be measured. Make another throw!')
                return render_template('measure.html', messages=messages, throw_info=throw_info)
        else:
            flash("Please calibrate the system before measuring.")
            return render_template('measure.html', messages=messages, throw_info=throw_info)
    else:
        return render_template('measure.html', messages=messages, throw_info=throw_info)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
