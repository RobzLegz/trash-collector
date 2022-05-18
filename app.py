﻿from operator import indexOf
import viz
import vizact
import vizcam
import vizinfo
import viztask
import vizproximity
import vizfx.postprocess
from vizfx.postprocess.color import GrayscaleEffect
from vizfx.postprocess.composite import BlendEffect

# from src.pick import *
from src.utils.randomiseTrash import get_random_trash
from src.utils.getBinFromIndex import bin_from_index
from src.apearance import set_appearance
from src.text import *

import math
import random

from src.constants import *

SCORE = 0
viz.setMultiSample(4)
viz.fov(80)
viz.go(viz.FULLSCREEN)
viz.collision(viz.ON)

player_picks = []

# Setup directional light
viz.MainView.getHeadLight().disable()
sky_light = viz.addDirectionalLight(euler=(0,20,0))
sky_light.color(viz.WHITE)
sky_light.ambient([0.8]*3)
viz.setOption('viz.lightModel.ambient',[0]*3)

# Setup keyboard/mouse tracker
tracker = vizcam.addWalkNavigate(moveScale=2.0)
tracker.setPosition([0,1.8,0])
viz.link(tracker,viz.MainView)
viz.mouse.setVisible(True)

# Load piazza environment
piazza = viz.addChild('piazza.osgb')
viz.addChild('piazza_animations.osgb')

# Swap out sky with animated sky dome
piazza.getChild('pz_skydome').remove()
day = viz.add('sky_day.osgb')

# Add avatar sitting on a bench
male = viz.addAvatar('vcc_male2.cfg',pos=(-6.5,0,13.5),euler=(90,0,0))
male.state(6)

#fn for setting game appearance
(flash_quad, status_bar, time_text, score_text, gray_effect) = set_appearance()

# List of hiding spots for trash_pile
trash_pile = []
recicle_bins = []

glass_trash = []
plastic_trash = []
paper_trash = []

bin_object = {}

for i in range(10):
    #Generate random values for position and orientation
    x = random.randint(-10, 10)
    z = random.randint(-7, 7)
    yaw = random.randint(0,360)

    #Load a trash
    random_trash_peace = get_random_trash()

    trash = viz.add(random_trash_peace)

    trash.setPosition([x,0,z])
    trash.setEuler([yaw,0,0])

    trash.visible(False)

    if random_trash_peace == "Bottle.osgb":
        plastic_trash.append(trash)
    elif random_trash_peace == "GlassBottle.osgb":
        glass_trash.append(trash)
    
    trash_pile.append(trash)

for i in range(3):
    x = i * 3
    z = 0
    yaw = random.randint(0,360)

    bin_type = bin_from_index(i)

    recycle_bin = viz.add(bin_type)

    recycle_bin.setPosition([x,0,z])
    recycle_bin.setEuler([yaw,0,0])

    recycle_bin.visible(False)

    if i == 0:
        bin_object["glass"] = recycle_bin
    elif i == 1:
        bin_object["plastic"] = recycle_bin
    elif i == 2:
        bin_object["paper"] = recycle_bin

    recicle_bins.append(recycle_bin)

def DisplayInstructionsTask():
    """Task that display instructions and waits for keypress to continue"""
    panel = vizinfo.InfoPanel(INSTRUCTIONS,align=viz.ALIGN_CENTER,fontSize=22,icon=False,key=None)
    trashClone = trash.clone(scale=[200]*3)
    trashClone.addAction(vizact.spin(0,1,0,45))
    trashClone.enable(viz.DEPTH_TEST,op=viz.OP_ROOT)
    panel.addItem(trashClone,align=viz.ALIGN_CENTER)
    yield viztask.waitKeyDown(' ')
    panel.remove()

# def UpdateScore():
#     """Update score text"""
#     score = 10 - len(trash_pile)

#     score_text.message('Found: {} / {}'.format(score, TRIAL_COUNT))

def pickTrash():
    object = viz.pick()

    if object == viz.VizChild(5) or not object.valid():
        return

    if object in recicle_bins and len(player_picks) == 1:
        glass_bin = bin_object['glass']
        plastic_bin = bin_object['plastic']
        paper_bin = bin_object['paper']

        player_pic = player_picks[0]

        if player_pic in glass_trash and object == glass_bin:
            player_picks.pop()
        elif player_pic in plastic_trash and object == plastic_bin:
            player_picks.pop()
        elif player_pic in paper_trash and object == paper_bin:
            player_picks.pop()

    elif object in trash_pile and len(player_picks) < 1:
        player_picks.append(object)
        object.visible(False)

vizact.onmousedown(viz.MOUSEBUTTON_LEFT, func=pickTrash)

def MainTask():
    # Display instructions and wait for key press to continue
    yield DisplayInstructionsTask()

    # Create panel to display trial results
    resultPanel = vizinfo.InfoPanel('',align=viz.ALIGN_CENTER,fontSize=25,icon=False,key=None)
    resultPanel.visible(False)

    # Go through each position
    for trash in trash_pile:
        trash.visible(True)

    for recycle_bin in recicle_bins:
        recycle_bin.visible(True)
        
    # UpdateScore(SCORE)

    if len(trash_pile) == 0:
        resultPanel.setText(RESULTS.format(SCORE, TRIAL_COUNT))
        resultPanel.visible(True)
        yield viztask.waitKeyDown(' ')
        resultPanel.visible(False)

viztask.schedule( MainTask() )