from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import requests
from django.conf import settings
import http.client
import mimetypes
from codecs import encode
# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')

    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()
        
        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (400, 400)
            img.thumbnail(new_img)
            img.save(self.avatar.path)


class UploadedImage(models.Model):
    # id=models.AutoField()
    # print('Image uploading')
    image = models.ImageField(default='default.jpg', upload_to='profile_images')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.TextField(default='Dog_name',blank=True, null=True)
    breed=models.TextField(default='Dog_Breed',blank=True, null=True)
    age=models.IntegerField(default=0,blank=True, null=True)