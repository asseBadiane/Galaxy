from kivy.uix.relativelayout import RelativeLayout


class MenuWidget(RelativeLayout):
    
    # keyboard keys will have no effect when the game is stopped
    def on_touch_down(self, touch):
        if self.opacity == 0:
            return False

        return super(RelativeLayout, self).on_touch_down(touch)
