qs = Model.objects.all()
for kw in q.split():
    q = models.Q()
    for f in fields:
        q |= Q('%s__iexact' % f.name: kw)
    qs = qs.filter(q)
