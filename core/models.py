import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Profile(models.Model):
    name      = models.CharField(max_length=255)
    uuid      = models.UUIDField(default = uuid.uuid4)
        
class Movie(models.Model):
    title           = models.CharField(max_length=255, blank = True, null = True)
    original_title  = models.CharField(max_length=255, blank = True, null = True)
    file            = models.FileField(upload_to = 'movies')
    description     = models.TextField(blank = True,null = True)
    backdrop_path   = models.TextField(blank = True,null = True)
    release_date    = models.TextField(blank = True, null = True)
    runtime         = models.CharField(max_length=255, blank = True, null = True)
    vote_average    = models.CharField(max_length=255, blank = True, null = True)
    tagline         = models.CharField(max_length=255, blank = True, null = True)
    
    created_at  =   models.DateTimeField(auto_now_add=True)
    uuid        =   models.UUIDField(default = uuid.uuid4)
    thumbnail   =   models.ImageField(upload_to = 'thumbnails',default='/thumbnails/default_thumbnail.jpg', blank = True,null = True)
    
class CustomUser(AbstractUser):
    profiles = models.ManyToManyField('Profile',blank=True)
    movies   = models.ManyToManyField(Movie)

class Genre(models.Model):
    genre        =   models.CharField(max_length = 10, blank = True,null = True)
    genre_id     =   models.UUIDField(default = uuid.uuid4)
    movies       =   models.ManyToManyField(Movie)
