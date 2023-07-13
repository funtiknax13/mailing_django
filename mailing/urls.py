from django.urls import path


from mailing.views import *

app_name = 'mailing'

urlpatterns = [
    path('', index, name="index"),
    path('clients', clients, name="clients"),
    path('messages', messages, name="messages"),
    path('add_client', add_client, name="add_client"),
    path('client<int:client_id>/delete', delete_client, name="delete_client"),
    path('client<int:client_id>/edit', edit_client, name="edit_client"),
    path('add_message', add_message, name="add_message"),
    path('message<int:message_id>/delete', delete_message, name="delete_message"),
    path('message<int:message_id>/edit', edit_message, name="edit_message"),
]