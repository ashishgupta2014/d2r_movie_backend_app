from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import threading,requests,queue
from d2r_modb.pagination import StandardResultsSetPagination
from movie.models import *
from movie.api_v1.serilizer import *
from d2r_modb.settings import omdbapi
def getSuggestionFromDB(param):
	return Movie.objects.filter(title__istartswith=param).values('title','id').order_by('-imdbRating')
def getSuggestionfromSource(param,queue_data):
	res=requests.get(omdbapi+'&s='+param).json()
	
	if res['Response']=='True':
		for movie in res['Search']:
			if not Movie.objects.filter(title=movie['Title'].strip()).exists():
				res_cast_rating=requests.get(omdbapi+'&t='+movie['Title']).json()
				if res_cast_rating['Response']=='True':
					Movie.objects.create( 
						title=movie['Title'].strip(),
						year= movie['Year'].strip(),
						mtype=movie['Type'].strip(),
						poster=movie['Poster'].strip(),
						imdbID=movie['imdbID'].strip(),
						casts=res_cast_rating['Actors'].strip(),
						imdbRating=res_cast_rating['imdbRating'].strip()
					)
	return queue_data.put(getSuggestionFromDB(param))
	

class ListMovieTitle(APIView):
	"""
	{{domain}}/api/v1/movie/autocomplete/?q=<key stokes>
	
	"""
	def get(self,request):
		queue_data = queue.Queue(maxsize=300)
		t1 = threading.Thread(target=getSuggestionfromSource, args=(request.GET['q'],queue_data))
		t1.start()
		t1.join()
		
		queryset=getSuggestionFromDB(request.GET['q'])
		if queryset:
			return Response(queryset[:5],status=status.HTTP_200_OK)
		else:
			queryset=queue_data.get()
			return Response(queryset[:5],status=status.HTTP_200_OK)
		

class ListMovieDetail(APIView):
	"""
	pass 0 incase of all movie list
	pass page_size to apply pagination result dynamically
		{{domain}}/api/v1/movie/movies/0/?page_size=5
	/api/v1/movie/movies/<movie_id>/
	specific movie details listing
	"""
	paginate_by = 2
	paginate_by_param = 'page_size'
	max_paginate_by = 3
	pagination_class=StandardResultsSetPagination
	@property
	def paginator(self):
		"""
		The paginator instance associated with the view, or `None`.
		"""
		if not hasattr(self, '_paginator'):
			if self.pagination_class is None:
				self._paginator = None
			else:
				self._paginator = self.pagination_class()
		return self._paginator

	def paginate_queryset(self, queryset):
		"""
		Return a single page of results, or `None` if pagination is disabled.
		"""
		if self.paginator is None:
			return None
		return self.paginator.paginate_queryset(queryset, self.request, view=self)

	def get_paginated_response(self, data):
		"""
		Return a paginated style `Response` object for the given output data.
		"""
		assert self.paginator is not None
		return self.paginator.get_paginated_response(data)
	def get(self,request,movie_id=0):
		"""
		return pagination result with offset values
		"""
		
		if int(movie_id)>0:
			queryset=Movie.objects.filter(id=int(movie_id))
			
		else:
			queryset=Movie.objects.all()
			
		results = self.paginate_queryset(queryset)
		serializer = MovieSerializer(results, many=True)
		return self.get_paginated_response(serializer.data)

	
		