from django import forms

from blog.models import Article
from utils.mixins import StyleFormMixin


class ArticleForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'text', 'image')


    @staticmethod
    def is_have_forbidden_words(text: str):
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа',
                           'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        for word in forbidden_words:
            if word in text.lower():
                return word
        return False

    def clean_text(self):
        cleaned_data = self.cleaned_data.get('text')
        answer = self.is_have_forbidden_words(cleaned_data)
        if answer:
            raise forms.ValidationError(f'Использовано запрещенное слово: {answer}')
        return cleaned_data

    def clean_title(self):
        cleaned_data = self.cleaned_data.get('title')
        answer = self.is_have_forbidden_words(cleaned_data)
        if answer:
            raise forms.ValidationError(f'Использовано запрещенное слово: {answer}')
        return cleaned_data