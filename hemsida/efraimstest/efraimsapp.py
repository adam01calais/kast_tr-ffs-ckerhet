from HejHej.image_processing_module import ImageProcessing
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calibrate', methods=['POST'])
def calibrate():
    # code to process calibration videos
    return "Calibration complete."

@app.route('/analyze', methods=['POST'])
def analyze():
    # code to process throw video and calculate velocity and accuracy
    velocity = 80 # example velocity value
    accuracy = "Bullseye" # example accuracy value
    # code to display accuracy on dartboard
    dartboard = "X" # example dartboard display
    return {'velocity': velocity, 'accuracy': accuracy, 'dartboard': dartboard}

if __name__ == '__main__':
    app.run()
