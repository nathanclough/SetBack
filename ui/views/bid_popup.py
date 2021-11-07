from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

class BidPopup(Popup):
    def __init__(self, send_result,**kwargs):
        super().__init__(**kwargs)
        # inject the update function
        self.send_result = send_result
        self.dropdown = DropDown()
        self.selection = 0
        for x in range(8):
            btn = Button(text=f"{x}",size_hint=(None,None))
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)
        self.mainbutton = Button(text='Show', size_hint=(None, None))

        # show the dropdown menu when the main button is released
        # note: all the bind() calls pass the instance of the caller (here, the
        # mainbutton instance) as the first argument of the callback (here,
        # dropdown.open.).
        self.mainbutton.bind(on_release=self.dropdown.open)

        # one last thing, listen for the selection in the dropdown list and
        # assign the data to the button text.
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))
        self.ids.container.add_widget(self.mainbutton)

        submitbutton = Button(text="submit",on_release=self.submit,size_hint=(None,None))
        self.ids.container.add_widget(submitbutton)

    def submit(self, args):
        # call update function 
        # Build the result message 
        message = self.mainbutton.text
        self.send_result(message)
        self.dismiss()

        

