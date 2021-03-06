from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Comment


class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(max_length=200, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email')

class UpdateUserProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['name', 'location', 'profile_picture', 'bio']

class ProgramForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('image', 'caption')

class stationForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].widget = forms.TextInput()
        self.fields['comment'].widget.attrs['placeholder'] = 'Add a comment...'

    class Meta:
        model = Comment
        fields = ('comment',)