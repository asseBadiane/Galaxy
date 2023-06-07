
from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '500')

from kivy.core.window import Window
import platform
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line, Quad, Triangle
from kivy.properties import Clock

import random
from kivy.lang.builder import Builder
from kivy.uix.relativelayout import RelativeLayout

Builder.load_file("menu.kv")
class MainWidget(RelativeLayout):
    from transforms import transform, transform_2D, transform_perspective
    from users_actions import keyboard_closed, on_keyboard_down, on_keyboard_up, on_touch_down, on_touch_up

    menu_widget = ObjectProperty()
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    V_NB_LINES = 8 # numbers the lines vertical
    V_LINES_SPACING = .4 # spaces between vertical lines
    Vertical_Lines = [] # list the lines vertical

    H_NB_LINES = 8  # numbers the lines horizontal
    H_LINES_SPACING = .15  # spaces between horizontal lines
    horizontal_Lines = [] # list the lines horizontal

    SPEED_y = .8 # speed vertically (y)
    current_offset_y = 0 # current offset y

    SPEED_x = 3.5 # speed horizontally (x)
    current_offset_x = 0 # current offset x
    current_speed_x = 0 # current speed x

    NB_TILES = 8 # numbers the tiles
    tiles = [] # list the tiles 
    tiles_coordinates = [] # list the tiles coordinates
    
    current_y_loop = 0 # current y loop

    SHIP_WIDTH = .1 # width of the ship
    SHIP_HEIGHT = 0.035 # height of the ship
    SHIP_BASE_Y = 0.04 # position 1 y of the ship
    SHIP = None # The ship
    ships_coordinates = [(0, 0), (0, 0), (0, 0)] # The coordinates of the 3 corners of the ship

    state_game_over = False
    state_game_has_started = False


    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)

        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)
        self.init_vertical_lines()
        self.init_horizontal_lines()
        
        self.init_tiles()
        self.init_ship()
        self.pre_fill_tiles_coordinates()
        self.generates_tiles_coordinates() 
        Clock.schedule_interval(self.update, 1.0/60.0)

    # Check if the device is a desktop
    def is_desktop(self):
        if platform in ('linux', 'win', 'macosx'):
            return True
        else:
            return False
        
    # Initialize the ship   
    def init_ship(self):
        with self.canvas:
            Color(0, 0, 0)
            self.SHIP = Triangle()

    # Update the ship 
    def update_ship(self):
        center_x = self.width / 2
        base_y = self.SHIP_BASE_Y * self.height
        half_width = self.SHIP_WIDTH * self.width / 2
        ship_height = self.SHIP_HEIGHT * self.height

        self.ships_coordinates[0] = (center_x - half_width, base_y)
        self.ships_coordinates[1] = (center_x , base_y + ship_height)
        self.ships_coordinates[2] = (center_x + half_width, base_y)
        
        x1, y1 = self.transform(*self.ships_coordinates[0])
        x2, y2 = self.transform(*self.ships_coordinates[1])
        x3, y3 = self.transform(*self.ships_coordinates[2])

        self.SHIP.points = [x1, y1, x2, y2, x3, y3]

    # is the ship still on course
    def check_ship_collision(self):
        for i in range(0, len(self.tiles_coordinates)):
            ti_x, ti_y = self.tiles_coordinates[i]
            if ti_y > self.current_y_loop + 1:
                return False
            if self.check_ship_collision_with_tiles(ti_x, ti_y):
                return True
        return False
        
    
    # If one of the 3 points of the ship is in the tiles
    def check_ship_collision_with_tiles(self, tile_x, tile_y):
        xmin, ymin = self.get_tiles_coordinates(tile_x, tile_y)
        xmax, ymax = self.get_tiles_coordinates(tile_x + 1, tile_y + 1)

        for i in range(0, 3):
            px, py = self.ships_coordinates[i]
            if xmin <= px <= xmax  and  ymin <= py <= ymax:
                return True
            
        return False
        
    # Initialize the tiles
    def init_tiles(self):
        with self.canvas:
            for i in range(0, self.NB_TILES):
                self.tiles.append(Quad())

    #  Initialize the 10 tiles cooordinates
    def pre_fill_tiles_coordinates(self):
        with self.canvas:
            for i in range(0, 10):
                self.tiles_coordinates.append((0, i))

    # Add, update and remove tiles coordinates
    def generates_tiles_coordinates(self):
        last_x = 0
        last_y = 0

        # Delete tile coordinates, already off screen
        for i in range(len(self.tiles_coordinates) -1, -1, -1):
            if self.tiles_coordinates[i][1] < self.current_y_loop:
                del self.tiles_coordinates[i]

        # Add a new tile coordinates at the end
        # Ex: si le derniere element est 0.3, on fait 0.3 + 1 qui fait 0.4
        if len(self.tiles_coordinates) > 0:
            last_coordinates = self.tiles_coordinates[-1]
            last_x = last_coordinates[0]
            last_y = last_coordinates[1] + 1

        # Which side generates new left or right tile coordinates
        for i in range(len(self.tiles_coordinates), self.NB_TILES):
            r = random.randint(0, 2)
            #  0 --> en avant
            #  1 --> à droite
            #  2 --> à gauche
            start_index = - int(self.V_NB_LINES / 2) + 1
            end_index = start_index + self.V_NB_LINES - 1
         
            if last_x <= start_index:
                r = 1
            if last_x >= end_index:
                r = 2

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

  
    # get row of x from index
    def get_line_x_from_index(self, index):
        central_line_x = self.perspective_point_x
        spacing = self.V_LINES_SPACING * self.width
        offset = index - 0.5
        line_x = central_line_x + offset * spacing + self.current_offset_x
        return int(line_x)
    
    # get row of y from index
    def get_line_y_from_index(self, index):
        spacing = self.H_LINES_SPACING * self.height
        line_y =  index * spacing - self.current_offset_y
        return int(line_y)

    # Get x and y coordinates
    def get_tiles_coordinates(self, tile_x, tile_y):
        tile_y = tile_y - self.current_y_loop
        x = self.get_line_x_from_index(tile_x)
        y = self.get_line_y_from_index(tile_y)
        return x, y
    
    # Update tiles
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

    # Create vertical lines
    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.V_NB_LINES):
                self.Vertical_Lines.append(Line())

    # Update vertical lines
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

    # Create horizontal lines
    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.H_NB_LINES):
                self.horizontal_Lines.append(Line())

    # Update horizontal lines
    def update_horizontal_lines(self):
        # central_line_x = self.width / 2 
        # spacing = self.V_LINES_SPACING * self.width
        # offset = - int(self.V_NB_LINES / 2) + 0.5
        start_index = - int(self.V_NB_LINES / 2) + 1 # here it is -3, if the V_NB_LINES is 8
        end_index = start_index + self.V_NB_LINES - 1 # here it is 4

        xmin =  self.get_line_x_from_index(start_index)
        xmax = self.get_line_x_from_index(end_index)
        # spacing_y = self.H_LINES_SPACING * self.height
        for i in range(0, self.H_NB_LINES):
            lines_y = self.get_line_y_from_index(i)
            x1, y1 = self.transform(xmin, lines_y)
            x2, y2 = self.transform(xmax, lines_y)
            self.horizontal_Lines[i].points = [x1, y1, x2, y2]


    # Updates the fontions
    def update(self, dt):
        time_factor = dt * 60
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.update_ship()

        if not self.state_game_over and self.state_game_has_started:
            speed_y = self.SPEED_y * self.height / 100
            self.current_offset_y += speed_y * time_factor
        
            spacing_y = self.H_LINES_SPACING * self.height
            while self.current_offset_y >= spacing_y:
                self.current_offset_y -= spacing_y
                self.current_y_loop += 1
                self.generates_tiles_coordinates()

            speed_x = self.current_speed_x * self.height / 100
            self.current_offset_x += speed_x * time_factor

        if not self.check_ship_collision() and not self.state_game_over:
            self.state_game_over = True
            self.menu_widget.opacity = 1
            print("GAME OVER")

    def on_menu_button_pressed(self):
        # print("button pressed")
        self.state_game_has_started = True
        self.menu_widget.opacity = 0



class GalaxyApp(App):
    pass

GalaxyApp().run()