from django.urls import path
from.views import webcam_view, save_image
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    path('webcam/', webcam_view, name='webcam-view'),
    path('save-image/', save_image, name='save-image'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
