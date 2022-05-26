import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

AGE_CHOICES = (
    ('Alle', 'Alle'),
    ('Børn', 'Børn'),
)

MOVIE_CHOICES = (
    ('serie', 'Serie'),
    ('film', 'Film'),
)

class Profile(models.Model):
    name      = models.CharField(max_length=255)
    age_limit = models.CharField(max_length=15,choices=AGE_CHOICES)
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
    type        =   models.CharField(max_length = 10,choices=MOVIE_CHOICES, blank = True,null = True)
    thumbnail   =   models.ImageField(upload_to = 'thumbnails',default='/thumbnails/default_thumbnail.jpg', blank = True,null = True)
    age_limit   =   models.CharField(max_length = 10, choices=AGE_CHOICES, blank = True,null = True)
    
class CustomUser(AbstractUser):
    profiles = models.ManyToManyField('Profile',blank=True)
    movies   = models.ManyToManyField(Movie)

class Genre(models.Model):
    genre        =   models.CharField(max_length = 10, blank = True,null = True)
    genre_id     =   models.UUIDField(default = uuid.uuid4)
    movies       =   models.ManyToManyField(Movie)
