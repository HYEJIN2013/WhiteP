class UserSearchView(View):
    
    def get(self, request, *args, **kwargs):
        search = request.GET.get('q')
        query = '.*'.join(search)
        users = User.objects.filter(username__iregex='^%s' % query).values_list('id', 'username')
        return HttpResponse(json.dumps(list(users)), content_type='application/json')
