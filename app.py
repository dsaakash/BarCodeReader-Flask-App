from flask import Flask, render_template, request
import csv
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import os
import base64

app = Flask(__name__)

def create_csv_file():
    with open('data.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Barcode'])

def update_csv_file(barcode_data):
    file_exists = os.path.isfile('data.csv')
    with open('data.csv', 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        if not file_exists:
            csv_writer.writerow(['Barcode'])
        csv_writer.writerow([barcode_data])

def convert_image_to_base64(image):
    _, buffer = cv2.imencode('.png', image)
    return base64.b64encode(buffer).decode('utf-8')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return render_template('index.html', error='No file selected')

    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error='No file selected')

    # Read the uploaded image using OpenCV
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Find and decode barcodes in the image
    barcodes = pyzbar.decode(image)

    if not barcodes:
        return render_template('index.html', error='No barcode found')

    # Assuming there is only one barcode in the image
    barcode_data = barcodes[0].data.decode('utf-8')

    # Update CSV file with barcode data
    update_csv_file(barcode_data)  # Replace 'Actual Information' with the appropriate value

    # Convert image to base64 format
    barcode_image = convert_image_to_base64(image)

    return render_template('index.html', data={'barcode': barcode_data, 'image': f'data:image/png;base64,{barcode_image}'})

if __name__ == '__main__':
    if not os.path.isfile('data.csv'):
        create_csv_file()
    app.run(debug=True)
