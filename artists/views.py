# In views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Artist, Art
from .forms import ArtistForm

#
# --- Public Views (User is NOT logged in) ---
#

def home(request):
    """
    Renders the main landing page (firstpage.html) for visitors.
    """
    return render(request, 'firstpage.html')

def homepage(request):
    """
    Renders the "Meet Our Artisans" page, showing all artists.
    This is a public page for visitors.
    """
    artists = Artist.objects.all()
    context = {'artists': artists}
    return render(request, 'meetartistpage.html', context)

#
# --- Authentication Views ---
#

def register_artist(request):
    """
    Handles new artist registration.
    """
    # ... (This function is correct and remains unchanged) ...
    if request.method == 'POST':
        form = ArtistForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = ArtistForm()
    return render(request, 'registrationartist.html', {'form': form})


def login_view(request):
    """
    Handles user login and redirects to the artist's personal art gallery.
    """
    if request.method == 'POST':
        username_from_form = request.POST.get('username')
        password_from_form = request.POST.get('password')
        try:
            artist = Artist.objects.get(username=username_from_form)
            if artist.password == password_from_form:
                request.session['username'] = artist.username
                # ✅ CORRECTED: Redirect to the personal art gallery after login
                return redirect('art_gallery') 
            else:
                messages.error(request, 'Invalid username or password.')
        except Artist.DoesNotExist:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

#
# --- Logged-In Artist Views ---
#

def art_gallery(request):
    """
    ✅ CORRECTED: This is now the main "Home" for a logged-in artist.
    It fetches and displays ONLY the art belonging to the logged-in artist.
    Corresponds to 'artpageartist.html'.
    """
    username = request.session.get('username')
    if not username:
        # If a non-logged-in user tries to access this, redirect them.
        return redirect('login') 

    try:
        # Fetch the logged-in artist and their specific artworks
        artist = Artist.objects.get(username=username)
        artworks = Art.objects.filter(artist_name=artist)
        context = {
            'artist': artist,
            'artworks': artworks,
            'no_artworks': not artworks.exists()
        }
        # Use the template designed to show a specific artist's work
        return render(request, 'artpageartist.html', context)
    except Artist.DoesNotExist:
        return redirect('login')

def artist_profile(request):
    """
    Displays the profile for the currently logged-in artist.
    """
    # ... (This function is correct and remains unchanged) ...
    username = request.session.get('username')
    if not username:
        return redirect('login')

    try:
        artist = Artist.objects.get(username=username)
        return render(request, 'artistprofile.html', {'artist': artist})
    except Artist.DoesNotExist:
        del request.session['username']
        return redirect('login')


def artist_artworks(request, username):
    """
    Displays all artworks for a specific artist (when viewing someone else's profile).
    """
    # ... (This function is correct and remains unchanged) ...
    try:
        artist = Artist.objects.get(username=username)
        artworks = Art.objects.filter(artist_name=artist)
        context = {
            'artist': artist,
            'artworks': artworks,
            'no_artworks': not artworks.exists()
        }
        return render(request, 'artpageartist.html', context)
    except Artist.DoesNotExist:
        return redirect('homepage')


#
# --- Story Generation Views ---
#
# ... (These functions are correct and remain unchanged) ...

def storypage(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')
    return render(request, 'storypage.html')

def preview_story(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        generated_story = f"Once, in the heart of India, a craftsperson skilled in {text} began a new masterpiece. With every touch, a story of heritage and passion was woven into the creation, a testament to generations of artistry."
        return JsonResponse({'story_text': generated_story})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def save_story(request):
    if request.method == 'POST':
        username = request.session.get('username')
        if not username:
            return JsonResponse({'error': 'Not authenticated'}, status=403)
        try:
            artist = Artist.objects.get(username=username)
            story_text = request.POST.get('story_text')
            artist.story = story_text
            artist.save()
            return JsonResponse({'success': True, 'message': 'Story saved successfully!'})
        except Artist.DoesNotExist:
            return JsonResponse({'error': 'Artist not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)