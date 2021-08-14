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
from kivy.core.window import Window
from setback import GetGamesResult
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
import uuid
import json

class HomePage():
    def __init__(self, response_handlers) -> None:
        self.response_handlers = response_handlers
        self.games = {}
        self.game_buttons = {}
        self.connection = None
        
    def set_connection(self,connection):
        self.connection = connection

    def render(self):
        # get a scrollable view 
        self.screen = Screen(name='homepage')
        self.scroll = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))        
        
        # Set the connection status to the default connecting 
        self.connection_status_label = Label(text='connecting...\n',size_hint_y=None,height=20)
        self.title = Label(text="Setback",font_size='50sp',size_hint_y=None, height= 300)
        # Create a vertical layout and add the status and create game options 
        self.menu_layout = GridLayout(cols=1, spacing=10,size_hint_y=None)       
        self.menu_layout.add_widget(self.title)
        self.menu_layout.add_widget(self.connection_status_label)
        self.menu_layout.add_widget(self.get_create_game())

        self.menu_layout.bind(minimum_height=self.menu_layout.setter('height'))
        self.scroll.add_widget(self.menu_layout)
        Clock.schedule_interval(self.get_games, 2.5)
        self.screen.add_widget(self.scroll)
        return self.screen

    def get_create_game(self):
        self.create_game_button = Button(size_hint_y=None,height=30,text="Create Game")
        self.create_game_button.bind(on_press=self.create_game)
        
        self.textbox = TextInput(size_hint_y=None,height=30, multiline=False)
        
        # Add to the layout 
        self.textbox_layout = BoxLayout(orientation="horizontal",size_hint_y=None,height=20)
        self.textbox_layout.add_widget(self.textbox)
        self.textbox_layout.add_widget(self.create_game_button)
        return self.textbox_layout


    def get_games(self, dt):
        if self.connection == None:
            return 
        id = str(uuid.uuid4())
        request = {
            "request_id" : id,
            "method": "get_games"
        }
        
        # add the handler to the dictionary 
        self.response_handlers[id] = self.handle_get_games

        # send the request 
        request = json.dumps(request)
        self.connection.write(request.encode('utf-8'))
        
    def handle_get_games(self, response):
        result = GetGamesResult.from_json(response)        
        for id  in result.games:
            if(not id in self.games):
                game = result.games[id]
                self.games[id] = game
                btn = self.get_join_game_button(id,game)
                self.menu_layout.add_widget(btn)
        
        for id in self.games:
            if(not id in result.games):
                self.menu_layout.remove_widget(self.game_buttons[id])
        
        self.games = result.games 


    def create_game(self, name):
        id = str(uuid.uuid4())

        request = {
            "request_id": id,
            "method": "create_game",
            "args": {
                "name" : self.textbox.text,
                "player": self.screen.manager.player
            }
        }
        self.response_handlers[id] = self.handle_create_game

        request = json.dumps(request, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        self.connection.write(request.encode('utf-8'))

    def handle_create_game(self,args):
        result = CreateGameResult.from_json(args)
        game = Game([self.screen.manager.player],[],result.name,result.id)
        self.screen.manager.game = game
        self.screen.manager.current = 'select_team'

    
    def get_join_game_button(self,id,game):
        btn =  Button(text=f"Join: {game.name}", size_hint_y=None, height=50)
        btn.bind(on_release=self.switch_to_select_team) 
        self.game_buttons[id] = btn
        return btn
    
    def switch_to_select_team(self,args):
        for id in self.game_buttons:
            if args == self.game_buttons[id]:
                self.join_game(id)

    def join_game(self,game_id):
        request_id = str(uuid.uuid4())
        request = { "request_id": request_id, 
            "method" : "join_game",
            "args" : { 
                "player" : self.screen.manager.player, 
                "game_id" : game_id,
                "team": 1
                }
            }
        request = json.dumps(request, default=lambda o: o.__dict__, sort_keys=True, indent=4)

        self.response_handlers[request_id] = self.handle_join_game
        self.connection.write(request.encode('utf-8'))
    
    def handle_join_game(self,args):
        result = Game.from_json(args)
        for p in result.team_one:
            if p.id == self.screen.manager.player.id:
                self.screen.manager.player.team = 1
        for p in result.team_two:
            if p.id == self.screen.manager.player.id:
                self.screen.manager.player.team = 2
        
        self.screen.manager.game = result
        self.screen.manager.current = 'select_team'




        