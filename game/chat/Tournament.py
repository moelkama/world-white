import asyncio, json, random
from datetime import datetime
from chat.cons import Match, User, send_to_group, racket, height, hh, width, ww, score_to_win, save_Match
from channels.generic.websocket import AsyncWebsocketConsumer
from . views import endpoint
N = 8
waiting = {}
tournaments = {}
tournament_name = 'tournament_' + datetime.now().time().strftime("%H_%M_%S_%f")
TIME_TO_START_MATCHS = 30

def serialize_Match(o):
    return{
        'type':'game.state',
        'players':[{'login':p.user.display_name, 'icon':p.user.photo_profile, 'racket':p.racket.serialize_racket()} for p in o.players],
        'ping':o.b.serialize_ball(),
        'team1_score':o.team1_score,
        'team2_score':o.team2_score,
    }

async def full_tournament(users, tournament_name):
    random.shuffle(users)
    tournaments[tournament_name] = {}
    while len(users) > 1:
        group_name = None
        for i in range(len(users)):
            if i % 2 == 0:
                group_name = 'Match_' + datetime.now().time().strftime("%H_%M_%S_%f")
            users[i].tournament_name = tournament_name
            users[i].group_name = group_name
            users[i].next_index = int(i / 2)
            await users[i].channel_layer.group_add(users[i].group_name, users[i].channel_name)
            # await users[i].channel_layer.group_add(tournament_name, users[i].channel_name)
            if i % 2 == 1:
                users[i].racket = racket((width - ww), (height - hh) / 2, 0, height)
                users[i - 1].racket = racket(0, (height - hh) / 2, 0, height)
                tournaments[tournament_name][users[i].group_name] = Match(2)
                tournaments[tournament_name][users[i].group_name].set_player(users[i - 1], 0)
                tournaments[tournament_name][users[i].group_name].set_player(users[i], 1)
        await tournaments[tournament_name][group_name].players[0].channel_layer.group_send(tournament_name,
        {
            'type': 'send_data',
            'data':json.dumps({'type':'tournament.info', 'players':[{'login':u.user.display_name, 'icon':u.user.photo_profile} for u in users]})
        })
        users.clear()
        await tournaments[tournament_name][group_name].players[0].channel_layer.group_send(tournament_name,
        {
            'type': 'send_data',
            'data':json.dumps({'type':'tournament.countdown', 'time': TIME_TO_START_MATCHS})
        })
        await asyncio.sleep(TIME_TO_START_MATCHS)
        tasks = [asyncio.create_task(run_game(m)) for m in tournaments[tournament_name].values()]
        users = await asyncio.gather(*tasks)
        tasks.clear()
        tournaments[tournament_name].clear()
        users = sorted(users, key=lambda item: item.next_index)
        await asyncio.sleep(3)
    if len(users) > 0:
        if users[0].avaible:
            await users[0].send(json.dumps({'type':'tournament.end', 'result':'Booyah'}))
    users.clear()

