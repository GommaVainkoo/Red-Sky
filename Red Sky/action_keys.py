from kivy.uix.relativelayout import RelativeLayout


def on_touch_down(self, touch):
    if not self.state_game and self.state_game_start:
        if touch.x < self.width / 2:
            self.change_x1 = self.speed_x
        else:
            self.change_x1 = -self.speed_x
    return super(RelativeLayout,self).on_touch_down(touch)

def on_touch_up(self, touch):
    self.change_x1 = 0

def _on_keyboard_up(self, keyboard, keycode):
    self.change_x1 = 0

def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == 'left':
        self.change_x1=self.speed_x
    elif keycode[1] == 'right':
        self.change_x1=-self.speed_x
    elif keycode[1] == 'up':
        pass
    elif keycode[1] == 'down':
        pass
    return True

def _keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    self._keyboard = None
    self._keyboard.unbind(on_key_up=self._on_keyboard_up)
    self._keyboard = None