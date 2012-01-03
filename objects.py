# Collections of objects needed by Vertexer

#  This file is part of:
#  " Vertexer "
#  by Rob Knegjens


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import copy
import math
from vectors import Vec3, Quat
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

class Camera :
    
    def __init__(self):
        self.pos = Vec3(0,0,0)
        self.view = Vec3(0,1,0)
        self.up = Vec3(0,0,1)
        self.cursorX = 0.0
        self.cursorY = 0.0

    def __getitem__(self, index):
        if     index == "pos" :
            return self.pos
        elif   index == "posX" :
            return self.pos["x"]
        elif   index == "posY" :
            return self.pos["y"]
        elif   index == "posZ" :
            return self.pos["z"]
        elif   index == "view" :
            return self.view
        elif   index == "viewX" :
            return self.view["x"]
        elif   index == "viewY" :
            return self.view["y"]
        elif   index == "viewZ" :
            return self.view["z"]
        elif   index == "up" :
            return self.up
        elif   index == "upX" :
            return self.up["x"]
        elif   index == "upY" :
            return self.up["y"]
        elif   index == "upZ" :
            return self.up["z"]
        elif   index == "cursorX" :
            return self.cursorX
        elif   index == "cursorY" :
            return self.cursorY
        raise Exception
        
    def __setitem__(self, index, item):
        if index == "cursorX" :
            self.cursorX = item
        elif index == "cursorY" :
            self.cursorY = item

    def hStrafe (self, dist ) :
        """
        Move side ways left (min) or right (plus)
        """
        if self.pos == self.view : raise Exception
        
        try :
            horizontal = (self.up.cross(self.pos - self.view)).normalise()
            self.pos += dist*horizontal
            self.view += dist*horizontal
            return True
        except :
            return False
    
    def vStrafe (self, dist ) :
        """
        Move vertically down (min) or up (plus)
        """
        vertical = self.up.normalise()
        self.pos += dist*vertical
        self.view += dist*vertical
        return True

    def zoom (self, dist ) :
        """
        Zoom in (min) or out (plus)
        """
        if self.pos == self.view : raise Exception
        forward = (self.view - self.pos).normalise()
        self.pos += dist*forward
        self.view += dist*forward

        return True

    def roll (self, angle ) :
        """
        Rotate view about viewing axis CW (min) or CCW (plus) 
        by given angle (degrees)
        """
        if self.pos == self.view : raise Exception
        forwardNorm = (self.view - self.pos).normalise()
        rQuat = Quat().initR(forwardNorm,angle*math.pi/180)
        self.up = rQuat.vecRotate(self.up)
        return True
    
    def yaw (self, angle ) :
        """
        Rotate view about up axis CW (min) or CCW (plus) 
        by given angle (degrees)
        """
        if self.pos == self.view : raise Exception
        upNorm = self.up.normalise()
        rQuat = Quat().initR(upNorm,-angle*math.pi/180)
        self.view = self.pos + rQuat.vecRotate(self.view - self.pos)
        return True

    def globalYaw (self, angle ) :
        """
        Rotate view about global z axis CW (min) or CCW (plus) 
        by given angle (degrees)
        """
        if self.pos == self.view : raise Exception
        rQuat = Quat().initR(Vec3(0,0,1),-angle*math.pi/180)
        self.up = rQuat.vecRotate(self.up)
        self.view = self.pos + rQuat.vecRotate(self.view - self.pos)
        return True

    def pitch (self, angle ) :
        """
        Rotate view about horizontal axis CW (min) or CCW (plus) 
        by given angle (degrees)
        """
        if self.pos == self.view : raise Exception
        try : 
            horizontal = (self.up.cross(self.view - self.pos)).normalise()
            rQuat = Quat().initR(horizontal,angle*math.pi/180)
            self.up = rQuat.vecRotate(self.up)
            self.view = self.pos + rQuat.vecRotate(self.view - self.pos)
            return True
        except :
            return False

    def mouseDrag (self, cursor_x, cursor_y, modifier=0.5 ) :
        """
        Compare new mouse coords with old and rotate: pitch and yaw
        Return the old cursor coords
        """
        yaw = cursor_x - self.cursorX
        pitch = cursor_y - self.cursorY
        oldX = self.cursorX
        oldY = self.cursorY
        self.cursorX = cursor_x
        self.cursorY = cursor_y
        self.pitch(pitch*modifier)
        self.globalYaw(yaw*modifier)
        return oldX, oldY

    def moveTo (self, newPos) :
        """ 
        Move camera to new position, while looking at same point
        """
        if not isinstance(newPos, Vec3) : raise Exception
        if self.pos == self.view or newPos == self.view : raise Exception
        
        try :
            newHoriz = ((self.view - newPos).cross(Vec3(0,0,1))).normalise()
        except:
            newHoriz = Vec3(1,0,0)

        quat = Quat().initR(newHoriz,math.pi/2)

        self.up = quat.vecRotate(self.view - newPos)
        print self.up
        self.pos = copy.deepcopy(newPos)
        return 

    def lookAt (self, newVw) :
        """
        Look at new point while keeping camera in same position
        """
        if not isinstance(newVw, Vec3) : raise Exception
        if self.pos == self.view or self.pos == newVw : raise Exception

        try :
            newHoriz = ((newVw - self.pos).cross(Vec3(0,0,1))).normalise()
        except :
            newHoriz = Vec3(1,0,0)
        quat = Quat().initR(newHoriz,math.pi/2)
        
        self.up = quat.vecRotate(newVw - self.pos)
        self.view = copy.deepcopy(newVw)
        return

