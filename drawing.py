# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 14:49:21 2022

@author: rgerritsen
"""

# Program to explain how to create drawing App in kivy
	
# import kivy module	
import kivy
	
# base Class of your App inherits from the App class.	
# app:always refers to the instance of your application
from kivy.app import App
	
# this restrict the kivy version i.e
# below this kivy version you cannot
# use the app or software
kivy.require('1.9.0')

# Widgets are elements of a
# graphical user interface that
# form part of the User Experience.
from kivy.uix.widget import Widget

from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen

# This layout allows you to set relative coordinates for children.
from kivy.uix.relativelayout import RelativeLayout

class First(RelativeLayout):
    pass

class windowManager(ScreenManager):
    pass

# Create the Widget class
class Paint_brush(Widget):
	pass

'''
def __init__(self, kwargs):
        super(Touch,self).__init__(**kwargs)
        
        with self.canvas:
            self.rect
'''

class button(Button):
    def __init__(self, **kwargs):
        super(button,self).__init__(**kwargs)
        self.text="you can't read"
        self.pos = (100,100)
        self.size_hint = (.8,.8)

# Create the layout class
# where you are defining the working of
# Paint_brush() class
class Drawing(RelativeLayout):

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

# Create the App class	
class DrawingApp(App):
	def build(self):
		return Drawing()

DrawingApp().run()
