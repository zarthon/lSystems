import sys
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random

#Important windo parameters
width = 800
height = 800

#Global Parameters declared
colorR=1.0
colorB=0.0
colorG=0.0
matrix = []

#Parameters to draw the L-System is declared
FILENAME='lsystems.txt'
AXIOM=None
RULES={}
ANGLE=None
VARIABLES = None
SIZE=None
ITERATE=None
SHAPE=''
VERT=False
TD=0

#Class encapsulation of world coordinates
class Coord:
	def __init__(self,l=0,r=0,b=0,t=0):
		self.l = l
		self.r = r
		self.t = t
		self.b = b

world_coord = Coord(-1,2,-0.5,2)
XS = 0
YS = 0

#Function to apply an iteration i.e apply rules to the axiom passed to the function
def Lindenmayer(axiom,rules):
	rules = rules.items()
	
	def apply_rule(axiom,(symbol,replacement)):    
		return axiom.replace(symbol,replacement.lower())

	while True:
		# Create a generator function
		yield axiom
		#get the next iteration of the system
		axiom = reduce(apply_rule,rules,axiom).upper()

#Class to generate the list of iteration when a particular iteration no. is being specified
class GenerateList(object):
	def __init__(self,generator):
		self.__generator = generator
		self.__list = []

	#to store the previous iterations and return the asked iteration string
	def __getitem__(self,index):
		for i in range(index-len(self.__list) +1):
			self.__list.append(self.__generator.next())
		return self.__list[index]


#Main class to apply the the drawing rules specified in the string returned by GenrateList.
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
	'&': Pitch down
	'^': Pitch up
	'\\': Roll left
	'/': Roll right

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
        '&': self.pitchDown,
        '^': self.pitchUp,
        '\\': self.rollLeft,
        '/': self.rollRight
        }
        super(L_System, self).__init__(Lindenmayer(start, rules))

