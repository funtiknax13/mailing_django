from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from mailing.forms import MessageForm, ClientForm, MailingForm
from mailing.models import Client, Message, Mailing, Log
from mailing.services import send_message_email


class ClientListView(ListView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ClientForm
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
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages')


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:messages')


class MailingListView(ListView):
    model = Mailing


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:index')

    def form_valid(self, form):
        if form.is_valid():
            new_mailing = form.save()
            new_mailing.save()

            if new_mailing.get_status() == 'started':
                send_message_email(new_mailing)

        return super().form_valid(form)


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:index')


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:index')


class LogListView(ListView):
    model = Log

def test(request):
    now = timezone.now()
    print(now)
    mailing = Mailing.objects.all()
    for m in mailing:
        m.get_status()
    mailing_list = Mailing.objects.exclude(status='closed')
    print(mailing_list)
    for mailing in mailing_list:

        last_send = mailing.log_set.filter(status='ok').order_by('-last_attempt').first()
        # send_message_email(mailing)
        print(mailing.pk, last_send)

    return HttpResponse("Hello test")



