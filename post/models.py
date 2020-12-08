from django.db import models

# Create your models here.
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     profile_picture = models.ImageField(upload_to='images/', default='default.png')
#     bio = models.TextField(max_length=500, default="My Bio", blank=True)
#     name = models.CharField(blank=True, max_length=120)