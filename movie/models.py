from django.db import models



class Movie(models.Model):
	"""
	Movie properties
	"""
	title=models.CharField(max_length=150)
	imdbID=models.CharField(max_length=100)
	year=models.CharField(max_length=10)
	mtype=models.CharField(max_length=20)
	poster=models.URLField(max_length=500)
	casts=models.TextField(blank=True)
	imdbRating=models.CharField(max_length=10,blank=True)   	
	def __str__(self):
		return u'%s' % (self.title)


