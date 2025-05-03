from ultralytics import YOLO
from PIL import Image,PngImagePlugin
import io

'''
def predict(contents):
    image = Image.open(io.BytesIO(contents))
    model = YOLO("best.pt")
    results = model()
    return model.predict(image)

test = Image.open('./../../СИПИ/test_image2.png')
img_byte_arr = io.BytesIO()
test.save(img_byte_arr, format='PNG')
test_bytes = img_byte_arr.getvalue()
result=predict(test_bytes)
print(result)
'''

model = YOLO("best.pt")

def predict(contents):
    image = Image.open(io.BytesIO(contents))
    results = model(image)
    probs = results[0].probs
    top1_class_id = probs.top1  # ID класса с наибольшей вероятностью
    #top1_confidence = probs.top1conf.item()  # Значение уверенности
    class_name = results[0].names[top1_class_id]
    return class_name
