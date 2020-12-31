from django import forms
from django.forms import ModelForm

from .models import User, Post

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['content']

        widgets = {
            'content' :forms.Textarea(attrs={'class':'form-control', 'placeholder':'Enter Post Content'})
        }