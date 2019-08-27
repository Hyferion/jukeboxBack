from django.conf.urls import url
from django.urls import path
from . import consumers

webbsocket_urlpatterns = [
    path('ws/test/<str:pk>', consumers.PlaylistConsumer, name='PlaylistConsumer'),
]
# docker run -p 6379:6379 -d redis:2.8
