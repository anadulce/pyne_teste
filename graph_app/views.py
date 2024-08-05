from django.shortcuts import render, redirect
import re

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