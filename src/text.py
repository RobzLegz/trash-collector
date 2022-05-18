from .constants import TRIAL_COUNT, TRIAL_DURATION, TRIAL_DELAY, PROXIMITY_RADIUS, FLASH_TIME

INSTRUCTIONS = """
Help find the escaped pigeons before they fly away!
{} pigeons flew the coop and are hiding out in the piazza.
You have {} seconds to catch each one before it flys away.
Listen carefully and you might be able to hear where they are hiding.
Use the mouse and WASD keys to move around.
Press spacebar to begin the hunt!""".format(TRIAL_COUNT,TRIAL_DURATION)

RESULTS = """You found {} of {} pigeons.
Press spacebar to start over or escape to exit."""

TRIAL_SUCCESS = 'You caught the pigeon!'
TRIAL_FAIL = 'The pigeon flew away!'