import face_recognition as frec
import my_os


class Face:

    def __init__(self, picture, location, encoding, name=None):
        self.picture = picture
        self.location = location
        self.encoding = encoding
        self.name = name

    def compare_to(self, encoding, tolerance=0.61):
        return frec.compare_faces([self.encoding], encoding, tolerance)[0]

    def distance_from(self, encoding):
        return frec.face_distance([self.encoding], encoding)[0]


class Image:
    def __init__(self, picture):
        self.picture = picture
        locations = frec.face_locations(img=frec.load_image_file(self.picture.absolute_path),
                                        model="cnn")
        self.faces = list(map(lambda loc: Face(self.picture,
                                               loc,
                                               frec.face_encodings(
                                                       face_image=frec.load_image_file(
                                                               self.picture.absolute_path),
                                                       known_face_locations=[loc]
                                                       )[0]
                                               ),
                              locations
                              )
                          )
        self.nbr_of_faces = len(self.faces)

    def contain(self, face):
        return len(list(filter(lambda f: f.compare_to(face.encoding), self.faces))) != 0

    @staticmethod
    def groups_list(images):
        grp = []
        existing_faces = Image.get_persons_exist(images)
        for f in existing_faces:
            di = {"folder": f.name, "files": []}
            for img in images:
                if img.contain(f):
                    di["files"].append(img.picture.absolute_path)
            grp.append(di)
        return grp

    @staticmethod
    def get_persons_exist(images):
        existing_faces = set()
        i = 0
        for img in images:
            for f in img.faces:
                exist = False
                enc = f.encoding
                for ef in existing_faces:
                    if ef.compare_to(enc):
                        exist = True
                        break

                if not exist:
                    f.name = "Unknown_{}".format(i)
                    existing_faces.add(f)
                    i += 1
        return existing_faces

