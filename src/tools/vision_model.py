from transformers import pipeline

_classifier = None

def get_bird_prediction(image_path: str):
    global _classifier
    
    MODEL_NAME = "dennisjooo/Birds-Classifier-EfficientNetB2"
    
    if _classifier is None:
        _classifier = pipeline("image-classification", model=MODEL_NAME, device=0)

    results = _classifier(image_path)
    
    top_result = results[0]
    label = top_result['label']
    score = top_result['score']
        
    print(f"🧠 Model Prediction: {label} (Confidence: {score:.2f})")
    
    '''if score < 0.40:
        return None'''
            
    return label