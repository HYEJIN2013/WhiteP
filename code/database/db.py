from google.appengine.ext import db

class Post(db.Model):
    title = db.StringProperty()
	slug = db.StringProperty()
	date = db.DateTimeProperty(auto_now_add=True)
	author = db.StringProperty()
	content = db.TextProperty()
	category = db.ReferenceProperty(Category, collection_name='posts')
	tags = db.ListProperty(db.Key)

class Page(db.Model):
	title = db.StringProperty()
	slug = db.StringProperty()
	content = db.TextProperty()

class Tag(db.Model):
	title = db.StringProperty()
	slug = db.StringProperty()

class Category(db.Model):
	title = db.StringProperty()
	slug = db.StringProperty()
