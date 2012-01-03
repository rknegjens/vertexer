# Config file for Vertexer

#  This file is part of:
#  " Vertexer "
#  by Rob Knegjens


# Keys
#######

# Mode selection
KEY_MODE_COMMAND = ':'
KEY_MODE_INSERT  = 'i'
KEY_MODE_VISUAL  = 'v'
KEY_MODE_DEFAULT = '\033'

# Insert mode
KEY_PLANE_UP     = 'k'
KEY_PLANE_DOWN   = 'j'
KEY_UNDO         = 'u'

# Visual mode
KEY_STRAFE_LEFT  = 'a'
KEY_STRAFE_RIGHT = 'd'
KEY_STRAFE_UP    = 'w'
KEY_STRAFE_DOWN  = 's'
KEY_ZOOM_IN      = 'e'
KEY_ZOOM_OUT     = 'q'
KEY_YAW_LEFT     = 'h'
KEY_YAW_RIGHT    = 'l'
KEY_PITCH_UP     = 'k'
KEY_PITCH_DOWN   = 'j'
KEY_GROW_GRID    = '+'
KEY_SHRINK_GRID  = '-'

# Vertexer
###########

# mode strings
# the following MUST be unique w.r.t to each other!
M_DEFAULT = ""
M_COMMAND = "-- COMMAND --"
M_INSERT = "-- INSERT --"
M_VISUAL = "-- VISUAL --"
M_HELP = "-- HELP --"
# Mode to startup with:
M_STARTUP = M_HELP
M_STARTUP_MODE = "HELP" # temp
M_DEFAULT_MODE = "INSERT" # temp

SAVE_EXT = ".vtx"
TXT_EXT = ".txt"

V_HSTRAFE_MODIFIER = 0.3 # modifier for horizontal strafe in visual mode
V_VSTRAFE_MODIFIER = 0.4 # modifier for vertical strafe in visual mode
V_ROTATE_MODIFIER = 0.4 # modifier for key-rotating in visual mode
V_ZOOM_MODIFIER = 1.5 # modifier for zooming in visual mode
V_MOUSE_SENSITIVITY = 0.5

# selection angle (radians)
D_SELECT_ANGLE = 10.*(3.14159/180.)

# filenames to protect from being overridden in output directory
OUTPUT_PROTECT = ["toolshed", "vectors"]

# Grid class
#############

DEF_DIM_X = 25  # default dimension of grid cube
DEF_DIM_Y = 25
DEF_DIM_Z = 12
MIN_DIM = 5 
MAX_DIM = 1000

GRID_LEN_UNIT = 1.0 # scale size of grid

# STRINGS
##########



STR_STARTUP_MSG = "Type %s for help, %s to quit and %s or %s to enter INSERT or VISUAL mode"\
        % (KEY_MODE_COMMAND+ 'h', KEY_MODE_COMMAND + 'q', KEY_MODE_INSERT, KEY_MODE_VISUAL)

STR_PATH_MAXLEN = 10

# DRAWING
##########

D_INS_RGB = [1.,1.,0.]
D_SEL_RGB = [1.,0.,1.]
D_NRM_RGB = [0.,1.,1.]
D_SEL_RAD = 3.0
D_NRM_RAD = 0.5

# PATHS
########

P_LINE_STYLES = ["line","curve","wiggle","helix","light"]
