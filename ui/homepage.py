from logging import root
from setback.results.create_game_result import CreateGameResult
from setback import Game
from typing import OrderedDict
from kivy.core import text
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.core.window import Window
from setback import GetGamesResult
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
import uuid
import json

class HomePage(Screen):
    connection_status_label = StringProperty("connecting ...")

    def __init__(self,**kw):
        self.games = {}
        self.game_buttons = {}
        super().__init__(**kw)

    def on_enter(self, *args):
        self.get_games_event = Clock.schedule_interval(self.get_games, 5) 
        return super().on_enter(*args)
    
    def on_leave(self, *args):
        Clock.unschedule(self.get_games_event)
        return super().on_leave(*args)

    def get_join_game_button(self,id,game):
        btn =  Button(text=f"Join: {game.name}", size_hint_y=None, height=50)
        btn.bind(on_release=self.switch_to_select_team) 
        self.game_buttons[id] = btn
        return btn
    
    def switch_to_select_team(self,args):
        for id in self.game_buttons:
            if args == self.game_buttons[id]:
                self.join_game(id)

    def get_games(self, dt):
        if self.manager.connection == None:
            return 
        id = str(uuid.uuid4())
        request = {
            "request_id" : id,
            "method": "get_games"
        }
        
        # add the handler to the dictionary 
        self.manager.response_handlers[id] = self.handle_get_games

        # send the request 
        request = json.dumps(request)
        self.manager.connection.write(request.encode('utf-8'))
    
    # Events 
    def create_game(self, name):
        id = str(uuid.uuid4())

        request = {
            "request_id": id,
            "method": "create_game",
            "args": {
                "name" : name,
                "player": self.manager.player
            }
        }
        self.manager.response_handlers[id] = self.handle_create_game

        request = json.dumps(request, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        self.manager.connection.write(request.encode('utf-8'))

    def join_game(self,game_id):
        request_id = str(uuid.uuid4())
        request = { "request_id": request_id, 
            "method" : "join_game",
            "args" : { 
                "player" : self.manager.player, 
                "game_id" : game_id,
                "team": 1
                }
            }
        request = json.dumps(request, default=lambda o: o.__dict__, sort_keys=True, indent=4)

        self.manager.response_handlers[request_id] = self.handle_join_game
        self.manager.connection.write(request.encode('utf-8'))
    
    # Handlers 
    def handle_join_game(self,args):
        result = Game.from_json(args)
        for p in result.team_one:
            if p.id == self.manager.player.id:
                self.manager.player.team = 1
        for p in result.team_two:
            if p.id == self.manager.player.id:
                self.manager.player.team = 2
        
        self.manager.game = result
        self.manager.current = 'select_team'

    def handle_create_game(self,args):
        result = CreateGameResult.from_json(args)
        game = Game([self.manager.player],[],result.name,result.id)
        self.manager.game = game
        self.manager.current = 'select_team'

    def handle_get_games(self, response):
        result = GetGamesResult.from_json(response)        
        for id  in result.games:
            if(not id in self.games):
                game = result.games[id]
                self.games[id] = game
                btn = self.get_join_game_button(id,game)
                self.ids.layout.add_widget(btn)
        
        for id in self.games:
            if(not id in result.games):
                self.ids.layout.remove_widget(self.game_buttons[id])
        
        self.games = result.games 