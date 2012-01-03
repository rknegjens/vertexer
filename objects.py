# Collections of objects needed by Vertexer

#  This file is part of:
#  " Vertexer "
#  by Rob Knegjens


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math 
import copy

class Vec3 :

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.X = x 
        self.Y = y 
        self.Z = z 

    def __eq__ (self, other) :
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


    def __repr__(self):
        return repr([self.X,self.Y,self.Z]) 
    
    def __getitem__(self, index):
        if   index == 0 or isinstance(index,str) and index.lower() == "x" :
            return self.X
        elif index == 1 or isinstance(index,str) and index.lower() == "y" :
            return self.Y 
        elif index == 2 or isinstance(index,str) and index.lower() == "z" :
            return self.Z

    def __setitem__(self, index, item):
        if   index == 0 or isinstance(index,str) and index.lower() == "x" :
            self.X = item
        elif index == 1 or isinstance(index,str) and index.lower() == "y" :
            self.Y = item
        elif index == 2 or isinstance(index,str) and index.lower() == "z" :
            self.Z = item

    def __add__(self, other) :
        if not isinstance(other, Vec3) : raise Exception
        return Vec3(self.X + other.X, self.Y + other.Y, self.Z + other.Z)

    __radd__ = __add__

    def __sub__(self, other) :
        if not isinstance(other, Vec3) : raise Exception
        return Vec3(self.X - other.X, self.Y - other.Y, self.Z - other.Z)
    
    def __rsub__(self, other) :
        if not isinstance(other, Vec3) : raise Exception
        return Vec3(-self.X + other.X, -self.Y + other.Y, -self.Z + other.Z)
    
    def __mul__(self,scalar) :
        return Vec3(self.X*scalar, self.Y*scalar, self.Z*scalar)

    __rmul__ = __mul__

    def __div__(self,scalar) :
        return Vec3(self.X/scalar, self.Y/scalar, self.Z/scalar)

    def __neg__(self):
        return Vec3(-self.X, -self.Y, -self.Z)

    def __pos__(self):
        return self

    def __len__(self):
        return 3
    
    def dot (self, other) :
        if not isinstance(other, Vec3) : raise Exception
        return self.X*other.X + self.Y*other.Y + self.Z*other.Z

    def angle (self, other) :
        if not isinstance(other, Vec3) : raise Exception
        """
        Angle constructed from dot product
        """
        cosTheta = self.dot(other)/(self.length()*other.length())
        return math.acos(cosTheta)   

    def cross (self, other) :
        if not isinstance(other, Vec3) : raise Exception
        newX = self.Y*other.Z - self.Z*other.Y
        newY = self.Z*other.X - self.X*other.Z
        newZ = self.X*other.Y - self.Y*other.X
        return Vec3(newX, newY, newZ)

    def length2 (self) :
        return self.X**2 + self.Y**2 + self.Z**2

    def length (self) :
        return math.sqrt(self.length2())
    
    def normalise (self) :
        length = self.length()
        if length == 0 : raise Exception
        return self/self.length()

