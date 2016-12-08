class SearchResponse(FormMixin, ListView):
		# formview stuff
		template_name = 'search.html'
		context_object_name = 'spaces'
		form_class = SearchForm

		def get_initial(self):
				if self.request.GET:
						initial = self.request.GET.dict()
						return initial

		# listview stuff
		def get_queryset(self):
				spaces = Space.objects.all()
				location = self.request.GET.get('location', '')
				radius = self.request.GET.get('radius')
				space_size = self.request.GET.get('size')
				venue_style = self.request.GET.get('style')
				# chain all filters below with if
				if location: # and radius?
						# create a geo POINT from location entry
						geocoder = GoogleV3()
						latlon = geocoder.geocode(location)
						latilongi = latlon[1]
						latitude, longitude = latilongi
						current_point = geos.fromstr("POINT({0} {1})".format(longitude, latitude))
						# get search radius from get request
						if not radius:
								radius = 2.0
						distance_from_point = float(radius)
						spaces = Space.objects.all()
						spaces = spaces.filter(location__distance_lte=(current_point, measure.D(mi=distance_from_point)))
				if space_size:
						spaces = spaces.filter(size__gte=space_size)
				if not venue_style == 'All Styles':
						spaces = spaces.filter(venue__style=venue_style)
						
				if not spaces:
						return None # return all objects if no radius or space.
				else:
						return spaces

		def get_context_data(self, **kwargs):
				context = super(SearchView, self).get_context_data(**kwargs)
				context["form"] = self.get_form()
				return context
				

		#return everything as json upon get request.
		def get(self, request, *args, **kwargs):
				response = serializers.serialize('json', self.get_queryset(), use_natural_primary_keys=True)
				return HttpResponse(response, {'MEDIA_URL': MEDIA_URL})
Raw
 Pageload.py
class SearchView(FormMixin, ListView):
		template_name = 'search.html'
		context_object_name = 'spaces'
		form_class = SearchForm
		
		def get_initial(self):
				'''get initial values from request params'''
				if self.request.GET:
						initial = self.request.GET.dict()
						return initial

		def get_queryset(self):
				'''return all spaces on initial get '''
				spaces = Space.objects.all() 
				return spaces

		def get_context_data(self, **kwargs):
				context = super(SearchView, self).get_context_data(**kwargs)
				context["form"] = self.get_form()
				return context
