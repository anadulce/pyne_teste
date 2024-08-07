from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('graph/', views.graph, name='graph'),
    path('reset_graph/', views.reset_graph, name='reset_graph'),

]
