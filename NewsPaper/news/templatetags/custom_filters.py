from django import template

register = template.Library()

CENSOR_WORDS = ["редиска", "дурак"]

@register.filter()
def censor(value):
    value = value.lower()
    for _ in CENSOR_WORDS:
        value = value.replace(_, "*" * len(_))
    return f'{value}'