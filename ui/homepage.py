from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from setback import GetGamesResult
import uuid
import json

class HomePage():
    def __init__(self, response_handlers) -> None:
        self.response_handlers = response_handlers
        
    def render_homepage(self):
        self.textbox_layout = BoxLayout(orientation="horizontal")
        self.textbox = TextInput(size_hint_y=.1, multiline=False)
        self.textbox.bind(on_text_validate=self.create_game)
        self.textbox_label = Label(text="Create Game")
        self.textbox_layout.add_widget(self.textbox_label)
        self.textbox_layout.add_widget(self.textbox)
        
        self.label = Label(text='connecting...\n')
        
        self.menu_layout = BoxLayout(orientation="vertical")       
        self.menu_layout.add_widget(self.textbox_layout)
        self.menu_layout.add_widget(self.label)
        
        return self.menu_layout

    def get_games(self):
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
        self.games = result.games 
        for id  in self.games:
            game = self.games[id]
            btn = Button(text=f"Join Game: {game.name}")
            # bind the button to join the game 
            # btn.bind(on_press=self.send_message(game))
            self.menu_layout.add_widget(btn)

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
        self.get_games()


        