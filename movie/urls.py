from django.conf.urls import url,include
from movie.api_v1.view import *
urlpatterns=[
	url(r'^autocomplete/$',ListMovieTitle.as_view()),
	url(r'^movies/(?P<movie_id>\d+)/$',ListMovieDetail.as_view()),
]