import viz

TRIAL_COUNT = 10             # Number of trials per game
TRIAL_DURATION = 20         # Amount of time allowed for finding each pigeon (in seconds)
TRIAL_DELAY = 4             # Delay time between trials
PROXIMITY_RADIUS = 3.0      # Radius for proximity sensor around pigeon
FLASH_TIME = 3.0            # Time to flash screen at beginning of each trial

arrow = viz.addChild('arrow.wrl')
arrow.setScale([0.1,0.1,0.1])
arrow.visible(viz.OFF)