class Quat :

    def __init__(self, x=0.0, y=0.0, z=0.0, w=0.0):
        self.X = x 
        self.Y = y 
        self.Z = z 
        self.W = w

    def __eq__ (self, other) :
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return repr([self.X,self.Y,self.Z,self.W]) 
    
    def __getitem__(self, index):
        if   index == 0 or isinstance(index,str) and index.lower() == "x" :
            return self.X
        elif index == 1 or isinstance(index,str) and index.lower() == "y" :
            return self.Y 
        elif index == 2 or isinstance(index,str) and index.lower() == "z" :
            return self.Z
        elif index == 3 or isinstance(index,str) and index.lower() == "w" :
            return self.W

    def __setitem__(self, index, item):
        if   index == 0 or isinstance(index,str) and index.lower() == "x" :
            self.X = item
        elif index == 1 or isinstance(index,str) and index.lower() == "y" :
            self.Y = item
        elif index == 2 or isinstance(index,str) and index.lower() == "z" :
            self.Z = item
        elif index == 3 or isinstance(index,str) and index.lower() == "w" :
            self.W = item

    def __add__(self, other) :
        if not isinstance(other, Quat) : raise Exception
        return Quat(self.X + other.X, self.Y + other.Y, self.Z + other.Z, self.W + other.W)

    __radd__ = __add__

    def __sub__(self, other) :
        if not isinstance(other, Quat) : raise Exception
        return Quat(self.X - other.X, self.Y - other.Y, self.Z - other.Z, self.W - other.W)
    
    def __rsub__(self, other) :
        if not isinstance(other, Quat) : raise Exception
        return Quat(-self.X + other.X, -self.Y + other.Y, -self.Z + other.Z, -self.W + other.W)

    def __div__(self,scalar) :
        return Quat(self.X/scalar, self.Y/scalar, self.Z/scalar, self.W/scalar)

    def __neg__(self):
        return Quat(-self.X, -self.Y, -self.Z, -self.W)

    def __pos__(self):
        return self

    def __len__(self):
        return 4

    def length2 (self) :
        return self.X**2 + self.Y**2 + self.Z**2 + self.W**2

    def length (self) :
        return math.sqrt(self.length2())
    
    def normalise (self) :
        return self/self.length()

    def conjugate (self) :
        return Quat(-self.X, -self.Y, -self.Z, self.W)

    def __mul__ (self, other) :
        """
        Quaternion multiplication from the right
        """
        
        if not isinstance(other, Quat) : raise Exception
        newX = self.W * other.X + self.X * other.W + self.Y * other.Z - self.Z * other.Y
        newY = self.W * other.Y + self.Y * other.W + self.Z * other.X - self.X * other.Z
        newZ = self.W * other.Z + self.Z * other.W + self.X * other.Y - self.Y * other.X
        newW = self.W * other.W - self.X * other.X - self.Y * other.Y - self.Z * other.Z
        return Quat(newX, newY, newZ, newW)

    def __rmul__ (self, other) :
        """
        Quaternion multiplication from the left
        """
        
        if not isinstance(other, Quat) : raise Exception
        newX = other.W * self.X + other.X * self.W + other.Y * self.Z - other.Z * self.Y
        newY = other.W * self.Y + other.Y * self.W + other.Z * self.X - other.X * self.Z
        newZ = other.W * self.Z + other.Z * self.W + other.X * self.Y - other.Y * self.X
        newW = other.W * self.W - other.X * self.X - other.Y * self.Y - other.Z * self.Z
        return Quat(newX, newY, newZ, newW)


    def vecRotate (self, vector ) :
        """
        Rotate vector (Vec3) by this quaternion, returning a vector (Vec3)
        """
        if not isinstance(vector, Vec3) : raise Exception

        vNorm = vector.normalise()
        vecQuat = Quat(vNorm.X, vNorm.Y, vNorm.Z, 0)
        
        resQuat = ( self * vecQuat ) * self.conjugate()
        return Vec3(resQuat.X, resQuat.Y, resQuat.Z)    
        
    def initR(self, vector, theta) :
        """
        Init quat as a rotation with vector (axis) and angle in radians
        """
        if not isinstance(vector, Vec3) : raise Exception
        vNorm = vector.normalise()
        sinTheta = math.sin(theta/2)
        self.X = vNorm.X*sinTheta
        self.Y = vNorm.Y*sinTheta
        self.Z = vNorm.Z*sinTheta
        self.W = math.cos(theta/2)
        return self

    def initVV(self, v1, v2) :
        """
        Init quat given a source (v1) and destination (v2) vector
        """
        if not isinstance(v1, Vec3) : raise Exception
        if not isinstance(v2, Vec3) : raise Exception
        rVec = v1 + v2
        rVec.normalise()
        qVec = rVec.cross(v2)
        self.X = qVec.X
        self.Y = qVec.Y
        self.Z = qVec.Z
        self.W = rVec.dot(v2)
        return self

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

##########################################################################
### Diagnostics
##########################################################################

v1 = Vec3(1,0,0)
v2 = Vec3(0,3,0)
v3 = 5*v2
v4 = Vec3(1,0,1)
print v1 == v4
v1[2] = 1
#print v1
#print v1.dot(v2)
#print v1.angle(v2)
print v2
#print (v1.normalise())
#print v1

q1 = Quat().initR(Vec3(1,0,0),math.pi/2)
q2 = Quat(0,1,0,2)
#print q1 + q2
#print q1*q2
#print q2*q1
print q1.vecRotate(v2)
