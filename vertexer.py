#!/usr/bin/env python2

"""
+--------------+
|   vertexer   |
+--+-----------+
   | version 1 
   +----------+
"""

__author__ = "Rob Knegjens"

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys, os
import shelve

from config import *
from objects import Grid, Camera, Path
from tools.vectors import Vec3

# File IO
output_path = None
workfile = None

# Number of the glut window.
window = 0

mouseDragging = False

# Display strings 
commandString = ""
messageString = ""
# Also encodes mode logic:
modeString = ""

helptxt1 = []
helptxt2 = []

# Camera object
cam = Camera()

# Grid object
grid = Grid()

# Path list 
paths = []

# Specials paths
pathCounter = 0 # keep unique count of paths 
insPath = None # Current insert path
hlPath = None # highlighted path (default mode)
selPath = None # selected path (default mode)

# For spheres 
quad = None

# A general OpenGL initialization function.  Sets all of the initial parameters. 
def InitGL(Width, Height):              # We call this right after our OpenGL window is created.
    
    global cam, messageString, quad
    global M_STARTUP, STR_STARTUP_MSG
    global output_path, workfile
    global helptxt1, helptxt2

    glShadeModel(GL_SMOOTH)             # Enables Smooth Color Shading
    glClearColor(0.0, 0.0, 0.0, 0.5)    # This Will Clear The Background Color To Black
    glClearDepth(1.0)                   # Enables Clearing Of The Depth Buffer
    glEnable(GL_DEPTH_TEST)             # Enables Depth Testing
    glEnable(GL_LINE_SMOOTH)            # needed?
    glDepthFunc(GL_LEQUAL)              # The Type Of Depth Test To Do
    glHint (GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST) # Really Nice Perspective Calculations

    cam.moveTo( Vec3(grid["dimX"]*(-0.25),grid["dimY"]*(-1.5),2*grid["dimZ"]) )
    cam.lookAt( Vec3(0.,0.,0.) )

    setMode(M_STARTUP)
    messageString = STR_STARTUP_MSG

    time = glutGet(GLUT_ELAPSED_TIME)

    quad = gluNewQuadric()
    
    # Get absolute path of script directory
    output_path = os.path.abspath(os.path.dirname(sys.argv[0])) + "/output/"
    workfile = output_path + "default"

    # read help files and put into nice string lists!
    try :
        f1 = open('doc/HELPTXT1', 'r')
        helptxt1 = f1.readlines()
        f1.close()
        
        f2 = open('doc/HELPTXT2', 'r')
        helptxt2 = f2.readlines()
        f2.close()
    except :
        return False

    return True                                 # // Initialization Went OK

def ReSizeGLScene(Width, Height):
    if Height == 0:                     # Prevent A Divide By Zero If The Window Is Too Small 
        Height = 1

    glViewport(0, 0, Width, Height)     # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 1000.0)
    glMatrixMode (GL_MODELVIEW)     # // Select The Modelview Matrix
    glLoadIdentity ()                   # // Reset The Modelview Matrix
    
    return

def drawString (text) :
    
    for char in text :
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char) )

