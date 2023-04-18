from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Line, Color, Quad, Triangle
from kivy.properties import NumericProperty, Clock, ObjectProperty, StringProperty
from kivy import platform
from kivy.lang import Builder
from kivy.core.audio import SoundLoader
from kivy.uix.relativelayout import RelativeLayout
Builder.load_file("menu.kv")

class MainWidget(RelativeLayout):

    from transforms import transform,transform_2D,transform_prespective
    from action_keys import on_touch_up,on_touch_down,_on_keyboard_down,_on_keyboard_up,_keyboard_closed
    from tiles import get_tile_cordinates,update_tile,generate_tiles
    main_menu=ObjectProperty()
    line1 = None
    no_lines=10
    lines_spacing=.25
    verical_lines=[]
    line2 = None
    no_lines_h=15
    lines_spacing_h=.1
    horzontal_lines=[]
    speed=0.6
    change=0
    speed_x=2.5
    change_x=0
    change_x1=0
    Tile=[]
    tiles_cord=[]
    no_tiles=16
    loop_no=0
    Ship=None
    ship_width=0.1
    ship_height=0.035
    ship_base=0.04
    ship_cord=[(0,0),(0,0),(0,0)]
    state_game=False
    state_game_start=False
    score_text1=StringProperty("")
    title_menu=StringProperty("R  E  D     S  K  Y")
    button_name = StringProperty("S T A R T")
    score_text=StringProperty("")
    sound1=None
    sound1 = None
    sound2 = None
    sound3 = None
    sound4 = None
    sound5 = None
    sound6 = None
    check=15
    def __init__(self,**kwargs):
        super(MainWidget,self).__init__(**kwargs)
        self.vertical_lines()
        self.horizontal_lines()
        self.tiles()
        self.ship()
        self.sound_track()
        self.reset()
        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
            self._keyboard.bind(on_key_down=self._on_keyboard_down)
            self._keyboard.bind(on_key_up=self._on_keyboard_up)
        Clock.schedule_interval(self.update, 1.0 / 60.0)


    def score(self):
        self.current_score=self.loop_no*10
        self.score_text=("Score: "+str(self.current_score))


    def sound_track(self):
        self.sound1 = SoundLoader.load("RESOURCES/audio/begin.wav")
        self.sound2 = SoundLoader.load("RESOURCES/audio/galaxy.wav")
        self.sound3 = SoundLoader.load("RESOURCES/audio/gameover_impact.wav")
        self.sound4 = SoundLoader.load("RESOURCES/audio/gameover_voice.wav")
        self.sound5 = SoundLoader.load("RESOURCES/audio/music1.wav")
        self.sound6 = SoundLoader.load("RESOURCES/audio/restart.wav")
        self.sound1.volume=0.2
    def reset(self):

        self.change = 0
        self.change_x = 0
        self.loop_no = 0
        self.change_x1 = 0
        self.speed=0.6
        self.tiles_cord=[]
        self.score_text="Score : 0"
        self.starting_game()
        self.generate_tiles()
        self.state_game=False
    def is_desktop(self):
        if platform in('linux','win','macosx'):
            return True

    def cordinates(self):
        self.x_cor=NumericProperty(0)
        self.y_cor = NumericProperty(0)


    def vertical_lines(self):
        with self.canvas:
            Color(0,0,0,.8)
            for i in range(0,self.no_lines):
                self.verical_lines.append(Line())

    def horizontal_lines(self):
        with self.canvas:
            Color(0,0,0,.8)
            for i in range(0,self.no_lines_h):
                self.horzontal_lines.append(Line())
    def tiles(self):
        with self.canvas:
            Color(0,0,0,0.8)
            for i in range(0,self.no_tiles):
                self.Tile.append(Quad())

    def ship(self):
        with self.canvas:
            Color(1,1,1,0.5)
            self.Ship=Triangle()
    def starting_game(self):
        last_y = 0
        last_x = 0
        for i in range(0, 10):
            self.tiles_cord.append((last_x, last_y))
            last_y += 1
    def start_index_x(self,index):
        central_line=self.x_cor
        spacing=self.lines_spacing*self.width
        offset=index-0.5
        line_x = (central_line + offset * spacing) + self.change_x
        return line_x

    def start_index_y(self, index):
        spacing = self.height * self.lines_spacing_h
        line_x = (index * spacing) - self.change
        return line_x

    def update_line_verical(self):
        start_index=-int(self.no_lines/2)+1
        for i in range(start_index,start_index+self.no_lines):
            line_x=self.start_index_x(i)
            x1,y1=self.transform(line_x,0)
            x2,y2=self.transform(line_x,self.height)
            self.verical_lines[i].points=[x1,y1,x2,y2]
    def update_line_horizontal(self):

        start_index = -int(self.no_lines / 2) + 1
        xmin=self.start_index_x(start_index)
        xmax=self.start_index_x(start_index+self.no_lines-1)
        start_index_1=self.no_lines_h
        for i in range(0, start_index_1):

            x1, y1 = self.transform(xmin,self.start_index_y(i))
            x2, y2 = self.transform(xmax,self.start_index_y(i))
            self.horzontal_lines[i].points = [x1, y1, x2, y2]


    def update_Ship(self):
        center_x=self.width/2
        base_y=self.ship_base*self.height
        ship_half_width=self.ship_width*self.width/2
        self.ship_cord[0]=(center_x-ship_half_width,base_y)
        self.ship_cord[1] = (center_x,base_y + (self.ship_height * self.height))
        self.ship_cord[2] = (center_x + ship_half_width, base_y)
        x1,y1=self.transform(*self.ship_cord[0])
        x2,y2=self.transform(*self.ship_cord[1])
        x3,y3 = self.transform(*self.ship_cord[2])

        self.Ship.points=[x1,y1, x2,y2, x3,y3]
    def check_tile_collision_with_tile(self,tx1,ty1):
        xmin,ymin=self.get_tile_cordinates(tx1,ty1)
        xmax,ymax=self.get_tile_cordinates(tx1+1,ty1+1)
        for i in range(0,3):
            px,py=self.ship_cord[i]
            if xmin<= px <=xmax and ymin<= py <=ymax :
                return True

        return False

    def check_tile_collision(self):
        for i in range(0,len(self.tiles_cord)):
            tx1,ty1=self.tiles_cord[i]
            if ty1 > self.loop_no+1:
                return False
            if self.check_tile_collision_with_tile(tx1,ty1):
                return True
        return False

    def Speed_increase(self):
        if(self.loop_no>self.check):
            self.speed+=.0001
            check=self.loop_no+25

    def update(self,dt):
        time_factor = dt * 60
        self.update_line_verical()
        self.update_line_horizontal()
        self.update_tile()
        self.update_Ship()

        self.Speed_increase()
        if not self.state_game and self.state_game_start:
            self.score()
            speed_y=self.speed*self.height/100
            speed_x = self.change_x1 * self.width/ 100
            self.change+=speed_y*time_factor
            self.change_x+=speed_x*time_factor
            spacing=self.lines_spacing_h*self.height
    
            if self.change >= spacing:
                self.change-=spacing
                self.loop_no += 1
                self.generate_tiles()

        if not self.check_tile_collision() and not self.state_game:
            self.score_text =""
            self.score_text1=("SCORE: "+str(self.current_score))
            self.title_menu="G  A  M  E    O  V  E  R"
            self.button_name="R E S T A R T"
            self.state_game=True
            self.main_menu.opacity = 1
            self.sound3.play()
            self.sound5.stop()
            Clock.schedule_once(self.game_over_voice,3)

    def game_over_voice(self,dt):
        if self.state_game:
            self.sound4.play()
    def on_start_button_pressed(self):
        print("Its working")
        if self.state_game:
            self.sound6.play()
        else:
            self.sound1.play()
        self.reset()
        self.state_game_start=True
        self.main_menu.opacity=0
        self.sound5.play()

class Red_SkyApp(App):
    pass

Red_SkyApp().run()