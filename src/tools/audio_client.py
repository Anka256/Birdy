from birdnetlib import Recording
from birdnetlib.analyzer import Analyzer
import os

_analyzer = None

def analyze_audio(file_path: str):
    global _analyzer

    if not os.path.exists(file_path):
        return None

    if _analyzer is None:
        _analyzer = Analyzer()

    recording = Recording(
        _analyzer,
        file_path,
        min_conf=0.01,
    )
        
    recording.analyze()
    
    detections = recording.detections
    
    if not detections:
        return None

    best_prediction = max(detections, key=lambda x: x['confidence'])
        
    return {
        "common_name": best_prediction['common_name'],
        "scientific_name": best_prediction['scientific_name'],
        "confidence": best_prediction['confidence']
    }
