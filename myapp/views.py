import base64
from datetime import datetime
from io import BytesIO
import os
import cv2
from PIL import Image
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .preprocessing import resize_image


def home(request):
    return render(request, 'index.html')


@csrf_exempt
def save_image(request):
    if request.method == 'POST':
        try:
            # Получение данных изображения из POST-запроса
            image_data = request.POST.get('image')

            # Удаление префикса data:image/png;base64, если он присутствует
            if image_data.startswith('data:image'):
                _, image_data = image_data.split(',', 1)

            # Декодируем строку base64 в байты
            image_bytes = base64.b64decode(image_data)

            # Создаем объект BytesIO из декодированных байтов
            image_io = BytesIO(image_bytes)

            # Открываем изображение с помощью PIL
            image = Image.open(image_io)

            # Сохраняем исходное изображение для проверки
            original_image_name = f'captured_images/original_{datetime.now().strftime("%Y%m%d%H%M%S")}.png'
            original_image_path = os.path.join(settings.MEDIA_ROOT, original_image_name)
            image.save(original_image_path)

            # Используем функцию resize_image для обработки изображения
            resized_face = resize_image(original_image_path)

            if resized_face is not None:
                # Сохраняем обработанное изображение
                resized_image_name = f'resized_face_{datetime.now().strftime("%Y%m%d%H%M%S")}.png'
                resized_image_path = os.path.join(settings.MEDIA_ROOT, 'captured_images', resized_image_name)
                cv2.imwrite(resized_image_path, resized_face)

                return JsonResponse({'message': 'Image processed and saved successfully', 'resized_image': resized_image_name})
            else:
                return JsonResponse({'error': 'No face detected in the image'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
