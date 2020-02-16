import os
import shutil


class Picture:
    ImgExt = [".jpg"]

    def __init__(self, absolute_path):
        self.absolute_path = absolute_path

    def get_basename(self):
        return os.path.basename(self.absolute_path).lower()

    def get_extension(self):
        return os.path.splitext(self.absolute_path)[1].lower()


class Folder:
    def __init__(self, absolute_path):
        self.absolute_path = absolute_path

    def get_pictures(self):
        files = filter(lambda f: os.path.splitext(f)[1].lower() in Picture.ImgExt,
                       os.listdir(self.absolute_path))
        return list(map(lambda pic: Picture(self.absolute_path + "\\" + pic), files))

    def create_folders(self, list_of_names):
        for name in list_of_names:
            try:
                os.mkdir("{}\\{}".format(self.absolute_path, name))
            except FileExistsError:
                print("folder is already exist !!")

    def group_in_folders(self, dict_list):
        self.create_folders(list(map(lambda i: i["folder"], dict_list)))
        condition = True
        for item in dict_list:
            for file in item["files"]:
                new_path = "{}\\{}\\{}".format(self.absolute_path, item["folder"],
                                               os.path.basename(file))
                try:
                    shutil.copy2(file, new_path)

                except:
                    condition = False
                    print("Error from my_os.py Folder group_in_folders copy2 !!!")
        if condition:
            for pic in self.get_pictures():
                try:
                    os.remove(pic.absolute_path)
                except:
                    print("Error from my_os.py Folder group_in_folders remove !!!")
