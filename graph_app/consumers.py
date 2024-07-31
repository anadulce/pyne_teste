# graph_app/consumers.py
import json
from random import randint
from channels.generic.websocket import AsyncWebsocketConsumer

class GraphConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope['user'].username
        if self.username == "":
            self.username = self.scope['query_string'].decode('utf-8')
        
        # Initialize nodes and links
        self.nodes = []
        self.links = []
        self.node_ids = set()  # To keep track of existing node IDs

        # Check if node already exists
        if self.username not in self.node_ids:
            # Add new node
            new_node = {'id': self.username, 'x': randint(0,900), 'y': randint(0, 600)}
            self.nodes.append(new_node)
            self.node_ids.add(self.username)
        
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
        new_nodes = data.get('nodes', [])
        new_links = data.get('links', [])

        # Update nodes and links
        self.nodes = new_nodes
        self.links = new_links
        self.node_ids = set(node['id'] for node in self.nodes)

        await self.channel_layer.group_send(
            "graph",
            {
                'type': 'graph_update',
                'data': {
                    'nodes': self.nodes,
                    'links': self.links
                }
            }
        )

    async def graph_update(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))

    async def send_graph_state(self):
        await self.send(text_data=json.dumps({
            'nodes': self.nodes,
            'links': self.links
        }))
