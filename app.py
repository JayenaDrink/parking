from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
from ultralytics import YOLO
import base64
from PIL import Image
import io
import os

app = Flask(__name__)

# Load the model (will download YOLOv8 if not present)
model = None

def load_model():
    global model
    if model is None:
        # Try to load custom trained model, fallback to pretrained
        if os.path.exists('models/parking_model.pt'):
            model = YOLO('models/parking_model.pt')
        else:
            # Use pretrained YOLOv8 for demo (can detect cars)
            model = YOLO('yolov8n.pt')
    return model

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect_parking():
    try:
        # Get image from request
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        # Read and process image
        image = Image.open(file.stream)
        img_array = np.array(image)
        
        # Load model and run inference
        model = load_model()
        results = model(img_array)
        
        # Process results
        detections = []
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    confidence = box.conf[0].cpu().numpy()
                    class_id = int(box.cls[0].cpu().numpy())
                    
                    detections.append({
                        'bbox': [float(x1), float(y1), float(x2), float(y2)],
                        'confidence': float(confidence),
                        'class': class_id,
                        'label': model.names[class_id] if hasattr(model, 'names') else 'object'
                    })
        
        # Count cars vs available spaces (simplified logic)
        car_count = len([d for d in detections if d['label'] == 'car'])
        
        # Draw results on image
        annotated_img = results[0].plot()
        
        # Convert to base64 for web display
        _, buffer = cv2.imencode('.jpg', annotated_img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({
            'success': True,
            'detections': detections,
            'car_count': car_count,
            'annotated_image': img_base64,
            'message': f'Detected {car_count} cars in the parking area'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
