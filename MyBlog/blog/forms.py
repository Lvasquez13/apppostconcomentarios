# En el archivo forms.py de tu aplicación 'blog'

from django import forms
from .models import Comment, Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title','content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']