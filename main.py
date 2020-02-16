import face_reco as fr
import my_os

if __name__ == '__main__':
    root_path = "pictures"
    folder = my_os.Folder(root_path)
    images = list(map(lambda p: fr.Image(p), folder.get_pictures()))
    my_dict = fr.Image.groups_list(images)
    folder.create_folders(list(map(lambda item: item["folder"], my_dict)))
    folder.group_in_folders(my_dict)
