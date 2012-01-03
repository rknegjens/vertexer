import math 

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
