"""
Tools needed for 3D diagrams
"""

__author__ = "Team Win"

###############################################################################
##
##  IMPORT & GLOBAL
##
###############################################################################

import math
from vectors import Vec3, Quat
from subprocess import call

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

def createPovFile(filename,camLoc=[0,0,0],camLookAt=[1,0,0],camUp=[0,1,0]) :

    global _povFile, _camLoc
    _povFile = filename

    if len(_povFile) == 0 :
        print "No povray file specified"    

    FILE = open(_povFile,"w")   

    preamble = [
        """// -w320 -h240\n""", 
        """// -w800 -h600 +a0.3\n""",
        """// Run with +ua for transparency\n\n""",
        """#include "colors.inc"\n""",
        """#include "textures.inc"\n\n"""
        ]

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

    camera = [
        "camera {\n",
        "   location <%f,%f,%f>\n"%(_camLoc["X"],_camLoc["Y"],_camLoc["Z"]),
        "   sky <%f,%f,%f>\n" %(_camUp["X"],_camUp["Y"],_camUp["Z"]),
        "   look_at  <%f,%f,%f>\n"%(_camLookAt["X"],_camLookAt["Y"],_camLookAt["Z"]),
        "}\n\n"
    ]

    FILE.writelines(preamble)
    FILE.writelines(camera)
    FILE.close()


def runPovFile(transparency=True, width=800, height=600) :
    # TODO handle inputs

    global _povFile

    if len(_povFile) == 0 :
        print "No povray file setup"

    call(["povray", "-w800", "-h600", "+a0.3", "+ua", _povFile])


def pointLight(x=[0,0,3]) :
    # TODO place relative to camera

    global _povFile

    if len(_povFile) == 0 :
        print "No povray file specified"    

    FILE = open(_povFile,"a")   
    
    light = [
        "light_source {\n",
        "   <%f,%f,%f>, %s\n" % (x[0],x[1],x[2], "White"),
        "}\n\n"
    ]
    
    FILE.writelines(light)  
    FILE.close()

def line(path, radius=1, colour="Yellow",arrow=False, arrPos=1, arrRad=2) :
    """
    INPUT :
        @path:      List of 3D coordinates (array [x,y,z]) 
        @radius:    Radius of line
        @colour:    Colour of line
        @arrow:     Whether to place arrow (True/False)
        @arrPos:    If placing arrow, relative position between v1 and v2 (0-1)
        @arrRad:    If placing arrow, radius relative to line radius (1>)
    """

    global _povFile

    if len(_povFile) == 0 :
        print "No povray file specified"    

    FILE = open(_povFile,"a")   

    # for now only look at first and last vertex in path
    v1 = path[0]
    v2 = path[-1]

    particle = [
        "cylinder {\n",
        "   <%f,%f,%f>, <%f,%f,%f>, %f\n" % (v1[0],v1[1],v1[2],v2[0],v2[1],v2[2],radius ), 
        "   pigment { color %s }\n" % colour,
        "   finish {\n",
        "       reflection %f\n" % (0.1), 
        "       phong %f\n" % (0.8),
        "       ambient %f\n" % (0.1), 
        "       diffuse %f\n" % (0.9),
        "   }\n",
        "}\n\n",
        "sphere {\n",
        "   <%f,%f,%f>, %f\n" % (v1[0],v1[1],v1[2],radius),
        "   pigment { color %s }\n" % colour,
        "   finish {\n",
        "       reflection %f\n" % (0.1), 
        "       phong %f\n" % (0.8),
        "       ambient %f\n" % (0.1), 
        "       diffuse %f\n" % (0.9),
        "   }\n",
        "}\n\n",
        "sphere {\n",
        "   <%f,%f,%f>, %f\n" % (v2[0],v2[1],v2[2],radius),
        "   pigment { color %s }\n" % colour,
        "   finish {\n",
        "       reflection %f\n" % (0.1), 
        "       phong %f\n" % (0.8),
        "       ambient %f\n" % (0.1), 
        "       diffuse %f\n" % (0.9),
        "   }\n",
        "}\n\n"
    ]

    FILE.writelines(particle)

    if arrow is True and arrRad > 1 and arrPos >= 0 and arrPos <= 1:
        # TODO calculate position of arrow
        # should it be pointy if at the end of line?
        # in that case need to remove relevant sphere...

        diff = [ v2[0]-v1[0] , v2[1]-v1[1] , v2[2]-v1[2] ]
        length = math.sqrt(diff[0]**2 + diff[1]**2 + diff[2]**2)

        a1 = v1
        a2 = v2

        arrow = [
            "cone {\n",
            "   <%f, %f, %f>, %f\n" % (a1[0],a1[1],a1[2],radius*arrRad),
            "   <%f, %f, %f>, %f\n" % (a2[0],a2[1],a2[2],radius),
            "   pigment { color %s }\n" % colour,
            "   finish {\n",
            "       reflection %f\n" % (0.1), 
            "       phong %f\n" % (0.8),
            "       ambient %f\n" % (0.1), 
            "       diffuse %f\n" % (0.9),
            "   }\n",
            "}\n\n"
        ]

        FILE.writelines(arrow)

    FILE.close()

