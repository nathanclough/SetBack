import kivy
from kivy.app import App
from kivy.uix.label import Label

class Homepage(App):
    def build(self):
        return Label(text="This the Homepage")
 
if __name__ == "__main__":
   Homepage().run()