from background_task import background
from movie.models import *
from d2r_modb.settings import omdbapi
import requests
@background(schedule=1)
def performMovieUpdate(movie_title_list):
	pass