from django.urls import path

from Juki import views

urlpatterns = [
    path('user', views.UserList.as_view(), name='user'),
    path('user/<str:pk>/', views.UserDetail.as_view(), name='userDetail'),
    path('playlist', views.PlaylistList.as_view(), name='playlist'),
    path('playlist/addMember', views.add_members_to_playlist, name='addMember'),
    path('playlist/<str:pk>/', views.PlaylistDetail.as_view(), name='playlistDetail'),
    path('song', views.SongList.as_view(), name='song'),
    path('song/<int:pk>/', views.SongDetail.as_view(), name='songDetail'),
    path('vote', views.VoteList.as_view(), name='vote'),
    path('vote/<int:pk>/', views.VoteDetail.as_view(), name='voteDetail'),
    path('authSpotify', views.trade_code_for_token, name='authSpotify'),
    path('refreshSpotify', views.trade_refresh_for_token, name='refreshToken'),
    path('play', views.play, name='play'),
]
