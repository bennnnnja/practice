import base64
from datetime import datetime
from io import BytesIO
import os
from PIL import Image 
import cv2
from django.conf import settings 
from django.core.files.storage import default_storage 
from django.http import JsonResponse, StreamingHttpResponse 
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def webcam_view(request):    
    return render(request, 'webcam_view.html')

@csrf_exempt
def save_image(request):
    if request.method == 'POST':
        try:
            # Получение данных изображения из POST-запроса
            image_data = request.POST.get('image')

            # Удаление префикса data:image/png;base64, если он присутствует
            if image_data.startswith('data:image'):
                print("Yes!")
                _, image_data = image_data.split(',', 1)

            # Декодируем строку base64 в байты
            image_bytes = base64.b64decode(image_data)

            # Создаем объект BytesIO из декодированных байтов
            image_io = BytesIO(image_bytes)

            # Открываем изображение с помощью PIL
            image = Image.open(image_io)

            # Используем текущее время для создания уникального имени файла
            photo_time = datetime.now().strftime("%Y%m%d%H%M%S")
            print(photo_time)
            image_name = f'captured_images/{photo_time}.png'
            
            # Правильный способ определения пути к директории
            image_dir = os.path.join(settings.MEDIA_ROOT, 'captured_images', image_name)

            # Сохранение изображения
            image.save(image_dir)

            return JsonResponse({'message': 'Image saved successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        if not success:
            return None
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

def video_feed(request):
    camera = VideoCamera()
    return StreamingHttpResponse(gen(camera), content_type='multipart/x-mixed-replace; boundary=frame')

def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame is None:
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
