from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from tkinter.simpledialog import *
from colorama import Fore, Style

try:
    from tkinterie.tkinterIE import WebView
except ImportError:
    print(Fore.RED + "Please Download tkinterie, install commnad: pip install tkinterie " + Style.RESET_ALL)
from Tki.KiCore import *
from Tki import *


class KiWidget(KiObject, KiPack, KiPlace):
    def __init__(self):
        super().__init__()
        try:
            self.Widget = Widget()
        except TypeError:
            pass

    def Init(self):
        self.SetRelief(Relief_Ridge)

    def SetMaster(self, Master):
        self.Widget.configure(master=Master)

    def SetState(self, State: str):
        self.Widget.configure(state=State)

    def SetRelief(self, Relief):
        self.Widget.configure(relief=Relief)

    def SetBackGround(self, Background):
        self.Widget.configure(background=Background)

    def SetBorder(self, Border):
        self.Widget.configure(Border)


class KiWindow(KiWidget):
    def __init__(self):
        super().__init__()
        self.Widget = Tk()
        self.SetTitle("Tki")
        self.Resize(500, 500)
        self.Init()

    def Attributes(self, Option: str, Value):
        self.Widget.attributes(Option, Value)

    def Maxmize(self, If: bool = True):
        self.Attributes(Window_Maximize, If)

    def Topmost(self, If: bool = True):
        self.Attributes(Window_Topmost, If)

    def Protocol(self, Name=None, Func=None):
        self.Widget.protocol(name=Name, func=Func)

    def SetMaxSize(self, Width, Height):
        self.Widget.maxsize(Width, Height)

    def SetMinSize(self, Width, Height):
        self.Widget.minsize(Width, Height)

    def SetTitle(self, Title: str):
        self.Widget.title(string=Title)

    def SetIcon(self, Icon):
        self.Widget.iconbitmap(bitmap=Icon)

    def Quit(self):
        self.Widget.quit()

    def Resize(self, Width: int, Height: int):
        self.Widget.geometry(f"{Width}x{Height}")

    def Center(self):
        X = round(int(self.GetScreenWidth()) / 2) + round(int(self.GetWidth()) / 2)
        Y = round(int(self.GetScreenHeight()) / 2) + round(int(self.GetHeight()) / 2)
        self.Move(X, Y)

    def Move(self, X: int = None, Y: int = None):
        self.Widget.geometry(f"+{X}+{Y}")

    def UpDate(self):
        self.Widget.update()

    def Run(self):
        self.MainLoop()


class KiToplevel(KiWidget):
    def __init__(self):
        super().__init__()
        self.Widget = Toplevel()
        self.SetTitle("Toplevel")
        self.Resize(500, 500)
        self.Init()

    def Attributes(self, Option: str, Value):
        self.Widget.attributes(Option, Value)

    def Maxmize(self, If: bool = True):
        self.Attributes(Window_Maximize, If)

    def Topmost(self, If: bool = True):
        self.Attributes(Window_Topmost, If)

    def Protocol(self, Name=None, Func=None):
        self.Widget.protocol(name=Name, func=Func)

    def SetMaxSize(self, Width, Height):
        self.Widget.maxsize(Width, Height)

    def SetMinSize(self, Width, Height):
        self.Widget.minsize(Width, Height)

    def SetTitle(self, Title: str):
        self.Widget.title(string=Title)

    def SetIcon(self, Icon):
        self.Widget.iconbitmap(bitmap=Icon)

    def Quit(self):
        self.Widget.quit()

    def Resize(self, Width: int, Height: int):
        self.Widget.geometry(f"{Width}x{Height}")

    def Center(self):
        X = round(int(self.GetScreenWidth()) / 2) + round(int(self.GetWidth()) / 2)
        Y = round(int(self.GetScreenHeight()) / 2) + round(int(self.GetHeight()) / 2)
        self.Move(X, Y)

    def Move(self, X: int = None, Y: int = None):
        self.Widget.geometry(f"+{X}+{Y}")

    def UpDate(self):
        self.Widget.update()

    def Run(self):
        self.MainLoop()


