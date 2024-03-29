import uuid
import boto3
import os
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Mood, Song, CustomUser, MoodPhoto
from .forms import CustomUserCreationForm, CustomUserChangeForm, SongForm
from django.views.generic import CreateView, UpdateView, DeleteView



from django.contrib.auth.decorators import login_required
import random



# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        return redirect('login')

def about(request):
  return render(request, 'about.html')

@login_required
def moods_index(request):
  songs=Song.objects.all()
  moods=Mood.objects.filter(user = request.user.id)
  return render(request, 'moods/index.html', {
    'songs': songs,
    'moods': moods,
  })

@login_required
def playlists(request):
  songs = Song.objects.all()
  return render(request, 'playlists.html', {
    'songs': songs
  })

class CreateMood(CreateView):
  model = Mood
  fields = ["title", "content"]
  
class MoodUpdate(UpdateView):
  model = Mood
  fields = [ 'title', 'content']
  
class MoodDelete(DeleteView):
  model = Mood
  success_url = '/moods'
  

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = CustomUserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

@login_required
def user_logout(request):
    if request.method == 'POST':
        # Log the user out
        logout(request)
        # Redirect to the home page or any other desired page
        return redirect('home')
    # If it's a GET request, you can handle it differently or just redirect to home
    # Log the user out
    logout(request)
    return redirect('home')
  
  
def moods_detail(request, mood_id):
    mood= Mood.objects.get(id=mood_id)
    songs = Song.objects.filter(mood= mood)
    song = songs[random.randint(0, songs.count()-1)]
    return render(request, 'moods/detail.html', {
        'mood' :mood,
        'song': song
        })
  
def song_file(request, mood_id):

  song_file = request.FILES.get('song-file', None)
  if song_file:
      s3 = boto3.client('s3')
    
      key = uuid.uuid4().hex[:6] + song_file.name[song_file.name.rfind('.'):]
      try:
        bucket = os.environ['S3_BUCKET']
        s3.upload_fileobj(song_file, bucket, key)
        url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
        Song.objects.create(url=url, mood_id=mood_id)
      except Exception as e:
        print('An error occurred uploading file to S3')
        print(e)
  return redirect('detail', mood_id=mood_id) 

def mood_not_found(request):
    return render(request, 'mood_not_found.html')

  
def happy_playlist(request):
    moods = Mood.objects.filter(title='HAPPY')

    if not moods.exists():
        return render(request, 'mood_not_found.html')

    mood = moods.first()
    songs = Song.objects.filter(mood=mood)

    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.get(id=request.user.id)
            new_song = form.save(commit=False)
            new_song.mood = mood
            new_song.save()
            user.favorites.add(new_song)
            return redirect('happy_playlist')
    else:
        form = SongForm()

    context = {'songs': songs, 'mood': mood, 'form': form, 'playlist': 'happy_playlist'}
    return render(request, 'playlists/happy_playlist.html', context)

def sad_playlist(request):
    moods = Mood.objects.filter(title='SAD')

    if not moods.exists():
        return render(request, 'mood_not_found.html')

    mood = moods.first()
    songs = Song.objects.filter(mood=mood)

    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.get(id=request.user.id)
            new_song = form.save(commit=False)
            new_song.mood = mood
            new_song.save()
            user.favorites.add(new_song)
            return redirect('sad_playlist')
    else:
        form = SongForm()

    context = {'songs': songs, 'mood': mood, 'form': form, 'playlist': 'sad_playlist'}
    return render(request, 'playlists/sad_playlist.html', context)

def angry_playlist(request):
    moods = Mood.objects.filter(title='ANGRY')

    if not moods.exists():
        return render(request, 'mood_not_found.html')
    
    mood = moods.first()
    songs = Song.objects.filter(mood=mood)

    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.get(id=request.user.id)
            new_song = form.save(commit=False)
            new_song.mood = mood
            new_song.save()
            user.favorites.add(new_song)
            return redirect('angry_playlist')
    else:
        form = SongForm()

    context = {'songs': songs, 'mood': mood, 'form': form, 'playlist': 'angry_playlist'}
    return render(request, 'playlists/angry_playlist.html', context)