#Draw different shapes
    def drawShape(self,which):
        global SIZE,colorR, colorB, colorG
        #glColor3d(random.random(),random.random(),random.random())
        if which == "line" and VERT == True:
            glBegin(GL_LINES)
            glVertex3d(0,0,0)
            glVertex3d(0,self.offset,0)
            glEnd()
        elif which == "quad" :

            glBegin(GL_QUADS);			# Start Drawing The Cube
            glColor3f(0.0,1.0,0.0);			# Set The Color To Blue
            glVertex3f( self.offset, self.offset,-self.offset);		# Top Right Of The Quad (Top)
            glVertex3f(-self.offset, self.offset,-self.offset);		# Top Left Of The Quad (Top)
            glVertex3f(-self.offset, self.offset, self.offset);		# Bottom Left Of The Quad (Top)
            glVertex3f( self.offset, self.offset, self.offset);		# Bottom Right Of The Quad (Top)

            glColor3f(1.0,0.5,0.0);			# Set The Color To Orange
            glVertex3f( self.offset,-self.offset, self.offset);		# Top Right Of The Quad (Bottom)
            glVertex3f(-self.offset,-self.offset, self.offset);		# Top Left Of The Quad (Bottom)
            glVertex3f(-self.offset,-self.offset,-self.offset);		# Bottom Left Of The Quad (Bottom)
            glVertex3f( self.offset,-self.offset,-self.offset);		# Bottom Right Of The Quad (Bottom)

            glColor3f(1.0,0.0,0.0);			# Set The Color To Red
            glVertex3f( self.offset, self.offset, self.offset);		# Top Right Of The Quad (Front)
            glVertex3f(-self.offset, self.offset, self.offset);		# Top Left Of The Quad (Front)
            glVertex3f(-self.offset,-self.offset, self.offset);		# Bottom Left Of The Quad (Front)
            glVertex3f( self.offset,-self.offset, self.offset);		# Bottom Right Of The Quad (Front)

            glColor3f(1.0,1.0,0.0);			# Set The Color To Yellow
            glVertex3f( self.offset,-self.offset,-self.offset);		# Bottom Left Of The Quad (Back)
            glVertex3f(-self.offset,-self.offset,-self.offset);		# Bottom Right Of The Quad (Back)
            glVertex3f(-self.offset, self.offset,-self.offset);		# Top Right Of The Quad (Back)
            glVertex3f( self.offset, self.offset,-self.offset);		# Top Left Of The Quad (Back)

            glColor3f(0.0,0.0,1.0);			# Set The Color To Blue
            glVertex3f(-self.offset, self.offset, self.offset);		# Top Right Of The Quad (Left)
            glVertex3f(-self.offset, self.offset,-self.offset);		# Top Left Of The Quad (Left)
            glVertex3f(-self.offset,-self.offset,-self.offset);		# Bottom Left Of The Quad (Left)
            glVertex3f(-self.offset,-self.offset, self.offset);		# Bottom Right Of The Quad (Left)

            glColor3f(1.0,0.0,1.0);			# Set The Color To Violet
            glVertex3f( self.offset, self.offset,-self.offset);		# Top Right Of The Quad (Right)
            glVertex3f( self.offset, self.offset, self.offset);		# Top Left Of The Quad (Right)
            glVertex3f( self.offset,-self.offset, self.offset);		# Bottom Left Of The Quad (Right)
            glVertex3f( self.offset,-self.offset,-self.offset);		# Bottom Right Of The Quad (Right)
            glEnd();				# Done Drawing The Quad
        elif which == "square":
            glBegin(GL_POLYGON)
            glVertex2d(0,0)
            glVertex2d(self.offset,0)
            glVertex2d(self.offset,self.offset)
            glVertex2d(0,self.offset)
            glEnd()
        elif which=="circle" :
            glBegin(GL_LINE_LOOP)
            for ang in range(0, 360, 5):
                x = cos(ang*pi/180)*SIZE
                y = sin(ang*pi/180)*SIZE
                glVertex2d(x, y)
            glEnd()
        elif which == "line" and VERT == False:
            glBegin(GL_LINES)
            glVertex3d(0,0,0)
            glVertex3d(self.offset,0,0)
            glEnd()
        elif which=="cylinder":
            quadratic=gluNewQuadric()
            gluQuadricNormals(quadratic, GLU_SMOOTH)
            gluCylinder(quadratic,self.offset,self.offset,self.offset*3,32,32)	

    #Move forward

    def forward(self):
		global SHAPE
		self.drawShape(SHAPE)
		if VERT==True:
			glTranslatef(0,self.offset,0)
		else:
			glTranslatef(self.offset,0,0)

    #Rotate Right
    def right(self): glRotated(self.angle,0,0,1)

    #Rotate Left
    def left(self): glRotated(-self.angle,0,0,1)

    #Jump forward without drawing
    def go(self):
		if VERT==True:
			glTranslatef(0,self.offset,0)
		else:
			glTranslatef(self.offset,0,0)

    #Save the state
    def save(self):
		global matrix
		temp = glGetFloatv(GL_MODELVIEW_MATRIX)
		matrix.append(temp)

	#Restore the last saved state
    def restore(self):
		global matrix
		temp = matrix.pop()
		glLoadMatrixd(temp)
	
    def pitchDown(self): glRotated(self.angle, 1,0,0)

    def pitchUp (self): glRotated(-self.angle, 1,0,0)

    def rollLeft (self): glRotated (self.angle, 0,1,0)
	
    def rollRight (self): glRotated (-self.angle, 0,1,0)
	
    def update(self): pass
    
    #Draw the LSystem with iter = index
    def draw(self, index):
        global TD,XS,YS
        glColor3d(colorR,colorB,colorG)
        glLineWidth(1)
        glLoadIdentity()
        glPushMatrix()
        print XS,YS,TD
        glTranslatef(XS,0,0)
        glTranslatef(0,YS,0)
        glRotated(TD, 0,1,0)
        for char in self[index]:
            if char in self.actions:
                self.actions[char]()
        glFlush()
        glPopMatrix()