class KiScrollBar(KiWidget):
    def __init__(self, Master: KiWidget = None,
                 Background: str = "white", ActiveBackground: str = "black", Relief: str = Relief_Flat,
                 Orient: str = Orient_Vertical,
                 Width=0):
        super().__init__()
        self.Widget = Scrollbar(master=Master, background=Background, activebackground=ActiveBackground, relief=Relief,
                                width=Width, orient=Orient)

    def Configure(self, Background: str = Always, ActiveBackground: str = Always, Relief: str = Always,
                  Width=Always):
        if Background == Always:
            self.Widget.configure(background=self.CGet("background"))
        else:
            self.Widget.configure(background=Background)
        if ActiveBackground == Always:
            self.Widget.configure(activebackground=self.CGet("activebackground"))
        else:
            self.Widget.configure(activebackground=ActiveBackground)
        if Relief == Always:
            self.Widget.configure(relief=self.CGet("relief"))
        else:
            self.Widget.configure(xscrollcommand=XScroll)
        if Width == Always:
            self.Widget.configure(width=self.CGet("width"))
        else:
            self.Widget.configure(width=Width)

    def SetValue(self, First, Last):
        self.Widget.set(first=First, last=Last)

    def GetValue(self):
        return self.Widget.get()


class KiTextView(KiWidget):
    def __init__(self, Master: KiWidget = None,
                 SelectBackground: str = "blue", SelectForeground: str = "white",
                 Background: str = "white", Foreground: str = "black", XScroll: KiScrollBar = None,
                 Relief: str = Relief_Flat,
                 YScroll: KiScrollBar = None, Wrap: str = Wrap_Char, Font=None,
                 Width=0):
        super().__init__()
        self.Widget = Text(master=Master, selectbackground=SelectBackground, selectforeground=SelectForeground,
                           relief=Relief,
                           background=Background, foreground=Foreground, wrap=Wrap, font=Font,
                           xscrollcommand=XScroll, yscrollcommand=YScroll, width=Width)
        self.Master = Master
        self.SelectBackground = SelectBackground
        self.SelectForeground = SelectForeground
        self.Background = Background
        self.Foreground = Foreground
        self.XScroll = XScroll
        self.YScroll = YScroll
        self.Relief = Relief
        self.Wrap = Wrap
        self.Width = Width

    def Configure(self, SelectBackground: str = Always, SelectForeground: str = Always,
                  Background: str = Always, Foreground: str = Always, XScroll: KiScrollBar = Always,
                  Relief: str = Always,
                  YScroll: KiScrollBar = Always, Wrap: str = Always, Font=Always,
                  Width=Always):
        if SelectBackground == Always:
            self.Widget.configure(selectbackground=self.CGet("selectbackground"))
        else:
            self.Widget.configure(selectbackground=SelectBackground)
        if SelectForeground == Always:
            self.Widget.configure(selectforeground=self.CGet("selectforeground"))
        else:
            self.Widget.configure(selectforeground=SelectForeground)
        if Background == Always:
            self.Widget.configure(background=self.CGet("background"))
        else:
            self.Widget.configure(background=Background)
        if Foreground == Always:
            self.Widget.configure(foreground=self.CGet("foreground"))
        else:
            self.Widget.configure(foreground=Foreground)
        if XScroll == Always:
            self.Widget.configure(xscrollcommand=self.CGet("xscrollcommnad"))
        else:
            self.Widget.configure(xscrollcommand=XScroll)

        if YScroll == Always:
            self.Widget.configure(yscrollcommand=self.CGet("yscrollcommand"))
        else:
            self.Widget.configure(yscrollcommand=YScroll)
        if Relief == Always:
            self.Widget.configure(relief=self.CGet("relief"))
        else:
            self.Widget.configure(relief=Relief)
        if Wrap == Always:
            self.Widget.configure(wrap=self.CGet("wrap"))
        else:
            self.Widget.configure(wrap=Wrap)
        if Width == Always:
            self.Widget.configure(width=self.CGet("width"))
        else:
            self.Widget.configure(width=Width)

        self.Widget.configure(master=Master, selectbackground=SelectBackground, selectforeground=SelectForeground,
                              relief=Relief,
                              background=Background, foreground=Foreground, wrap=Wrap, font=Font,
                              xscrollcommand=XScollBar, yscrollcommand=YScroll, width=Width)

    def WidgetCreate(self, Index, Widget: KiWidget):
        self.Widget.window_create(index=Index, window=Widget)

    def WidgetConfigure(self, Index):
        self.Widget.window_configure(index=Index)

    def WidgetCGet(self, Index):
        return self.Widget.window_cget(index=Index)

    def TagConfig(self, TagName: str, Start: str, End: str = None, Background="white", Foreground="black",
                  BorderWidth: int = 0, Justify: str = Jusitfy_Left, Font=None):
        self.Widget.tag_config(tagName=TagName, index1=Start, index2=End, background=Background, foreground=Foreground,
                               borderwidth=BorderWidth, justify=Justify, font=Font)

    def TagAdd(self, TagName: str, Start: str, End: str = None, Background="white", Foreground="black",
               BorderWidth: int = 0, Justify: str = Jusitfy_Left, Font=None):
        self.Widget.tag_add(tagName=TagName, index1=Start, index2=End, background=Background, foreground=Foreground,
                            borderwidth=BorderWidth, justify=Justify, font=Font)

    def TagRemove(self, TagName: str, Start: str, End: str = None):
        self.Widget.tag_remove(tagName=TagName, index1=Start, index2=End)

    def TagBind(self, TagName: str, Sequence, Func):
        return self.Widget.tag_bind(tagName=TagName, sequence=Sequence, func=Func)

    def TagRanges(self, TagName: str):
        self.Widget.tag_ranges(tagName=TagName)

    def TagUnBind(self, TagName: str, Sequence, FuncId=None):
        self.Widget.tag_unbind(tagName=TagName, sequence=Sequence, funcid=FuncId)

    def TagDelete(self, TagName: str):
        self.Widget.tag_delete(TagName)

    def TagCGet(self, TagName: str, Option):
        self.Widget.tag_cget(tagName=TagName, option=Option)

    def Edit(self, Flag):
        self.Widget.edit(Flag)

    def EditUndo(self):
        self.Widget.edit_undo()

    def EditRedo(self):
        self.Widget.edit_redo()

    def EditModified(self):
        self.Widget.edit_modified()

    def EditSeparator(self):
        self.Widget.edit_separator()

    def EditReset(self):
        self.Widget.edit_reset()

    def Delete(self, Start: str, End: str = None):
        self.Widget.delete(index1=Start, index2=End)

    def Insert(self, Index: str, Chars: str = None):
        self.Widget.insert(index=Index, chars=Chars)

    def See(self, Index: str):
        self.Widget.see(Index)

    def Search(self, String: str, Index: str, StopIndex=End):
        self.Widget.search(pattern=String, index=Index, stopindex=StopIndex)

    def Clear(self):
        self.Widget.delete()

    def Get(self, Start: str, End: str = None):
        self.Widget.get(index1=Start, index2=End)


