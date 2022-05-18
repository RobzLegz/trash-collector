import viz
import vizfx
import vizfx.postprocess
from vizfx.postprocess.color import GrayscaleEffect
from vizfx.postprocess.composite import BlendEffect

def set_appearance():
    # Create flash screen quad
    flash_quad = viz.addTexQuad(parent=viz.ORTHO)
    flash_quad.color(viz.WHITE)
    flash_quad.alignment(viz.ALIGN_LEFT_BOTTOM)
    flash_quad.drawOrder(-10)
    flash_quad.blendFunc(viz.GL_ONE,viz.GL_ONE)
    flash_quad.visible(False)
    viz.link(viz.MainWindow.WindowSize,flash_quad,mask=viz.LINK_SCALE)

    # Create status bar background
    status_bar = viz.addTexQuad(parent=viz.ORTHO)
    status_bar.color(viz.BLACK)
    status_bar.alpha(0.5)
    status_bar.alignment(viz.ALIGN_LEFT_BOTTOM)
    status_bar.drawOrder(-1)
    viz.link(viz.MainWindow.LeftTop,status_bar,offset=[0,-80,0])
    viz.link(viz.MainWindow.WindowSize,status_bar,mask=viz.LINK_SCALE)

    # Create time limit text
    time_text = viz.addText('',parent=viz.ORTHO,fontSize=40)
    time_text.alignment(viz.ALIGN_CENTER_TOP)
    time_text.setBackdrop(viz.BACKDROP_OUTLINE)
    viz.link(viz.MainWindow.CenterTop,time_text,offset=[0,-20,0])

    # Create score text
    score_text = viz.addText('',parent=viz.ORTHO,fontSize=40)
    score_text.alignment(viz.ALIGN_LEFT_TOP)
    score_text.setBackdrop(viz.BACKDROP_OUTLINE)
    viz.link(viz.MainWindow.LeftTop,score_text,offset=[20,-20,0])

    # Create post process effect for blending to gray scale
    gray_effect = BlendEffect(None,GrayscaleEffect(),blend=0.0)
    gray_effect.setEnabled(False)
    vizfx.postprocess.addEffect(gray_effect)

    return (flash_quad, status_bar, time_text, score_text, gray_effect)