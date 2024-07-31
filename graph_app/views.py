from django.shortcuts import render, redirect

def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        request.session['name'] = name
        return redirect('graph')
    return render(request, 'graph_app/index.html')

def graph(request):
    return render(request, 'graph_app/graph.html')