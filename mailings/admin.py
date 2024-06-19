from django.contrib import admin
from mailings.models import (Message, Client, Mail, Log)


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'period', 'status', 'start_time', 'end_time_last', 'mail_active', 'owner')
    list_filter = ('status', 'period')
    search_fields = ('content',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'owner')
    search_fields = ('title', 'content',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'comment', 'owner')
    search_fields = ('name',)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('last_attempt', 'status', 'server_response','owner')
    list_filter = ('status',)
