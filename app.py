from flask import Flask, request, jsonify, render_template
import cv2
import base64


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/capture')
def capture_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return jsonify({'error': 'Cannot open camera'}), 500

    ret, frame = cap.read()
    if not ret:
        return jsonify({'error': 'Failed to capture image'}), 500

    cv2.imwrite('captured_image.jpg', frame)
    cap.release()  # Release the capture after the image is saved

    return jsonify({'message': 'Image captured successfully!'})

def load_model():
    pass

def classify_image(image_path):
    load_model()
    return "skin_condition_class"

@app.route('/classify', methods=['POST'])
def classify():
    data = request.get_json()
    image_data = data['image']
    header, encoded = image_data.split(",", 1)
    binary_data = base64.b64decode(encoded)

    with open('captured_image.jpg', 'wb') as f:
        f.write(binary_data)

    result = classify_image('captured_image.jpg')
    return jsonify({'classification': result})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
