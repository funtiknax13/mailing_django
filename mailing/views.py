from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from blog.models import Article
from config.settings import CACHE_ENABLED
from mailing.forms import MessageForm, ClientForm, MailingForm
from mailing.models import Client, Message, Mailing, Log
from mailing.services import send_message_email
from users.models import User
from utils.mixins import CreatorRequiredMixin


def index(request):
    mailing_count = Mailing.objects.all().count()
    active_mailing_count = Mailing.objects.filter(status='started').count()
    client_count = Client.objects.all().count()

    if CACHE_ENABLED:
        key = f'articles_list'
        articles_list = cache.get(key)
        if articles_list is None:
            articles_list = Article.objects.order_by('?')[:3]
            cache.set(key, articles_list)
    else:
        articles_list = Article.objects.order_by('?')[:3]

    context = {'mailing_count': mailing_count,
               'active_mailing_count': active_mailing_count,
               'client_count': client_count,
               'object_list': articles_list}
    return render(request, 'mailing/index.html', context)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(creator=self.request.user).order_by("email")
        return queryset


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients')

    def form_valid(self, form):
        self.object = form.save()
        self.object.creator = self.request.user
        self.object.save()

        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, CreatorRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients')


class ClientDeleteView(LoginRequiredMixin, CreatorRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:clients')


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(creator=self.request.user).order_by("title")
        return queryset


class MessageDetailView(LoginRequiredMixin, CreatorRequiredMixin, DetailView):
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages')

    def form_valid(self, form):
        self.object = form.save()
        self.object.creator = self.request.user
        self.object.save()

        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, CreatorRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages')


class MessageDeleteView(LoginRequiredMixin, CreatorRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:messages')


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(creator=self.request.user).order_by("start_time")
        return queryset


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_kwargs(self):
        kwargs = super(MailingCreateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs
    # def get_form(self, form_class=None):
    #     form_class = MailingForm(self.request.user)
    #     return form_class

    def form_valid(self, form):
        if form.is_valid():
            new_mailing = form.save()
            new_mailing.creator = self.request.user
            new_mailing.save()

            if new_mailing.get_status() == 'started':
                send_message_email(new_mailing)

        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, CreatorRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:index')


class MailingDeleteView(LoginRequiredMixin, CreatorRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:index')


class LogListView(LoginRequiredMixin, ListView):
    model = Log

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(mailing__creator=self.request.user).order_by("last_attempt")
        return queryset


class ModerationMailingListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing/moderation_mailing_list.html'
    permission_required = ["mailing.set_active", ]


class ModerationUserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    template_name = 'mailing/moderation_user_list.html'
    permission_required = ["users.set_active", ]

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.exclude(is_superuser=True)
        return queryset


class ModerationMailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    fields = ('is_active', )
    template_name = 'mailing/moderation_mailing_form.html'
    permission_required = ["mailing.set_active", ]
    success_url = reverse_lazy('mailing:moderation_mailing_list')


class ModerationUserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    fields = ('is_active', )
    template_name = 'mailing/moderation_user_form.html'
    permission_required = ["users.set_active", ]
    success_url = reverse_lazy('mailing:moderation_users')


def manual_sending(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    send_message_email(mailing)
    return redirect('/mailing')




