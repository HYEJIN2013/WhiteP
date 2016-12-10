from django.conf import settings
from django.template import Context, loader
from django.core.mail import send_mail

def send_template_mail(slug, context, recipient_list, from_email=settings.DEFAULT_FROM_EMAIL):
    if isinstance(recipient_list, basestring):
        recipient_list = [recipient_list]
    if not isinstance(context, Context):
        context = Context(context)
    subject_tmpl = loader.get_template('mail/%s/subject.txt' % (slug,))
    body_tmpl = loader.get_template('mail/%s/body.txt' % (slug,))
    subject = subject_tmpl.render(context)
    body = body_tmpl.render(context)
    send_mail(subject, body, from_email, recipient_list)