class KiButton(KiWidget):
    def __init__(self, Master: KiWidget = None, Text: str = EmptyString, Command=EmptyFunc,
                 ActiveBackground: str = "white", ActiveForeground: str = "black", Font=None, Relief: str = Relief_Flat,
                 Background: str = "white", Foreground: str = "black", Justify: str = Jusitfy_Center,
                 Width=0):
        super().__init__()
        self.Widget = Button(master=Master, text=Text, command=Command,
                             activebackground=ActiveBackground, activeforeground=ActiveForeground, relief=Relief,
                             background=Background, foreground=Foreground, justify=Justify, font=Font,
                             width=Width)
        self.Init()

    def SetText(self, Text):
        self.Configure(Text=Text)

    def SetCommand(self, Func):
        self.Configure(Command=Func)

    def Configure(self, Text: str = Always, Command=Always,
                  ActiveBackground: str = Always, ActiveForeground: str = Always,
                  Background: str = Always, Foreground: str = Always, Justify: str = Always,
                  Width=Always):
        if ActiveBackground == Always:
            self.Widget.configure(activebackground=self.CGet("activebackground"))
        else:
            self.Widget.configure(activebackground=ActiveBackground)
        if ActiveForeground == Always:
            self.Widget.configure(activeforeground=self.CGet("activeforeground"))
        else:
            self.Widget.configure(activeforeground=ActiveForeground)
        if Background == Always:
            self.Widget.configure(background=self.CGet("background"))
        else:
            self.Widget.configure(background=Background)
        if Foreground == Always:
            self.Widget.configure(foreground=self.CGet("foreground"))
        else:
            self.Widget.configure(foreground=Foreground)
        if Text == Always:
            self.Widget.configure(text=self.CGet("text"))
        else:
            self.Widget.configure(text=Text)
        if Command == Always:
            self.Widget.configure(command=self.CGet("command"))
        else:
            self.Widget.configure(command=Command)
        if Justify == Always:
            self.Widget.configure(justify=self.CGet("justify"))
        else:
            self.Widget.configure(justify=Justify)
        if Width == Always:
            self.Widget.configure(width=self.CGet("width"))
        else:
            self.Widget.configure(width=Width)

    def Flash(self):
        self.Widget.flash()


