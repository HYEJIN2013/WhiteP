from django.core.mail import send_mail
import smtplib

class QueuedEmail(models.Model):
	"""
	DATABASE EMAIL QUEUE --
	QueuedEmail stashes your sites' messages in a table, so you don't have to wait on
	synchronous calls to django.core.mail.send_mail. Mail stays in the database after
	sending for as long as you leave them there, which provides a paper trail and
	a basis for analytics. I wrote it for use with an invitation-only site, where
	the flushqueuedemail.py script is run with a cron job.
	
	USAGE EXAMPLE --
	This simple bit here will queue a new message from within any python code:
	
	def some_view_function(request):
		(...)
		invitation = FSQueuedEmail(
			toaddress=invite.sentto,
			subject="Welcome",
			body=u'''
			Hello,
		
			Welcome to the site, %s. Your username is %s.
		
			Regards,
			The Management
			''' % (
				request.user.get_full_name(),
				request.user.username,
			)
		)
		invitation.save()
		(...)
	
	You can pass either an instance of django.contrib.auth.models.User in the 'to' param, or use
	a string with an email address in it with 'toaddress'. One can easily integrate templating,
	or compose emails programmatically, or embed the email text for quick development and testing.
	
	Add this model to your site, and flush the queue with the attached command-line tool (or write your
	own, it's like one query and one loop, and hey it could be smaller.)
	
	Enjoy!
	
	-fish2000
	
	"""
	class Meta:
		abstract = False
		verbose_name = "queued email message"
		verbose_name_plural = "queued email messages"
	status = models.IntegerField(verbose_name="Status",
		editable=True,
		null=False,
		default=0,
		choices=(
			(-1, 'SMTP Fail'),
			(0, 'Queued'),
			(1, 'Sent OK'),
			(2, 'Unexpected Error'),
		))
	createdate = models.DateTimeField('Created on',
		default=datetime.now,
		blank=True,
		editable=False)
	modifydate = models.DateTimeField('Last modified on',
		default=datetime.now,
		blank=True,
		editable=False)
	senddate = models.DateTimeField('Send after',
		default=datetime.now,
		blank=True,
		editable=True)
	subject = models.CharField(verbose_name="Subject",
		default="",
		unique=False,
		blank=True,
		max_length=255)
	body = models.TextField(verbose_name="Body",
		default="",
		unique=False,
		blank=True)
	to = models.ForeignKey(User,
		default=None,
		unique=False,
		blank=True,
		null=True,
		verbose_name="To (User)")
	toaddress = models.EmailField(verbose_name="To (Additional address or addresses)",
		default=None,
		unique=False,
		blank=True,
		null=True,
		max_length=255)
	def save(self, force_insert=False, force_update=False):
		self.modifydate = datetime.now()
		super(QueuedEmail, self).save(force_insert, force_update)
	def sendit(self):
		if self.senddate < datetime.now():
			if self.subject and self.body:
				if self.toaddress:
					try:
						self.status = send_mail(
							# one can insert [sitename] or somesuch 
							# at the start of the subject here
							"%s" % self.subject,
							self.body,
							settings.EMAIL_HOST_USER,
							[self.toaddress]
						)
					except smtplib.SMTPException:
						self.status = -1
						self.save()
					else:
						self.save()
				elif self.to and self.to.email:
					try:
						self.status = send_mail(
							"%s" % self.subject, 
							self.body,
							settings.EMAIL_HOST_USER,
							[self.to.email]
						)
					except smtplib.SMTPException:
						self.status = -1
						self.save()
					else:
						self.save()
		return self.status
