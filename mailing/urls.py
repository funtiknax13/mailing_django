from django.urls import path


from mailing.views import *

app_name = 'mailing'

urlpatterns = [
    path('', MailingListView.as_view(), name="index"),
    path('test', test, name='test'),
    path('add_mailing', MailingCreateView.as_view(), name='add_mailing'),
    path('mailing<int:pk>/delete', MailingDeleteView.as_view(), name="delete_mailing"),
    path('mailing<int:pk>/edit', MailingUpdateView.as_view(), name="edit_mailing"),
    path('clients', ClientListView.as_view(), name="clients"),
    path('messages', MessageListView.as_view(), name="messages"),
    path('add_client', ClientCreateView.as_view(), name="add_client"),
    path('client<int:pk>/delete', ClientDeleteView.as_view(), name="delete_client"),
    path('client<int:pk>/edit', ClientUpdateView.as_view(), name="edit_client"),
    path('add_message', MessageCreateView.as_view(), name="add_message"),
    path('message<int:pk>/delete', MessageDeleteView.as_view(), name="delete_message"),
    path('message<int:pk>/detail', MessageDetailView.as_view(), name="detail_message"),
    path('message<int:pk>/edit', MessageUpdateView.as_view(), name="edit_message"),
]