from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from NewsPaper import settings
from news.models import PostCategory

from NewsPaper.settings import SITE_URL


def send_notification(preview, pk, post_title, subscribers):
    html_context = render_to_string(
        'post_created_email.html',
        {
            'text': subscribers,
            'link': f'{SITE_URL}/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=post_title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notification(instance.preview(), instance.pk, instance.post_title, subscribers)