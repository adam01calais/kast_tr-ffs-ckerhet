import os
import cv2
from calibration_module import calibrate_cross
from flask import Flask, render_template, request, redirect, url_for, flash, session, get_flashed_messages
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key


if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def home():
    return '''
    <h1>Welcome to the Basic Website</h1>
    <a href="/calibration">Calibration</a>
    <br>
    <a href="/measure">Measure</a>
    '''

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
def measure():
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

            # Run the measure function with the calibration results and the file paths
            x_list_side, y_list_side = measure_throw(file_path1, ball_radius_side, 'side')
            x_list_floor, y_list_floor = measure_throw(file_path2, ball_radius_floor, 'floor')

            if len(x_list_side) and len(x_list_floor) > 3:
                flash('Throw successfully measured')
                session['measure_results'] = {'x_list_side': x_list_side, 'y_list_side': y_list_side, 'x_list_floor': x_list_floor, 'y_list_floor': y_list_floor}

            else:
                flash('Throw could not be measured. Make another throw!')

            # Do something with the measure_result (e.g., display it or store it in the session)
            # ...

        return redirect(url_for('measure'))

    return render_template('measure.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
