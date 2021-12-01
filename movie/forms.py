from django import forms
from django.db.models import fields 
from .models import Movie,Comment

class MovieRatingForm(forms.ModelForm):
	class Meta:
		model = Movie 
		fields = ['rating']

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['name','message']
