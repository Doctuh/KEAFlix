from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from core.forms import ProfileForm,MovieForm
from core.models import Profile, Movie, Genre, CustomUser
import requests
import json



api_key = 'c9ad551c621fd58b2a973511eb5b4306'

def get_movie_id(title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&language=en-US&query={title}&page=1&include_adult=false"
    response = requests.get(url)
    
    if response.status_code == 200:
        print(response.status_code)
        json_data = json.loads(response.text)
        print(json_data['total_results'])
        if json_data['total_results'] == 0:
            print("Returning None!!!!")
            return None
        else:
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
        genres = list()
        
        json_genres = json_data['genres']
        for i in json_genres:
            current_genre = i['name']
            genres.append(current_genre)
            
    return description,backdrop_path,original_title,release_date,runtime,vote_average,tagline, genres

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
        user = request.user
        duplicate_movie = False
        
        print(form.is_valid())
        if form.is_valid():
            print(form.cleaned_data)
            title = form.cleaned_data['title']
            file = form.cleaned_data['file']
            
            if get_movie_id(title) != None:
                movie_id = get_movie_id(title)
            else:
                return redirect('upload_film')
            
            description,backdrop_path,original_title,release_date,runtime,vote_average,tagline,genres = get_movie_details(movie_id)
            
            movie = Movie()
            movie.title = title
            movie.file = file
            movie.description = description
            movie.original_title = original_title
            movie.release_date = release_date
            movie.runtime = runtime
            movie.vote_average = vote_average
            if backdrop_path != None:
                movie.backdrop_path = "https://image.tmdb.org/t/p/original" + backdrop_path
            movie.tagline = tagline
            
            movies = Movie.objects.all()
            db_genre = ""
            
            for mov in movies:
                if mov.original_title == movie.original_title:
                    duplicate_movie = True                
            
            print("movie dup?: " + str(duplicate_movie))
            
            for genre in genres:
                try:
                    genre_to_save = Genre.objects.get(genre=genre)
                except Genre.DoesNotExist:
                    print(genre + " is not in database, adding an entry for it!")
                    genre_to_save = Genre()
                    genre_to_save.genre = genre
                    genre_to_save.save()
                    print("Added genre: " + str(genre) + " to database")                     
                    0
                                
                print(genre_to_save, genre)
                
            if not duplicate_movie:
                movie.save()
                genre_to_save.movies.add(movie)
                print("Added movie: " + str(movie) + " to: " + str(genre) + " relationship") 
                genre_to_save = Genre.objects.get(genre=genre)
                genre_to_save.movies.add(movie)
                user.movies.add(movie)
                print("Added movie: " + str(movie.original_title) + " to database for user: " + user.username)
                    
            elif duplicate_movie:
                mov = Movie.objects.get(original_title = movie.original_title)
                movie_owners = mov.customuser_set.all()
                try: 
                    movie_owners.get(username=user)
                        
                except (CustomUser.DoesNotExist):
                    print(mov.original_title + " exists in database but user: " + user.username + " does not own it ")
                    print("Adding: " + user.username + " to owner!")
                    user.movies.add(mov)
                    
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
            user = request.user
            try:
                profile = Profile.objects.get(uuid = profile_id)
                movies = user.movies.all()
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

                first_genre = movie.genre_set.first()

                movies_genre = first_genre.movies.all()[:5]

                return render(request, 'movie_detail.html',{'movie':movie, 'related_movies':movies_genre})

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
    
class GenresList(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, 'genre_list.html')

class Search(View):
    def get(self, request, *args, **kwargs):
        movie_found = False
        genre_found = False
        if request.user.is_authenticated:    
            search_query =  request.GET.get('search')     
            print("Search query is: " + str(search_query)) 
            try:
                status = Movie.objects.filter(original_title__contains=search_query)
                if status.exists():
                    movie_found = True
                else:
                    status = None
                    movie_found = False
                    try:
                        status = Genre.objects.filter(genre__contains=search_query)
                        if status.exists():
                            status = status.first()
                            genre_found = True
                            movies_found = status.movies.all()
                            print(status)
                        else:
                            status = None
                            genre_found = False
                    except Genre.DoesNotExist:
                        status = None
            
            except Movie.DoesNotExist:
                status = None
            
            print(f"Status {status} {movie_found} {genre_found}")   
            if  movie_found:    
                return render(request,"search.html",{"movies":status, "movie_found":movie_found})
            elif genre_found:
                return render(request,"search.html",{"genres":movies_found, "genre_found":genre_found})
        
        return render(request,"search.html",{"movie_found":movie_found,"genre_found":genre_found})