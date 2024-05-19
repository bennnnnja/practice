import cv2
import os

def resize_image(image_path):
    if not os.path.isfile(image_path):
        print(f"File '{image_path}' does not exist.")
        return None

    # Загружаем изображение
    img = cv2.imread(image_path)

    if img is None:
        print(f"Unable to read image '{image_path}'.")
        return None

    # Преобразуем изображение в оттенки серого для улучшения производительности
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Загружаем предобученный классификатор для обнаружения лиц
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Ищем лица на изображении
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) > 0:
        # Берем первое обнаруженное лицо (можно выбрать любое, если нужно)
        x, y, w, h = faces[0]

        # Обрезаем лицо квадратом
        face_square = img[y:y+h, x:x+w]

        # Ужимаем изображение до 44x44 пикселей
        resized_face = cv2.resize(face_square, (44, 44))

        return resized_face
    else:
        print("Лицо не найдено")
        return None
