# graph_app/models.py
from django.db import models

class Node(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    x = models.FloatField(default=100)
    y = models.FloatField(default=100)

class Link(models.Model):
    source = models.ForeignKey(Node, related_name='source_links', on_delete=models.CASCADE)
    target = models.ForeignKey(Node, related_name='target_links', on_delete=models.CASCADE)
