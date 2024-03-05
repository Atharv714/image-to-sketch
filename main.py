import os
from flask import Flask, render_template, request, send_from_directory
import cv2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

def convert_to_sketch(input_image_path):
    image = cv2.imread(input_image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inverted_image = cv2.bitwise_not(gray_image)
    smooth_image = cv2.GaussianBlur(inverted_image, (101, 101), 0)
    again_actual = cv2.bitwise_not(smooth_image)
    sketch_image = cv2.divide(gray_image, again_actual, scale=256.0)
    return sketch_image

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('index.html', error='No file part')

    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error='No selected file')

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        sketch_image = convert_to_sketch(file_path)
        result_path = os.path.join(app.config['UPLOAD_FOLDER'], 'result.jpg')
        cv2.imwrite(result_path, sketch_image)

        return render_template('index.html', original_image=file.filename, result_image='result.jpg')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete_image', methods=['POST'])
def delete_image():
    uploaded_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'result.jpg')
    

    original_image_name = request.form.get('original_image')
    original_image_path = os.path.join(app.config['UPLOAD_FOLDER'], original_image_name)


    if os.path.exists(uploaded_image_path):
        os.remove(uploaded_image_path)


    if original_image_name and os.path.exists(original_image_path):
        os.remove(original_image_path)

    return 'Images deleted successfully'


if __name__ == '__main__':
    app.run(debug=False, host = '0.0.0.0')
