import os
import cv2
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from calibration_module import calibrate_cross

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/calibration', methods=['GET', 'POST'])
def calibration():
    if request.method == 'POST':
        file1 = request.files['file1']
        file2 = request.files['file2']
        filename1 = secure_filename(file1.filename)
        filename2 = secure_filename(file2.filename)
        file_path1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
        file_path2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
        file1.save(file_path1)
        file2.save(file_path2)

        calibrate_cross(file_path1)  # Run the calibration function for the first file
        calibrate_cross(file_path2)  # Run the calibration function for the second file

        return redirect(url_for('calibration'))

    return render_template('calibration.html')

@app.route('/measure')
def measure():
    return render_template('measure.html')

if __name__ == '__main__':
    app.run(debug=True)