def calm_playlist(request):
    moods = Mood.objects.filter(title='CALM')

    if not moods.exists():
      return render(request, 'mood_not_found.html')

    mood = moods.first()
    songs = Song.objects.filter(mood=mood)

    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.get(id=request.user.id)
            new_song = form.save(commit=False)
            new_song.mood = mood
            new_song.save()
            user.favorites.add(new_song)
            return redirect('calm_playlist')
    else:
        form = SongForm()

    context = {'songs': songs, 'mood': mood, 'form': form, 'playlist': 'calm_playlist'}
    return render(request, 'playlists/calm_playlist.html', context)

def bored_playlist(request):
    moods = Mood.objects.filter(title='BORED')

    if not moods.exists():
      return render(request, 'mood_not_found.html')

    mood = moods.first()
    songs = Song.objects.filter(mood=mood)

    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.get(id=request.user.id)
            new_song = form.save(commit=False)
            new_song.mood = mood
            new_song.save()
            user.favorites.add(new_song)
            return redirect('bored_playlist')
    else:
        form = SongForm()

    context = {'songs': songs, 'mood': mood, 'form': form, 'playlist': 'bored_playlist'}
    return render(request, 'playlists/bored_playlist.html', context)

def anxious_playlist(request):
    moods = Mood.objects.filter(title='ANXIOUS')

    if not moods.exists():
      return render(request, 'mood_not_found.html')

    mood = moods.first()
    songs = Song.objects.filter(mood=mood)

    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.get(id=request.user.id)
            new_song = form.save(commit=False)
            new_song.mood = mood
            new_song.save()
            user.favorites.add(new_song)
            return redirect('anxious_playlist')
    else:
        form = SongForm()

    context = {'songs': songs, 'mood': mood, 'form': form, 'playlist': 'anxious_playlist'}
    return render(request, 'playlists/anxious_playlist.html', context)

def add_song(request, mood_id):
    try:
        mood = Mood.objects.get(pk=mood_id)
    except Mood.DoesNotExist:
        return redirect('home')

    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            new_song = form.save(commit=False)
            new_song.mood = mood
            new_song.save()
            user = CustomUser.objects.get(id=request.user.id)
            user.favorites.add(new_song)
            return redirect(f'{mood.title.lower()}_playlist')  # Redirect to the specific playlist page
    else:
        form = SongForm()

    return render(request, 'add_song.html', {'form': form})

def delete_song(request, song_id, playlist):
    try:
        song = Song.objects.get(id=song_id)
        song.delete()
    except Song.DoesNotExist:
        print("Song Does Not Exist")
    
    return redirect(playlist)

def edit_song(request, song_id, playlist):
    try:
        song = Song.objects.get(id=song_id)
        mood = song.mood

        if request.method == 'POST':
            form = SongForm(request.POST, instance=song)
            if form.is_valid():
                form.save()
                return redirect(playlist)  # Redirect back to the appropriate playlist URL
        else:
            form = SongForm(instance=song)

        return render(request, 'edit_song.html', {'form': form, 'song': song, 'mood': mood, 'playlist': playlist})
    except Song.DoesNotExist:
        print("Song Does Not Exist")
    
    return redirect(playlist)  # Redirect back to the appropriate playlist URL

def add_photo(request, user_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        bucket = os.environ['S3_BUCKET']
        s3.upload_fileobj(photo_file, bucket, key)
        url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
        user = CustomUser.objects.get(id=user_id)
        user.avatar = url
        user.save()
    return redirect('home')

def user_detail(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    return render(request, 'user/user_detail.html', {
        'user': user
    })
    

def add_moodphoto(request,mood_id):
    moodphoto_file = request.FILES.get('moodphoto_file', None)
    if moodphoto_file:
        s3=boto3.client('s3')
        
        key = uuid.uuid4().hex[:6] + moodphoto_file.name[moodphoto_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_MOOD_BUCKET']
            s3.upload_fileobj(moodphoto_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            MoodPhoto.objects.create(url=url, mood_id=mood_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', mood_id=mood_id)