from PyQt6.QtWidgets import QGraphicsDropShadowEffect
import string
from PyQt6.QtGui import QColor

def create_card_shadow(blur_radius=5, x_offset=3, y_offset=4, color=QColor(0, 0, 0, 55)):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur_radius)
    shadow.setXOffset(x_offset)
    shadow.setYOffset(y_offset)
    shadow.setColor(color)
    return shadow

def navShadow():
    return  create_card_shadow(blur_radius=13, x_offset=7, y_offset=0, color=QColor(0, 0, 0, 40))
def inputShadowEffect():
    return create_card_shadow(blur_radius=3, x_offset=2, y_offset=2, color=QColor(0, 0, 0, 60))