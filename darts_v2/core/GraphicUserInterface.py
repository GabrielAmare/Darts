from tkinter import *

from tools import ImageService

from .Application import Application


class FullScreenBinded(Tk):
    def __init__(self, default_full_screen: bool = False):
        super().__init__()
        self.full_screen = default_full_screen

        self.bind("<F11>", self.toggle_fullScreen)
        self.bind("<Escape>", self.quit_fullScreen)

    def toggle_fullScreen(self, _):
        self.full_screen = not self.full_screen

    def quit_fullScreen(self, _):
        self.full_screen = False

    @property
    def full_screen(self):
        return self._full_screen

    @full_screen.setter
    def full_screen(self, value):
        self._full_screen = value
        self.attributes("-fullscreen", value)


class FrameContainer(Frame):
    def __init__(self, root, app: Application, **cfg):
        super().__init__(root, **cfg)
        self.app: Application = app

    def new(self, cls, styles=None, **config):
        if styles is None:
            styles = []

        if issubclass(cls, FrameContainer):
            widget = cls(root=self, app=self.app, **config)
        else:
            widget = cls(self, **config)

        self.app.apply_graphic_style(widget, *styles)

        return widget


class ImageLabel(Label):
    def __init__(self, root, path: str, **cfg):
        super().__init__(root, **cfg)
        self.path = path

    def set(self, name: str):
        fp = f"{self.path}\\{name}.png"
        image = ImageService.get(fp, size=(48, 48))
        self.configure(image=image)
        self.update_idletasks()


class Header(FrameContainer):
    def __init__(self, root, app: Application, **cfg):
        super().__init__(root, app, **cfg)

        self.logo = self.new(
            cls=Label,
            image=ImageService.load(app.images_fp + "app-logo.png", (48, 48)),
            styles=["logo"]
        )
        self.name = self.new(
            cls=Label,
            text=app.app_name, padx=40,
            styles=["name", "font-lg"]
        )

        self.vi_icon = self.new(
            cls=Label,
            styles=[]
        )
        self.vi_text = self.new(
            cls=Label,
            text="",
            styles=["font-md"]
        )

        self.app.map_to("feedback_icon", self)
        self.app.map_to("feedback_text", self)

        self.feedback_icon = "neutral"
        self.feedback_text = ""

        self.logo.pack(side=LEFT, fill=Y)
        self.name.pack(side=LEFT, fill=BOTH, expand=True)
        self.vi_icon.pack(side=LEFT, fill=Y, padx=40)
        self.vi_text.pack(side=LEFT, fill=BOTH, expand=True)

    @property
    def feedback_icon(self):
        return self._fb_icon_state

    @feedback_icon.setter
    def feedback_icon(self, value):
        self._fb_icon_state = value
        image = ImageService.load(self.app.images_fp + "vi/" + value + ".png", (48, 48))
        self.vi_icon.configure(image=image)
        self.vi_icon.update_idletasks()

    @property
    def feedback_text(self):
        return self._feedback_text

    @feedback_text.setter
    def feedback_text(self, value):
        self._feedback_text = value
        self.vi_text.configure(text=value)
        self.vi_text.update_idletasks()


class GraphicUserInterface(FullScreenBinded):
    def __init__(self, app: Application):
        super().__init__(default_full_screen=app.production)
        self.app: Application = app

        self.title(f"{app.app_name} - {app.version.major}.{app.version.minor}.{app.version.patch}")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        self.tk.call('wm', 'iconphoto', self._w, ImageService.load(app.images_fp + "app-logo.png"))

        app.apply_graphic_style(self)

        self.header = Header(self, app=app, height=48)
        self.header.pack(side=TOP, anchor=NW)
        app.apply_graphic_style(self.header)

    def destroy(self):
        self.app.save()
        super().destroy()
