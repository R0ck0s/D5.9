from django import template

register = template.Library()

CENSOR_WORDS = ["редиска","Редиска", "дурак", "Дурак"]

@register.filter()
def censor(value):
    for _ in CENSOR_WORDS:
        # value = value.lower()
        value = value.replace(_, "*" * len(_))

    return f'{value}'