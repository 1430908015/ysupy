import math
from contextlib import nullcontext

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.vector import Vector
import random
import main as Local


class Ball(Widget):
    def __init__(self, kind, pos, velocity, radius, **kwargs):
        super().__init__(**kwargs)
        self.color="green"
        self.kind=kind
        self.pos = pos
        self.velocity = velocity
        self.radius = radius

    def on_touch_down(self,touch):
        print("a")
    def setColor(self,color):
        self.color=color

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PhysicsWidget(Widget):
    def addBall(self,kind, pos, velocity, radius, **kwargs):
        ball=Ball(kind, pos, velocity, radius, **kwargs)
        self.add_widget(ball)
        ball.color = Local.种类颜色表["none"]
        with self.canvas:
            Color(*ball.color)
            ball.ellipse = Ellipse(pos=Vector(self.move[0] + self.rate * ball.pos[0] + Window.width / 2,
                                              self.move[1] + self.rate * ball.pos[1] + Window.height / 2),
                                   size=Vector(2 * ball.radius * self.rate, 2 * ball.radius * self.rate))

    def __init__(self, **kwargs):
        self.rate = 1.0
        self.move = (0.0, 0.0)
        super().__init__(**kwargs)
        self.leftmode = 0
        self.damping =  Local.阻尼  # 速度阻尼

        # 创建5个小球
        colors = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1), (1, 1, 0, 1), (1, 0, 1, 1)]
        for _ in range(2000):
            radius = random.randint(2, 10)
            pos = (random.randint(-1000,1000),
                   random.randint(-1000,1000))
            velocity = Vector(random.uniform(-5, 5), random.uniform(-5, 5))
            self.addBall("null",pos, velocity, radius)


    def update(self, dt):
        # 更新所有小球的位置和速度
        for ball in self.children:


            # 应用速度阻尼
            ball.velocity *= self.damping

            # 更新位置
            ball.move()


    def rend(self,dt):
        for ball in self.children:
            ball.ellipse.pos =Vector(self.move[0]+self.rate*ball.pos[0]+Window.width/2-ball.radius*self.rate,self.move[1]+self.rate*ball.pos[1]+Window.height/2-ball.radius*self.rate)


    def rerend_size(self):
        self.canvas.clear()
        for ball in self.children:


            with (self.canvas):
                Color(*ball.color)
                #s = move+rate*r + w/2
                #r = (-move - w/2 + s)/rate
                ball.ellipse = Ellipse(pos=Vector(self.move[0]+self.rate*ball.pos[0]+Window.width/2-ball.radius*self.rate,self.move[1]+self.rate*ball.pos[1]+Window.height/2-ball.radius*self.rate), size=Vector(2*ball.radius*self.rate,2*ball.radius*self.rate))

    def scan_to_phy(self, pos):
        return Vector((-self.move[0] - Window.width / 2.0 + pos[0]) / self.rate, (-self.move[1] - Window.height / 2.0 + pos[1]) / self.rate)


    def on_touch_move(self, touch):
        if touch.button == "left":
            ball=self.sellect
            if type(ball) == Ball:
                ball.pos = self.scan_to_phy(Vector(touch.x,touch.y))


    def on_touch_up(self, touch):
        if touch.button == "left":
            print("end")

    def on_touch_down(self, touch):
        pos = self.scan_to_phy(touch.pos)
        if touch.button == "left":
            self.leftmode = 0
            self.sellect = 0
            for ball in self.children:
                if math.sqrt((pos[0] - ball.pos[0])**2+(pos[1]- ball.pos[1])**2) <= ball.radius:
                    self.sellect = ball


        if touch.is_mouse_scrolling:
            if touch.button == 'scrolldown':
                self.rate *= 1.2
                self.rerend_size()
            elif touch.button == 'scrollup':
                self.rate *= 0.8
                self.rerend_size()




class MainWindow(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.window = PhysicsWidget()
        Clock.schedule_interval(self.window.update, 1.0 / 60.0)
        Clock.schedule_interval(self.window.rend, 1.0 / 200.0)
        self.add_widget(self.window)

class PhysicsApp(App):
    def build(self):
        mw = MainWindow()
        return mw


def phy_start():
    PhysicsApp().run()



