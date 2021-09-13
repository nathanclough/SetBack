from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
import json

class HomePage(Screen):
    connection_status_label = StringProperty("connecting ...")
    username = StringProperty("")

    def __init__(self,**kw):
        self.games = {}
        self.game_buttons = {}
        super().__init__(**kw)

    def on_enter(self, *args):
        self.manager.bind(games_to_join=self.render_buttons)
        self.username = self.manager.player.name
        self.manager.get_lobbies()
        return super().on_enter(*args)

    def on_leave(self, *args):
        return super().on_leave(*args)

    def render_buttons(self,instance,value):
        self.ids.button_layout.clear_widgets()
        for game in self.manager.games_to_join:
            btn =  Button(text=f"Join: {game.name}",size_hint_y=None, height=50)
            btn.id = game.id
            btn.bind(on_release=self.switch_to_select_team) 
            self.ids.button_layout.add_widget(btn)
        
    def switch_to_select_team(self,args):
        self.join_lobby(args.id)
    
    def create_lobby(self, name):
        request = {
            "method": "create_lobby",
            "args": {
                "name" : name,
                "player": self.manager.player
            }
        }

        request = json.dumps(request, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        self.manager.connection.write(request.encode('utf-8'))
        self.manager.current = "select_team"
    
    def update_username(self,name):
        self.username = name
        self.ids.name_input.text = "enter user name"
        self.manager.player.name = name

    def join_lobby(self,game_id):
        request = { 
            "method" : "join_lobby",
            "args" : { 
                "player" : self.manager.player, 
                "game_id" : game_id,
                "team": 1
                }
            }
        request = json.dumps(request, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        self.manager.connection.write(request.encode('utf-8'))
        self.manager.current = "select_team"

