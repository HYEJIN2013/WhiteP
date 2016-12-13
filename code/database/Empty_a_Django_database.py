from django.db.models import get_models
for model in get_models():
  try:
    model.objects.all().delete()
  except Exception, e:
    print e
