#
# from django.urls import path
# from .views import VideoInfoAPIView, GenerateDownloadLinkAPIView
#
# urlpatterns = [
#     path('video-info/', VideoInfoAPIView.as_view(), name='video_info'),
#     path('generate-link/', GenerateDownloadLinkAPIView.as_view(), name='generate_link'),
# ]


# api/urls.py

# video_downloader_app/urls.py
# api/urls.py

from django.urls import path
from .views import GetVideoInfoView, DownloadAudioView

urlpatterns = [
    path('get-video-info/', GetVideoInfoView.as_view(), name='get-video-info'),
    path('download-audio/', DownloadAudioView.as_view(), name='download-audio'),
]
