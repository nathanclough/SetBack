from setback.results.create_game_result import CreateGameResult
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

    def render_homepage(self):
        # get a scrollable view 
        self.root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))        
        
        # Set the connection status to the default connecting 
        self.connection_status_label = Label(text='connecting...\n',size_hint_y=None,height=20)
        self.title = Label(text="Setback",font_size='50sp',size_hint_y=None, height= 300)
        # Create a vertical layout and add the status and create game options 
        self.menu_layout = GridLayout(cols=1, spacing=10,size_hint_y=None)       
        self.menu_layout.add_widget(self.title)
        self.menu_layout.add_widget(self.connection_status_label)
        self.menu_layout.add_widget(self.get_create_game())

        self.menu_layout.bind(minimum_height=self.menu_layout.setter('height'))
        self.root.add_widget(self.menu_layout)
        Clock.schedule_interval(self.get_games, 2.5)
        return self.root

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
        id = str(uuid.uuid4)
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
                btn = self.get_join_game_button(id,game.name)
                self.menu_layout.add_widget(btn)
        
        for id in self.games:
            if(not id in result.games):
                self.menu_layout.remove_widget(self.game_buttons[id])
        
        self.games = result.games 


    def create_game(self, name):
        id = str(uuid.uuid4)

        request = {
            "request_id": id,
            "method": "create_game",
            "args": {
                "name" : self.textbox.text,
                "player": {
                    "name" : "Nathan",
                    "id" : 123,
                    "team": 1
                }
            }
        }
        self.response_handlers[id] = self.handle_create_game

        request = json.dumps(request)
        self.connection.write(request.encode('utf-8'))

    def handle_create_game(self,args):
        result = CreateGameResult.from_json(args)
    
    def get_join_game_button(self,id,name):
        btn =  Button(text=f"Join: {name}", size_hint_y=None, height=50)
        # bind button to join game function 
        self.game_buttons[id] = btn
        return btn



        