class KiEntry(KiWidget):
    def __init__(self, Master: KiWidget = None, Text: str = EmptyString,
                 Background: str = "white", Foreground: str = "black", Font=None,
                 Justify: str = Jusitfy_Left, Width=0):
        super().__init__()
        self.Text = KiStringVar()
        self.Widget = Entry(master=Master, textvariable=self.Text.Get(), background=Background, foreground=Foreground,
                            font=Font,
                            justify=Justify, width=Width)
        self.SetText(Text)

    def Configure(self, Text: str = Always,
                  Background: str = Always, Foreground: str = Always, Font=Always,
                  Justify: str = Always, Width=Always):
        if Text == Always:
            self.SetText(self.CGet("textvariable").set(Text))
        else:
            self.SetText(Text)
        if Background == Always:
            self.Widget.configure(background=self.CGet("background"))
        else:
            self.Widget.configure(background=Background)
        if Foreground == Always:
            self.Widget.configure(foreground=self.CGet("foreground"))
        else:
            self.Widget.configure(foreground=Foreground)
        if Font == Always:
            self.Widget.configure(font=self.CGet("font"))
        else:
            self.Widget.configure(font=Font)
        if Justify == Always:
            self.Widget.configure(justify=self.CGet("justify"))
        else:
            self.Widget.configure(justify=Justify)
        if Width == Always:
            self.Widget.configure(width=self.CGet("width"))
        else:
            self.Widget.configure(width=Width)

    def SetText(self, Text):
        self.Text.SetVar(Text)

    def GetText(self):
        return self.Text.GetVar()


class KiFrame(KiWidget):
    def __init__(self, Master: KiWidget = None, Background: str = "white",
                 Padx=0, Pady=0, Relief: str = Relief_Sunken,
                 Width=0):
        super().__init__()
        self.Widget = Frame(master=Master, background=Background, width=Width,
                            padx=Padx, pady=Pady)

    def Configure(self, Background: str = Always,
                  Padx=Always, Pady=Always, iPadx=Always, iPady=Always, Relief: str = Always,
                  Width=Always):
        if Background == Always:
            self.Widget.configure(background=self.CGet("background"))
        else:
            self.Widget.configure(background=Background)
        if Padx == Always:
            self.Widget.configure(padx=self.CGet("padx"))
        else:
            self.Widget.configure(padx=Padx)
        if Pady == Always:
            self.Widget.configure(pady=self.CGet("pady"))
        else:
            self.Widget.configure(pady=Pady)
        if Relief == Always:
            self.Widget.configure(relief=self.CGet("relief"))
        else:
            self.Widget.configure(relief=Relief)
        if Width == Always:
            self.Widget.configure(width=self.CGet("width"))
        else:
            self.Widget.configure(width=Width)


