from django.urls import path
from.views import webcam_view, save_image, video_feed
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    path('webcam/', webcam_view, name='webcam-view'),
    path('save-image/', save_image, name='save-image'),
    path('video_feed/', video_feed, name='video-feed'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
