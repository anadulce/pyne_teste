# graph_app/models.py
from django.db import models

class Node(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    x = models.FloatField(default=100)
    y = models.FloatField(default=100)

    def __str__(self) -> str:
        return f"{self.id}({self.x}, {self.y})"
    
    def __repr__(self) -> str:
        return f"Node(id={self.id}, x={self.x}, y={self.y})"


class Link(models.Model):
    source = models.ForeignKey(Node, related_name='source_links', on_delete=models.CASCADE)
    target = models.ForeignKey(Node, related_name='target_links', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.source} <-> {self.target}"
    
    def __repr__(self) -> str:
        return f"Link(source={self.source}, target={self.target})"