# The main drawing function. 
def DrawGLScene():

    global cam, quad, insPath, selPath, hlPath
    global commandMode, helpMode, visualMode, commandString, messageString, modeString
    global M_INSERT, M_HELP, M_COMMAND, M_VISUAL, M_DEFAULT
    global helptxt1, helptxt2

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); # Clear The Screen And The Depth Buffer

    # Attempt at optimization
    if mouseDragging :
        glDisable(GL_LINE_SMOOTH)
        glDisable(GL_POINT_SMOOTH)
    else :
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POINT_SMOOTH)

    # The 3D world
    #######################
   
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(  cam["posX"],cam["posY"],cam["posZ"], \
                cam["viewX"],cam["viewY"],cam["viewZ"], \
                cam["upX"],cam["upY"],cam["upZ"])
    
    # Draw grid
    grid.drawGrid()

    # Draw pointer
    if modeString == M_INSERT :
        grid.drawPointer()
        # Draw line to last insert point
        if insPath is not None :
            lastVertex = insPath["vertices"][-1]
            
            vertex = [grid["pointerX"],grid["pointerY"],grid["planeZ"]]
            pos = Vec3(vertex[0], vertex[1], vertex[2])
            colGrad = 1.0 - (pos - cam["pos"]).length()/250.0
            
            glLineWidth(D_SEL_RAD)
            glColor3f(colGrad*D_INS_RGB[0],colGrad*D_INS_RGB[1],colGrad*D_INS_RGB[2])
            glBegin(GL_LINES)
            glVertex3f(vertex[0], vertex[1], vertex[2])
            glVertex3f(lastVertex[0], lastVertex[1], lastVertex[2])
            glEnd()
            glLineWidth(1.0)

    # Draw paths
    for path in paths :
        lw = D_NRM_RAD 
        rgb= D_NRM_RGB

        if path == selPath or path == hlPath:
            lw= D_SEL_RAD

        if path == insPath :
            rgb= D_INS_RGB

        if modeString == M_DEFAULT and path == selPath :
            rgb = D_SEL_RGB

        path.draw(grid, cam, quad, rgb=rgb,lw=lw)

    # 2D text overlay (orthographic projection)
    ####################################

    window_width = glutGet(GLUT_WINDOW_WIDTH)
    window_height = glutGet(GLUT_WINDOW_HEIGHT)
    
    glDisable(GL_DEPTH_TEST)                # Disable Depth Testing
    glDisable(GL_DITHER)

    # Save your projection matrix
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0.0,window_width,window_height,0.0,-1.0,1.0)

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity()                    
    #glTranslatef(0,0,-1.0)

    # Draw mode string
    if len(modeString) > 0 :
        glColor3f(1.0,1.0,1.0)  
        glRasterPos3f(15, window_height -35 ,0 )
        drawString(modeString)
    
    # Draw command line
    if modeString == M_COMMAND :
        glColor3f(1.0,1.0,1.0)  
        glRasterPos3f(15, window_height -15 ,0 )
        drawString(":" + commandString)
    else :
        glColor3f(0.5,0.5,0.5)  
        glRasterPos3f(15, window_height -15 ,0 )
        drawString(messageString)


    if modeString == M_INSERT and grid["pointerOn"] :
        glColor3f(1.0,1.0,1.0)  
        pointerPos = "%d, %d, %d" % (grid["pointerX"], grid["pointerY"], grid["planeZ"])
        glRasterPos3f(window_width - 10*len(pointerPos) -15, 30 ,0 )
        drawString(pointerPos)

    if modeString == M_DEFAULT :
        if hlPath is not None :
            glColor3f(1.0,1.0,1.0)  
            nameString =   "Name  : %10s" % (hlPath["name"])
            styleString =  "Style : %10s" % (hlPath["style"])
            radiusString = "Radius: %10s" % (hlPath["radius"])
            arrowString =  "Arrow : %10s" % (hlPath["arrow"])
            glRasterPos3f(window_width - 10*len(nameString) -15, 30 ,0 )
            drawString(nameString)
            glRasterPos3f(window_width - 10*len(styleString) -15, 50 ,0 )
            drawString(styleString)
            glRasterPos3f(window_width - 10*len(styleString) -15, 70 ,0 )
            drawString(radiusString)
            glRasterPos3f(window_width - 10*len(styleString) -15, 90 ,0 )
            drawString(arrowString)
        elif selPath is not None :
            glColor3f(1.0,1.0,1.0)  
            nameString =   "Name  : %10s" % (selPath["name"])
            styleString =  "Style : %10s" % (selPath["style"])
            radiusString = "Radius: %10s" % (selPath["radius"])
            arrowString =  "Arrow : %10s" % (selPath["arrow"])
            glRasterPos3f(window_width - 10*len(nameString) -15, 30 ,0 )
            drawString(nameString)
            glRasterPos3f(window_width - 10*len(styleString) -15, 50 ,0 )
            drawString(styleString)
            glRasterPos3f(window_width - 10*len(styleString) -15, 70 ,0 )
            drawString(radiusString)
            glRasterPos3f(window_width - 10*len(styleString) -15, 90 ,0 )
            drawString(arrowString)

    # Draw help hint or complete message
    if modeString == M_HELP :
        
        th = 20 # text height
        glColor3f(1.0,1.0,1.0)
        lc = 0
        for line in helptxt1 :
            glRasterPos3f(15, window_height*0.05 + th*lc,0 )
            drawString(line[:-1])
            lc += 1
        
        lc = 0
        for line in helptxt2 :
            glRasterPos3f(500, window_height*0.05 + th*lc,0 )
            drawString(line[:-1])
            lc += 1

    # get back the old prespective projection matrix
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    

    glEnable(GL_DEPTH_TEST) 
    glEnable(GL_DITHER)
    
    glFlush ()                              # // Flush The GL Rendering Pipeline
    #  since this is double buffered, swap the buffers to display what just got drawn. 
    glutSwapBuffers()

