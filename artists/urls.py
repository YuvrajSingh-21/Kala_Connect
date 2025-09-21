from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register_artist, name="register"),
    path('login/', views.login_view, name="login"),
    # path('logout/', views.logout_view, name="logout"),
    path("gallery/", views.art_gallery, name="art_gallery"),
    path("profile/", views.artist_profile, name="artist_profile"),
    path("story/", views.storypage, name="storypage"),
    path('homepage/', views.homepage, name="homepage"),
    path('homepage/<str:username>/arts/', views.artist_artworks, name="artist_artworks"),
    # path("generate-video/", generate_video, name="generate_video"),
    # path("save-story/", views.save_story, name="save_story"),
    # path("preview-story-video/", views.preview_story_video, name="preview_story_video"),
    path("story/", views.storypage, name="storypage"),
    path("preview-story/", views.preview_story, name="preview_story"),
    path("save-story/", views.save_story, name="save_story"),
    path("add-artwork/", views.add_artwork, name="add_artwork"),
    path("logout/", views.logout_view, name="logout"),
    path('art/<int:art_id>/edit/', views.edit_artwork, name='edit_artwork'),
    path('art/<int:art_id>/delete/', views.delete_artwork, name='delete_artwork'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
