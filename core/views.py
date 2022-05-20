from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from core.forms import ProfileForm,MovieForm
from core.models import Profile, Movie
import requests
import json



api_key = 'c9ad551c621fd58b2a973511eb5b4306'

def get_movie_id(title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&language=en-US&query={title}&page=1&include_adult=false"
    response = requests.get(url)
    
    if response.status_code == 200:
        json_data = json.loads(response.text)
        guess_movie_id = json_data['results'][0]['id']
    return guess_movie_id

def get_movie_details(movie_id):
     
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)
    
    if response.status_code == 200:
        json_data = json.loads(response.text)
        description = json_data['overview']
        backdrop_path = json_data['backdrop_path']
        original_title = json_data['original_title']
        release_date = json_data['release_date']
        runtime = json_data['runtime']
        vote_average = json_data['vote_average']
        tagline = json_data['tagline']
        
    return description,backdrop_path,original_title,release_date,runtime,vote_average,tagline

class Home(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:profiles')
        return render(request, 'core/index.html')
    
class UploadMovie(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/accounts/login')
        else:
            return render(request, 'core/video_upload.html')

    def post(self,request,*args,**kwargs):
        form = MovieForm(request.POST, request.FILES or None)
        duplicate_movie = False
        print(form.is_valid())
        if form.is_valid():
            print(form.cleaned_data)
            title = form.cleaned_data['title']
            file = form.cleaned_data['file']
            
            movie_id = get_movie_id(title)
            description,backdrop_path,original_title,release_date,runtime,vote_average,tagline = get_movie_details(movie_id)
            
            movie = Movie()
            movie.title = title
            movie.file = file
            movie.description = description
            movie.original_title = original_title
            movie.release_date = release_date
            movie.runtime = runtime
            movie.vote_average = vote_average
            movie.backdrop_path = "https://image.tmdb.org/t/p/original" + backdrop_path
            movie.tagline = tagline
            
            movies = Movie.objects.all()
            
            for mov in movies:
                if mov.title == movie.original_title:
                    duplicate_movie == True
                    return redirect('core:profiles')

                
            if not duplicate_movie:
                movie.save()
                return redirect('core:profiles')

                
            return redirect('core:profiles')
            
class ProfileList(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            profiles = request.user.profiles.all()
            return render(request, 'profile_list.html', { 'profiles':profiles })
        return render(request, 'core/index.html')
    
class CreateProfile(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = ProfileForm()
            return render(request, 'profile_create.html', {'form':form})
        return render(request, 'core/index.html')
    
    def post(self,request,*args,**kwargs):
        form = ProfileForm(request.POST or None)

        if form.is_valid():
            #print(form.cleaned_data)
            profile = Profile.objects.create(**form.cleaned_data)
            if profile:
                request.user.profiles.add(profile)
                return redirect('core:profiles')
        return render(request, 'profile_create.html', {'form':form})
class ProfileHome(View):
    def get(self, request, profile_id, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                profile = Profile.objects.get(uuid = profile_id)
                movies = Movie.objects.all()
                try:
                    show_case = movies.last()
                except:
                    show_case = None
                
                if profile not in request.user.profiles.all():
                    return redirect(to='core:profiles')    
                
                return render(request, 'movie_list.html', {'movies':movies, 'show_case':show_case})
            except Profile.DoesNotExist:
                return redirect(to='core:profiles')
        return render(request, 'core/index.html')
            
class MovieDetail(View):
    def get(self, request, movie_id, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                movie = Movie.objects.get(uuid = movie_id)
                return render(request, 'movie_detail.html',{'movie':movie})
            except movie.DoesNotExist:
                redirect(to='core:profileHome')
        return render(request, 'core/index.html')

class ShowMovie(View):
    def get(self, request, movie_id, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                movie = Movie.objects.get(uuid = movie_id)
                
                return render(request, 'show_movie.html',{'movie':movie})
            except movie.DoesNotExist:
                redirect(to='core:profileHome')
        return render(request, 'core/index.html')
            
            
