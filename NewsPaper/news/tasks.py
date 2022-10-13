import datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category, Subscribers

def send_post_list():
    start_date = datetime.datetime.today() - datetime.timedelta(days=7)
    for category in Category.objects.all():
        week_posts = Post.objects.filter(post_date__gt=start_date.isoformat(), category=category)
        subscriptions = Subscribers.objects.filter(category=category)
        for subscription in subscriptions:
            html_content = render_to_string(
                'week_news.html',
                {'posts': week_posts, 'subscription': subscription}
            )
            text_body = ""
            for post in week_posts:
                text_body = text_body+f'{post.title} \n http://127.0.0.1:8000{post.get_absolute_url()} \n \n'
            msg = EmailMultiAlternatives(
                subject='Рассылка по подписке за неделю',
                body=text_body,
                from_email='skilltests77@yandex.ru',
                to=[subscription.user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()