# Set the mode (INSERT, VISUAL, COMMAND, HELP)
def setMode( modeToSet ):
    
    global messageString, modeString, commandString, insPath, selPath
    global M_INSERT, M_HELP, M_COMMAND, M_VISUAL, M_DEFAULT

    glutSetCursor(GLUT_CURSOR_INHERIT)

    modeString = modeToSet

    if modeString == M_COMMAND :
        commandString = ""
        messageString = ""
    elif modeString == M_VISUAL :
        glutSetCursor(GLUT_CURSOR_CROSSHAIR)
    elif modeString == M_INSERT :
        selPath = insPath

    return

def keyPressed(*args):

    global insPath, selPath, pathCounter, grid
    global messageString, modeString, commandString
    global paths, cam, output_path, workfile
    global V_ZOOM_MODIFIER, V_HSTRAFE_MODIFIER, V_VSTRAFE_MODIFIER, V_ROTATE_MODIFIER 
    global KEY_STRAFE_LEFT, KEY_STRAFE_RIGHT, KEY_STRAFE_UP, KEY_STRAFE_DOWN, \
           KEY_ZOOM_IN, KEY_ZOOM_OUT, KEY_YAW_LEFT, KEY_YAW_RIGHT, \
           KEY_PITCH_UP, KEY_PITCH_DOWN, KEY_PLANE_UP, KEY_PLANE_DOWN, KEY_UNDO, \
           KEY_MODE_INSERT, KEY_MODE_VISUAL, KEY_MODE_COMMAND, KEY_MODE_DEFAULT, \
           KEY_GROW_GRID, KEY_SHRINK_GRID, \
           SAVE_EXT
    global M_INSERT, M_HELP, M_COMMAND, M_VISUAL, M_DEFAULT

    # Mode selection keys
    ##################################

    # : - Enter COMMAND mode  
    if ( args[0] == KEY_MODE_COMMAND and modeString != M_COMMAND ) :
        setMode(M_COMMAND)
    
    # v - Enter VISUAL mode
    elif ( args[0] == KEY_MODE_VISUAL and modeString != M_COMMAND ) :
        setMode(M_VISUAL)

    # i - Enter INSERT mode
    elif ( args[0] == KEY_MODE_INSERT and modeString != M_COMMAND) :
        setMode(M_INSERT)
    
    # Esc - Escape to DEFAULT mode 
    elif args[0] == KEY_MODE_DEFAULT :
        setMode(M_DEFAULT)

    # Mode-specific keys

    # COMMAND mode
    ##################################
    elif modeString == M_COMMAND :

        # Enter - Evaluate the entered command
        if args[0] == '\015' :
            
            print(("Command: %s" % commandString))

            if commandString == "q" :
                # Quit (prompt?)
                glutDestroyWindow(window)
                sys.exit()

            elif commandString == "h" or commandString == "help" :
                setMode(M_HELP) 

            elif commandString == "w" or commandString[:2] == "w\040":
                # Save to file
                # First word is 'w', next word assumed to 
                # be filename

                filename = workfile
                endname = commandString[2:] 

                writeOK = True

                if len(endname) != 0 :
                    # Currently just overwrite...
                    filename = output_path + endname 
                    if filename[-4:] == SAVE_EXT :
                        filename = filename[:-4]
                    elif filename[-3:] == ".py" :
                        filename = filename[:-3]
                    
                    for protected in OUTPUT_PROTECT :
        
                        if endname == protected or endname == (protected + ".py") :
                            messageString = "Writing failed: %s is a protected file"% endname 
                            writeOK = False
                            break

                    #if os.path.exists(filename + ".py") or os.path.exists(filename + SAVE_EXT):
                    #    # Prompt??
                    #    messageString = "Writing failed as filename(s) already exist(s)" 
                    #    writeOK = False

                if writeOK :
                    workfile = filename

                    # SAVE shelf file
                    #######################################
                    
                    try :
                        shelf = shelve.open(filename + SAVE_EXT)
                        shelf["paths"] = paths
                        shelf["pathCounter"] = pathCounter
                        shelf["camera"] = cam
                        shelf.close()
                    except :
                        messageString = "Writing to file %s.%s failed" % ( filename, SAVE_EXT )

                    # SAVE text file
                    #######################################

                    # Add the paths
                    pathsStrTxt = []
                    for path in paths :
                        pathsStrTxt.append(path.printAscii())

                    try :
                        FILE = open(filename + TXT_EXT,"w")   
                        FILE.writelines(pathsStrTxt)
                        FILE.close()
                    except :
                        messageString = "Writing to file %s.%s failed" % ( filename, TXT_EXT )
                    
                    # SAVE python file
                    #######################################

                    # File header
                    hdrStr = [
                        "#!/usr/bin/env python2\n\n",
                        "# NOTE:\n",
                        "# This python script was automatically generated by 'vertexer'.\n",
                        "# Do not manually edit - use vertexer to load the .vtx file instead.\n",
                        "# When run with python, this script will generate a POV-ray file,\n",
                        "# and attempt to run it with povray.\n\n",
                        "# toolshed module must exist in PYTHONPATH\n",
                        "import toolshed as ts\n\n",
                    ]

                    # Add the paths
                    pathsStr = []
                    for path in paths :
                        pathsStr.append(path.printPython())
                    pathsStr.append("\n")

                    # and the camera
                    camStr = []
                    camStr.append("""%s = [%f,%f,%f]\n"""%("camLocation",cam["posX"],cam["posY"],cam["posZ"])) 
                    camStr.append("""%s = [%f,%f,%f]\n"""%("camLookAt",cam["viewX"],cam["viewY"],cam["viewZ"])) 
                    camStr.append("\n")
                   
                    # feynRay lines
                    feynStr = []
                    feynStr.append("""ts.createPovFile("%s.pov",camLookAt=camLookAt,camLoc=camLocation,camUp=[0,0,1])\n"""%(filename))
                    for path in paths :
                        feynStr.append("""ts.%s(%s, name="%s:%s")\n"""%(path["style"],path["name"],path["style"],path["name"]))

                    # light now integrated as a path (each vertex is light source)
                    #feynStr.append("ts.pointLight()\n\n")
                    feynStr.append("ts.runPovFile()\n\n")

                    try :
                        FILE = open(filename + ".py","w")   
                        FILE.writelines(hdrStr)
                        FILE.writelines(pathsStr)
                        FILE.writelines(camStr)
                        FILE.writelines(feynStr)
                        FILE.close()
                        messageString = "Saved files as %s[%s,%s,.py]" % ( filename, SAVE_EXT, TXT_EXT )
                    except :
                        messageString = "Writing to files %s[%s,.py,%s] failed" % ( filename, SAVE_EXT, TXT_EXT )

                setMode(M_DEFAULT)
            
            elif commandString[:3] == "pov" :
                # Execute python .pov production 
                try :
                    filename = workfile + ".py"
                    # check if file exists
                    FILE = open(filename)
                    FILE.close()

                    from subprocess import call
                    call(["python2", filename])
                except IOError as e:
                    messageString = "Could not initiate povray as %s does not exist" % ( filename )
                
                setMode(M_DEFAULT)

            elif commandString[:2] == "e\040" :
                # Edit file
                # First word is 'e', next word assumed to 
                # be filename

                editOK = True
                # for now it looks in output directory
                filename = output_path + commandString[2:] 
                if filename[-4:] == SAVE_EXT :
                    filename = filename[:-4]
                shelf = shelve.open(filename + SAVE_EXT)
                try :
                    if not isinstance(shelf["camera"],Camera) or not isinstance(shelf["paths"],list) :
                        raise Exception
                except :
                    messageString = "Opening file %s for editing failed" % (filename + SAVE_EXT)
                    editOK = False

                if editOK :
                    cam = shelf["camera"]
                    paths = shelf["paths"]
                    pathCounter = shelf["pathCounter"]
                    messageString = "File %s successfully opened for editing" % (filename + SAVE_EXT)
                    workfile = filename
                
                shelf.close
                setMode(M_DEFAULT)

            elif commandString[:3] == "mv\040" :
                # rename selected path
                newName = commandString[3:]
                goodName = True
                
                if len(newName) > STR_PATH_MAXLEN :
                    goodName = False 
                    messageString = "Path name entered exceeds %d characters" % STR_PATH_MAXLEN
                elif not newName.isalnum() :
                    goodName = False
                    messageString = "Path name must be purely alphanumeric"
                else : 
                    for path in paths :
                        if path["name"] == newName :
                            goodName = False 
                            messageString = "Path name %s already exists" % newName 
                            break
                if goodName :
                    selPath["name"] = newName
                    messageString = "Path name changed to %s" % newName 
                setMode(M_DEFAULT)

            elif commandString[:3] == "ls\040" :
                # restyle selected path
                style = commandString[3:]
               
                if style in P_LINE_STYLES :
                    selPath["style"] = style
                    messageString = "Line style changed to %s" % style 
                else :
                    messageString = "Line style %s does not exists" % style 
                
                setMode(M_DEFAULT)

            elif commandString[:3] == "lr\040" :
                # change selected path radius
                radius = commandString[3:]
               
                try :
                    selPath["radius"] = float(radius)
                    messageString = "Line radius changed to %s" % float(radius)
                except ValueError :
                    messageString = "Line radius %s not valid float" % radius 
                
                setMode(M_DEFAULT)

            elif commandString[:2] == "rm" :
                # delete selected path
                if insPath == selPath :
                    insPath = None
                paths.remove(selPath)
                selPath = None
                hlPath = None
                setMode(M_DEFAULT)

            elif commandString[:5] == "reset" :
                # delete all paths
                paths = []
                insPath = None
                selPath = None
                hlPath  = None
                setMode(M_DEFAULT)

        # Backspace key deletes last character from command string
        elif args[0] == '\010' :
            if len(commandString) > 0 :
                commandString = commandString[:-1]

        # Else, register pressed keys
        else  :
            commandString += args[0]

    # INSERT mode
    ##################################
    elif modeString == M_INSERT :
          
        if args[0] == KEY_PLANE_DOWN :
            grid.shiftPlane(-1)
        elif args[0] == KEY_PLANE_UP :
            grid.shiftPlane(+1)
        elif args[0] == KEY_UNDO :
            if insPath is not None :
                if len(insPath) <= 1 :
                    paths.remove(insPath)
                    insPath = None
                else :
                    insPath.pop() 
    
    
    # VISUAL mode
    ##################################
    elif modeString == M_VISUAL :
        
        # Strafe left 
        if args[0] == KEY_STRAFE_LEFT :
            cam.hStrafe(-V_HSTRAFE_MODIFIER) 
        # Strafe right
        elif args[0] == KEY_STRAFE_RIGHT :
            cam.hStrafe(+V_HSTRAFE_MODIFIER) 
        # Strafe up 
        elif args[0] == KEY_STRAFE_UP :
            cam.vStrafe(+V_VSTRAFE_MODIFIER) 
        # Strafe down
        elif args[0] == KEY_STRAFE_DOWN :
            cam.vStrafe(-V_VSTRAFE_MODIFIER) 
        # Move forward 
        elif args[0] == KEY_ZOOM_IN :
            cam.zoom(+V_ZOOM_MODIFIER)
        # Move backward
        elif args[0] == KEY_ZOOM_OUT :
            cam.zoom(-V_ZOOM_MODIFIER)
        # Key-alternatives to mouse
        # Pitch up 
        elif args[0] == KEY_PITCH_UP :
            cam.pitch(-V_ROTATE_MODIFIER) 
        # Pitch down
        elif args[0] == KEY_PITCH_DOWN :
            cam.pitch(+V_ROTATE_MODIFIER) 
        # Global yaw left 
        elif args[0] == KEY_YAW_LEFT :
            cam.globalYaw(-V_ROTATE_MODIFIER)
        # Global yaw right
        elif args[0] == KEY_YAW_RIGHT :
            cam.globalYaw(+V_ROTATE_MODIFIER)
        # Global yaw right
        elif args[0] == KEY_GROW_GRID :
            xDim = grid["dimX"]
            yDim = grid["dimY"]
            zDim = grid["dimZ"]
            grid["dimX"] = xDim + 1 
            grid["dimY"] = yDim + 1 
            grid["dimZ"] = zDim + 1 
        # Global yaw right
        elif args[0] == KEY_SHRINK_GRID :
            xDim = grid["dimX"]
            yDim = grid["dimY"]
            zDim = grid["dimZ"]
            grid["dimZ"] = zDim - 1 
            # keep ratio (assuming zDim started life smaller)
            if grid["dimZ"] < zDim : 
                grid["dimX"] = xDim - 1 
                grid["dimY"] = yDim - 1 

    # update scene
    #DrawGLScene()
    glutPostRedisplay()
    return