class Path :
    
    # should it take the first vertex or a list of vertices?
    def __init__(self, name, style="line"):
        self.vertices = []
        self.name = name 
        self.style = style

    # is this fast enough? could also just do it with unique names...
    def __eq__ (self, other) :
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


    def __len__(self):
        return len(self.vertices) 

    def __getitem__(self, index):
        if   index.lower() == "vertices" :
            # copy this somehow?
            return self.vertices[:]
        elif index.lower() == "name" :
            return self.name
        elif index.lower() == "style" :
            return self.style

    def __setitem__(self, index, item):
        if index.lower() == "name" :
            if item.isalnum() :
                self.name = item
        elif index.lower() == "style" :
            self.style = item

    def append(self, vertex) :
        self.vertices.append(vertex[:])

    def pop(self) :
        last = self.vertices[-1]
        self.vertices.remove(last)
        return last

    # TODO redesign so not passing so many objects
    def draw(self, grid, cam, quad, rgb=[0.0,1.0,1.0], lw=0.5 ) :
        lastVertex = self.vertices[0]
        for vertex in self.vertices :
            pos = Vec3(vertex[0], vertex[1], vertex[2])
            colGrad = 1.0 - (pos - cam["pos"]).length()/250.0
            if vertex[2] == grid["planeZ"] :
                glColor3f(colGrad, colGrad, colGrad)
            elif vertex[2] > grid["planeZ"] :
                glColor3f(0, 0, colGrad)
            else :
                glColor3f(colGrad, 0, 0)
                
            glTranslatef(vertex[0], vertex[1], vertex[2])
            gluSphere(quad, 0.2, 32, 32) 
            glTranslatef(-vertex[0], -vertex[1], -vertex[2])
            # Draw line to plane
            glLineWidth(0.5)
            glBegin(GL_LINES)
            glVertex3f(vertex[0], vertex[1], vertex[2])
            glVertex3f(vertex[0], vertex[1], grid["planeZ"])
            glEnd()
            glLineWidth(1.0)
            # Draw line to last vertex
            #if  not (   vertex[0] == lastVertex[0] \
            #        and vertex[1] == lastVertex[1] \
            #        and vertex[2] == lastVertex[2] ) :
            if vertex[:3] != lastVertex[:3] :
                glLineWidth(lw)
                glColor3f(rgb[0]*colGrad, rgb[1]*colGrad, rgb[2]*colGrad)
                glBegin(GL_LINES)
                glVertex3f(vertex[0], vertex[1], vertex[2])
                glVertex3f(lastVertex[0], lastVertex[1], lastVertex[2])
                glEnd()
                glLineWidth(1.0)
                
            lastVertex = vertex
    
    def printPython (self) :
        pStr = "%s = [" % self.name
        for vertex in self.vertices :
            vertStr = "[%f,%f,%f]" % (vertex[0],vertex[1],vertex[2])
            pStr = pStr + vertStr + ","
        # ingnore last comma:
        return pStr[:-1] + "]\n"

    def printAscii (self) :
        pStr = "%s %s %d  " % (self.name, self.style,len(self.vertices))
        for vertex in self.vertices :
            vertStr = "%f %f %f" % (vertex[0],vertex[1],vertex[2])
            pStr = pStr + vertStr + "  "
        return pStr + "\n"

