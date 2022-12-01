# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 11:12:50 2022

@author: rgerritsen
"""
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.app import App
from kivy.lang import Builder
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.uix.widget import Widget
from PIL import Image
import numpy
import imagehash
from sewar.full_ref import mse, rmse, psnr, uqi, ssim, ergas, scc, rase, sam, msssim, vifp
import RPi.GPIO as GPIO

from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
Window.fullscreen = "auto"


GPIO.setmode(GPIO.BOARD)
GPIO.setup(18,GPIO.IN)

Data = []

sound = SoundLoader.load('ding.mp3')

class Global():
    TrialNum = 0
    status = False
    feedback = False
    

class MainWindow(Screen):
    def on_enter(self, args):
        GPIO.setup(18,GPIO.IN)
        Clock.schedule_interval(self.received)
    def received(self, arg):
        if GPIO.input(18):
            #monitor pin for signal from feeder
            GPIO.cleanup()
            self.Next()
    def Next(self, arg):
        self.manager.current = 'second'
        

class SecondWindow(Screen):
    
    def __init__(self, **kwargs):
        super(SecondWindow, self).__init__(**kwargs)
        
    def on_enter(self, **kwargs):
        Clock.schedule_once(self.Next, 20)
        sound.play()
        with self.canvas:
            Color(0, 0, 0)
            Rectangle(pos=self.pos, size=self.size)
        
    def Next(self, arg):
        self.manager.current = 'three'
        Clock.schedule_once(self.export, 1)
        
    # On mouse press how Paint_brush behave
    def on_touch_down(self, touch):
        Global.feedback = True
        with self.canvas:
            Color(1, 1, 1)
            d = 4.
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
        if Global.feedback == True:
            GPIO.setup(18,GPIO.OUT)
            GPIO.output(18,GPIO.HIGH)
            #send signal to feeder to feed
        Clock.schedule_once(compare, 2)
        Clock.schedule_once(self.Next, 10)
        
    def Next(self, arg):
        GPIO.cleanup()
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
        MainManager = ScreenManager(transition=NoTransition())
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
    if Global.TrialNum == 0:
        print("First trial has nothing to compare to so reward for interacting")
    else:
        pic1 = Image.open('ImageTrial'+str(Global.TrialNum-1)+'.png')
        img1 = numpy.array(pic1)
        pic2 = Image.open('ImageTrial'+str(Global.TrialNum)+'.png')
        img2 = numpy.array(pic2)
        print(mse(img1,img2))
        print(rmse(img1,img2))
        print(psnr(img1,img2))
        print(ssim(img1,img2))
        print(uqi(img1,img2))
        print(ergas(img1,img2))
        print(scc(img1,img2))
        print(rase(img1,img2))
        print(sam(img1,img2))
        print(vifp(img1,img2))
        Global.status = True
    
if __name__== "__main__":
    MyMainApp().run()