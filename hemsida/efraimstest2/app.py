import os
import cv2
from calibration_module import calibrate_cross
from measure_module import measure_throw
from velocity_module import velocity
from accuracy_module import accuracy
from flask import Flask, render_template, request, redirect, url_for, flash, session, get_flashed_messages, current_app, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse, urljoin
from datetime import timedelta, datetime


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


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
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()

        if existing_user is None:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('You have successfully registered! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('A user with that username already exists. Please choose a different username.', 'error')
            return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query the user from the database
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            if next_page and is_safe_url(next_page):
                flash('You have successfully logged in!', 'success')
                return redirect(next_page)
            return redirect(url_for('measure'))

        flash('Invalid username or password.', 'error')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()  # Clear the session data
    return redirect(url_for('home'))


@app.route('/')
def home():
    return render_template('index.html')

   

@app.route('/calibration', methods=['GET', 'POST'])
@login_required
def calibration():
    if request.method == 'POST':
        side_camera_file = request.files['sideCamera']
        underneath_camera_file = request.files['underneathCamera']
        filename1 = secure_filename(side_camera_file.filename)
        filename2 = secure_filename(underneath_camera_file.filename)
        file_path1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
        file_path2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
        side_camera_file.save(file_path1)
        underneath_camera_file.save(file_path2)

        cross_position_x_side, cross_position_y_side, ball_radius_side = calibrate_cross(file_path1)  # Run the calibration function for the first file
        cross_position_x_floor, cross_position_y_floor, ball_radius_floor = calibrate_cross(file_path2)  # Run the calibration function for the second file

        # Check if both results are valid (you can customize the condition as needed)
        if cross_position_x_side is not None and cross_position_x_floor is not None:
            # Store the calibration results in the session
            session['calibration_results'] = {'x_side': cross_position_x_side, 'y_side': cross_position_y_side, 'bollradie_side': ball_radius_side, 'x_floor': cross_position_x_floor, 'y_floor': cross_position_y_floor, 'bollradie_floor': ball_radius_floor}

            # Display a success message
            session.pop('_flashes', None)
            flash('Calibration successful!', 'success')
        else:
            session.pop('_flashes', None)
            flash('The dodgeball could not be detected. Choose a new calibration video.', 'error')

    return render_template('calibration.html')


@app.route('/measure', methods=['GET', 'POST'])
@login_required
def measure():
    throw_info = session.get('throw_info', {'velocity': None, 'accuracy_x': None, 'accuracy_y': None, 'total_distance': None})
    if request.method == 'POST':
        file1 = request.files['file1']
        file2 = request.files['file2']
        filename1 = secure_filename(file1.filename)
        filename2 = secure_filename(file2.filename)
        file_path1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
        file_path2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
        file1.save(file_path1)
        file2.save(file_path2)
        frame_rate = int(request.form.get('frame_rate', 0))

        calibration_results = session.get('calibration_results', None)

        if calibration_results:
            # Import the measure function from measure_module.py

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
                throw_velocity, throw_ok = velocity(x_list_side, y_list_side, x_list_floor, y_list_floor, ball_radius_side, ball_radius_floor, frame_rate)
                if throw_ok == False:
                    flash('Throw could not be measured. Choose another video.', 'error')
                    return render_template('measure.html', throw_info=throw_info)
                if throw_velocity == None:
                    session.pop('_flashes', None)
                    flash('Throw could not be measured. Choose another video.', 'error')
                else:
                    accuracy_x, accuracy_y, total_distance = accuracy(x_list_floor, y_list_side, ball_radius_side, ball_radius_floor, cal_x_floor, cal_y_floor, cal_x_side, cal_y_side)
                    session.pop('_flashes', None)
                    flash('Throw successfully measured!', 'success')
                    session['measure_results'] = {'x_list_side': x_list_side, 'y_list_side': y_list_side, 'x_list_floor': x_list_floor, 'y_list_floor': y_list_floor}
                    session['throw_info'] = {'velocity': throw_velocity, 'accuracy_x': accuracy_x, 'accuracy_y': accuracy_y, 'total_distance': total_distance}
                return render_template('measure.html', throw_info=throw_info)
            
            else:
                session.pop('_flashes', None)
                flash('Throw could not be measured. Choose another video.', 'error')
                return render_template('measure.html', throw_info=throw_info)
        else:
            session.pop('_flashes', None)
            flash("You need to calibrate before measuring.", 'error')
            return render_template('measure.html', throw_info=throw_info)
    else:
        return render_template('measure.html', throw_info=throw_info)
    

@app.route('/how-it-works', methods=['GET'])
def how_it_works():
    return render_template('how_it_works.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5002)
