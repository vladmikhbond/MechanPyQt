import math
from datetime import datetime
from model.Central import Central
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QOpenGLWidget)
from OpenGL.GL import *
import OpenGL.GLU as glu

class GLWidget(QOpenGLWidget):

    def __init__(self, parent, model, settings):
        super().__init__(parent)
        self.model = model
        self.reset(settings)
        self.cell = self.model.cell

    def reset(self, text):
        o = eval('{' + text + '}')
        self.kz = o['kz']
        self.view = o['view']
        self.light = o['light']
        self.cell = o['cell']

    def initializeGL(self):
        MAT_COLOR = [0.3, 0.3, 1]
        DIFFUSE_COLOR = [1, 1, 1, 1.0]
        AMBIENT_COLOR = [0.5, 0.5, 0.5, 1.0]
        SPECULAR_COLOR = [0.3, 0.3, 0.3, 1.0]
        SPECULAR_MATERIAL = [0.2, 0.2, 0.2, 1.0]

        glEnable(GL_DEPTH_TEST)

        glClearColor(0, 0, 0, 0)
        glShadeModel(GL_FLAT)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHTING)

        # light: цвета источника
        glLightfv(GL_LIGHT0, GL_AMBIENT, AMBIENT_COLOR)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, DIFFUSE_COLOR )
        # glLightfv(GL_LIGHT0, GL_SPECULAR, SPECULAR_COLOR )
        glEnable(GL_LIGHT0)

        # материал
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        glColor3fv(MAT_COLOR)
        # отражательная способность (только ухудшает вид)
        # glMaterialfv(GL_FRONT, GL_SPECULAR, SPECULAR_MATERIAL)
        # glMateriali(GL_FRONT, GL_SHININESS, 32)

        glEnable(GL_CULL_FACE)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)




    #   v0 ---- v2
    #   |     / |
    #   |   /   |
    #   | /     |
    #   v1 ---- v3
    def paintGL(self):
        stamp = datetime.now().timestamp()  #######

        if Central.V(0, 0) is None:
            return

        # save current model view matrix
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()

        # set camera position
        camY = math.sin(self.view * math.pi / 180) * 1000
        camZ = math.cos(self.view * math.pi / 180) * 1000
        glu.gluLookAt(0, camY, camZ,   0, 0, 0,    0, 1, 0)

        # light position
        posX = math.sin(self.light * math.pi / 180)
        posZ = math.cos(self.light * math.pi / 180)
        glLightfv(GL_LIGHT0, GL_POSITION, [posX, 0, posZ, 0])

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        w = self.model.width // 2
        h = self.model.height // 2
        d = self.cell

        for x in range(-w, w + d, d):
            glBegin(GL_TRIANGLE_STRIP)
            y = -h
            v0 = [x, y, self.z(x, y)]
            v1 = [x + d, y, self.z(x + d, y)]
            v2 = [x, y + d, self.z(x, y + d)]
            n1 = normcrossprod(v0, v1, v2)
            glNormal3fv(n1)
            glVertex3fv(v0)
            glVertex3fv(v1)

            for y in range(-h, h + d, d):
                v2 = [x, y + d, self.z(x, y + d)]
                v3 = [x + d, y + d, self.z(x + d, y + d)]
                n1 = normcrossprod(v2, v0, v1)
                n2 = normcrossprod(v3, v2, v1)
                glNormal3fv(n1)
                glVertex3fv(v2)

                glNormal3fv(n2)
                glVertex3fv(v3)
                v0, v1 = v2, v3
            glEnd()

        glPopMatrix()
        print(f"paintGL: {datetime.now().timestamp() - stamp}")  #######


    def resizeGL(self, width, height):
        side = min(width, height) / 2
        if side < 0:
            return
        # окно просмотра - ни на что не влияет ???
        glViewport(0, 0, width, height)

        # загрузка 1-матрицы проекций
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # режим ортогональной поекции
        z_from, z_to = -1000, 2000
        glOrtho(-side, side, -side, side, z_from, z_to)

        # загрузка 1-матрицы наблюдения модели
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def z(self, x, y):
        return Central.V(x, y) * self.kz

def normcrossprod(v0, v1, v2):
    ax = v1[0] - v0[0]
    ay = v1[1] - v0[1]
    az = v1[2] - v0[2]
    bx = v2[0] - v0[0]
    by = v2[1] - v0[1]
    bz = v2[2] - v0[2]
    out = [ay * bz - by * az, ax * bz - bx * az, ax * by - bx * ay]
    normalize(out)
    return out

def normalize(v):
    d = (v[0] * v[0] + v[1] * v[1] + v[2] * v[2]) ** 0.5
    if d == 0:
        raise Exception("zero length vector")
    v[0] /= d
    v[1] /= d
    v[2] /= d
