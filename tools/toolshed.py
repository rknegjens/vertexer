"""
Tools needed for drawing 3D line diagrams .

If a .pov file already exists, don't modify existing
"named" paths. The user should first manually remove
them to have them regenerated.
"""

# TODO
# make lines, helix, wiggle, light objects and inheret
# from a common interface
# Let all paths have optional "arrows" as end points only

__author__ = "Team Win"

###############################################################################
##
##  IMPORT & GLOBAL
##
###############################################################################

import math
import os.path
from vectors import Vec3, Quat
from subprocess import call

###############################################################################
##
##  HELPERS
##
###############################################################################

def nameHeader(name) :
    return [
        "//@@@ %s\n" % name,
        "//################################\n",
    ]

def lineHeader(radius, colour, reflection=0.1, phong=0.8, ambient=0.1, diffuse=0.9 ) :
    return [
        "#declare RADIUS = %f;\n" % radius,
        "#declare COLOUR = %s;\n" % colour,
        "#declare FINISH = finish { reflection %f phong %f ambient %f diffuse %f }\n" % (reflection, phong, ambient, diffuse),
        "\n",
    ]

###############################################################################
##
##  FUNCTIONS
##
###############################################################################

# Global variables
_povFile = ""
_camLoc = Vec3()  # camera location (needed for rotating wiggles etc.)
_camLookAt = Vec3()  # camera direction (needed for rotating wiggles etc.)
_camUp = Vec3() # up direction of camera
_existing = [] # existing paths/objects in the file that should not be overwritten

def createPovFile(filename,camLoc=[0,0,0],camLookAt=[1,0,0],camUp=[0,1,0]) :

    global _povFile, _camLoc, _camLookAt, _camUp, _existing
    _povFile = filename

    if len(_povFile) == 0 :
        print "No povray file specified"
        return

    try :
        # If file already exists, extract existing paths/objects
        # that should not be overwritten
        FILE = open(_povFile,"r")
        
        import re
        regex = re.compile(r'//@@@ (?P<name>\w+:?\w*)') 
        for line in FILE.readlines() :
            m = regex.match(line)
            if m :
                print m.group('name')
                _existing.append(m.group('name'))

        FILE.close()

    except IOError as e :
        # File doesn't exists, so create new one
        FILE = open(_povFile,"w")
        FILE.writelines([
            """// -w320 -h240\n""", 
            """// -w800 -h600 +a0.3\n""",
            """// Run with +ua for transparency\n\n""",
            """#include "colors.inc"\n""",
            """#include "textures.inc"\n\n"""
        ])
        FILE.close()

    # If no camera setup, make one now
    if "camera" not in _existing :

        try :
            FILE = open(_povFile,"a")
        except IOError as e :
            print "Could not open specified .pov file: %s" % _povFile
            return

        # global cam variables
        _camLoc["X"] = camLoc[0]
        _camLoc["Y"] = camLoc[1]
        _camLoc["Z"] = camLoc[2]
        _camLookAt["X"] = camLookAt[0]
        _camLookAt["Y"] = camLookAt[1]
        _camLookAt["Z"] = camLookAt[2]
        _camUp["X"] = camUp[0]
        _camUp["Y"] = camUp[1]
        _camUp["Z"] = camUp[2]

        FILE.writelines(nameHeader("camera"))
        FILE.writelines([
            "camera {\n",
            "   location <%f,%f,%f>\n"%(_camLoc["X"],_camLoc["Y"],_camLoc["Z"]),
            "   sky <%f,%f,%f>\n" %(_camUp["X"],_camUp["Y"],_camUp["Z"]),
            "   look_at  <%f,%f,%f>\n"%(_camLookAt["X"],_camLookAt["Y"],_camLookAt["Z"]),
            "}\n\n"
        ])
        FILE.close()

def runPovFile(transparency=True, width=800, height=600) :
    # TODO handle inputs

    global _povFile

    if len(_povFile) == 0 :
        print "No povray file setup"
        return

    call(["povray", "-w800", "-h600", "+a0.3", "+ua", _povFile])

