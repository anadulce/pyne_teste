import re

from django.conf import settings
from django.shortcuts import render, redirect

from graph_app.models import Node

def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        # Se o nome tiver qualquer coisa diferente de letras e espaços, tá barrado
        if re.fullmatch(r"[\w ]*", name):
            request.session['name'] = name
            return redirect('graph')
    return render(request, 'graph_app/index.html')

def graph(request):
    return render(request, 'graph_app/graph.html')

def reset_graph(request):
    if request.method == 'GET':
        key = request.GET.get('key')
        if key == settings.DATABASE_RESTORE_KEY:
            Node.objects.all().delete()
    return redirect('index')
    