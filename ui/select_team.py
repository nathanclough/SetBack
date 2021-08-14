from re import S
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
import json
import uuid

class SelectTeam():
    def __init__(self, response_handlers):
        self.response_handlers = response_handlers
        self.connection = None
    
    def set_connection(self, connection):
        self.connection = connection

    def render(self):
        self.screen = Screen(name="select_team")
        header =  BoxLayout(orientation="vertical")
        self.leave_button = Button(text="Leave Game")
        self.leave_button.bind(on_release=self.leave)
        self.start_button = Button(text="start_game")
        self.label = Label(text="")
        self.screen.bind(on_pre_enter=self.setValues)
        
        self.teams = BoxLayout(orientation="horizontal")
        self.team_one_label = Label(text="Team One\n Player, Player")
        self.team_two_label = Label(text="Team Two \n Player, Player")
        self.teams.add_widget(self.team_one_label)
        self.teams.add_widget(self.team_two_label)
                
        header.add_widget(self.label)
        header.add_widget(self.teams)
        header.add_widget(self.leave_button)
        header.add_widget(self.start_button)
        self.screen.add_widget(header)
        return self.screen
    
    def setValues(self, args):
        self.label.text = self.screen.manager.game.name
        self.update_teams()

    def update_teams(self):
        text = "Team One \n"
        for player in self.screen.manager.game.team_one:
            text += player.name + "\n"
        self.team_one_label.text = text
        text = "Team Two \n"
        for player in self.screen.manager.game.team_two:
            text += player.name +"\n"
        self.team_two_label.text = text

    def switch_teams(self,args):
        pass

    def leave(self,args):
        id = str(uuid.uuid4())
        request ={ "request_id": id,
            "method": "leave_game",
            "args" : { "game_id": self.screen.manager.game.id, "player_id" : self.screen.manager.player.id}}
        request = json.dumps(request, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        self.response_handlers[id] = self.handle_leave
        self.connection.write(request.encode('utf-8'))
        
    
    def handle_leave(self,args):
        self.screen.manager.current="homepage"