async def run_game(match):
    await match.players[0].channel_layer.group_send(match.players[0].group_name, #await
    {
        'type': 'send_data',
        'data':json.dumps(match, default=serialize_Match)
    })
    for channel in match.players:
        if channel.avaible:
            await channel.send(json.dumps({'type':'game.countdown', 'time':3}))
    await asyncio.sleep(4)
    while match.players[0].avaible and match.players[1].avaible:
        match.move()
        await match.players[0].channel_layer.group_send(match.players[0].group_name, #await
        {
            'type': 'send_data',
            'data':json.dumps(match, default=serialize_Match)
        })
        await asyncio.sleep(0.001)
        if (match.team2_score == score_to_win):
            if match.players[0].avaible:
                await match.players[0].send(json.dumps({'type':'game.end', 'result':'Winner'}))
            if match.players[1].avaible:
                await match.players[1].send(json.dumps({'type':'game.end', 'result':'Loser'}))
            await match.players[1].channel_layer.group_discard(
                match.players[1].group_name,
                match.players[1].channel_name
            )
            await match.players[1].channel_layer.group_discard(
                match.players[1].tournament_name,
                match.players[1].channel_name
            )
            # match.players[1].avaible = False
            # await match.players[1].close()
            await save_Match(match, 0)
            return match.players[0]
        elif (match.team1_score == score_to_win):
            if match.players[1].avaible:
                await match.players[1].send(json.dumps({'type':'game.end', 'result':'Winner'}))
            if match.players[0].avaible:
                await match.players[0].send(json.dumps({'type':'game.end', 'result':'Loser'}))
            await match.players[0].channel_layer.group_discard(
                match.players[0].group_name,
                match.players[0].channel_name
            )
            await match.players[0].channel_layer.group_discard(
                match.players[0].tournament_name,
                match.players[0].channel_name
            )
            # match.players[0].avaible = False
            # await match.players[0].close()
            await save_Match(match, 1)
            return match.players[1]
    if match.players[0].avaible:
        if match.players[0].avaible:
            await match.players[0].send(json.dumps({'type':'game.end', 'result':'Winner'}))
        return (match.players[0])
    elif match.players[1].avaible:
        if match.players[0].avaible:
            await match.players[1].send(json.dumps({'type':'game.end', 'result':'Winner'}))
        return (match.players[1])

# x = 1
class   Tournament(AsyncWebsocketConsumer):
    async def connect(self):
        global x
        global tournament_name
        await self.accept()
        self.group_name = "None"
        self.avaible = True
        query_parameters = self.scope['query_string'].decode().split('&')
        token = query_parameters[0].split('=')[1]
        id = query_parameters[1].split('=')[1]
        # game_type = query_parameters[2].split('=')[1]
        data = endpoint(token, id)
        self.user = User(data)
        self.tournament_name = tournament_name
        await self.channel_layer.group_add(self.tournament_name, self.channel_name)
        ########################
        if self.user.username in waiting:
            if waiting[self.user.username].avaible:
                await waiting[self.user.username].send(json.dumps({'type':'discard', 'game_type':'Tournament_game'}))
            await waiting[self.user.username].close()
        waiting[self.user.username] = self
        ########################
        #***********************#
        # global x
        # self.user.x = x
        # waiting[str(x)] = self
        # self.x = str(x)
        # x += 1
        #***********************#
        await self.channel_layer.group_send(self.tournament_name,
        {
            'type': 'send_data',
            'data':json.dumps({'type':'tournament.list', 'players':[{'login':u.user.display_name, 'icon':u.user.photo_profile} for u in waiting.values()]})
        })
        if len(waiting) == N:
            # x = 1
            asyncio.create_task(full_tournament(list(waiting.values()), tournament_name))
            tournament_name = 'tournament_' + datetime.now().time().strftime("%H_%M_%S_%f")
            waiting.clear()

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get('type') == 'move':
            self.racket.change_direction(data.get('move'))

    async def send_data(self, event):
        if self.avaible:
            await self.send(event['data'])

    async def disconnect(self, code):
        #################################################################
        # if (self.x in waiting):
        #     del waiting[self.x]
        #     await self.channel_layer.group_send(self.tournament_name,
        #     {
        #         'type': 'send_data',
        #         'data':json.dumps({'type':'tournament.list', 'players':[{'login':u.user.display_name, 'icon':u.user.photo_profile} for u in waiting.values()]})
        #     })
        #################################################################
        if self.user.username in waiting:
            del waiting[self.user.username]
            await self.channel_layer.group_send(self.tournament_name,
            {
                'type': 'send_data',
                'data':json.dumps({'type':'tournament.list', 'players':[{'login':u.user.display_name, 'icon':u.user.photo_profile} for u in waiting.values()]})
            })
        await self.channel_layer.group_discard(
            self.tournament_name,
            self.channel_name
        )
        await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
        self.avaible = False