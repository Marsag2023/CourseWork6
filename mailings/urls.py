from django.urls import path
from django.views.decorators.cache import never_cache

from mailings.views import (MailListView, MailDetailView, MailCreateView, MailUpdateView, MailDeleteView, \
                            ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView,
                            MessageListView, \
                            HomePageView, MessageCreateView, MessageDetailView, MessageDeleteView, MessageUpdateView, \
                            LogDetailView, LogListView, PermMailUpdateView)
from mailings.apps import MailingsConfig
app_name = MailingsConfig.name

urlpatterns = [
    path('', never_cache(HomePageView.as_view()), name='homepage'),

    path('mail/', never_cache(MailListView.as_view()), name="mail_list"),
    path('mail/<int:pk>/', MailDetailView.as_view(), name="mail_detail"),
    path('mail/create/', MailCreateView.as_view(), name="mail_create"),
    path('mail/update/<int:pk>/', MailUpdateView.as_view(), name='mail_update'),
    path('mail/update_perm/<int:pk>/', PermMailUpdateView.as_view(), name='mail_updateperm'),
    path('mail/delete/<int:pk>/', MailDeleteView.as_view(), name='mail_delete'),

    path('client/', never_cache(ClientListView.as_view()), name="client_list"),
    path('client/<int:pk>/', ClientDetailView.as_view(), name="client_detail"),
    path('client/create/', ClientCreateView.as_view(), name="client_create"),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

    path('message/', never_cache(MessageListView.as_view()), name="message_list"),
    path('message/<int:pk>/', MessageDetailView.as_view(), name="message_detail"),
    path('message/create/', MessageCreateView.as_view(), name="message_create"),
    path('message/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),

    path('log/<int:pk>/', never_cache(LogDetailView.as_view()), name='log_detail'),
    path('log/', LogListView.as_view(), name='log_list'),
]
