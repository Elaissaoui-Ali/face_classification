import face_reco as fr
import my_os
from gui import *

# if __name__ == '__main__':
#     root_path = "pictures"
#     folder = my_os.Folder(root_path)
#     images = list(map(lambda p: fr.Image(p), folder.get_pictures()))
#
#     my_dict = fr.Image.groups_list(images)
#     folder.create_folders(list(map(lambda item: item["folder"], my_dict)))
#     folder.group_in_folders(my_dict)

if __name__ == '__main__':
    app = tk.Tk()

    dirFrame = DirectoryFrame(master=app)
    dirFrame.pack()

    choiceFrame = ChoiceFrame(master=app)
    choiceFrame.pack()

    infoFrame = InfoFrame(master=app)
    infoFrame.pack()

    labelingFrame = LabelingFrame(master=app)
    labelingFrame.pack()

    controlFrame = ControlFrame(master=app)
    controlFrame.pack()

    app.mainloop()