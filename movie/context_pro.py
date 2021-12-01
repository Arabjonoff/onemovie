from .models import *


def view_all(request):
	context = {
		'movies':Movie.objects.all().order_by('?')[:3],
		'last_m':Movie.objects.all().order_by('-id')[:15],
		'latest_post':Post.objects.all()[:15],
		'latest_posts':Post.objects.all()[:2],
		'tags':Tags.objects.all(),
		'top_post':Post.objects.filter(top=True),

		'genres':Genre.objects.all(),
		'country':Country.objects.all(),
	}
	return context

