from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line

class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    V_NB_LINES = 7 # numbers the lines
    V_LINES_SPACING = .1 # perrcentage the screen
    Vertical_Lines = [] # list the lines

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        # self.perspective_x = self.width / 2
        # self.perspective_y = self.height * 0.75
        # print(f"Perspective X: {self.width}, Perspective Y: {self.height}")
        self.init_vertical_lines()
       
        
    def on_parent(self, widget, parent):
        # print(f"Perspective X: {self.width}, Perspective Y: {self.height}")
        pass

    def on_size(self, *args):
        self.update_vertical_lines()
        # print("on_size")
        # print(f"Perspective X: {self.perspective_point_x}, Perspective Y: {self.perspective_point_y}")
    
    def on_perspective_point_x(self, widget, value):
        # print(f"Perspective X: {value}")
        pass

    def on_perspective_point_y(self, widget, value):
        # print(f"Perspective Y: {value}")
        pass
    

    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            # self.lines = Line(points=[100, 0, 100, 100])
            for i in range(0, self.V_NB_LINES):
                self.Vertical_Lines.append(Line())

    def update_vertical_lines(self):
        # self.lines.points = [self.perspective_point_x, 0, self.perspective_point_x, self.height]
        central_line_x = self.width / 2
        spacing = self.V_LINES_SPACING * self.width
        offset = - int(self.V_NB_LINES / 2)
        for i in range(0, self.V_NB_LINES):
            lines_x = int(central_line_x + offset * spacing)
            x1 = int(central_line_x + offset * spacing)
            y1 = 0
            x2 = x1
            y2 = self.height
         
            self.Vertical_Lines[i].points = [x1, y1, x2, y2]
            # print(f"{i}- X1: {x1}, Y1: {y1}, X2:{x2}, Y2: {y2}")
            offset += 1

class GalaxyApp(App):
    pass

GalaxyApp().run()