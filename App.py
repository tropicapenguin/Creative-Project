# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 11:12:50 2022

@author: rgerritsen
"""
from kivy.clock import Clock
from kivy.app import App
from kivy.lang import Builder
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.uix.widget import Widget
from PIL import Image
import imagehash

from kivy.uix.screenmanager import ScreenManager, Screen

class Global():
    TrialNum = 0
    status = False

class MainWindow(Screen):
    pass

class SecondWindow(Screen):
    
    def __init__(self, **kwargs):
        super(SecondWindow, self).__init__(**kwargs)
        
    def on_enter(self, **kwargs):
        Clock.schedule_once(self.Next, 20)
        with self.canvas:
            Color(.2, .5, .5)
            Rectangle(pos=self.pos, size=self.size)
        
    def Next(self, arg):
        self.manager.current = 'three'
        Clock.schedule_once(self.export, 1)
        
    # On mouse press how Paint_brush behave
    def on_touch_down(self, touch):
        with self.canvas:
            Color(0, 1, 1)
            d = 3.
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y))
        
    # On mouse movement how Paint_brush behave
    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]
        
    def export(self, dt):
        name = 'ImageTrial'+str(Global.TrialNum)+'.png'
        self.export_as_image().save(name)
        
class ThirdWindow(Screen):
    def on_enter(self, **kwargs):
        #print(Global.TrialNum)
        Clock.schedule_once(compare, 2)
        Clock.schedule_once(self.Next, 10)
        
    def Next(self, arg):
        self.manager.current = 'main'
        Global.TrialNum += 1
        
        
#class MainManager(ScreenManager):
#    pass

kv = Builder.load_file("my.kv")

#MainManager.add_widget(MainWindow(name='main'))
#MainManager.add_widget(SecondWindow(name='second'))
#MainManager.add_widget(ThirdWindow(name='three'))

class MyMainApp(App):
    def build(self):
        MainManager = ScreenManager()
        MainManager.add_widget(MainWindow(name='main'))
        MainManager.add_widget(SecondWindow(name='second'))
        MainManager.add_widget(ThirdWindow(name='three'))
        return MainManager
        
def endtrial():
    MyMainApp.get_running_app().stop()
    #print('worked')
'''
the comparing function for between the images
'''
def compare(dt):
    if Global.TrialNum > 0:
        hash1 = imagehash.average_hash(Image.open('ImageTrial'+str(Global.TrialNum-1)+'.png'))
        hash2 = imagehash.average_hash(Image.open('ImageTrial'+str(Global.TrialNum)+'.png'))
        similarity = hash1 - hash2
        Global.status = True
        print(similarity)
    else:
        print('Nothing to compare')
if __name__== "__main__":
    MyMainApp().run()