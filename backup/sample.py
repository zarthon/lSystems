import sys
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
width = 800
height = 800

def spiro( rOuter, rInner, rOffset, revs ):
    theta = 0.0
    glColor3d(1.0, 0.0, 0.0)
    glLineWidth(1)
    st="A+B+A-B-A-B-A+B+A"
    glLoadIdentity()
    glPushMatrix()
    for i in st:
        print i
        if i == 'A'or i =='B':
            print "inside F"
            glBegin(GL_LINES)
            glVertex2d(0, 0)
            glVertex2d(rOffset,0)
            glEnd()
            glTranslated(rOffset,0,0)
        elif i == '+':
            print "inside 90"
            glRotated(60,0,0,1)
        elif i=='-':
            print "inside -90"
            glRotated(-60,0,0,1)
            

    glPopMatrix()
    theta = 90.0
    glFlush()

def display():
    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    spiro( 1, .55, .09, 50)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("Simple OpenGL Examples")
    glutDisplayFunc(display)
    glutMainLoop()


if __name__ == "__main__":
    main()



