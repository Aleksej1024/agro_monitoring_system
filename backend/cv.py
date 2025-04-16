from ultralytics import YOLO
from PIL import Image
import io

def predict(contents):
    image = Image.open(io.BytesIO(contents))
    model = YOLO("best.pt")
    results = model()
    return results[0]
