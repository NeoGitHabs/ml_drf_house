from modeltranslation.translator import TranslationOptions, register
from .models import Review


@register(Review)
class ReviewTranslationOptions(TranslationOptions):
    fields = ('comment',)
