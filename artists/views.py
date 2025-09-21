# In views.py

from django.shortcuts import render, redirect , get_object_or_404
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


# def login_view(request):
#     """
#     Handles user login and redirects to the artist's personal art gallery.
#     """
#     if request.method == 'POST':
#         username_from_form = request.POST.get('username')
#         password_from_form = request.POST.get('password')
#         try:
#             artist = Artist.objects.get(username=username_from_form)
#             if artist.password == password_from_form:
#                 request.session['username'] = artist.username
#                 # ✅ CORRECTED: Redirect to the personal art gallery after login
#                 return redirect('art_gallery') 
#             else:
#                 messages.error(request, 'Invalid username or password.')
#         except Artist.DoesNotExist:
#             messages.error(request, 'Invalid username or password.')
#     return render(request, 'login.html')
def login_view(request):
    """
    Handles user login and redirects correctly.
    """
    if request.method == 'POST':
        username_from_form = request.POST.get('username')
        password_from_form = request.POST.get('password')
        try:
            artist = Artist.objects.get(username=username_from_form)
            
            # ⚠️ SECURITY NOTE: This password check is insecure. See below.
            if artist.password == password_from_form:
                request.session['username'] = artist.username
                
                # --- THIS IS THE NEW LOGIC ---
                # Check if the URL has a 'next' parameter
                next_page = request.GET.get('next')
                if next_page:
                    # If it exists, redirect the user to that page
                    return redirect(next_page)
                else:
                    # Otherwise, send them to the default gallery page
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
        return render(request, 'artpage.html', context)
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


from django.contrib.auth.decorators import login_required
from .forms import ArtForm

def add_artwork(request):
    """
    Handles the "Add Artwork" page for a logged-in artist.
    """
    # 1. Check if the user is logged in using your session method
    username = request.session.get('username')
    if not username:
        # If not logged in, redirect to the login page
        return redirect('login')

    # 2. Get the Artist object for the logged-in user
    try:
        artist = Artist.objects.get(username=username)
    except Artist.DoesNotExist:
        # If the user in the session doesn't exist, send them to login
        return redirect('login')

    # 3. Process the form
    if request.method == 'POST':
        # Pass POST data and uploaded files to the form
        form = ArtForm(request.POST, request.FILES)
        if form.is_valid():
            # Create the art object but don't save it yet
            art = form.save(commit=False)
            
            # ✅ THIS IS THE KEY: Set the artist to the logged-in user
            art.artist_name = artist
            
            # Now, save the complete art object to the database
            art.save()

            # Redirect to the artist's personal gallery page after success
            return redirect('art_gallery')
    else:
        # If it's a GET request, just show a blank form
        form = ArtForm()

    # Render the page with the form
    return render(request, 'add_art.html', {'form': form})


def logout_view(request):
    """
    Handles user logout by clearing the session and redirecting to the login page.
    """
    try:
        del request.session['username']
    except KeyError:
        pass
    return redirect('firstpage')


def edit_artwork(request, art_id):
    """
    Handles editing an existing piece of artwork.
    """
    username = request.session.get('username')
    if not username:
        return redirect('login')

    # Get the specific art piece, or return a 404 error if it doesn't exist
    art = get_object_or_404(Art, id=art_id)

    # SECURITY CHECK: Ensure the logged-in user is the owner of the art
    if art.artist_name.username != username:
        # If not the owner, redirect them away (e.g., to their own gallery)
        return redirect('art_gallery')

    if request.method == 'POST':
        # Pre-fill the form with the existing art instance
        form = ArtForm(request.POST, request.FILES, instance=art)
        if form.is_valid():
            form.save()
            # Redirect to the gallery after a successful edit
            return redirect('art_gallery')
    else:
        # If it's a GET request, show the form pre-filled with the art's current data
        form = ArtForm(instance=art)

    # Use the 'edit_art.html' template for the form
    return render(request, 'artists/edit_art.html', {'form': form, 'art': art})

def delete_artwork(request, art_id):
    """
    Handles deleting a piece of artwork. This view now only accepts POST requests.
    """
    # 1. Security check: Only allow POST requests for deletion
    if request.method != 'POST':
        # If someone tries to access this URL directly, redirect them away.
        return redirect('art_gallery')

    # 2. Authentication check
    username = request.session.get('username')
    if not username:
        return redirect('login')

    # 3. Get the artwork and check for ownership
    art = get_object_or_404(Art, id=art_id)
    if art.artist_name.username != username:
        # Prevent users from deleting other artists' work
        return redirect('art_gallery')

    # 4. If all checks pass, delete the artwork and redirect
    art.delete()
    # You can add a success message here if you like
    # messages.success(request, f'"{art.art_name}" has been deleted.')
    return redirect('art_gallery')

def edit_profile(request):
    """
    Handles displaying and processing the artist profile edit form.
    """
    # 1. Get the username from the session and check if the user is logged in
    username = request.session.get('username')
    if not username:
        return redirect('login')

    # 2. Get the artist object for the logged-in user
    try:
        artist = Artist.objects.get(username=username)
    except Artist.DoesNotExist:
        # If user in session doesn't exist, log them out
        del request.session['username']
        return redirect('login')

    # 3. Handle the form submission
    if request.method == 'POST':
        # Pre-populate the form with the artist's existing data
        form = ArtistForm(request.POST, request.FILES, instance=artist)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            # Redirect back to the profile page to see the changes
            return redirect('artist_profile') # Assumes you have a URL named 'artist_profile'
    else:
        # For a GET request, show the form pre-filled with the artist's current data
        form = ArtistForm(instance=artist)

    return render(request, 'artists/edit_profile.html', {'form': form, 'artist': artist})
