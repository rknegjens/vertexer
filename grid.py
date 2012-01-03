# Grid object for Vertexer

#  This file is part of:
#  " Vertexer "
#  by Rob Knegjens


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from objects import Vec3
from config import *

class Grid :


    def __init__ (self) :
        
        global DEF_DIM_X, DEF_DIM_Y, DEF_DIM_Z

        self.dimX = DEF_DIM_X
        self.dimY = DEF_DIM_Y
        self.dimZ = DEF_DIM_Z
        #self.planeZ = self.dimZ/2
        self.planeZ = 0 
       
        # cursor is on viewport
        self.cursorX = 0
        self.cursorY = 0
        # Pointer is on grid
        self.pointerX = 0
        self.pointerY = 0
        self.pointerOn = False   

    def __getitem__(self, index):
        if       index == "dimX" :
            return self.dimX
        elif     index == "dimY" :
            return self.dimY
        elif     index == "dimZ" :
            return self.dimZ
        elif     index == "planeZ" :
            return self.planeZ
        elif     index == "pointerX" :
            return self.pointerX
        elif     index == "pointerY" :
            return self.pointerY
        elif     index == "cursorX" :
            return self.cursorX
        elif     index == "cursorY" :
            return self.cursorY
        elif     index == "pointerOn" :
            return self.pointerOn
        raise Exception
        
    def __setitem__(self, index, item):

        global MIN_DIM, MAX_DIM

        if       index == "dimX" :
            if item > MIN_DIM and item < MAX_DIM :
                self.dimX = item
        elif     index == "dimY" :
            if item > MIN_DIM and item < MAX_DIM :
                self.dimY = item
        elif     index == "dimZ" :
            if item > MIN_DIM and item < MAX_DIM :
                self.dimZ = item
            if self.planeZ >= self.dimZ :
                self.planeZ = self.dimZ - 1
            elif self.planeZ <= -self.dimZ :
                self.planeZ = -(self.dimZ - 1)
        elif     index == "planeZ" :
            if item >= 0 and item < self.dimZ :
                self.planeZ = item
        elif     index == "cursorX" :
            self.cursorX = item 
        elif     index == "cursorY" :
            self.cursorY = item 

    def drawGrid (self) :

        global GRID_LEN_UNIT
        lu = GRID_LEN_UNIT # length unit

        # Draw bounding cube
        ########################################

        glColor3f(0.2,0.2,0.2)			# Dark Grey
    
        # Z-lines
        glBegin(GL_LINES)
        glVertex3f(-(self.dimX-1)*lu,-(self.dimY-1)*lu,-(self.dimZ-1)*lu) 
        glVertex3f(-(self.dimX-1)*lu,-(self.dimY-1)*lu, (self.dimZ-1)*lu) 
        glEnd()

        glBegin(GL_LINES)
        glVertex3f((self.dimX-1)*lu,-(self.dimY-1)*lu,-(self.dimZ-1)*lu) 
        glVertex3f((self.dimX-1)*lu,-(self.dimY-1)*lu, (self.dimZ-1)*lu) 
        glEnd()

        glBegin(GL_LINES)
        glVertex3f(-(self.dimX-1)*lu,(self.dimY-1)*lu,-(self.dimZ-1)*lu) 
        glVertex3f(-(self.dimX-1)*lu,(self.dimY-1)*lu, (self.dimZ-1)*lu) 
        glEnd()

        glBegin(GL_LINES)
        glVertex3f((self.dimX-1)*lu,(self.dimY-1)*lu,-(self.dimZ-1)*lu) 
        glVertex3f((self.dimX-1)*lu,(self.dimY-1)*lu, (self.dimZ-1)*lu) 
        glEnd()


        # Y-lines

        glBegin(GL_LINES)
        glVertex3f(-(self.dimX-1)*lu,-(self.dimY-1)*lu,-(self.dimZ-1)*lu) 
        glVertex3f(-(self.dimX-1)*lu, (self.dimY-1)*lu,-(self.dimZ-1)*lu) 
        glEnd()

        glBegin(GL_LINES)
        glVertex3f((self.dimX-1)*lu,-(self.dimY-1)*lu,-(self.dimZ-1)*lu) 
        glVertex3f((self.dimX-1)*lu, (self.dimY-1)*lu,-(self.dimZ-1)*lu) 
        glEnd()

        glBegin(GL_LINES)
        glVertex3f(-(self.dimX-1)*lu,-(self.dimY-1)*lu,(self.dimZ-1)*lu) 
        glVertex3f(-(self.dimX-1)*lu, (self.dimY-1)*lu,(self.dimZ-1)*lu) 
        glEnd()

        glBegin(GL_LINES)
        glVertex3f((self.dimX-1)*lu,-(self.dimY-1)*lu,(self.dimZ-1)*lu) 
        glVertex3f((self.dimX-1)*lu, (self.dimY-1)*lu,(self.dimZ-1)*lu) 
        glEnd()

        # X-lines

        glBegin(GL_LINES)
        glVertex3f(-(self.dimX-1)*lu,-(self.dimY-1)*lu,-(self.dimZ-1)*lu) 
        glVertex3f( (self.dimX-1)*lu,-(self.dimY-1)*lu,-(self.dimZ-1)*lu) 
        glEnd()

        glBegin(GL_LINES)
        glVertex3f(-(self.dimX-1)*lu,(self.dimY-1)*lu,-(self.dimZ-1)*lu) 
        glVertex3f( (self.dimX-1)*lu,(self.dimY-1)*lu,-(self.dimZ-1)*lu) 
        glEnd()

        glBegin(GL_LINES)
        glVertex3f(-(self.dimX-1)*lu,-(self.dimY-1)*lu,(self.dimZ-1)*lu) 
        glVertex3f( (self.dimX-1)*lu,-(self.dimY-1)*lu,(self.dimZ-1)*lu) 
        glEnd()
        
        glBegin(GL_LINES)
        glVertex3f(-(self.dimX-1)*lu,(self.dimY-1)*lu,(self.dimZ-1)*lu) 
        glVertex3f( (self.dimX-1)*lu,(self.dimY-1)*lu,(self.dimZ-1)*lu) 
        glEnd()

        # Draw plane
        ########################################

        glColor3f(0.0,0.3,0.0)			# Green
        # place lines parallel to y axis 
        #for ix in range(0,self.dimX) :
        for ix in range(-(self.dimX-1),self.dimX) :
            glBegin(GL_LINES)
            glVertex3f(ix*lu,-(self.dimY-1)*lu,self.planeZ) 
            glVertex3f(ix*lu, (self.dimY-1)*lu,self.planeZ) 
            glEnd()
        
        # place lines parallel to x axis 
        #for iy in range(0,self.dimY) :
        for iy in range(-(self.dimY-1),self.dimY) :
            glBegin(GL_LINES)
            #glVertex3f(0.0,iy*lu,self.planeZ) 
            glVertex3f(-(self.dimX-1)*lu,iy*lu,self.planeZ) 
            glVertex3f( (self.dimX-1)*lu,iy*lu,self.planeZ) 
            glEnd()


    def drawPointer (self) :

        global GRID_LEN_UNIT
        lu = GRID_LEN_UNIT # length unit

        if self.pointerToGrid() :
            glutSetCursor(GLUT_CURSOR_NONE)
            glTranslatef(self.pointerX, self.pointerY, self.planeZ)
            glColor3f(1.0, 1.0, 1.0)
            glLineWidth(2.0)
            glBegin(GL_LINES)
            glVertex3f(0, -0.5*lu, 0.01*lu)
            glVertex3f(0, +0.5*lu, 0.01*lu)
            glEnd()
            glBegin(GL_LINES)
            glVertex3f(-0.5*lu, 0.0, 0.01*lu)
            glVertex3f(+0.5*lu, 0.0, 0.01*lu)
            glEnd()
            glLineWidth(1.0)
            glTranslatef(-self.pointerX, -self.pointerY, -self.planeZ)
        else :
            glutSetCursor(GLUT_CURSOR_INHERIT)


    def shiftPlane (self, incr) :
        
        #if self.planeZ + incr < self.dimZ and self.planeZ + incr >= 0 :
        if self.planeZ + incr < self.dimZ and self.planeZ + incr > -self.dimZ :
            self.planeZ += incr

    def pointerOnPlane(self, cursor_x, cursor_y, zPlane ) :
        """
        Given pointer viewport coords, give position on grid plane
        """
        # Viewport to world
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev( GL_PROJECTION_MATRIX )
        viewport = glGetIntegerv( GL_VIEWPORT ) 

        wX = cursor_x
        wY = viewport[3] - cursor_y

        (r1X, r1Y, r1Z ) = gluUnProject(wX,wY,0,modelview,projection,viewport)
        (r2X, r2Y, r2Z ) = gluUnProject(wX,wY,1,modelview,projection,viewport)
        r1 = Vec3(r1X, r1Y, r1Z) 
        r2 = Vec3(r2X, r2Y, r2Z) 
        rayVec = (r2-r1).normalise()
        point = Vec3(0,0,zPlane)
        normal = Vec3(0,0,1)

        # Intersect ray with plane
        try :
            pointer = r1 + ( (point-r1).dot(normal)/rayVec.dot(normal) )*rayVec
            return pointer["X"], pointer["Y"]
        except :
            raise Exception("Could not place pointer on grid")

    def pointerToGrid (self ) :
        """
        Project pointer from viewport onto grid        
        """
        
        try:
            pX, pY = self.pointerOnPlane(self.cursorX, self.cursorY, self.planeZ)
        except :
            self.pointerOn = False
            return False
        
        #if     pX < 0 or pX >= self.dimX-1 or \
                #       pY < 0 or pY >= self.dimY-1 :
        if     pX < -(self.dimX-1) or pX >= (self.dimX-1) or \
               pY < -(self.dimX-1) or pY >= (self.dimY-1) :
            self.pointerOn = False
            return False  
        else :
            self.pointerX = round(pX)
            self.pointerY = round(pY)
            self.pointerOn = True
            return True

