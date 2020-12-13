from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import User
import cloudinary
from cloudinary.models import CloudinaryField
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="movie update website "),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )

class CustomAccountManager(BaseUserManager):
    
    def create_superuser(self, email, username, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, first_name, password,  **other_fields)
          
            
    def create_user(self, email, username, first_name, password, channel, **other_fields):
        
        if not email:
            raise ValueError(_('You must provide an email address'))
    
        email = self.normalize_email(email)
        user = self.model(email=email, username=username,first_name=first_name, **other_fields)
        user.set_password(password)
        user.channel = channel
        user.save()
        return user  
    
    
class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    channel = models.CharField(max_length=150, blank=True)   
    about = models.TextField(_(
        'about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'channel']

    def __str__(self):
        return self.username
    
      
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='images/', default='default.png')
    bio = models.TextField(max_length=350, default="My Bio", blank=True)
    name = models.CharField(blank=True, max_length=150)
    location = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    # @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    # @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def save_profile(self):
        self.user

    def delete_profile(self):
        self.delete()

    @classmethod
    def search_profile(cls, name):
        return cls.objects.filter(user__username__icontains=name).all()
    
class Station(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    broadcast = models.CharField(max_length=30, blank=True)    
    
    def __str__(self):
        return f'{self.user.username} Profile' 
    
class Program(models.Model):
    image = models.ImageField(upload_to='posts/')
    name = models.CharField(max_length=250, blank=True)
    caption = models.CharField(max_length=250, blank=True)    
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    created = models.DateTimeField(auto_now_add=True, null=True)
    start_time = models.DateTimeField(default=timezone.now, null=False)
    end_time = models.DateTimeField(default=timezone.now, null=False)
    image = CloudinaryField('image')

    class Meta:
        ordering = ["-pk"]

    def get_absolute_url(self):
        return f"/post/{self.id}"

    @property
    def get_all_comments(self):
        return self.comments.all()

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()    

    def __str__(self):
        return f'{self.user.name} Post'
