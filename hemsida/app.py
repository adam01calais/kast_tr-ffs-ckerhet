from flask import Flask, render_template, request
from HejHej.image_processing_module import ImageProcessing

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ImageProcessing('/Users/efraimzetterqvist/Documents').calibrate_cross('/Users/efraimzetterqvist/Documents/kal_side2.mov', 'side')
    return render_template('efraimstest.html')

if __name__ == '__main__':
    app.run()

