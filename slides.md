---
marp: true
theme: default
class: lead
paginate: true
---

# Saindo do básico com Django Channels

---

## O que é Django Channels?

- **Django Channels** é um framework que utiliza como suporte o framework web Django.
- Provê suporte a:
  - **WebSockets**
  - **Eventos assíncronos**
  - **Comunicação em tempo real**
- Permite criar aplicações web que necessitam de comunicação em tempo real.

---

## Características

- **WebSockets**
- **Assincrono**
- **Protocolos de Rede**

---

## Como Funciona?

1. **Django Channels** utiliza **ASGI (Asynchronous Server Gateway Interface)**.
2. Uma das maneiras de prover comunicação assíncrona no Django.
3. Adiciona suporte para **consumers** que tratam conexões WebSocket e outras conexões assíncronas.

---

## Quais bibliotecas serão utilizadas

- channels["daphne"]
- django
- channels-redis

---

## Outros recursos necessários

- Redis

---

## Aplicação exemplo

Como toda aplicação clássica com websockets, vamos exibir uma aplicação simples que implementa um chat