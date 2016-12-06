# Created by: Mr. Coxall
# Created on: Sep 2016
# Created for: ICS3U
# This program is the first file in a multi-scene game template
#    This template is meant to be used with the Xcode template,
#    to make apps for the App Store.
#
# Originally from: Ole Zorn, from the Xcode template
# for use with https://github.com/omz/PythonistaAppTemplate
# Also from the Pythonista community forum.
#
# This file creates the UIView that will be used by Xcode,
#  then creates the scene inside it. once everything is ready
#  to go, the scene transitions immediately to the first scene.
# It is assumed you bring along all your assets, 
#   and not use any of the mornal ones built into Pythonista.
#
# To exit the app in Pythonista, pull down with 2 fingers.

from scene import *
import ui

from splash_scene import *


#  ..use when deploying app for Xcode and the App Store
main_view = ui.View()
scene_view = SceneView(frame = main_view.bounds, flex = 'WH')
main_view.add_subview(scene_view)
scene_view.scene = SplashScene()
main_view.present(hide_title_bar = True, animated = False)