def mouseDragged (cursor_x, cursor_y):
    """ Mouse cursor is moving
        Glut calls this function (when mouse button is down)
        and pases the mouse cursor postion in window coords as the mouse moves.
    """
    global mouseDragging, time
    global V_MOUSE_SENSITIVITY, V_ZOOM_MODIFIER 
    global M_VISUAL
    
    #if glutGet(GLUT_ELAPSED_TIME) - time < EVENT_MIN_TIME : 
    #    return
    #time = glutGet(GLUT_ELAPSED_TIME)

    # Divide functionality into modes
    
    # VISUAL 
    ##################################
    if modeString == M_VISUAL :

        if (mouseDragging):
            cam.mouseDrag(cursor_x, cursor_y, modifier=V_MOUSE_SENSITIVITY)

    # update scene
    #DrawGLScene()
    glutPostRedisplay()
    return

def mouseClicked (button, button_state, cursor_x, cursor_y):
    """ Mouse button clicked.
    """
    global mouseDragging, grid, insPath, selPath, pathCounter
    global M_INSERT, M_VISUAL
    global V_ZOOM_MODIFIER 

    #if glutGet(GLUT_ELAPSED_TIME) - time < EVENT_MIN_TIME : 
    #    return
    #time = glutGet(GLUT_ELAPSED_TIME)
    
    mouseDragging = False

    # Divide functionality into modes
    
    # INSERT mode
    ##################################
    if modeString == M_INSERT :

        if button == GLUT_LEFT_BUTTON :
            # left mouse button clicked
            if  button_state == GLUT_DOWN :
                if grid["pointerOn"] :
                    # vertex point to add
                    vertex = [grid["pointerX"],grid["pointerY"],grid["planeZ"]]

                    ## check if vertex already exists
                    if insPath is not None :
                       # check if same vertex clicked
                        if vertex[:3] == insPath["vertices"][-1][:3] :
                            # done with this path...
                            #paths.append(insPath) 
                            insPath = None
                            selPath = None
                        else : 
                            insPath.append(vertex)
                    else :
                        # create new path and add to list
                        pathName = "path%d" % pathCounter
                        pathCounter += 1
                        newPath = Path(pathName) 
                        newPath.append(vertex)
                        insPath = newPath
                        selPath = insPath

                        paths.append(newPath)
                        
        elif button == 3:
            # Scroll wheel up:
            if button_state == GLUT_DOWN :
                grid.shiftPlane(+1)

        elif button == 4:
            # Scroll wheel down:
            if button_state == GLUT_DOWN :
                grid.shiftPlane(-1)

    # VISUAL MODE
    ##################################
    elif modeString == M_VISUAL :
            
        if button == GLUT_LEFT_BUTTON :
            if  button_state == GLUT_DOWN :
                mouseDragging = True                
                cam["cursorX"] = cursor_x
                cam["cursorY"] = cursor_y
            elif button_state == GLUT_UP :
                mouseDragging = False

        elif button == 3:
            # Scroll wheel up:
            if button_state == GLUT_DOWN :
                cam.zoom(V_ZOOM_MODIFIER)

        elif button == 4:
            # Scroll wheel down:
            if button_state == GLUT_DOWN :
                cam.zoom(-V_ZOOM_MODIFIER)

    # VISUAL MODE
    ##################################
    elif modeString == M_DEFAULT :
        if hlPath is not None :
            selPath = hlPath
        
        glutPostRedisplay()

    # update scene
    #DrawGLScene()
    glutPostRedisplay()
    return

