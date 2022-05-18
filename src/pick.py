import viz
from .constants import *

def pickTrash(score):
    object = viz.pick()
    print(object)

    if object == viz.VizChild(5):
        return

    if object.valid():
        object.visible(False)