def wiggle(path, radius=1, colour="Yellow", ampl=4, waveLen=4, arrow=False, arrPos=1, arrRad=2) :
    """
    INPUT :
        @path:      List of 3D coordinates (array [x,y,z]) 
        @radius:    Radius of line
        @colour:    Colour of line
        @ample:     Amplitude of wiggle
        @waveLen: Suggested length of wiggle wavelenfth 
        @arrow:     Whether to place arrow (True/False)
        @arrPos:    If placing arrow, relative position between v1 and v2 (0-1)
        @arrRad:    If placing arrow, radius relative to line radius (1>)
    """

    global _povFile, _camLoc

    if len(_povFile) == 0 :
        print "No povray file specified"    

    FILE = open(_povFile,"a")   

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
        "   <%f,%f,%f>, %f,\n" % (p1[0],p1[1],p1[2],radius)
    ]

    for point in wigglePts :
        wiggleStr.append("  <%f,%f,%f>, %f,\n" % (point[0],point[1],point[2],radius))

    wiggleStr.extend([
        "   <%f,%f,%f>, %f\n" % (p2[0],p2[1],p2[2],radius),
        "   pigment { color %s }\n" % colour,
        "   finish {\n",
        "       reflection %f\n" % (0.1), 
        "       phong %f\n" % (0.8),
        "       ambient %f\n" % (0.1), 
        "       diffuse %f\n" % (0.9),
        "   }\n",
        "}\n\n"
    ])


    FILE.writelines(wiggleStr)

    FILE.close()

def helix(path, radius=1, colour="Yellow", ampl=4, waveLen=4, arrow=False, arrPos=1, arrRad=2) :
    """
    INPUT :
        @path:      List of 3D coordinates (array [x,y,z]) 
        @radius:    Radius of line
        @colour:    Colour of line
        @ample:     Amplitude of helix
        @waveLen:   Suggested length of helix wavelenfth 
        @arrow:     Whether to place arrow (True/False)
        @arrPos:    If placing arrow, relative position between v1 and v2 (0-1)
        @arrRad:    If placing arrow, radius relative to line radius (1>)
    """

    global _povFile, _camLoc

    if len(_povFile) == 0 :
        print "No povray file specified"    

    FILE = open(_povFile,"a")   

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
        "   <%f,%f,%f>, %f,\n" % (p1[0],p1[1],p1[2],radius)
    ]

    for point in helixPts :
        helixStr.append("  <%f,%f,%f>, %f,\n" % (point[0],point[1],point[2],radius))

    helixStr.extend([
        "   <%f,%f,%f>, %f\n" % (p2[0],p2[1],p2[2],radius),
        "   pigment { color %s }\n" % colour,
        "   finish {\n",
        "       reflection %f\n" % (0.1), 
        "       phong %f\n" % (0.8),
        "       ambient %f\n" % (0.1), 
        "       diffuse %f\n" % (0.9),
        "   }\n",
        "}\n\n"
    ])


    FILE.writelines(helixStr)

    FILE.close()

###############################################################################
##
##  TESTS
##
###############################################################################

