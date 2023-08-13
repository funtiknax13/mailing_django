from django.contrib import admin

from mailing.models import Client, Message, Mailing, Log


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email',)
    search_fields = ('first_name', 'last_name', 'email',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title', 'text',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'status', 'message')
    list_filter = ('status',)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'last_attempt', 'status')