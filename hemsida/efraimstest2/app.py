import os
from calibration_module import calibrate_cross
from measure_module import measure_throw
from velocity_module import velocity
from accuracy_module import accuracy
from flask import Flask, render_template, request, redirect, url_for, flash, session, current_app, abort, jsonify, send_from_directory, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf.csrf import generate_csrf
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse, urljoin
from datetime import datetime
from PIL import Image
import base64
from io import BytesIO
import numpy as np
from typing import Union

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://efraimzetterqvist:@localhost/dodgeball_throws' #'postgresql://johannaedh:@localhost/postgres', behöver ändras för olika datorer om man vill testa
app.add_url_rule('/uploads/<path:filename>', 'uploaded_file', build_only=True)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Calibration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cross_position_x_side = db.Column(db.Float, nullable=False)
    cross_position_y_side = db.Column(db.Float, nullable=False)
    ball_radius_side = db.Column(db.Float, nullable=False)
    cross_position_x_floor = db.Column(db.Float, nullable=False)
    cross_position_y_floor = db.Column(db.Float, nullable=False)
    ball_radius_floor = db.Column(db.Float, nullable=False)
    cross_position_x_side_percentage = db.Column(db.Float, nullable=False)
    cross_position_y_side_percentage = db.Column(db.Float, nullable=False)
    cross_position_x_floor_percentage = db.Column(db.Float, nullable=False)
    cross_position_y_floor_percentage = db.Column(db.Float, nullable=False)
    image_side_format = db.Column(db.String(255), nullable=False)
    image_floor_format = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"Calibration('{self.name}', '{self.date}')"
    
