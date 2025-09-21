from django import forms
from .models import Artist

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        # Ensure your profile image field (e.g., 'profile') is in this list
        fields = [
            'name', 'username', 'password', 'email', 'contact',
            'address', 'state', 'about', 'art_category', 'profile'
        ]
        # This helps hide the password field's current value
        widgets = {
            'password': forms.PasswordInput(render_value=False),
        }
        
        
from django import forms
from .models import Art

class ArtForm(forms.ModelForm):
    class Meta:
        model = Art
        # All fields the user should fill out
        fields = ['art_name', 'art_category', 'description', 'art_image']
        widgets = {
            'art_name': forms.TextInput(attrs={'placeholder': 'Enter art name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter description'}),
        }