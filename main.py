
from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '500')

from kivy.core.window import Window
import platform
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.properties import Clock
from kivy.graphics.vertex_instructions import Quad
import random

class MainWidget(Widget):
    from transforms import transform, transform_2D, transform_perspective
    from users_actions import keyboard_closed, on_keyboard_down, on_keyboard_up, on_touch_down, on_touch_up
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    V_NB_LINES = 4 # numbers the lines
    V_LINES_SPACING = .1 # perrcentage the screen
    Vertical_Lines = [] # list the lines

    H_NB_LINES = 15 
    H_LINES_SPACING = .1 
    horizontal_Lines = [] 

    SPEED_y = 1
    current_offset_y = 0

    SPEED_x = 6
    current_offset_x = 0
    current_speed_x = 0

    NB_TILES = 8
    tiles = [] # list the tiles 
    tiles_coordinates = [] # list the coordinates
    

    current_y_loop = 0

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)

        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_down=self.on_keyboard_up)
        self.init_vertical_lines()
        self.init_horizontal_lines()
        Clock.schedule_interval(self.update, 1.0/60.0)
        self.init_tiles()
        self.generates_tiles_coordinates() 

    def is_desktop(self):
        if platform in ('linux', 'win', 'macosx'):
            return True
        else:
            return False
        
    def init_tiles(self):
        with self.canvas:
            for i in range(0, self.NB_TILES):
                self.tiles.append(Quad())

    def generates_tiles_coordinates(self):
        last_x = 0
        last_y = 0
        for i in range(len(self.tiles_coordinates) -1, -1, -1):
            if self.tiles_coordinates[i][1] < self.current_y_loop:
                del self.tiles_coordinates[i]

        if len(self.tiles_coordinates) > 0:
            last_coordinates = self.tiles_coordinates[i]
            last_x = last_coordinates[0]
            last_y = last_coordinates[1] + 1
        
        #  0 --> en avant
        #  1 --> à droite
        #  2 --> à gauche
        for i in range(len(self.tiles_coordinates), self.NB_TILES):
            r = random.randint(0, 2)
            self.tiles_coordinates.append((last_x , last_y))
            if r == 1:
                last_x += 1
                self.tiles_coordinates.append((last_x , last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x , last_y))
            elif r == 2:
                last_x -= 1
                self.tiles_coordinates.append((last_x , last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x , last_y))

            last_y += 1

    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.V_NB_LINES):
                self.Vertical_Lines.append(Line())

    def get_line_x_from_index(self, index):
        central_line_x = self.perspective_point_x
        spacing = self.V_LINES_SPACING * self.width
        offset = index - 0.5
        line_x = central_line_x + offset * spacing + self.current_offset_x
        return int(line_x)
    

    def get_line_y_from_index(self, index):
        spacing = self.H_LINES_SPACING * self.height

        line_y =  index * spacing - self.current_offset_y
        return int(line_y)

    def get_tiles_coordinates(self, tile_x, tile_y):
        tile_y = tile_y - self.current_y_loop
        x = self.get_line_x_from_index(tile_x)
        y = self.get_line_y_from_index(tile_y)
        return x, y
    
    def update_tiles(self):
        for i in range(0, self.NB_TILES):
            tile = self.tiles[i]
            tiles_coordinates = self.tiles_coordinates[i]

            xmin, ymin = self.get_tiles_coordinates(tiles_coordinates[0], tiles_coordinates[1])
            xmax, ymax = self.get_tiles_coordinates(tiles_coordinates[0] + 1, tiles_coordinates[1] + 1)
            # 2      3
            #
            # 1      4
            x1, y1 = self.transform(xmin, ymin)
            x2, y2 = self.transform(xmin, ymax)
            x3, y3 = self.transform(xmax, ymax)
            x4, y4 = self.transform(xmax, ymin)

            tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]


    def update_vertical_lines(self):
        # self.lines.points = [self.perspective_point_x, 0, self.perspective_point_x, self.height]
        # central_line_x = self.width / 2 
        # spacing = self.V_LINES_SPACING * self.width
        # offset = - int(self.V_NB_LINES / 2) + 0.5
        start_index = - int(self.V_NB_LINES / 2) + 1
        for i in range(start_index, start_index + self.V_NB_LINES):
            lines_x = self.get_line_x_from_index(i)
      
            x1, y1 = self.transform(lines_x, 0)
            x2, y2 = self.transform(lines_x, self.height)
            self.Vertical_Lines[i].points = [x1, y1, x2, y2]


    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.H_NB_LINES):
                self.horizontal_Lines.append(Line())

    def update_horizontal_lines(self):
        # central_line_x = self.width / 2 
        # spacing = self.V_LINES_SPACING * self.width
        # offset = - int(self.V_NB_LINES / 2) + 0.5
        start_index = - int(self.V_NB_LINES / 2) +1
        end_index = start_index + self.V_NB_LINES - 1

        xmin =  self.get_line_x_from_index(start_index)
        xmax = self.get_line_x_from_index(end_index)
        # spacing_y = self.H_LINES_SPACING * self.height
        for i in range(0, self.H_NB_LINES):
            lines_y = self.get_line_y_from_index(i)
            x1, y1 = self.transform(xmin, lines_y)
            x2, y2 = self.transform(xmax, lines_y)
            self.horizontal_Lines[i].points = [x1, y1, x2, y2]



    def update(self, dt):
        time_factor = dt * 60
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.current_offset_y += self.SPEED_y * time_factor
      
        spacing_y = self.H_LINES_SPACING * self.height
        if self.current_offset_y >= spacing_y:
            self.current_offset_y -= spacing_y
            self.current_y_loop += 1
            self.generates_tiles_coordinates()

        # self.current_offset_x += self.current_speed_x * time_factor
     
class GalaxyApp(App):
    pass

GalaxyApp().run()