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
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )

class CustomAccountManager(BaseUserManager):
    
    def create_superuser(self, email, user_name, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, first_name, password, **other_fields)
          
            
    def create_user(self, email, user_name, first_name, password, **other_fields):
        
        if not email:
            raise ValueError(_('You must provide an email address'))
    
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user  
    
    
class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_(
        'about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name']

    def __str__(self):
        return self.user_name
    
    
class Profile (models.Model):
        
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    email = models.CharField(max_length=50)
    status = models.BooleanField()
    image = CloudinaryField('Profile pic', default = 'profile.jpg')
    
    def __str__(self):
        return f'{self.user.first_name} Profile'
    
    def save_profile(self):
        self.save()
        
    def delete_profile(self):
        self.delete()
        
    @classmethod
    def update_profile(cls, id, value):
        cls.objects.filter(id=id).update(name=value)

# class Profile (models.Model):
#     name = models.CharField(max_length=30)
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     email = models.CharField(max_length=50)
#     status = models.BooleanField()
#     # image = CloudinaryField('Profile pic', default = 'profile.jpg')
#     image = cloudinary.models.CloudinaryField('image')
#     def __str__(self):
#         return f'{self.user.username} Profile'
#     def save_profile(self):
#         self.save
#     def delete_profile(self):
#         self.delete()
        
# class Post(models.Model):
#     title = models.CharField(max_length=100)
#     image = CloudinaryField('image', null=True, blank=True)
#     text = models.TextField()
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     date = models.DateField(auto_now_add=True)
#     neighbourhood = models.ForeignKey(
#         Neighbourhood, on_delete=models.CASCADE, default='', null=True, blank=True)

#     def __str__(self):
#         return f'{self.title} Post'

#     def save_post(self):
#         self.save()

#     def delete_post(self):
#         self.delete()
        
# class Business(models.Model):
#     business_name = models.CharField(max_length=250)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     business_profile = CloudinaryField('Profile pic', null=True, blank=True)
#     neighbourhood = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE)
#     business_email = models.CharField(max_length=30)

#     def __str__(self):
#         return f'{self.business_name} business'

#     def save_business(self):
#         self.save()

#     def delete_business(self):
#         self.delete()