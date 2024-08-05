from random import randint
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Node, Link
from django.core.serializers.json import DjangoJSONEncoder
from urllib.parse import parse_qs

GRAPH = "graph"


class GraphConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        query_string = self.scope.get('query_string', b'').decode()
        params = parse_qs(query_string)
        self.username = params.get('username', [''])[0]
        self.width = int(params.get('width', [100])[0])
        self.height = int(params.get('height', [100])[0])
        
        # Cria o nó se ele já não existe
        await self.add_node()
        
        # Seta o grupo
        await self.channel_layer.group_add(
            GRAPH,
            self.channel_name
        )

        # Habilita para receber conexão
        await self.accept()
        
        # Mostra na tela a versão atual do grafo
        await self.send_graph_state()

    async def disconnect(self, close_code):
        # Fecha a conexão
        await self.channel_layer.group_discard(
            GRAPH,
            self.channel_name
        )

    async def receive(self, text_data):
        # Recupera os dados
        data = json.loads(text_data)
        target = data.get('target')

        # Cria o link se tiver um link a ser criado
        if target:
            await self.add_link(target)

        # Mostra na tela a versão atual do grafo
        await self.send_graph_state()

    async def send_graph_state(self):
        # Recupera as informações atuais do grafo a partir do banco
        graph_state = await self.get_graph_state()

        # Envia para o grupo
        await self.channel_layer.group_send("graph", {
                'type': 'send_json_message', 
                "message": graph_state
                }
            )
    
    async def send_json_message(self, event):
        # Envia a mensagem JSON para cada websocket
        graph_state = event["message"]        
        await self.send(text_data=json.dumps(graph_state, cls=DjangoJSONEncoder))

    @database_sync_to_async
    def add_link(self, target):
        # Recupera o nó atual
        source_node, source_error = Node.objects.get_or_create(id=self.username, defaults={"x":randint(10, self.width), "y":randint(10, self.height)})
        
        # Recupera o nó a ser ligado
        target_node, target_error = Node.objects.get_or_create(id=target, defaults={"x":randint(10, self.width), "y":randint(10, self.height)})
        
        # Se não houver erros, cria o link
        if not source_error and not target_error:
            Link.objects.create(source=source_node, target=target_node)

    @database_sync_to_async
    def get_graph_state(self):
        # Monta o json para exibição na tela
        return {
            'nodes': list(Node.objects.values('id', 'x', 'y')),
            'links': list(Link.objects.values('source', 'target'))
        }

    @database_sync_to_async
    def add_node(self):
        # Cria um nó
        return Node.objects.get_or_create(id=self.username, defaults={"x":randint(10, self.width), "y":randint(10, self.height)})
