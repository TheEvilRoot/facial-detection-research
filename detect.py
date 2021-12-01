from PIL import Image
import io
import cv2
import numpy

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def process(data):
    if not isinstance(data, numpy.ndarray):
        image = Image.open(io.BytesIO(data)).convert('RGB')
        image = numpy.array(image, dtype=numpy.uint8)
    else:
        image = data
    source = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(source, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
    if not isinstance(data, numpy.ndarray):
        image = Image.fromarray(image)
        output = io.BytesIO()
        image.save(output, "PNG")
        result = output.getvalue()
    else:
        result = image
    return result 


