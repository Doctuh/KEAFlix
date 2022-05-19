from django.urls import path
from core.views import Home, ProfileList, CreateProfile,ProfileHome,MovieDetail,ShowMovie,UploadMovie

app_name = 'core'

urlpatterns = [
    path('',Home.as_view()),
    path('profile/', ProfileList.as_view(), name='profiles'),
    path('profile/create', CreateProfile.as_view(), name='create_profile'),
   
]