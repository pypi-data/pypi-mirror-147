from tkinter import *
import tkinter

def EmptyFunc():
    pass

EmptyString = ""


Always = "Always"

# icons
Message_Icons_ERROR = "error"
Message_Icons_INFO = "info"
Message_Icons_QUESTION = "question"
Message_Icons_WARNING = "warning"

# types
Message_Type_ABORTRETRYIGNORE = "abortretryignore"
Message_Type_OK = "ok"
Message_Type_OKCANCEL = "okcancel"
Message_Type_RETRYCANCEL = "retrycancel"
Message_Type_YESNO = "yesno"
Message_Type_YESNOCANCEL = "yesnocancel"

# replies
Message_ABORT = "abort"
Message_RETRY = "retry"
Message_IGNORE = "ignore"
Message_OK = "ok"
Message_CANCEL = "cancel"
Message_YES = "yes"
Message_NO = "no"

# Edit
Edit_Modified = "edit_modified"
Edit_Undo = "edit_undo"
Edit_Redo = "edit_redo"
Edit_Reset = "edit_reset"
Edit_Separator = "edit_separator"
Insert = INSERT
End = END

# Warp
Wrap_Word = WORD
Wrap_Char = CHAR
Wrap_None = NONE

# TtkStyle
Style_SunValley = "Style-SunValley"
Style_Azure = "Style-Azure"
Style_File = "Style-File"
Theme_Light = "light"
Theme_Dark = "dark"
Button_Accent = "Accent.TButton"

# SideBarSide
SideBarSide_Left = LEFT
SideBarSide_Right = RIGHT

# Attributes
Window_Maximize = "-fullscreen"
Window_Topmost = "-topmost"
Window_Delete = "WM_DELETE_WINDOW"
Window_Save_YouSelf = "WM_SAVE_YOURSELF"

# Orient
Orient_Horizontal = HORIZONTAL
Orient_Vertical = VERTICAL

# Relief "raised", "sunken", "flat", "ridge", "solid", "groove"
Relief_Raised = RAISED
Relief_Sunken = SUNKEN
Relief_Flat = FLAT
Relief_Ridge = RIDGE
Relief_Solid = SOLID
Relief_Groove = GROOVE

# Jusitfy "left", "center", "right"
Jusitfy_Left = LEFT
Jusitfy_Center = CENTER
Jusitfy_Right = RIGHT

# Anchor "nw", "n", "ne", "w", "center", "e", "sw", "s", "se"
Anchor_Nw = NW
Anchor_N = N
Anchor_Ne = NE
Anchor_W = W
Anchor_Center = CENTER
Anchor_E = E
Anchor_Sw = SW
Anchor_S = S
Anchor_Se = SE

# Fill "none", "both", "x", "y"
Fill_None = NONE
Fill_BOTH = BOTH
Fill_X = X
Fill_Y = Y

# Expand "yes", "no"
Expand_YES = YES
Expand_NO = NO

# Side "left", "right", "top", "bottom"
Side_Left = LEFT
Side_Right = RIGHT
Side_Top = TOP
Side_Bottom = BOTTOM

# Bind

class KiVar(object):
    def SetVar(self, Value):
        self.Widget.set(Value)

    def GetVar(self):
        return self.Widget.get()

    @property
    def Var(self):
        return self.Widget

    def Get(self):
        return self.Widget


class KiStringVar(KiVar):
    def __init__(self):
        self.Widget = StringVar()


class KiIntVar(KiVar):
    def __init__(self):
        self.Widget = IntVar()


class KiBooleanVar(KiVar):
    def __init__(self):
        self.Widget = BooleanVar()