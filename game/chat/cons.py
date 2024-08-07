import asyncio, json, math
from datetime import datetime
from . views import endpoint
from channels.generic.websocket import AsyncWebsocketConsumer # type: ignore
from asgiref.sync import sync_to_async
# from auth_app.models import User
import requests
width = 600
height = 300
hh = 80
ww = 5
racket_speed = 1
score_to_win = 3
def add_padding(data):
    return data + '=' * (-len(data) % 4)
import os
from cryptography.fernet import Fernet
class racket:
    def __init__(self, x, y, min, max):
        self.x = x
        self.y = y
        self.min = min
        self.max = max
        self.h = hh
        self.w = ww
        self.vy = 0
        self.score = 0

    def change_direction(self, data):
        if (data == 'Up'):
            self.vy = -racket_speed
        elif (data == 'Down'):
            self.vy = racket_speed
        elif (data == 'Stop'):
            self.vy = 0

    def move(self):
        if self.vy < 0:
            if self.y + self.vy > self.min:
                self.y += self.vy
            else:
                self.y = self.min
        else:
            if self.y + self.vy < self.max - self.h:
                self.y += self.vy
            else:
                self.y = self.max - self.h

    def serialize_racket(self):
        return {
            'x': self.x,
            'y': self.y,
            'h': self.h,
            'w': self.w,
            'score':self.score,
        }

class ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 10
        self.angl = 0
        self.speed = 0.9
        self.vx = math.cos(self.angl * math.pi / 180) * self.speed
        self.vy = math.sin(self.angl * math.pi / 180) * self.speed
    def serialize_ball(self):
        return{
            'x':self.x,
            'y':self.y,
            'r':self.r,
        }

class   Match:
    def __init__(self, N):
        self.starting = False
        self.players = [None] * N
        self.b = ball(width / 2, height / 2)
        self.team1_score = 0
        self.team2_score = 0
        # self.match_begin = False

    def set_player(self, player, index):
        self.players[index] = player

    def move(self):
        if (self.b.x + self.b.r < ww):
            self.team1_score += 1
            self.b.x = width / 2
            self.b.y = height / 2
            # self.b.__init__(width / 2, height / 2)
            # await asyncio.sleep(1)
        if (self.b.x - self.b.r > width - ww):
            self.team2_score += 1
            self.b.x = width / 2
            self.b.y = height / 2
            # self.b.__init__(width / 2, height / 2)
            # await asyncio.sleep(1)
        if (self.b.vx > 0):
            if ((self.b.x + self.b.r) + self.b.vx < (width - ww)):
                self.b.x += self.b.vx
            else:
                if ((self.b.y) < self.players[1].racket.y or self.b.y >self.players[1].racket.y + hh):
                    self.b.x += self.b.vx
                else:
                    self.b.x += (width - ww) - (self.b.x + self.b.r)
                    self.b.vx = -self.b.vx
        else:
            if (self.b.y < self.players[0].racket.y or self.b.y >self.players[0].racket.y + hh or (self.b.x - self.b.r) + self.b.vx > ww):
                self.b.x += self.b.vx
            else:
                self.b.x = ww + self.b.r
                self.b.vx = -self.b.vx
        if (self.b.vy > 0):
            if (self.b.y + self.b.r + self.b.vy < (height - 0)):
                self.b.y += self.b.vy
            else:
                self.b.y = (height - 0) - self.b.r
                self.b.vy = -self.b.vy
        else:
            if ((self.b.y - self.b.r) + self.b.vy > 0):
                self.b.y += self.b.vy
            else:
                self.b.y = self.b.r + 0
                self.b.vy = -self.b.vy
        for player in self.players:
            player.racket.move()

    async def run_game(self):
        while self.players[0].avaible and self.players[1].avaible:
            self.move()
            await send_to_group(self.players, {'data':json.dumps(self, default=serialize_Match)})
            # await self.players[0].channel_layer.group_send(self.players[0].group_name,
            # {
            #     'type': 'send_data',
            #     'data':json.dumps(self, default=serialize_Match)
            # })
            if (self.team1_score == score_to_win):
                return 1
            if (self.team2_score == score_to_win):
                return 2
            await asyncio.sleep(0.001)
        # if self.players[0].avaible:
        #     self.team1_score = score_to_win
        #     return 2
        # self.team2_score = score_to_win
        # return 1

async def send_to_group(group, data):
    for channel in group:
        await channel.send_data(data)

def serialize_Users(o):
    return{
        'type': 'game.info',
        'players':[p.user.serialize_User() for p in o.players],
    }

