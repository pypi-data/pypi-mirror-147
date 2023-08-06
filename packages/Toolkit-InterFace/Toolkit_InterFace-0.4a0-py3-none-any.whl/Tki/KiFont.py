from tkinter.font import *


class KiFont(object):
    def __init__(self, Root=None, Family: str = "Cascadia Mono", Size: int = 10, Weight: str = "light"):
        self.Widget = Font(root=Root, family=Family, size=Size, weight=Weight)

    def Families(self, Root=None):
        return families(root=Root)

    def CGet(self, Option):
        self.Widget.cget(option=Option)

    def Config(self, Root=None, Family: str = "Cascadia Mono", Size: int = 10, Weight: str = "light"):
        self.Widget.config(root=Root, family=Family, size=Size, weight=Weight)

    def GetFont(self):
        return self.Widget