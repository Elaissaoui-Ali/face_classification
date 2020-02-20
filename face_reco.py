import face_recognition as fr
from PIL import Image as PilImage


class Face:

    def __init__(self, picture, location, encoding, name=None, pil_image=None):
        self.picture = picture
        self.location = location
        self.encoding = encoding
        self.name = name
        self.pil_image = pil_image

    def compare_to(self, encoding, tolerance=0.61):
        return fr.compare_faces([self.encoding], encoding, tolerance)[0]

    def distance_from(self, encoding):
        return fr.face_distance([self.encoding], encoding)[0]


class Image:
    def __init__(self, picture):
        self.picture = picture
        locations = fr.face_locations(img=fr.load_image_file(self.picture.absolute_path),
                                      model="cnn")
        self.faces = list()
        for location in locations:
            image = fr.load_image_file(self.picture.absolute_path)
            face_encoding = fr.face_encodings(face_image=image,
                                              known_face_locations=[location])[0]
            top, right, bottom, left = location
            face_image = image[top:bottom, left:right]
            pil_image = PilImage.fromarray(face_image)
            pil_image = pil_image.resize((128, 128))
            face = Face(self.picture, location, face_encoding, pil_image=pil_image)
            self.faces.append(face)
        self.nbr_of_faces = len(self.faces)

    def contain(self, face):
        return len(list(filter(lambda f: f.compare_to(face.encoding), self.faces))) != 0

    @staticmethod
    def groups_list(images, existing_faces=None):
        grp = []
        if not existing_faces:
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
        existing_faces = list()
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
                    existing_faces.append(f)
                    i += 1
        return existing_faces
