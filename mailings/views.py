import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView

from blogs.models import Blog
from mailings.forms import MailForm, ClientForm, MessageForm, LogForm, PermMailForm
from mailings.models import Mail, Client, Message, Log


class HomePageView(TemplateView):
    template_name = 'mailings/home.html'

    def get_context_data(self, **kwargs):
        count = Mail.objects.count()
        is_active = Mail.objects.filter(mail_active=True).count()
        unique = Client.objects.distinct('email').count()
        blog_list = list(Blog.objects.all())
        random.shuffle(blog_list)
        random_blog_list = blog_list[:3]
        context_data = {
            'count': count,
            'is_active': is_active,
            'unique': unique,
            'random_blog_list': random_blog_list,
        }
        return context_data


class MailListView(LoginRequiredMixin, ListView):
    """ Просмотр списка рассылок """
    model = Mail
    login_url = "/users/login/"

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.has_perm('mailings.change_status'):
            return Mail.objects.all()
        else:
            return Mail.objects.filter(owner=self.request.user)


class MailDetailView(DetailView):
    """ Просмотр деталей рассылки """
    model = Mail
    login_url = "/users/login/"


class MailCreateView(CreateView):
    """ Создание рассылки """
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('mailings:mail_list')

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(MailCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MailUpdateView(LoginRequiredMixin, UpdateView):
    """ Редактирование данных рассылки """
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('mailings:mail_list')


class PermMailUpdateView(LoginRequiredMixin, UpdateView):
    """ Редактирование данных рассылки """
    model = Mail
    form_class = PermMailForm
    success_url = reverse_lazy('mailings:mail_list')


class MailDeleteView(LoginRequiredMixin, DeleteView):
    """ Удаление рассылки """
    model = Mail
    success_url = reverse_lazy('mailings:mail_list')

    def get_context_data(self, **kwargs):
        """
        Права доступа владельца.
        """
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        if user == self.object.owner:
            return context_data
        raise PermissionDenied


class ClientListView(LoginRequiredMixin, ListView):
    """ Просмотр списка клиентов """
    model = Client
    login_url = "/users/login/"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Client.objects.all()
        else:
            return Client.objects.filter(owner=self.request.user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    """Просмотр одного клиента"""
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Создание клиента"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:client_list')

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование данных клиента"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:client_list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ClientForm
        raise PermissionDenied


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление клиента"""
    model = Client
    success_url = reverse_lazy('mailings:client_list')

    def get_context_data(self, **kwargs):
        """
        Права доступа владельца.
        """
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        if user == self.object.owner:
            return context_data
        raise PermissionDenied


class MessageListView(LoginRequiredMixin, ListView):
    """ Просмотр списка сообщений """
    model = Message
    login_url = "/users/login/"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Message.objects.all()
        else:
            return Message.objects.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    """Просмотр деталей сообщения"""
    model = Message
    login_url = "/users/login/"


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Создание сообщения"""
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailings:message_list')

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование сообщения"""
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailings:message_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление сообщения"""
    model = Message
    success_url = reverse_lazy('mailings:message_list')

    def get_context_data(self, **kwargs):
        """
        Права доступа владельца.
        """
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        if user == self.object.owner:
            return context_data
        raise PermissionDenied


class LogDetailView(LoginRequiredMixin, DetailView):
    """Просмотр деталей логов"""
    model = Log
    login_url = "/users/login/"


class LogListView(ListView):
    """Класс отображения логов"""
    model = Log

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Log.objects.all()
        else:
            return Log.objects.filter(owner=self.request.user)