class Throw(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    velocity = db.Column(db.Float, nullable=False)
    distance = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    accuracy_x = db.Column(db.Float, nullable=False)  
    accuracy_y = db.Column(db.Float, nullable=False) 
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"Throw('{self.id}', '{self.velocity}', '{self.distance}', '{self.date}', '{self.accuracy_x}', '{self.accuracy_y}')"

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def encode_image_base64(img):
    img_pil = Image.fromarray(img)
    buffered = BytesIO()
    img_pil.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    return img_base64

def convert_to_json_serializable(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, tuple):
        return tuple(convert_to_json_serializable(item) for item in obj)
    return obj

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
            new_user = User()
            new_user.username = username
            new_user.password = hashed_password
            db.session.add(new_user)
            db.session.commit()
            flash('You have successfully registered! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('A user with that username already exists. Please choose a different username.', 'error')
            return redirect(url_for('register'))

    return render_template('sign_up.html')


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
    return render_template('home.html')

@app.route('/uploads/<path:filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/api/calibrate', methods=['POST'])
@login_required
def api_calibrate():
    if request.method == 'POST':
        data = request.get_json()

        #print("Received data:", data)

        center1 = data['center1']
        edge1 = data['edge1']
        center2 = data['center2']
        edge2 = data['edge2']
        width1 = data['width1']
        height1 = data['height1']
        width2 = data['width2']
        height2 = data['height2']
        image1_filename = data['image1_filename']
        image2_filename = data['image2_filename']
        orig_width1 = data['orig_width1']
        orig_height1 = data['orig_height1']
        orig_width2 = data['orig_width2']
        orig_height2 = data['orig_height2']

        results = calibrate_cross(image1_filename, 
                                  image2_filename, 
                                  center1, 
                                  edge1, 
                                  center2, 
                                  edge2, 
                                  width1, 
                                  height1,
                                  width2,
                                  height2,
                                  orig_width1, 
                                  orig_height1, 
                                  orig_width2,
                                  orig_height2,
                                  app.config['UPLOAD_FOLDER'])
        img1, img2, x_side, y_side, x_floor, y_floor, bollradie_side, bollradie_floor, cross_position_x1_percentage, cross_position_y1_percentage, cross_position_x2_percentage, cross_position_y2_percentage, image_side_format, image_floor_format = results

        new_calibration = Calibration(
            name="Calibration",  # Replace with desired name
            user_id=current_user.id,
            cross_position_x_side=x_side,
            cross_position_y_side=y_side,
            ball_radius_side=bollradie_side,
            cross_position_x_floor=x_floor,
            cross_position_y_floor=y_floor,
            ball_radius_floor=bollradie_floor,
            cross_position_x_side_percentage=cross_position_x1_percentage,
            cross_position_y_side_percentage=cross_position_y1_percentage,
            cross_position_x_floor_percentage=cross_position_x2_percentage,
            cross_position_y_floor_percentage=cross_position_y2_percentage,
            image_side_format=image_side_format,
            image_floor_format=image_floor_format
        )
        db.session.add(new_calibration)
        db.session.commit()

        json_results = convert_to_json_serializable(results)

        session['calibration_results'] = json_results

        return jsonify(json_results)

    return "Error"

@app.route('/api/upload-images', methods=['POST'])
@login_required
def upload_images():
    if request.method == 'POST':
        image1 = request.files['image1']
        image2 = request.files['image2']

        image1_filename = secure_filename(image1.filename)
        image2_filename = secure_filename(image2.filename)

        image1_path = os.path.join(app.config['UPLOAD_FOLDER'], image1_filename)
        image2_path = os.path.join(app.config['UPLOAD_FOLDER'], image2_filename)

        print(f"Saving image1 to {image1_path}")  # Add this line
        print(f"Saving image2 to {image2_path}")  # Add this line

        image1.save(image1_path)
        image2.save(image2_path)

        return jsonify({'image1_filename': image1_filename, 'image2_filename': image2_filename})

    return "Error"

@app.route('/calibration', methods=['GET', 'POST'])
@login_required
def calibration() -> Union[str, Response]:
    if request.method == 'GET':
        return render_template('calibration.html')
    return "Error"

@app.route('/measure', methods=['GET', 'POST'])
@login_required
def measure():
    selected_calibration_id = session.get('selected_calibration_id', None)
    frames_side_base64 = []
    frames_floor_base64 = []
    frame_rate = 0
    throw_info = session.get('throw_info', {'velocity': None, 
                                            'accuracy_x': None, 
                                            'accuracy_y': None, 
                                            'total_distance': None})
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

        # Check if the user has a completed calibration in the database
        if selected_calibration_id:
            calibration = Calibration.query.get(selected_calibration_id)
        else:
            calibration = Calibration.query.filter_by(user_id=current_user.id).first()

        if calibration:
            calibration_results = {
                'x_side': calibration.cross_position_x_side,
                'y_side': calibration.cross_position_y_side,
                'bollradie_side': calibration.ball_radius_side,
                'x_floor': calibration.cross_position_x_floor,
                'y_floor': calibration.cross_position_y_floor,
                'bollradie_floor': calibration.ball_radius_floor
            }
        else:
            calibration_results = None

        if calibration_results:
            # Import the measure function from measure_module.py

            # Get ball_radius_side and ball_radius_floor from calibration results
            ball_radius_side = calibration_results['bollradie_side']
            ball_radius_floor = calibration_results['bollradie_floor']
            cal_x_side = calibration_results['x_side']
            cal_y_side = calibration_results['y_side']
            cal_x_floor = calibration_results['x_floor']
            cal_y_floor = calibration_results['y_floor']

            # Run the measure function with the calibration results and the file paths
            x_list_side, y_list_side, frames_side, video_format_side, video_side_width, video_side_height = measure_throw(file_path1, ball_radius_side, 'side')
            x_list_floor, y_list_floor, frames_floor, video_format_floor, video_floor_width, video_floor_height = measure_throw(file_path2, ball_radius_floor, 'floor')
            print(video_format_floor)
            print(video_format_side)

            # Convert the frames to Base64-encoded images
            frames_side_base64 = [encode_image_base64(frame) for frame in frames_side]
            frames_floor_base64 = [encode_image_base64(frame) for frame in frames_floor]

            if frames_side and frames_floor:
                session['frames_side_base64'] = [encode_image_base64(frame) for frame in frames_side]
                session['frames_floor_base64'] = [encode_image_base64(frame) for frame in frames_floor]

            if len(x_list_side) and len(x_list_floor) > 3:
                throw_velocity, throw_ok = velocity(x_list_side, 
                                                    y_list_side, 
                                                    x_list_floor, 
                                                    y_list_floor, 
                                                    ball_radius_side, 
                                                    ball_radius_floor, 
                                                    frame_rate)
                if throw_ok == False:
                    flash('Throw could not be measured. Choose another video.', 'error')
                    return render_template('measure.html', 
                                           throw_info=throw_info,
                                           frames_side_base64=frames_side_base64, 
                                           frames_floor_base64=frames_floor_base64, 
                                           frame_rate=frame_rate)
                if throw_velocity == None:
                    session.pop('_flashes', None)
                    flash('Throw could not be measured. Choose another video.', 'error')
                else:
                    accuracy_x, accuracy_y, total_distance = accuracy(x_list_floor, 
                                                                      y_list_side, 
                                                                      ball_radius_side, 
                                                                      ball_radius_floor, 
                                                                      cal_x_floor, 
                                                                      cal_y_floor, 
                                                                      cal_x_side, 
                                                                      cal_y_side,
                                                                      calibration.cross_position_x_floor_percentage,
                                                                      calibration.cross_position_y_floor_percentage,
                                                                      calibration.cross_position_x_side_percentage,
                                                                      calibration.cross_position_y_side_percentage,
                                                                      video_format_side,
                                                                      video_format_floor,
                                                                      calibration.image_side_format,
                                                                      calibration.image_floor_format,
                                                                      video_side_width,
                                                                      video_side_height,
                                                                      video_floor_width,
                                                                      video_floor_height)
                    session.pop('_flashes', None)
                    flash('Throw successfully measured!', 'success')
                    throw_info = {'velocity': throw_velocity, 
                                  'accuracy_x': accuracy_x, 
                                  'accuracy_y': accuracy_y, 
                                  'total_distance': total_distance}
                    session['throw_info'] = throw_info
                    # Save the throw data to the database
                    throw_count = Throw.query.filter_by(user_id=current_user.id).count()
                    new_throw = Throw(user_id=current_user.id, 
                                      velocity=throw_velocity, 
                                      distance=total_distance, 
                                      accuracy_x=accuracy_x, 
                                      accuracy_y=accuracy_y, 
                                      name=f"Throw {throw_count + 1}")
                    db.session.add(new_throw)
                    db.session.commit()

                return render_template('measure.html', 
                                       throw_info=throw_info, 
                                       frames_side_base64=frames_side_base64, 
                                       frames_floor_base64=frames_floor_base64, 
                                       frame_rate=frame_rate)

            else:
                session.pop('_flashes', None)
                flash('Throw could not be measured. Choose another video.', 'error')
                return render_template('measure.html', 
                                       throw_info=throw_info, 
                                       frames_side_base64=frames_side_base64, 
                                       frames_floor_base64=frames_floor_base64, 
                                       frame_rate=frame_rate)
        else:
            session.pop('_flashes', None)
            flash("You need to calibrate before measuring.", 'error')
            return render_template('measure.html', 
                                   throw_info=throw_info, 
                                   frames_side_base64=frames_side_base64, 
                                   frames_floor_base64=frames_floor_base64, 
                                   frame_rate=frame_rate)
    else:
        return render_template('measure.html', 
                               throw_info=throw_info, 
                               frames_side_base64=frames_side_base64, 
                               frames_floor_base64=frames_floor_base64, 
                               frame_rate=frame_rate)
    

@app.route('/how-it-works', methods=['GET'])
def how_it_works():
    return render_template('how_it_works.html')


@app.route('/my-page', methods=['GET', 'POST'])
@login_required
def my_page():
    user_throws = Throw.query.filter_by(user_id=current_user.id).all()
    calibrations = Calibration.query.filter_by(user_id=current_user.id).all()
    csrf_token = generate_csrf()
    return render_template('my_page.html', throws=user_throws, calibrations=calibrations, csrf_token=csrf_token)


@app.route('/remove-throw/<int:throw_id>', methods=['POST'])
@login_required
def remove_throw(throw_id):
    throw = Throw.query.get_or_404(throw_id)
    if throw.user_id != current_user.id:
        abort(403)
    db.session.delete(throw)
    db.session.commit()
    flash('Throw removed successfully.', 'success')
    return redirect(url_for('my_page'))

@app.route('/remove_calibration/<int:calibration_id>', methods=['POST'])
@login_required
def remove_calibration(calibration_id):
    calibration = Calibration.query.get(calibration_id)
    if calibration is not None and calibration.user_id == current_user.id:
        db.session.delete(calibration)
        db.session.commit()
        flash('Calibration removed.', 'success')
    else:
        flash('Calibration not found or not authorized.', 'danger')
    return redirect(url_for('my_page'))

@app.route('/select_calibration/<int:calibration_id>')
@login_required
def select_calibration(calibration_id):
    calibration = Calibration.query.get_or_404(calibration_id)
    if calibration.user_id != current_user.id:
        abort(403)
    session['selected_calibration_id'] = calibration_id
    return redirect(url_for('my_page'))

@app.route('/update_calibration_name/<int:calibration_id>', methods=['POST'])
@login_required
def update_calibration_name(calibration_id):
    calibration = Calibration.query.get_or_404(calibration_id)
    if calibration.user_id != current_user.id:
        abort(403)

    new_name = request.json.get('name')
    if new_name and len(new_name.strip()) > 0:
        calibration.name = new_name.strip()
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Invalid name'})

@app.route('/update_throw_name/<int:throw_id>', methods=['POST'])
@login_required
def update_throw_name(throw_id):
    throw = Throw.query.get_or_404(throw_id)
    if throw.user_id != current_user.id:
        abort(403)

    new_name = request.json.get('name')
    if new_name and len(new_name.strip()) > 0:
        throw.name = new_name.strip()
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Invalid name'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5002)
