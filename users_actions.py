def keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_keyboard_down)
        self._keyboard.unbind(on_key_up=self.on_keyboard_up)
        self._keyboard = None

# Define left and right keys / version 1
def on_touch_down(self, touch):
    if touch.x < self.width / 2:
        self.current_speed_x = self.SPEED_x
    else:
        self.current_speed_x = -self.SPEED_x
# Stop / version 1
def on_touch_up(self, touch):
    self.current_speed_x = 0

# Define left and right keys / versions search
def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode.x < self.width / 2:
        # print("left")
        self.current_speed_x = self.SPEED_x
    else:
        # print("right")
        self.current_speed_x = -self.SPEED_x
    return True

# Stop / versions search
def on_keyboard_up(self, keyboard, keycode):
    self.current_speed_x = 0
    return True