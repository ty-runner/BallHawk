from flask import Flask, request, jsonify
from flask_cors import CORS
import os
# this is going to be the upload point of the frontend, from here the video quality will be graded

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        return jsonify({'message': 'No video file part'}), 400

    file = request.files['video']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    try:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        return jsonify({'message': 'File uploaded successfully', 'file': filepath}), 200
    except Exception as e:
        return jsonify({'message': 'Error uploading file', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