class KiMessage(KiWidget):
    def __init__(self, Master: KiWidget = None, Text: str = EmptyString,
                 ActiveBackground: str = "white", ActiveForeground: str = "black",
                 Background: str = "white", Foreground: str = "black", Justify: str = Jusitfy_Center, Font=None,
                 Width=0):
        super().__init__()
        self.Widget = Message(master=Master, text=Text, background=Background, foreground=Foreground, justify=Justify,
                              font=Font,
                              width=Width)

    def Configure(self, Master: KiWidget = None, Text: str = EmptyString,
                  ActiveBackground: str = "white", ActiveForeground: str = "black",
                  Background: str = "white", Foreground: str = "black", Justify: str = Jusitfy_Center,
                  Width=0):
        self.Widget.configure(master=Master, text=Text, background=Background, foreground=Foreground,
                              justify=Justify, width=Width)

    def SetText(self, Text):
        self.Configure(Text=Text)


class KiMDI(KiFrame):
    def __init__(self, Master: KiWidget = None, Background: str = "#808080",
                 Padx=0, Pady=0, iPadx=0, iPady=0, Relief: str = Relief_Sunken,
                 Width=0):
        super().__init__()
        self.Widget = Frame(master=Master, background=Background, width=Width,
                            padx=Padx, pady=Pady)


class KiTEntry(KiWidget):
    def __init__(self, Master: KiWidget = None, Text: str = EmptyString, Font=None,
                 Justify: str = Jusitfy_Left, Width=0):
        super().__init__()
        self.Text = KiStringVar()
        self.Widget = ttk.Entry(master=Master, textvariable=self.Text.Get(), justify=Justify, width=Width, font=Font)
        self.SetText(Text)

    def Configure(self, Text: str = Always, Font=Always, Style: str = Always, Width=Always, Justify: str = Always):
        if Text == Always:
            self.SetText(self.CGet("textvariable").set(Text))
        else:
            self.SetText(Text)
        if Font == Always:
            self.Widget.configure(font=self.CGet("font"))
        else:
            self.Widget.configure(font=Font)
        if Style == Always:
            self.Widget.configure(style=self.CGet("style"))
        else:
            self.Widget.configure(style=Style)
        if Justify == Always:
            self.Widget.configure(justify=self.CGet("justify"))
        else:
            self.Widget.configure(justify=Justify)
        if Width == Always:
            self.Widget.configure(width=self.CGet("width"))
        else:
            self.Widget.configure(width=Width)

    def SetText(self, Text):
        self.Text.SetVar(Text)

    def GetText(self):
        return self.Text.GetVar()


class KiTButton(KiWidget):
    def __init__(self, Master: KiWidget = None, Text: str = EmptyString, Command=EmptyFunc, Style: str = None,
                 Width=0):
        super().__init__()
        self.Widget = ttk.Button(master=Master, text=Text, command=Command,
                                 width=Width, style=Style)

    def Configure(self, Text: str = Always, Command=Always, Style: str = Always,Width=Always):
        if Text == Always:
            self.Widget.configure(text=self.CGet("text"))
        else:
            self.Widget.configure(text=Text)
        if Command == Always:
            self.Widget.configure(command=self.CGet("command"))
        else:
            self.Widget.configure(command=Command)
        if Style == Always:
            self.Widget.configure(style=self.CGet("style"))
        else:
            self.Widget.configure(style=Style)
        if Width == Always:
            self.Widget.configure(width=self.CGet("width"))
        else:
            self.Widget.configure(width=Width)

    def SetAccent(self):
        self.Configure(Style="Accent.TButton")

    def SetText(self, Text):
        self.Configure(Text=Text)

    def SetCommand(self, Func):
        self.Configure(Command=Func)

    def Flash(self):
        self.Widget.flash()


class KiTFrame(KiWidget):
    def __init__(self, Master: KiWidget = None, Relief: str = Relief_Sunken, Width=0, Style: str = None):
        super().__init__()
        self.Widget = ttk.Frame(master=Master, relief=Relief, width=Width, style=Style)

    def Configure(self, Relief: str = Relief_Sunken, Style: str = None, Width=0):
        if Relief == Always:
            self.Widget.configure(relief=self.CGet("relief"))
        else:
            self.Widget.configure(relief=Relief)
        if Style == Always:
            self.Widget.configure(style=self.CGet("style"))
        else:
            self.Widget.configure(style=Style)
        if Width == Always:
            self.Widget.configure(width=self.CGet("width"))
        else:
            self.Widget.configure(width=Width)


