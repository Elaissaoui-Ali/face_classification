import tkinter as tk
from tkinter import ttk, filedialog, Widget
import face_reco as fr
import os
from PIL import Image, ImageTk

from my_os import Folder


class FindEntry(ttk.Entry):
    def __init__(self, master):
        super().__init__(master=master)
        self.config(width=60)
        self.directory = os.getcwd()
        self.set_directory(self.directory)

    def set_directory(self, directory):
        self.directory = directory
        self.delete(0, tk.END)
        self.insert(0, directory)


class FindBt(ttk.Button):
    def __init__(self, master):
        super().__init__(master=master)
        self.master = master
        self.config(text="...", command=self.onClick)

    def onClick(self):
        for item in self.master.winfo_children():
            if isinstance(item, FindEntry):
                directory = filedialog.askdirectory(initialdir=item.directory)
                if directory != "":
                    item.set_directory(directory)
                break


class DirectoryFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        label = ttk.Label(self, text="Pictures' Folder : ")
        label.pack()
        search_entry = FindEntry(self)
        search_entry.pack()
        search_bt = FindBt(self)
        search_bt.pack()


class CheckBt(ttk.Checkbutton):
    def __init__(self, master):
        super().__init__(master)
        self.config(text=" Use names to label faces.")
        self.check = tk.StringVar()
        self.check.set("False")
        self.config(variable=self.check, onvalue="True", offvalue="False")


class ChoiceFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        checkBt = CheckBt(self)
        checkBt.pack()


class InfoLabel(ttk.Label):
    def __init__(self, master):
        super().__init__(master)
        self.config(text="INFO : Click on Scan! ")


class InfoFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        infoLabel = InfoLabel(self)
        infoLabel.pack()


class LabelingBt(ttk.Button):
    def __init__(self, master):
        super().__init__(master)
        self.config(text="Next", command=self.onClick, state="disabled")
        self.imageLabel = None
        self.faces_exist = None
        self.labelingEntry = None
        self.classifyBt = None
        self.count = 0

    def onClick(self):

        length = len(self.faces_exist)
        if self.count < length:
            self.faces_exist[self.count].name = self.labelingEntry.get()
            self.labelingEntry.delete(0, tk.END)
            self.count += 1
        if self.count < length:
            self.imageLabel.set_image(self.faces_exist[self.count].pil_image)
        if self.count >= length:
            self.config(state="disable")
            self.labelingEntry.config(state="disable")
            self.classifyBt.config(state="!disable")
            self.classifyBt.faces_exist = self.faces_exist


class LabelingEntry(ttk.Entry):
    def __init__(self, master):
        super().__init__(master)
        self.config(width=20, state="disabled")


class ImageLabel(ttk.Label):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.Image = Image.open("res\\portrait.png")
        self.Image = self.Image.resize((128, 128))
        self.picture = ImageTk.PhotoImage(self.Image)
        self.config(image=self.picture, compound="image")

    def set_image(self, image):
        self.Image = image.resize((128, 128))
        self.picture = ImageTk.PhotoImage(self.Image)
        self.config(image=self.picture)


class LabelingFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        imageLabel = ImageLabel(self)
        imageLabel.pack()

        labelingEntry = LabelingEntry(self)
        labelingEntry.pack()

        labelingBt = LabelingBt(self)
        labelingBt.pack()


class ScanBt(ttk.Button):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.config(text="Scan", command=self.onClick)
        self.directory = self.get_directory()

    def onClick(self):
        self.directory = self.get_directory()
        folder = Folder(self.directory)
        images = list(map(lambda p: fr.Image(p), folder.get_pictures()))
        faces_sets = fr.Image.groups_list(images)
        faces_exist = fr.Image.get_persons_exist(images)
        nbr_faces = len(faces_sets)
        infoLabel = None
        check = None
        choiceLabel = None
        labelingEntry = None
        labelingBt = None
        imageLabel = None
        classifyBt = None
        app = self.nametowidget(self.master.winfo_parent())
        for frame in app.winfo_children():
            if isinstance(frame, ChoiceFrame):
                for widget in frame.winfo_children():
                    if isinstance(widget, CheckBt):
                        check = True if widget.check.get() == "True" else False
                        choiceLabel = widget
            if isinstance(frame, InfoFrame):
                for widget in frame.winfo_children():
                    if isinstance(widget, InfoLabel):
                        infoLabel = widget
            if isinstance(frame, LabelingFrame):
                for widget in frame.winfo_children():
                    if isinstance(widget, LabelingEntry):
                        labelingEntry = widget
                    if isinstance(widget, LabelingBt):
                        labelingBt = widget
                    if isinstance(widget, ImageLabel):
                        imageLabel = widget
            if isinstance(frame, ControlFrame):
                for widget in frame.winfo_children():
                    if isinstance(widget, ClassifyBt):
                        classifyBt = widget
        classifyBt.folder = folder
        classifyBt.images = images
        classifyBt.face_set = faces_sets
        classifyBt.choiceLabel = choiceLabel
        classifyBt.scanBt = self
        classifyBt.imageLabel = imageLabel

        infoLabel.config(text="INFO: Pictures = {}\nINFO: Persons = {}".format(
                len(folder.get_pictures()), len(faces_sets)))
        if check and nbr_faces != 0:
            labelingEntry.config(state="!disabled")
            labelingBt.config(state="!disabled")
            imageLabel.set_image(faces_exist[0].pil_image)
            labelingBt.imageLabel = imageLabel
            labelingBt.faces_exist = faces_exist
            labelingBt.labelingEntry = labelingEntry
            labelingBt.classifyBt = classifyBt

            self.config(state="disable")
            choiceLabel.config(state="disable")

        if not check and nbr_faces != 0:
            self.config(state="disable")
            choiceLabel.config(state="disable")
            classifyBt.config(state="!disable")

    def get_directory(self):
        app = self.nametowidget(self.master.winfo_parent())
        for widget in app.winfo_children():
            if isinstance(widget, DirectoryFrame):
                for widget2 in widget.winfo_children():
                    if isinstance(widget2, FindEntry):
                        return widget2.directory


class ClassifyBt(ttk.Button):
    def __init__(self, master):
        super().__init__(master)
        self.config(text="Classify", command=self.onClick, state="disable")
        self.folder = None
        self.images = None
        self.faces_set = None
        self.faces_exist = None

        self.choiceLabel = None
        self.scanBt = None
        self.imageLabel = None

    def onClick(self):
        my_dict = fr.Image.groups_list(self.images, self.faces_exist)
        self.folder.group_in_folders(my_dict)
        self.choiceLabel.config(state="!disable")
        self.scanBt.config(state="!disable")
        self.config(state="disable")
        image = Image.open("res\\portrait.png")
        image = image.resize((128, 128))
        self.imageLabel.picture = ImageTk.PhotoImage(image)
        self.imageLabel.config(image=self.imageLabel.picture, compound="image")


class ControlFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.scanBT = ScanBt(master=self)
        self.scanBT.pack()
        classifyBt = ClassifyBt(master=self)
        classifyBt.pack()