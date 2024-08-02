from django.shortcuts import render, redirect

def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        request.session['name'] = name
        # from ipdb import set_trace
        # set_trace()
        return redirect('graph')
    return render(request, 'graph_app/index.html')

def graph(request):
    # from ipdb import set_trace
    # set_trace()
    return render(request, 'graph_app/graph.html')