def line(path, name, radius=0.5, colour="Yellow") :
    """
    INPUT :
        @path:      List of 3D coordinates (array [x,y,z]) 
        @name:      A unique identifier
        @radius:    Radius of line
        @colour:    Colour of line
        @arrow:     Whether to place arrow (True/False)
                    (if multiple lines, place arrow on each)
        @arrPos:    If placing arrow, relative position between v1 and v2 (0-1)
        @arrRad:    If placing arrow, radius relative to line radius (1>)
    """

    global _povFile, _existing

    if name in _existing :
        print "Path %s already exists, skipping" % name
        return

    try :
        FILE = open(_povFile,"a")
    except IOError as e :
        print "Could not open specified .pov file: %s" % _povFile
        return
    
    FILE.writelines(nameHeader(name))
    FILE.writelines(lineHeader(radius,colour))
    
    def writeVertex(vIndex) :
        return [
            "sphere {\n",
            "   VERTEX_%d, RADIUS\n" % (vIndex),
            "   pigment { color COLOUR }\n",
            "   finish  { FINISH }\n",
            "}\n\n",
        ]

    # write vertex names
    for i in range(len(path)) :
        v = path[i]
        FILE.write("#declare VERTEX_%d = <%f,%f,%f>;\n" % (i,v[0],v[1],v[2])) 
    FILE.write("\n") 

    # draw first vertex
    FILE.writelines(writeVertex(0))
    
    i1 = 0
    for i2 in range(len(path[1:])) :
        i2 = i2+1
        FILE.writelines([ 
            "cylinder {\n",
            "   VERTEX_%d, VERTEX_%d, RADIUS\n" % (i1,i2), 
            "   pigment { color COLOUR }\n",
            "   finish  { FINISH }\n",
            "}\n\n",
        ])
        FILE.writelines(writeVertex(i2))

        #if arrow is True and arrRad > 1 and arrPos >= 0 and arrPos <= 1:
        #    # Make arrow 20% of line length
        #    # should it be pointy if at the end of line?
        #    # in that case need to remove relevant sphere...
        #    v1 = path[i1]
        #    v2 = path[i2]
        #    
        #    vec1 = Vec3(v1[0],v1[1],v1[2])
        #    vec2 = Vec3(v2[0],v2[1],v2[2])
        #    
        #    diff = vec2 - vec1
        #    length = diff.length()
        #   
        #    # arrPos is centre of arrow cone
        #    if arrPos > 0.90 : 
        #        arrPos = 0.90
        #    elif arrPos < 0.10 :
        #        arrPos = 0.10

        #    a1 = vec1 + diff*(arrPos-0.1)
        #    a2 = vec1 + diff*(arrPos+0.1)

        #    FILE.writelines([
        #        "cone {\n",
        #        "   <%f, %f, %f>, %f\n" % (a1[0],a1[1],a1[2],radius*arrRad),
        #        "   <%f, %f, %f>, %f\n" % (a2[0],a2[1],a2[2],radius),
        #        "   pigment { color COLOUR }\n",
        #        "   finish  { FINISH }\n",
        #        "}\n\n",
        #    ])


        i1 = i2

    FILE.close()

def curve(path, name, radius=0.5, colour="Yellow") :
    """
    INPUT :
        @path:      List of 3D coordinates (array [x,y,z]) 
        @name:      A unique identifier
        @radius:    Radius of line
        @colour:    Colour of line
    """

    global _povFile, _existing

    if name in _existing :
        print "Path %s already exists, skipping" % name
        return

    try :
        FILE = open(_povFile,"a")
    except IOError as e :
        print "Could not open specified .pov file: %s" % _povFile
        return
    
    FILE.writelines(nameHeader(name))
    FILE.writelines(lineHeader(radius,colour))
    
    # write vertex names
    for i in range(len(path)) :
        v = path[i]
        FILE.write("#declare VERTEX_%d = <%f,%f,%f>;\n" % (i,v[0],v[1],v[2])) 
    FILE.write("\n") 

    FILE.writelines([
        "sphere_sweep {\n",
        "   b_spline\n",
        "   %d,\n"% (len(path)+2),
        "   VERTEX_%d, RADIUS,\n" % (0),
    ])

    for i in range(len(path)) :
        FILE.write("  VERTEX_%d, RADIUS,\n" % (i))

    FILE.writelines([
        "   VERTEX_%d, RADIUS\n" % (len(path)-1),
        "   pigment { color COLOUR }\n",
        "   finish  { FINISH }\n",
        "}\n\n"
    ])

    FILE.close()

