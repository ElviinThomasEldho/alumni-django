from django.forms import ModelForm
from .models import *
from django import forms


class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['account', 'date_created', 'likes', 'comments']

        widgets = {
            'caption' : forms.TextInput()
        }

