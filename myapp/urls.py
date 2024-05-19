from django.urls import path
from.views import home, save_image
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    path('', home, name='home'),
    path('save-image/', save_image, name='save-image'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

