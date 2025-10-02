from flask import Flask, request, jsonify, render_template
import base64
from PIL import Image, ImageDraw
import io
import os
import random

app = Flask(__name__)

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
        
        # Create a copy for annotation
        annotated_img = image.copy()
        draw = ImageDraw.Draw(annotated_img)
        
        # Mock parking detection (simulate AI results)
        width, height = image.size
        
        # Generate random car detections
        car_count = random.randint(3, 8)
        detections = []
        
        for i in range(car_count):
            # Random bounding box
            x1 = random.randint(50, width - 200)
            y1 = random.randint(50, height - 150)
            x2 = x1 + random.randint(80, 150)
            y2 = y1 + random.randint(60, 100)
            
            # Draw bounding box
            draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
            draw.text((x1, y1-20), f"Car {i+1}", fill="red")
            
            detections.append({
                'bbox': [x1, y1, x2, y2],
                'confidence': round(random.uniform(0.7, 0.95), 2),
                'class': 2,
                'label': 'car'
            })
        
        # Convert annotated image to base64
        buffer = io.BytesIO()
        annotated_img.save(buffer, format='JPEG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        # Calculate parking info
        total_spaces = random.randint(15, 25)
        empty_spaces = total_spaces - car_count
        
        return jsonify({
            'success': True,
            'detections': detections,
            'car_count': car_count,
            'empty_spaces': empty_spaces,
            'total_spaces': total_spaces,
            'annotated_image': img_base64,
            'message': f'Detected {car_count} cars, {empty_spaces} empty spaces available'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'Simple parking detector running'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
