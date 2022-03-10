# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 11:12:50 2022

@author: rgerritsen
"""
from kivy.clock import Clock
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line
from kivy.uix.screenmanager import ScreenManager, Screen


class MainWindow(Screen):
    pass

class SecondWindow(Widget):
        
    def on_enter(self, **kwargs):
        Clock.schedule_once(self.Next, 200)

    def Next(self):
        self.manager.current = 'three'
        
    # On mouse press how Paint_brush behave
    def on_touch_down(self, touch):
        with self.canvas:
            Color(1, 1, 0)
            d = 30.
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y))
        
    # On mouse movement how Paint_brush behave
    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]
     
class ThirdWindow(Screen):
    def on_enter(self, args):
        Clock.schedule_once(self.Next, 10)

    def Next(self):
        self.manager.current = 'main'
        
class MainManager(ScreenManager):
    pass
'''
class Paint_brush(Widget):
    pass
'''

kv = Builder.load_file("my.kv")

class MyMainApp(App):
    def build(self):
        return kv
    
def endtrial():
    MyMainApp.get_running_app().stop()
    #print('worked')
    
if __name__== "__main__":
    MyMainApp().run()
    
'''
# On mouse press how Paint_brush behave
    def on_touch_down(self, touch):
        pb = Paint_brush()
        pb.center = touch.pos
        self.add_widget(pb)
        
    # On mouse movement how Paint_brush behave
    def on_touch_move(self, touch):
        pb = Paint_brush()
        pb.center = touch.pos
        self.add_widget(pb)
'''

## whats in the kivy
'''
<Paint_brush>:
    size_hint: None, None
    size: 1, 1
    canvas:
        Color:
            rgb: 0, 0, 1
        Ellipse:
            pos: self.x, self.y
'''