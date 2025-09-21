from django.db import models

# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=70)
    username = models.CharField(max_length=20,unique=True,primary_key=True)
    password= models.CharField(max_length=16)
    email = models.EmailField()
    contact = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
    state = models.CharField(max_length=50)
    about = models.CharField(max_length=500,null=True,blank=True)
    art_category = models.CharField(max_length=60)
    # Story= models.CharField(max_length=3000,null=True,blank=True)
    # story_video = models.FileField(upload_to="videos",null=True,blank=True)
    story = models.TextField(max_length=3000, null=True, blank=True)
    
    # Replaced FileField with URLField to store the cloud video link
    # video_url = models.URLField(max_length=1024, null=True, blank=True)
    story_video = models.FileField(upload_to='story_videos/', null=True, blank=True)
    # profile = models.ImageField(upload_to="artists",null=True,blank=True)
    profile= models.ImageField(upload_to="artists",null=True,blank=True)
    
    
    def __str__(self):
        return self.username
    
    
class Art(models.Model):
    art_name = models.CharField(max_length=100)
    art_category = models.CharField(max_length=60)
    artist_name = models.ForeignKey("artists.Artist", verbose_name=("username"), on_delete=models.CASCADE)
    description = models.CharField()
    art_image = models.ImageField(upload_to="artists")
    
    def __str__(self):
        return self.art_name
    

