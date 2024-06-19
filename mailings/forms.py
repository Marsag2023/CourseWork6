from django.forms import ModelForm, DateTimeInput
from mailings.models import Mail, Message, Client, Log
from django.forms.fields import BooleanField


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, ModelForm):
    """
    Класс для отображения формы модели клиента
    """
    class Meta:
        model = Client
        exclude = ['owner']


class MailForm(StyleFormMixin, ModelForm):
    """
    Класс для отображения формы модели рассылки
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(MailForm, self).__init__(*args, **kwargs)
        self.fields['clients'].queryset = Client.objects.filter(owner=self.user)
        self.fields['content'].queryset = Message.objects.filter(owner=self.user)

    class Meta:
        model = Mail
        exclude = ['owner', 'status']

        widgets = {
            'start_date': DateTimeInput(attrs={'placeholder': 'ДД.ММ.ГГГГ ЧЧ:ММ:СС', 'type': 'datetime-local'}),
            'end_date': DateTimeInput(attrs={'placeholder': 'ДД.ММ.ГГГГ ЧЧ:ММ:СС', 'type': 'datetime-local'}),
        }

class MessageForm(StyleFormMixin, ModelForm):
    """
    Класс для отображения формы модели сообщения
    """
    class Meta:
        model = Message
        exclude = ['owner']


class PermMailForm(StyleFormMixin, ModelForm):
    """
    Класс для отображения формы модели рассылки
    для редактирования менеджером
    """
    class Meta:
        model = Mail
        fields = ['mail_active']

class LogForm(StyleFormMixin, ModelForm):
    """Класс формы рассылки"""
    class Meta:
        model = Log
        fields = "__all__"
