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
        self.manager.get_games()
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
        self.join_game(args.id)
    
    def create_game(self, name):
        request = {
            "method": "create_game",
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

    def join_game(self,game_id):
        request = { 
            "method" : "join_game",
            "args" : { 
                "player" : self.manager.player, 
                "game_id" : game_id,
                "team": 1
                }
            }
        request = json.dumps(request, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        self.manager.connection.write(request.encode('utf-8'))
        self.manager.current = "select_team"
    # # Handlers 
    # def handle_join_game(self,args):
    #     result = Game.from_json(args)
    #     for p in result.team_one:
    #         if p.id == self.manager.player.id:
    #             self.manager.player.team = 1
    #     for p in result.team_two:
    #         if p.id == self.manager.player.id:
    #             self.manager.player.team = 2
        
    #     self.manager.game = result
    #     self.manager.current = 'select_team'

    # def handle_create_game(self,args):
    #     result = CreateGameEvent.from_json(args)
    #     game = Game([self.manager.player],[],result.name,result.id)
    #     self.manager.game = game
    #     self.manager.current = 'select_team'

