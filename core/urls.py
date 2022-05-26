from django.urls import path
from core.views import Home, ProfileList, CreateProfile,ProfileHome,MovieDetail,ShowMovie,UploadMovie,GenresList,Search



app_name = 'core'

urlpatterns = [
    path('',Home.as_view(), name = 'home'),
    path('home/search/', Search.as_view(), name='search'),
    path('profile/', ProfileList.as_view(), name='profiles'),
    path('profile/create', CreateProfile.as_view(), name='create_profile'),
    path('home/<str:profile_id>/', ProfileHome.as_view(), name='profileHome'),
    path('genres/', GenresList.as_view(), name='genres_list'),
    path('movie/detail/<str:movie_id>/', MovieDetail.as_view(), name='show_movie'),
    path('movie/play/<str:movie_id>', ShowMovie.as_view(), name='movie_play'),
    
]