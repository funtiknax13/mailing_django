from django import forms

from mailing.models import Message, Client, Mailing
from utils.mixins import StyleFormMixin


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ('title', 'text')


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


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'patronymic', 'email')


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('start_time', 'end_time', 'periodicity', 'message', 'clients')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(MailingForm, self).__init__(*args, **kwargs)
        self.fields['message'].queryset = Message.objects.filter(creator=self.request.user)
        self.fields['clients'].queryset = Client.objects.filter(creator=self.request.user)