def mouseMoved ( cursor_x, cursor_y ) :
    
    global grid, hlPath
    global M_INSERT, M_DEFAULT
    #global EVENT_MIN_TIME

    #if glutGet(GLUT_ELAPSED_TIME) - time < EVENT_MIN_TIME : 
    #    return
    #time = glutGet(GLUT_ELAPSED_TIME)
   
    # INSERT mode
    ##################################
    if modeString == M_INSERT :
        grid["cursorX"] = cursor_x
        grid["cursorY"] = cursor_y
        
        glutPostRedisplay()
        
    # DEFAULT mode
    ##################################
    elif modeString == M_DEFAULT :
        # check for intersection of mouse with existing path

        # setup 3D world 
        glMatrixMode (GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(  cam["posX"],cam["posY"],cam["posZ"], \
                    cam["viewX"],cam["viewY"],cam["viewZ"], \
                    cam["upX"],cam["upY"],cam["upZ"])

        # find path to highlight 
        # iterate through paths
        hlPath = None
        for path in paths :
            # needed if we want bottom path 
            if hlPath is not None :
                break
            for vertex in path["vertices"] :
                try :
                    pX, pY = grid.pointerOnPlane(cursor_x, cursor_y, vertex[2])
                    if round(pX) == vertex[0] and round(pY) == vertex[1] :
                        hlPath = path                
                        break
                except : None

        glutPostRedisplay()

def main():
    global window

    glutInit(sys.argv)

    # Select type of Display mode:   
    #  Double buffer 
    #  RGBA color
    # Alpha components supported 
    # Depth buffer
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)

    # get a 640 x 480 window 
    glutInitWindowSize(800, 600)
    
    # the window starts at the upper left corner of the screen 
    glutInitWindowPosition(0, 0)

    # Okay, like the C version we retain the window id to use when closing, but for those of you new
    # to Python (like myself), remember this assignment would make the variable local and not global
    # if it weren't for the global declaration at the start of main.
    window = glutCreateWindow("Vertexer")

    # Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
    # set the function pointer and invoke a function to actually register the callback, otherwise it
    # would be very much like the C version of the code.    
    glutDisplayFunc(DrawGLScene)
    #glutDisplayFunc()

    # Uncomment this line to get full screen.
    # glutFullScreen()

    # When we are doing nothing, redraw the scene.
    # Is this needed if nothings moving?
    #glutIdleFunc(DrawGLScene)
        
    # Register the function called when our window is resized.
    glutReshapeFunc(ReSizeGLScene)

    # Register the function called when the keyboard is pressed.  
    glutKeyboardFunc(keyPressed)

    # GLUT When mouse buttons are clicked in window
    glutMouseFunc (mouseClicked)

    # GLUT When the mouse moves while clicked 
    glutMotionFunc (mouseDragged)

    # GLUT When mouse moves with no click
    glutPassiveMotionFunc (mouseMoved)

    # Initialize our window. 
    InitGL(800, 600)

    # Start Event Processing Engine 
    glutMainLoop()
    
if __name__ == "__main__":
    print("Type :q to quit.")
    main()
        
