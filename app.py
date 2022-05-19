from operator import indexOf
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
import datetime
import time

from src.constants import *

viz.setMultiSample(4)
viz.fov(80)
viz.go(viz.FULLSCREEN)
viz.collision(viz.ON)

player_picks = []

# Setup keyboard/mouse tracker
tracker = vizcam.addWalkNavigate(moveScale=2.0)
tracker.setPosition([0,1.8,0])
viz.link(tracker,viz.MainView)
viz.mouse.setVisible(True)

# Load piazza environment
piazza = viz.addChild('CityPark.osgb')
# viz.addChild('piazza_animations.osgb')

mylight = viz.addLight() 

#Set the light parameters 
mylight.position(0,10,0) 
mylight.direction(0,0,90) 
mylight.spread(180) 
mylight.intensity(20) 
mylight.spotexponent(2) 
mylight.setPosition(0,10,0) 

mylight2 = viz.addLight() 
#Set the light parameters 
mylight2.position(0,1000,0) 
mylight2.direction(0,0,90) 
mylight2.spread(180) 
mylight2.intensity(20) 
mylight2.spotexponent(2) 
mylight2.setPosition(0,1000,0)

#fn for setting game appearance
(flash_quad, status_bar, time_text, score_text, gray_effect, inventory, resultPanel) = set_appearance()

# List of hiding spots for trash_pile
trash_pile = []
recicle_bins = []

glass_trash = []
plastic_trash = []
paper_trash = []

collected_trash = []

bin_object = {}

for i in range(10):
    #Generate random values for position and orientation
    x = random.randint(-2, 2)
    z = random.randint(-5, 15)
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
    elif random_trash_peace == "CardboardBox.osgb":
        paper_trash.append(trash)
    
    trash_pile.append(trash)

for i in range(3):
    xer = i + 1

    x = xer * -2 - 2
    z = 3
    yaw = random.randint(0, 20)

    bin_type = bin_from_index(i)

    recycle_bin = viz.add(bin_type)

    recycle_bin.setPosition([x,0,z])
    recycle_bin.setEuler([yaw,0,0])

    recycle_bin.visible(False)

    if i == 0:
        bin_object["glass"] = recycle_bin
    elif i == 1:
        bin_object["paper"] = recycle_bin
    elif i == 2:
        bin_object["plastic"] = recycle_bin

    recicle_bins.append(recycle_bin)

def DisplayInstructionsTask():
    panel = vizinfo.InfoPanel(INSTRUCTIONS,align=viz.ALIGN_CENTER,fontSize=22,icon=False,key=None)
    trashClone = trash.clone(scale=[200]*3)
    trashClone.addAction(vizact.spin(0,1,0,45))
    trashClone.enable(viz.DEPTH_TEST,op=viz.OP_ROOT)
    panel.addItem(trashClone,align=viz.ALIGN_CENTER)
    yield viztask.waitKeyDown(' ')
    panel.remove()

def removeObjects():
    for trash in trash_pile:
        trash.visible(False)

    for recycle_bin in recicle_bins:
        recycle_bin.visible(False)

def showResults():
    if len(collected_trash) >= 9:
        resultPanel.setText(RESULTS)
        resultPanel.visible(True)
        removeObjects()

def DisplayInventory():
    if len(player_picks) < 1:
        inventory.message("")
    else:
        item = player_picks[0]

        item_type = ""

        if item in plastic_trash:
            item_type = "plastmasas"
        elif item in glass_trash:
            item_type = "stikla"
        elif item in paper_trash:
            item_type = "papīra"

        inventory.message(PICKED_TRASH.format(item_type))

    if len(collected_trash) >= 9:
        showResults()

def dropTrash(object):
    player_picks.pop()
    collected_trash.append(object)

    DisplayInventory()

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
            dropTrash(object)
        elif player_pic in plastic_trash and object == plastic_bin:
            dropTrash(object)
        elif player_pic in paper_trash and object == paper_bin:
            dropTrash(object)

    elif object in trash_pile and len(player_picks) < 1:
        player_picks.append(object)
        object.visible(False)

    DisplayInventory()

vizact.onmousedown(viz.MOUSEBUTTON_LEFT, func=pickTrash)

def MainTask():
    # Display instructions and wait for key press to continue
    yield DisplayInstructionsTask()

    # Go through each position
    for trash in trash_pile:
        trash.visible(True)

    for recycle_bin in recicle_bins:
        recycle_bin.visible(True)

viztask.schedule( MainTask() )