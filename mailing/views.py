from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from mailing.models import Client, Message, Mailing, Log
from mailing.services import send_message_email


def test(request):
    now_time = timezone.now().time().replace(microsecond=0).replace(second=0)
    clients_email = list(
        Client.objects.values_list('email', flat=True)
    )

    print(now_time)
    mailing_list = Mailing.objects.filter(time=now_time)
    # for mailing in mailing_list:
    #     if mailing.get_status() == 'started':
    #         send_message_email(mailing, clients_email)
    # mailing_list = Mailing.objects.all()
    for mailing in mailing_list:
        print(mailing)
    return HttpResponse("You're looking at question.")


class ClientListView(ListView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    fields = ('first_name', 'last_name', 'patronymic', 'email')
    success_url = reverse_lazy('mailing:clients')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('first_name', 'last_name', 'patronymic', 'email')
    success_url = reverse_lazy('mailing:clients')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:clients')


class MessageListView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    fields = ('title', 'text')
    success_url = reverse_lazy('mailing:messages')


class MessageUpdateView(UpdateView):
    model = Message
    fields = ('title', 'text')
    success_url = reverse_lazy('mailing:messages')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:messages')


class MailingListView(ListView):
    model = Mailing


class MailingCreateView(CreateView):
    model = Mailing
    fields = ('start_time', 'end_time', 'time', 'periodicity', 'message')
    success_url = reverse_lazy('mailing:index')


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ('start_time', 'end_time', 'time', 'periodicity', 'message')
    success_url = reverse_lazy('mailing:index')


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:index')



