import sys
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
width = 800
height = 800


def Lindenmayer(axiom,rules):

    rules = rules.items()
    def apply_rule(axiom,(symbol,replacement)):    
        return axiom.replace(symbol,replacement.lower())

    while True:
        # Create a generator function
        yield axiom
        #get the next iteration of the system
        axiom = reduce(apply_rule,rules,axiom).upper()

class GenerateList(object):
    def __init__(self,generator):
        self.__generator = generator
        self.__list = []

    #to store the previous iterations
    def __getitem__(self,index):
        for i in range(index-len(self.__list) +1):
            self.__list.append(self.__generator.next())
        return self.__list[index]

class L_System(GenerateList):
    """
    Sample class to manipulate the L String generated by Lindenmayer function defined above.

    It is expected that the user follows the following convention to define the rules, Source
    http://en.wikipedia.org/wiki/L-system

    'F': Draw a Line
    '+': Turn Right by predefined angle i.e. objects angle
    '-': Turn Left by predefined angle
    'G': Move forward without drawing
    ']': Restore previously saved states
    '[': Save current state

    """
    def __init__(self,offset,start,rules,angle):
        self.offset = offset
        self.states = []
        self.angle = angle
        self.actions = {
            'F': self.forward,
            '+': self.right,
            '-': self.left,
            'G': self.go,
            '[': self.save,
            ']': self.restore,
        }
        super(L_System, self).__init__(Lindenmayer(start, rules))
    
##########################3
    def forward(self):
        glBegin(GL_LINES)
        glVertex2d(0,0)
        glVertex2d(self.offset,0)
        glEnd()
        glTranslated(self.offset,0,0)
    def right(self):
        glRotated(self.angle,0,0,1)
    def left(self):
        glRotated(-self.angle,0,0,1)
######################################
    def go(self):
        self.turtle.up()
        self.turtle.forward(self.size)
        self.turtle.down()

    def save(self):
        x, y = self.turtle.xcor(), self.turtle.ycor()
        h, c = self.turtle.heading(), self.turtle.pencolor()
        self.states.append((x, y, h, c))

    def restore(self):
        turtle.up()
        x, y, h, c = self.states.pop()
        turtle.setx(x)
        turtle.sety(y)
        turtle.setheading(h)
        turtle.pencolor(c)
        turtle.down()

    def update(self):
        pass

    def draw(self, index):
        glColor3d(1.0,0.0,0.0)
        glLineWidth(1)
        glLoadIdentity()
        glPushMatrix()
        for char in self[index]:
            if char in self.actions:
                self.actions[char]()


def display():
    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )



if __name__=='__main__':
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("Simple OpenGL Examples")
    glutDisplayFunc(display)

    fractals = {
        'snowflake': L_System( 0.001,'F++F++F', {'F': 'F-F++F-F'}, 60),
        'dragon': L_System( 0.01,'FX', {'X': 'X+YF', 'Y': 'FX-Y'}, 90),
        'plant': L_System(0.001,'FX', {'X': 'F-[[X]+X]+F[+FX]-X', 'F': 'FF'}, 25),
        'sierpinsky': L_System(0.001,'FA', {'FA': 'FB-FA-FB', 'FB': 'FA+FB+FA'}, 60),
        'koch':L_System(0.001,'F',{'F':'F+F-F-F+F'},90)
    }

    name,num = sys.argv[1], int(sys.argv[2])

    fractals[name].draw(num)
    glutMainLoop()