#Main Display CallBack Function
def display():
    print "inside display"
    initialize()
    glLoadIdentity()
    glClear (GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    gluLookAt(0.0,0.0,8.0,0.0,0.0,0.0,0.0,1.0,0.0)

#File Handle function to parse the file
def file_handle():
    try:
        global AXIOM,RULES,ANGLE,SIZE,ITERATE,SHAPE,XS,VERT,YS
        fin = open(FILENAME,"r")
        lineList = fin.readlines()
        fin.close()

    	VERT=True
        print "Inside File Handle"
        for line in lineList:
            temp = line.split(";")
            if temp[0] == "Va":
                VARIABLES = temp[1].rstrip()
            elif temp[0] == "Ax":
                AXIOM = temp[1].rstrip()
            elif temp[0] == "Ru":
                key, val = temp[1].rstrip().split(":")[0],temp[1].rstrip().split(":")[1]
                RULES[key] = val
            elif temp[0] == "An":
                ANGLE = int(temp[1].rstrip()) 
            elif temp[0] == "Si":
                SIZE = float(temp[1].rstrip())
                #XS = SIZE
                #YS = SIZE
            elif temp[0] == "It":
                ITERATE = int(temp[1].rstrip())
            elif temp[0] == "Sh":
                SHAPE = temp[1].rstrip()
    except IOError:
        print "File Not Found"
        sys_exit(1)
    print XS, YS
    DrawSystem()
    return 0

#Call Back function for reshape
def reshape(w,h):
    global width,height,world_coord
    width,height = (w,h)
    glViewport(0,0,w,h)
    cx = 0.5*(world_coord.l + world_coord.r )
    dy = world_coord.t - world_coord.b
    world_coord.l = cx - 0.5*dy * w/h
    world_coord.r = cx + 0.5*dy * w/h
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    #gluOrtho2D(world_coord.l,world_coord.r,world_coord.b,world_coord.t)
    gluPerspective(40.0,w/h,5,20.0)
    glMatrixMode(GL_MODELVIEW)

#Main function to draw an L-System
def DrawSystem():
    global SIZE, AXIOM,RULES,ANGLE,ITERATE
    glClearDepth(1.0)
    glClear (GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    L_System( SIZE,AXIOM, RULES,ANGLE).draw(ITERATE)
    return 0

#RightClick Menu
def createMenu():
	submenu1 = glutCreateMenu(processMenuEvents)
	glutAddMenuEntry("Dragon",1)
	glutAddMenuEntry("Snowflake",2)
	glutAddMenuEntry("Sierpinsky",3)
	glutAddMenuEntry("Plant",4)
	submenu2 = glutCreateMenu(colorChange)
	glutAddMenuEntry("Red",4)
	glutAddMenuEntry("Orange",5)
	submenu3 = glutCreateMenu(shapeChange)
	glutAddMenuEntry("Line",1)
	glutAddMenuEntry("Circle",2)
	glutAddMenuEntry("Square",3)
	glutAddMenuEntry("Cylinder",4)
	glutCreateMenu(processMenuEvents)
	glutAddSubMenu("color",submenu2)
	glutAddSubMenu("System",submenu1)
	glutAddSubMenu("Shapes",submenu3)
	glutAddMenuEntry("Load File",5)
	glutAttachMenu (GLUT_RIGHT_BUTTON)

#Shape Change Menu Function
def shapeChange(option):
	global SHAPE
	if option  == 1:
		SHAPE = "line"
	elif option == 2:
		SHAPE = "circle"
	elif option == 3:
		SHAPE = "square"
	elif option==4:
		SHAPE="cylinder"
	else:
		SHAPE = "line"
	DrawSystem()
	return 0

#Global ColorChange function
def colorChange(option):
	global colorR, colorB, colorG
	if option == 4:
		colorR=1.0
		colorB=0.0
		colorG=0.0
		DrawSystem()
	elif option == 5:
		colorR=0.9
		colorB=0.6
		colorG=0.5
		DrawSystem()
	return 0

#Standard L-System Drawing Function

def processMenuEvents(option):
    global SIZE,AXIOM,RULES,ANGLE,ITERATE,VERT,XS,YS
    if option == 1:
        #DRAGON
        VERT = False
        SIZE  = 0.01
        #XS = SIZE
        #YS = SIZE
        AXIOM = 'FX'
        RULES = {'X':'X+YF','Y':'FX-Y'}
        ANGLE = 90
        ITERATE = 10
        L_System( SIZE,AXIOM,RULES,ANGLE).draw(ITERATE)
    elif option == 2:
        #SnowFlake
        VERT = False
        SIZE = 0.01
        #XS = SIZE
        #YS = SIZE
        AXIOM = 'F++F++F'
        RULES = {'F':'F-F++F-F'}
        ANGLE = 60
        ITERATE = 3
        L_System(SIZE,AXIOM,RULES,ANGLE).draw(ITERATE)
    elif option == 3:
        #Sierpinski
        VERT = False
        SIZE = 0.01
        #XS = SIZE
        #YS = SIZE
        AXIOM = 'FA'
        RULES = {'FA': 'FB-FA-FB', 'FB': 'FA+FB+FA'}
        ANGLE = 60
        ITERATE = 8
        L_System(SIZE,AXIOM, RULES,ANGLE).draw(ITERATE)
    elif option==4:
        #Plant
        VERT = True
        SIZE = 0.01
        #XS = SIZE
        #YS = SIZE
        AXIOM = 'FX'
        RULES = {'X': 'F&[[X]+X]+F[+FX]-X', 'F': 'FF'}
        ANGLE = 25
        ITERATE = 3
        L_System(SIZE,AXIOM,RULES,ANGLE).draw(ITERATE)
    else:
        file_handle()
    return 0

#0.05 addition for each shift
def keyboard_spe(key,x,y):
    global XS,YS
    if key == GLUT_KEY_RIGHT:
        XS = XS  + (0.05)
    if key == GLUT_KEY_LEFT:
        XS = XS - (0.05)
    if key == GLUT_KEY_UP:
        YS = YS + (0.05)
    if key == GLUT_KEY_DOWN:
        YS = YS - (0.05)
    DrawSystem()

#Basic KeyBoard functionality for rotation and zooming
def keyboard(key,x,y):
    global TD,SIZE
    if key == chr(27):
        sys.exit(0)
    if key == 'r': 
        TD = (TD + 15)%360
    if key == 'R':
        TD = (TD - 15)%360   
        TD = -(360-TD)
        #print TD
    if key == 'z':
        SIZE = SIZE + (SIZE*0.05)
    if key == 'Z':
        SIZE = SIZE - (SIZE*0.05)
    DrawSystem()

#System Initialisation
def initialize():
    global world_coord
    glColor3d(1.0,0.0,0.0)
    glClearDepth(3.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glDepthMask(GL_TRUE)
    glClear (GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    #glFrustum(-1.0,1.0,-1.0,1.0,1.5,20.0)
    #gluPerspective(40.0,(width)/height,0.01,20.0)
    gluOrtho2D(world_coord.l,world_coord.r,world_coord.b,world_coord.t)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    #gluLookAt(0.0,0.0,8.0,0.0,0.0,0.0,0.0,1.0,0.0)

if __name__=='__main__':
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DEPTH | GLUT_RGB)
	glutInitWindowSize(width, height)
	glutInitWindowPosition(100, 100)
	glutCreateWindow("L-Systems Generator")
	glutReshapeFunc(reshape)
	initialize()
	createMenu()
	glutDisplayFunc(display)
	glutKeyboardFunc(keyboard)
	glutSpecialFunc(keyboard_spe)
	file_handle()
	glutMainLoop()

