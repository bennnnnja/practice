import base64
from datetime import datetime
from io import BytesIO
import os 
from PIL import Image 
from django.conf import settings 
from django.core.files.storage import default_storage 
from django.http import JsonResponse 
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

            # Декодирование base64 изображения
            image_bytes = base64.b64decode(image_data)

            # Создание объекта изображения из байтов
            image = Image.open(BytesIO(image_bytes))

            # Генерация уникального имени файла
            # Используем текущее время для создания уникального имени файла
            photo_time = datetime.now().strftime("%Y%m%d%H%M%S")
            print(photo_time)
            image_name = f'captured_images/{photo_time}.png'
            

            # Проверка существования директории и ее создание, если необходимо
            image_dir = os.path.join(settings.MEDIA_ROOT, image_name)

            # Сохранение изображения
            image.save(image_dir)

            return JsonResponse({'message': 'Image saved successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

