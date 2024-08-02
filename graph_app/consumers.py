# graph_app/consumers.py
from random import randint
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Node, Link
from django.core.serializers.json import DjangoJSONEncoder
from urllib.parse import parse_qs



class GraphConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        query_string = self.scope.get('query_string', b'').decode()
        params = parse_qs(query_string)
        self.username = params.get('username', [''])[0]
        

        # Add user node if not already present
        await self.add_node(self.username)
        
        await self.channel_layer.group_add(
            "graph",
            self.channel_name
        )
        await self.accept()
        
        # Send current graph state
        await self.send_graph_state()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "graph",
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        nodes = data.get('nodes', [])
        links = data.get('links', [])
        print("TESTEEEEEEEEEEE")

        # Save updated state to database
        from ipdb import set_trace
        set_trace()
        await self.save_graph_state(nodes, links)

        await self.channel_layer.group_send(
            "graph",
            {
                'type': 'graph_update',
                'data': {
                    'nodes': nodes,
                    'links': links
                }
            }
        )

    async def graph_update(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data, cls=DjangoJSONEncoder))

    @database_sync_to_async
    def save_graph_state(self, nodes, links):
        Node.objects.all().delete()  # Clear existing nodes
        Link.objects.all().delete()  # Clear existing links
        # Save nodes
        for node in nodes:
            Node.objects.create(id=node['id'], x=node['x'], y=node['y'])
        # Save links
        for link in links:
            source_node = Node.objects.get(id=link['source'])
            target_node = Node.objects.get(id=link['target'])
            Link.objects.create(source=source_node, target=target_node)

    @database_sync_to_async
    def get_graph_state(self):
        nodes = list(Node.objects.values('id', 'x', 'y'))
        links = list(Link.objects.values('source', 'target'))
        return {
            'nodes': nodes,
            'links': links
        }

    async def send_graph_state(self):
        graph_state = await self.get_graph_state()
        await self.send(text_data=json.dumps(graph_state, cls=DjangoJSONEncoder))
    
    @database_sync_to_async
    def add_node(self, username):
        if not Node.objects.filter(id=username).exists():
            Node.objects.create(id=username, x=randint(10, 1000), y=randint(10, 1000))
