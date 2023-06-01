from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line

class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)



    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.perspective_x = self.width / 2
        self.perspective_y = self.height * 0.75
        print(f"Perspective X: {self.width}, Perspective Y: {self.height}")
       
        
    def on_parent(self, widget, parent):
        # print(f"Perspective X: {self.width}, Perspective Y: {self.height}")
        pass

    def on_size(self, *args):
        print("on_size")
        print(f"Perspective X: {self.perspective_point_x}, Perspective Y: {self.perspective_point_y}")
    
    def on_perspective_point_x(self, widget, value):
        print(f"Perspective X: {value}")

    def on_perspective_point_y(self, widget, value):
        print(f"Perspective Y: {value}")
    


  

class GalaxyApp(App):
    pass

GalaxyApp().run()