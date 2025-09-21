from django import forms
from .models import Artist

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'username', 'password', 'email', 'contact', 'address', 'state', 'about', 'art_category']
