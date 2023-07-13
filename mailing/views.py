from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from mailing.models import Client, Message, Mailing, Log


def index(request):
    return render(request, 'mailing/index.html')


def clients(request):
    clients = Client.objects.all()
    context = {"clients": clients}
    return render(request, 'mailing/clients.html', context)


def messages(request):
    messages = Message.objects.all()
    context = {"messages": messages}
    return render(request, 'mailing/messages.html', context)


def add_client(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        patronymic = request.POST.get("patronymic")
        email = request.POST.get("email")
        new_client = Client(first_name=first_name, last_name=last_name, patronymic=patronymic, email=email)
        new_client.save()
        return HttpResponseRedirect(reverse('mailing:clients'))
    return render(request, 'mailing/add_client.html')


def delete_client(request, client_id):
    try:
        client = Client.objects.get(id=client_id)
    except:
        raise Http404("Клиент не найден!")
    client.delete()
    return HttpResponseRedirect(reverse('mailing:clients'))


def edit_client(request, client_id):
    try:
        client = Client.objects.get(id=client_id)
    except:
        raise Http404("Клиент не найден!")

    if request.method == 'POST':
        client.first_name = request.POST.get("first_name")
        client.last_name = request.POST.get("last_name")
        client.patronymic = request.POST.get("patronymic")
        client.email = request.POST.get("email")
        client.save()
        return HttpResponseRedirect(reverse('mailing:clients'))
    context = {'client': client}
    return render(request, 'mailing/edit_client.html', context)


def add_message(request):
    if request.method == "POST":
        title = request.POST.get("title")
        text = request.POST.get("text")
        new_message = Message(title=title, text=text)
        new_message.save()
        return HttpResponseRedirect(reverse('mailing:messages'))
    return render(request, 'mailing/add_message.html')


def delete_message(request, message_id):
    try:
        message = Message.objects.get(id=message_id)
    except:
        raise Http404("Письмо не найдено!")
    message.delete()
    return HttpResponseRedirect(reverse('mailing:messages'))


def edit_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id)

    if request.method == 'POST':
        message.title = request.POST.get("title")
        message.text = request.POST.get("text")
        message.save()
        return HttpResponseRedirect(reverse('mailing:messages'))
    context = {'message': message}
    return render(request, 'mailing/edit_message.html', context)