def save_Match(group_name, idx):
    query_parameters = rooms[group_name].players[abs(idx-1)].scope['query_string'].decode().split('&')
    losee_token = query_parameters[0].split('=')[1]
    # losee_token = rooms[group_name].players[abs(idx-1)].scope['query_string'].decode().split('=')[1]
    key = os.environ.get('encrypt_key')
    f = Fernet(key)
    losee_token = f.decrypt(add_padding(losee_token).encode()).decode()
    headers = {'Authorization': f'Token {losee_token}'}
    body = {
        'lose': rooms[group_name].players[abs(idx-1)].user.lose + 1,
    }
    idloser = rooms[group_name].players[abs(idx-1)].user.id
    url = f'http://auth:8000/api/tasks/{idloser}/'
    requests.patch(url=url, headers=headers, data=body)

    """ update winner score"""
    query_parameters = rooms[group_name].players[idx].scope['query_string'].decode().split('&')
    win_token = query_parameters[0].split('=')[1]
    # win_token = rooms[group_name].players[idx].scope['query_string'].decode().split('=')[1]
    win_token = f.decrypt(add_padding(win_token).encode()).decode()
    headers = {'Authorization': f'Token {win_token}'}
    body = {
        'score': rooms[group_name].players[idx].user.score + 10,
        'win': rooms[group_name].players[idx].user.win + 1,
    }
    idwinner = rooms[group_name].players[idx].user.id
    url = f'http://auth:8000/api/tasks/{idwinner}/'
    requests.patch(url=url, headers=headers, data=body)

    """ save match to database"""
    data = {
        'winner': idwinner,
        'loser': idloser,
        'score1': rooms[group_name].team1_score if rooms[group_name].team1_score > rooms[group_name].team2_score else rooms[group_name].team2_score,
        'score2': rooms[group_name].team1_score if rooms[group_name].team1_score < rooms[group_name].team2_score else rooms[group_name].team2_score,}
    url = f'http://auth:8000/api/match/'
    requests.post(url=url, headers=headers, data=data)

async def start_game(group_name):
    # await asyncio.sleep(4)
    print("---------------game start-------------")
    winner = await rooms[group_name].run_game()
    if group_name in rooms:
        print("---------------game end succefly-------------")
        result = ['Winner', 'Winner']
        idx = 0
        if winner == 1:
            idx = 1
            result[0] = 'Loser'
        else:
            result[1] = 'Loser'
        for i in range(2):
            if rooms[group_name].players[i].avaible:
                print("---------------", rooms[group_name].players[i].user.username, "-------------")
                await rooms[group_name].players[i].send(json.dumps({'type':'game.end', 'result':result[i % 2]}))
                rooms[group_name].players[i].avaible = False
                await rooms[group_name].players[i].close()
        save_Match(group_name, idx)
        del rooms[group_name]

def serialize_Match(o):
    return{
        'type':'game.state',
        'players':[{'racket':p.racket.serialize_racket()} for p in o.players],
        'ping':o.b.serialize_ball(),
        'team1_score':o.team1_score,
        'team2_score':o.team2_score,
    }

rooms = {}
group_name = 'Match_' + datetime.now().time().strftime("%H_%M_%S_%f")

class   User:
    def __init__(self, dict):
        for key, value in dict.items():
            setattr(self, key, value)

    def serialize_User(self):
        return{
            'login':self.username,
            'icon':self.photo_profile,
        }

from . main_socket import connects

class RacetCunsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("----------------connect----------------")
        global group_name
        await self.accept()
        self.avaible = True
        self.ready = False
        query_parameters = self.scope['query_string'].decode().split('&')
        token = query_parameters[0].split('=')[1]
        id = query_parameters[1].split('=')[1]
        game_type = query_parameters[2].split('=')[1]
        room_creater = query_parameters[3].split('=')[1]
        
        key = os.environ.get('encrypt_key')
        f = Fernet(key)
        token = f.decrypt(add_padding(token).encode()).decode()

        data = endpoint(token, id)
        self.user = User(data)
        if game_type == 'random':
            self.group_name = group_name
        else:
            self.group_name = connects[room_creater].room_name
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        if self.group_name in rooms:
            if rooms[self.group_name].players[0].user.username != self.user.username:
                self.racket = racket(width - ww, (height - hh) / 2, 0, height)
                self.i = 1
                rooms[self.group_name].set_player(self, self.i)
                await send_to_group(rooms[self.group_name].players, {'data':json.dumps(rooms[self.group_name], default=serialize_Users)})
                group_name = 'Match_' + datetime.now().time().strftime("%H_%M_%S_%f")
            # else:
            #     await self.close()
        else:
            self.racket = racket(0, (height - hh) / 2, 0, height)
            rooms[self.group_name] = Match(2)
            self.i = 0
            rooms[self.group_name].set_player(self, self.i)

    async def receive(self, text_data):
        global rooms
        data = json.loads(text_data)
        if data.get('type') == 'move':
            self.racket.change_direction(data.get('move'))
        elif data.get('type') == 'action':
            if data.get('action') == 'Continue':
                self.ready = True
                if rooms[self.group_name].players[abs(self.i - 1)].ready == True:
                    rooms[self.group_name].starting = True
                    asyncio.create_task(start_game(self.group_name))
            elif data.get('action') == 'Give_Up':
                await self.close()

    async def send_data(self, event):
        if self.avaible:
            await self.send(event['data'])

    async def disconnect(self, code):
        print("----------disconnect-----------", self.user.username, "with code::", code)
        self.avaible = False
        if self.group_name in rooms:
            self.avaible = False
            if rooms[self.group_name].starting:
                await rooms[self.group_name].players[abs(self.i - 1)].send(json.dumps({'type':'game.end', 'result':'Winner'}))
                if self.i == 0:
                    rooms[self.group_name].team1_score = score_to_win
                else:
                    rooms[self.group_name].team2_score = score_to_win
                save_Match(self.group_name, abs(self.i - 1))
            else:
                if rooms[self.group_name].players[abs(self.i - 1)] and rooms[self.group_name].players[abs(self.i - 1)].user.username in connects:
                    await connects[rooms[self.group_name].players[abs(self.i - 1)].user.username].send(json.dumps({'type':'game.refuse', 'vs': self.user.serialize_User()}))
            del rooms[self.group_name]