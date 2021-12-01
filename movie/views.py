from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from .models import *
import telebot 

from .forms import MovieRatingForm,CommentForm
# Create your views here.

my_id = 1705528794
bot = telebot.TeleBot('1726200909:AAHoV9Tw8UUHl5X2Vj9rWCtC5zukTmmK10A')

class HomePageView(View):
	# Home Page Movies View
	def get(self,request):
		model = Contact.objects.all()
		form = MovieRatingForm(request.GET)
		if form.is_valid():
			form.save()
		else:
			form = MovieRatingForm()
		movie = Movie.objects.all()

		top_viewed = Movie.objects.all().order_by('-views')[:2]
		recent_add = Movie.objects.all().order_by('-id')[:10]
		random_movies = Movie.objects.all().order_by('?')[:2]
		context = {
			'top_viewed':top_viewed,
			'movies':movie,
			'recent_add':recent_add,
			'random_movies':random_movies,
			'form':form,
			'model':model,
		}
		return render(request, 'index.html', context)


class MovieDetailView(DetailView):
	# Movie Dewtail Page View
	model = Movie
	template_name = 'single.html'
	slug_field = 'slug'



class MultiDetailView(DetailView):
	# Movie Dewtail Page View
	model = Multik
	template_name = 'single.html'
	slug_field = 'slug'




# Test  views 

class AllPostView(ListView):
	model = Post
	paginated_by = 10
	template_name = 'news.html'
	context_object_name = 'posts'

class PostDetailView(DetailView):
	model = Post
	slug_field = 'slug'
	template_name = 'news-single.html'


def getCatPost(request,category_slug):
	category = PostCategory.objects.get(slug=category_slug)
	posts = category.posts.all
	return render(request, 'cat_post.html', {'posts':posts})

def getTagPost(request,tag_slug):
	tag = Tags.objects.get(slug=tag_slug)
	posts = tag.posts.all()
	return render(request, 'news.html', {'posts':posts})



# Genres And Categories

def genreDetail(request, genre):
	genre = get_object_or_404(Genre, slug=genre)
	movie = Movie.objects.filter(genre=genre)
	context = {
		'movie':movie
	}
	return render(request, 'genres.html', context)

def countryDetail(request, country):
	country = get_object_or_404(Country, slug=country)
	movie = Movie.objects.filter(country=country)
	context = {
		
		'movie':movie,
	}
	return render(request, 'genres.html', context)


def search(request):
	q = request.GET.get('search', None)
	movies = Movie.objects.filter(title__icontains=q)
	posts = Post.objects.filter(title__icontains=q)
	total_results = len(movies) + len(posts)
	query = request.GET['search']
	context = {
		'movies':movies,
		'posts':posts,
		'total_results':total_results,
		'query':query
	}
	return render(request, 'searchResult.html', context)

class MultikView(View):
	def get(self,request):
		post = Movie.objects.all().order_by('-id')[:10]
		multik = Multik.objects.all()
		context = {
			'post':post,
			'multik':multik,
			
		}
		return render(request, 'series.html',context)


def contact(request):
	if request.method == 'POST':
		first_name = request.POST['name']
		last_name = request.POST['last_name']
		email = request.POST['email']
		phone = request.POST['phone']
		message = request.POST['message']
		Contact.objects.create(first_name=first_name,last_name=last_name,subject=phone,email=email,message=message)
		# messages.add_message(request, messages.SUCCESS, 'Tabriklaymiz aloqa muofaqiyat amalga oshirildi tez orada sizbilan bog\'lanamiz')
		bot.send_message(my_id,f"Sayitdan xabar bor\nIsmi:  {first_name}\n Familiyasi: {last_name}\n Telfon raqami:  {phone}\nEmail:  {email}\n Xabari:  {message}")
	return render(request,'contact.html')

# Errors 


def customHandler404(request, exception=None):
	return render(request, '404.html')