class KiSideBar(KiFrame):
    def __init__(self, Master: KiWidget = None, ActiveBackground: str = "white", ActiveForeground: str = "black",
                 Background: str = "white", Foreground: str = "black", Justify: str = Jusitfy_Center,
                 Padx=0, Pady=0, iPadx=0, iPady=0,
                 Width=0):
        super().__init__()
        self.Widget = KiFrame(Master=Master.GetWidget(), ActiveBackground=ActiveBackground,
                              ActiveForeground=ActiveForeground,
                              Background=Background, Foreground=Foreground, Justify=Justify,
                              Width=Width, Padx=Padx, Pady=Pady, iPadx=iPadx, iPady=iPady)

    def Put(self, Side=SideBarSide_Left,
            Padx: int = 0, Pady: int = 0, iPadx: int = 0, iPady: int = 0, ):
        self.Widget.PackWidget(Side=Side, Fill=Fill_Y, Padx=Padx, Pady=Pady, iPadx=iPadx, iPady=iPady)


class KiWebViewIE(KiFrame):
    def __init__(self, Master: KiWidget, Width, Height, Url):
        super().__init__()
        self.Widget = WebView(Master.GetWidget(), Width, Height, Url)


class KiMessgaeBox(KiWindow):
    def __init__(self):
        super().__init__()
        self.Widget = Message()

    def ShowInfo(self, Title: str = "Info", Message: str = "This is a info dialog", Icon: str = Message_Icons_INFO,
                 Parent=None):
        return showinfo(title=Title, message=Message, icon=Icon, parent=Parent)

    def ShowError(self, Title: str = "Error", Message: str = "This is a error dialog", Icon: str = Message_Icons_ERROR,
                  Parent=None):
        return showerror(title=Title, message=Message, icon=Icon, parent=Parent)

    def ShowWarning(self, Title: str = "Warning", Message: str = "This is a warning dialog",
                    Icon: str = Message_Icons_WARNING, Parent=None):
        return showwarning(title=Title, message=Message, icon=Icon, parent=Parent)

    def AskYesNo(self, Title: str = "Ask", Message: str = "This is a yesno dialog", Icon: str = Message_Icons_QUESTION,
                 Parent=None):
        return askyesno(title=Title, message=Message, icon=Icon, parent=Parent)

    def AskOkCanel(self, Title: str = "Warning", Message: str = "This is a okcanel dialog",
                   Icon: str = Message_Icons_QUESTION, Parent=None):
        return askokcancel(title=Title, message=Message, icon=Icon, parent=Parent)

    def AskQuestion(self, Title: str = "Warning", Message: str = "This is a question dialog",
                    Icon: str = Message_Icons_QUESTION, Parent=None):
        return askquestion(title=Title, message=Message, icon=Icon, parent=Parent)

    def AskRetryCanel(self, Title: str = "Warning", Message: str = "This is a retrycanel dialog",
                      Icon: str = Message_Icons_QUESTION, Parent=None):
        return askretrycancel(title=Title, message=Message, icon=Icon, parent=Parent)

    def AskYesNoCanel(self, Title: str = "Warning", Message: str = "This is a yesnocanel dialog",
                      Icon: str = Message_Icons_QUESTION, Parent=None):
        return askyesnocancel(title=Title, message=Message, icon=Icon, parent=Parent)


class KiMessgaeSimple(KiWindow):
    def AskFloat(self, Title: str = "ask float", Prompt: str = "plase entry float"):
        return askfloat(title=Title, prompt=Prompt)

    def AskInteger(self, Title: str = "ask integer", Prompt: str = "plase entry integer"):
        return askinteger()

    def AskString(self, Title: str = "ask string", Prompt: str = "plase entry string"):
        return askstring()
