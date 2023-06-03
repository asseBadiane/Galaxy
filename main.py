from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.properties import Clock

class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    V_NB_LINES = 10 # numbers the lines
    V_LINES_SPACING = .25 # perrcentage the screen
    Vertical_Lines = [] # list the lines

    H_NB_LINES = 15 
    H_LINES_SPACING = .1 
    horizontal_Lines = [] 

    SPEED = 4
    current_offset_y = 0

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        # self.perspective_x = self.width / 2
        # self.perspective_y = self.height * 0.75
        # print(f"Perspective X: {self.width}, Perspective Y: {self.height}")
        self.init_vertical_lines()
        self.init_horizontal_lines()
        Clock.schedule_interval(self.update, 1.0/60.0)
       
        
    def on_parent(self, widget, parent):
        # print(f"Perspective X: {self.width}, Perspective Y: {self.height}")
        pass

    def on_size(self, *args):
        pass
        # self.update_vertical_lines()
        # self.update_horizontal_lines()
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
        offset = - int(self.V_NB_LINES / 2) + 0.5
        for i in range(0, self.V_NB_LINES):
            lines_x = int(central_line_x + offset * spacing)
            # x1 = int(central_line_x + offset * spacing)
            # y1 = 0
            # x2 = x1
            # y2 = self.height
            x1, y1 = self.transform(lines_x, 0)
            x2, y2 = self.transform(lines_x, self.height)
            self.Vertical_Lines[i].points = [x1, y1, x2, y2]
            # print(f"{i}- X1: {x1}, Y1: {y1}, X2:{x2}, Y2: {y2}")
            offset += 1

    def transform(self, x, y):
        # return self.transform_2D(x, y)
        return self.transform_perspective(x, y)
    
    def transform_2D(self, x, y):
        return int(x), int(y)
    
    def transform_perspective(self, x, y):
        lin_y = self.perspective_point_y * y / self.height
        if lin_y > self.perspective_point_y:
            lin_y = self.perspective_point_y
        
        diff_y = self.perspective_point_y - lin_y
        diff_x = x - self.perspective_point_x
        
        factor_y = diff_y / self.perspective_point_y
        factor_y = pow(factor_y, 4)

        offset_x = diff_x * factor_y

        tr_x = self.perspective_point_x + offset_x
        tr_y = self.perspective_point_y - factor_y * self.perspective_point_y

        return int(tr_x), int(tr_y)

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.H_NB_LINES):
                self.horizontal_Lines.append(Line())

    def update_horizontal_lines(self):
        
        central_line_x = self.width / 2 
        spacing = self.V_LINES_SPACING * self.width
        offset = - int(self.V_NB_LINES / 2) + 0.5

        xmin = central_line_x - offset * spacing
        xmax = central_line_x + offset * spacing
        spacing_y = self.H_LINES_SPACING * self.height
        for i in range(0, self.H_NB_LINES):
            lines_y = i * spacing_y - self.current_offset_y
            x1, y1 = self.transform(xmin, lines_y)
            x2, y2 = self.transform(xmax, lines_y)
            self.horizontal_Lines[i].points = [x1, y1, x2, y2]

    def update(self, dt):
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.current_offset_y += self.SPEED
      
        spacing_y = self.H_LINES_SPACING * self.height
        if self.current_offset_y >= spacing_y:
            self.current_offset_y -= spacing_y

class GalaxyApp(App):
    pass

GalaxyApp().run()