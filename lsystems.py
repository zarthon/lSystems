from openGL import GLUT
from openGL import GLU

DEFAULT_FORWARD_LENGTH = 0.006
EFAULT_SPHERE_RADIUS = 0.015
DEFAULT_TURN_VALUE = 35.0
DEFAULT_VARIATION = 5.0 

SYMBOL_FORWARD_F = 'F'
SYMBOL_FORWARD_G = 'G'
SYMBOL_FORWARD_NO_DRAW_F = 'f'
SYMBOL_FORWARD_NO_DRAW_G = 'g'
SYMBOL_PITCH_DOWN = '&'
SYMBOL_PITCH_UP = '%'
SYMBOL_POP_MATRIX = ']'
SYMBOL_PUSH_MATRIX = '['
SYMBOL_ROLL_LEFT = '/'
SYMBOL_ROLL_RIGHT = '\\'
SYMBOL_SPHERE = '@'
SYMBOL_TURN_180 = '|'
SYMBOL_TURN_LEFT = '+'
SYMBOL_TURN_RIGHT = '-'


class LSystem():
    class Point3f():
        x=0.0
        y=0.0
        z=0.0
    class ReproductionRule():
        _from='a'
        to="asd"
    def __init__(self,axiom,):
        pass



