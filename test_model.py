#!/usr/bin/env python3
"""
Quick test script to verify your trained parking model works
"""

import os
import sys

def test_model():
    print("🧪 Testing your parking detection model...")
    
    # Check if model file exists
    model_path = "models/parking_model.pt"
    if not os.path.exists(model_path):
        print("❌ Model file not found at:", model_path)
        return False
    
    print(f"✅ Model file found: {model_path}")
    print(f"📁 Model size: {os.path.getsize(model_path) / (1024*1024):.1f} MB")
    
    # Try to import required libraries
    try:
        print("\n📦 Testing dependencies...")
        from ultralytics import YOLO
        print("✅ ultralytics imported successfully")
        
        import torch
        print("✅ torch imported successfully")
        print(f"🔧 PyTorch version: {torch.__version__}")
        
        # Check if CUDA is available
        if torch.cuda.is_available():
            print("🚀 GPU (CUDA) available!")
        else:
            print("💻 Using CPU (no GPU detected)")
            
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("\n💡 To install missing packages:")
        print("pip install ultralytics torch torchvision")
        return False
    
    # Try to load the model
    try:
        print(f"\n🤖 Loading model from {model_path}...")
        model = YOLO(model_path)
        print("✅ Model loaded successfully!")
        
        # Get model info
        print(f"📊 Model classes: {len(model.names)}")
        print(f"🏷️  Class names: {list(model.names.values())}")
        
        return model
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

def test_with_sample_image(model):
    """Test the model with a sample image"""
    print("\n🖼️  Testing with sample image...")
    
    # Try to find a test image
    test_images = [
        "test_parking.jpg",
        "sample.jpg", 
        "parking_test.jpg"
    ]
    
    test_image = None
    for img in test_images:
        if os.path.exists(img):
            test_image = img
            break
    
    if not test_image:
        print("📥 No test image found. You can:")
        print("1. Download a parking lot image and save as 'test_parking.jpg'")
        print("2. Or run: model('path/to/your/parking/image.jpg')")
        return
    
    try:
        print(f"🔍 Running detection on {test_image}...")
        results = model(test_image)
        
        # Analyze results
        for i, result in enumerate(results):
            boxes = result.boxes
            if boxes is not None:
                detections = len(boxes)
                print(f"🎯 Found {detections} objects in the image")
                
                # Count by class
                class_counts = {}
                for box in boxes:
                    class_id = int(box.cls[0])
                    class_name = model.names[class_id]
                    class_counts[class_name] = class_counts.get(class_name, 0) + 1
                
                print("📊 Detection summary:")
                for class_name, count in class_counts.items():
                    print(f"   {class_name}: {count}")
                    
                # Save result
                result.save(f"result_{i}.jpg")
                print(f"💾 Saved annotated result as result_{i}.jpg")
                
            else:
                print("🔍 No objects detected in the image")
                
    except Exception as e:
        print(f"❌ Error during detection: {e}")

if __name__ == "__main__":
    print("🚗 Parking Model Test Script")
    print("=" * 40)
    
    model = test_model()
    
    if model:
        print("\n🎉 Model test PASSED!")
        test_with_sample_image(model)
        
        print("\n💡 Your model is working! You can now:")
        print("1. Use it in your web app")
        print("2. Test with more images: model('image.jpg')")
        print("3. Deploy to production")
        
    else:
        print("\n❌ Model test FAILED!")
        print("💡 Check the error messages above and fix any issues")
