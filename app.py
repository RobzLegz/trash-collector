import viz
import vizact
import vizcam
import vizinfo
import viztask
import vizproximity
import vizfx.postprocess
from vizfx.postprocess.color import GrayscaleEffect
from vizfx.postprocess.composite import BlendEffect

from src.apearance import set_appearance
from src.text import *

import math
import random

from src.constants import TRIAL_COUNT, TRIAL_DURATION, TRIAL_DELAY, PROXIMITY_RADIUS, FLASH_TIME

viz.setMultiSample(4)
viz.fov(60)
viz.go(viz.FULLSCREEN)

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
viz.mouse.setVisible(False)

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

# List of hiding spots for pigeons
pigeons = []

for i in range(10):
    #Generate random values for position and orientation
    x = random.randint(-10, 10)
    z = random.randint(-7, 7)
    yaw = random.randint(0,360)

    #Load a pigeon
    pigeon = viz.addAvatar('pigeon.cfg')

    #Set position, orientation, and state
    pigeon.setPosition([x,0,z])
    pigeon.setEuler([yaw,0,0])
    pigeon.state(1)

    pigeon.visible(False)

    #Append the pigeon to a list of pigeons
    pigeons.append(pigeon)

def DisplayInstructionsTask():
    """Task that display instructions and waits for keypress to continue"""
    panel = vizinfo.InfoPanel(INSTRUCTIONS,align=viz.ALIGN_CENTER,fontSize=22,icon=False,key=None)
    pigeonClone = pigeon.clone(scale=[200]*3)
    pigeonClone.addAction(vizact.spin(0,1,0,45))
    pigeonClone.enable(viz.DEPTH_TEST,op=viz.OP_ROOT)
    panel.addItem(pigeonClone,align=viz.ALIGN_CENTER)
    yield viztask.waitKeyDown(' ')
    panel.remove()

def TrialCountDownTask():
    """Task that count downs to time limit for trial"""

    # Action for text fading out
    text_fade = vizact.parallel(
        vizact.fadeTo(0,time=0.8,interpolate=vizact.easeOut)
        ,vizact.sizeTo([1.5,1.5,1.0],time=0.8,interpolate=vizact.easeOut)
    )

    # Reset time text
    time_text.clearActions()
    time_text.alpha(1.0)
    time_text.color(viz.WHITE)
    time_text.setScale([1,1,1])
    time_text.message(str(int(TRIAL_DURATION)))

    # Countdown from time limit
    start_time = viz.getFrameTime()
    last_remain = int(TRIAL_DURATION)
    while (viz.getFrameTime() - start_time) < TRIAL_DURATION:

        # Compute remaining whole seconds
        remain = int(math.ceil(TRIAL_DURATION - (viz.getFrameTime() - start_time)))

        # Update text if time remaining changed
        if remain != last_remain:
            if remain <= 5:
                time_text.alpha(1.0)
                time_text.color(viz.RED)
                time_text.setScale([1]*3)
                time_text.runAction(text_fade)
                viz.playSound('sounds/beep.wav')
            time_text.message(str(remain))
            last_remain = remain

        # Wait tenth of second
        yield viztask.waitTime(0.1)

def FlashScreen():
    """Flash screen and fade out"""
    flash_quad.visible(True)
    flash_quad.color(viz.WHITE)
    fade_out = vizact.fadeTo(viz.BLACK,time=FLASH_TIME,interpolate=vizact.easeOutStrong)
    flash_quad.runAction(vizact.sequence(fade_out,vizact.method.visible(False)))

def FadeToGrayTask():
    gray_effect.setBlend(0.0)
    gray_effect.setEnabled(True)
    yield viztask.waitCall(gray_effect.setBlend,vizact.mix(0.0,1.0,time=1.0))

def UpdateScore(score):
    """Update score text"""
    score_text.message('Found: {} / {}'.format(score,TRIAL_COUNT))

def TrialTask(pigeon):
    # Create proximity sensor for pigeon using main view as target
    pigeon.visible(True)

    manager = vizproximity.Manager()

    manager.addTarget( vizproximity.Target(viz.MainView) )

    sensor = None

    sensor = vizproximity.Sensor(vizproximity.Sphere(PROXIMITY_RADIUS), pigeon)
    manager.addSensor(sensor)

        # Wait until pigeon is found or time runs out
    wait_find = vizproximity.waitEnter(sensor)
    data = yield viztask.waitAny([wait_find])

    # Hide pigeon and remove proximity sensor
    manager.remove()
    pigeon.visible(False)

    # Return whether pigeon was found
    viztask.returnValue(data.condition is wait_find)

def MainTask():
    """Top level task that controls the game"""

    # Display instructions and wait for key press to continue
    yield DisplayInstructionsTask()

    # Create panel to display trial results
    resultPanel = vizinfo.InfoPanel('',align=viz.ALIGN_CENTER,fontSize=25,icon=False,key=None)
    resultPanel.visible(False)

    while True:
        score = 0
        # Reset score
        UpdateScore(score)

        # Go through each position
        for pigeon in pigeons:
            # Perform a trial
            found = yield TrialTask(pigeon)

            if found:
                score += 1
                UpdateScore(score)

        if score == len(pigeons):
            #Display results and ask to quit or play again 
            resultPanel.setText(RESULTS.format(score,TRIAL_COUNT))
            resultPanel.visible(True)
            yield viztask.waitKeyDown(' ')
            resultPanel.visible(False)

viztask.schedule( MainTask() )

# Pre-load sounds
viz.playSound('sounds/beep.wav',viz.SOUND_PRELOAD)
viz.playSound('sounds/pigeon_fly.wav',viz.SOUND_PRELOAD)
viz.playSound('sounds/pigeon_catch.wav',viz.SOUND_PRELOAD)