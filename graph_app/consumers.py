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
        self.width = int(params.get('width', [100])[0])
        self.height = int(params.get('height', [100])[0])
        
        # Cria o nó se ele já não existe
        await self.add_node()
        
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
        from ipdb import set_trace
        set_trace()
        data = json.loads(text_data)
        # nodes = data.get('nodes', [])
        # links = data.get('links', [])
        target = data.get('target')

        # Save updated state to database
        if target:
            await self.add_link(target)

        # await self.channel_layer.group_send(
        #     "graph",
        #     {
        #         'type': 'graph_update',
        #         'data': {
        #             'nodes': nodes,
        #             'links': links
        #         }
        #     }
        # )
        graph_state = await self.get_graph_state()
        
        await self.send(text_data=json.dumps(graph_state, cls=DjangoJSONEncoder))

    async def graph_update(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data, cls=DjangoJSONEncoder))

    @database_sync_to_async
    def add_link(self, target):
        # from ipdb import set_trace
        # set_trace()
        source_node, source_error = Node.objects.get_or_create(id=self.username, defaults={"x":randint(10, self.width), "y":randint(10, self.height)})
        target_node, target_error = Node.objects.get_or_create(id=target, defaults={"x":randint(10, self.width), "y":randint(10, self.height)})
        if not source_error and not target_error:
            Link.objects.create(source=source_node, target=target_node)

    @database_sync_to_async
    def get_graph_state(self):
        return {
            'nodes': list(Node.objects.values('id', 'x', 'y')),
            'links': list(Link.objects.values('source', 'target'))
        }

    async def send_graph_state(self):
        graph_state = await self.get_graph_state()
        await self.send(text_data=json.dumps(graph_state, cls=DjangoJSONEncoder))
    
    @database_sync_to_async
    def add_node(self):
        return Node.objects.get_or_create(id=self.username, defaults={"x":randint(10, self.width), "y":randint(10, self.height)})