def wiggle(path, name, radius=0.5, colour="Yellow", ampl=4, waveLen=4) :
    """
    INPUT :
        @path:      List of 3D coordinates (array [x,y,z]) 
        @name:      A unique identifier
        @radius:    Radius of line
        @colour:    Colour of line
        @ample:     Amplitude of wiggle
        @waveLen: Suggested length of wiggle wavelenfth 
    """

    global _povFile, _camLoc, _existing

    if name in _existing :
        print "Path %s already exists, skipping" % name
        return

    try :
        FILE = open(_povFile,"a")
    except IOError as e :
        print "Could not open specified .pov file: %s" % _povFile
        return
    
    FILE.writelines(nameHeader(name))
    FILE.writelines(lineHeader(radius,colour))

    # for now only look at first and last vertex in path
    v1 = path[0]
    v2 = path[-1]

    wigglePts = []

    p1 = Vec3(v1[0],v1[1],v1[2])
    p2 = Vec3(v2[0],v2[1],v2[2])

    lVec = (p2-p1).normalise()
    normal = (_camLoc-p1).normalise()
    amplVec = lVec.cross(normal).normalise()

    dist = (p2-p1).length()
    halfLen = dist / round(dist / (waveLen/2))
    numPts = int(2*round(dist/halfLen) + 1 )

    #normal = (p1-_camLoc).cross(lVec)

    for i in range(numPts) :
        p = p1 + i*(halfLen/2)*lVec
        j = i % 4
        if j == 1 :
            p = p + ampl*amplVec
        elif j == 3 :
            p = p - ampl*amplVec
        wigglePts.append(p)

    wiggleStr = [
        "sphere_sweep {\n",
        "   b_spline\n",
        "   %d,\n"% (len(wigglePts)+2),
        "   <%f,%f,%f>, RADIUS,\n" % (p1[0],p1[1],p1[2])
    ]

    for point in wigglePts :
        wiggleStr.append("  <%f,%f,%f>, RADIUS,\n" % (point[0],point[1],point[2]))

    wiggleStr.extend([
        "   <%f,%f,%f>, RADIUS\n" % (p2[0],p2[1],p2[2]),
        "   pigment { color COLOUR }\n",
        "   finish  { FINISH }\n",
        "}\n\n"
    ])


    FILE.writelines(wiggleStr)

    FILE.close()

def helix(path, name, radius=0.5, colour="Yellow", ampl=4, waveLen=4) :
    """
    INPUT :
        @path:      List of 3D coordinates (array [x,y,z]) 
        @name:      A unique identifier
        @radius:    Radius of line
        @colour:    Colour of line
        @ample:     Amplitude of helix
        @waveLen:   Suggested length of helix wavelenfth 
    """

    global _povFile, _camLoc, _existing

    if name in _existing :
        print "Path %s already exists, skipping" % name
        return

    try :
        FILE = open(_povFile,"a")
    except IOError as e :
        print "Could not open specified .pov file: %s" % _povFile
        return
    
    FILE.writelines(nameHeader(name))
    FILE.writelines(lineHeader(radius,colour))

    # for now only look at first and last vertex in path
    v1 = path[0]
    v2 = path[-1]

    helixPts = []

    p1 = Vec3(v1[0],v1[1],v1[2])
    p2 = Vec3(v2[0],v2[1],v2[2])

    lVec = (p2-p1).normalise()
    normal = (_camLoc-p1).normalise()
    amplVec = lVec.cross(normal).normalise()
    perpVec = lVec.cross(amplVec).normalise()

    dist = (p2-p1).length()
    halfLen = dist / round(dist / (waveLen/2))
    numPts = int(2*round(dist/halfLen) + 1 )

    #normal = (p1-_camLoc).cross(lVec)

    for i in range(numPts) :
        p = p1 + i*(halfLen/2)*lVec
        j = i % 4
        if j == 1 :
            p = p + ampl*amplVec + ampl*perpVec
        elif j == 2 :
            p = p + 2.*ampl*perpVec   
        elif j == 3 :
            p = p - ampl*amplVec + ampl*perpVec
        helixPts.append(p)

    helixStr = [
        "sphere_sweep {\n",
        "   b_spline\n",
        "   %d,\n"% (len(helixPts)+2),
        "   <%f,%f,%f>, RADIUS,\n" % (p1[0],p1[1],p1[2])
    ]

    for point in helixPts :
        helixStr.append("  <%f,%f,%f>, RADIUS,\n" % (point[0],point[1],point[2]))

    helixStr.extend([
        "   <%f,%f,%f>, RADIUS\n" % (p2[0],p2[1],p2[2]),
        "   pigment { color COLOUR }\n",
        "   finish  { FINISH }\n",
        "}\n\n"
    ])


    FILE.writelines(helixStr)

    FILE.close()

def light(path, name, radius=0.5,colour="White") :
    """
    INPUT :
        @path:      List of 3D coordinates (array [x,y,z]) 
        @name:      A unique identifier
        @radius:    Unused (need a rewrite) 
        @colour:    Colour of light
    """

    global _povFile, _existing

    if name in _existing :
        print "Path %s already exists, skipping" % name
        return

    try :
        FILE = open(_povFile,"a")
    except IOError as e :
        print "Could not open specified .pov file: %s" % _povFile
        return

    FILE.writelines(nameHeader(name))
    
    for v in path :
        FILE.writelines([  
            "light_source {\n",
            "   <%f,%f,%f>, %s\n" % (v[0],v[1],v[2], colour),
            "}\n\n",
        ])

    FILE.close()

###############################################################################
##
##  TESTS
##
###############################################################################

