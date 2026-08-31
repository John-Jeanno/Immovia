from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ClientForm
from .models import Client


@login_required
def index(request):
    return render(request, 'clients/index.html', {'clients': Client.objects.all()})


@login_required
def create(request):
    form = ClientForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        client = form.save()
        messages.success(request, f'Le client {client} a été enregistré.')
        return redirect('clients:list')

    return render(request, 'clients/create.html', {'form': form})
