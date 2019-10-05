import math
from datetime import datetime
from model.Central import Central
from model.Settings import settings as ss
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QOpenGLWidget)
from OpenGL.GL import *
import OpenGL.GLU as glu

class GLWidget(QOpenGLWidget):

    def __init__(self, parent, model, ss):
        super().__init__(parent)
        self.model = model

    def initializeGL(self):
        MAT_COLOR = [1, 1, 1]
        DIFFUSE_COLOR = [0.3, 0.3, 1, 1.0]
        AMBIENT_COLOR = [0, 0, 0.1, 1.0]
        DIFFUSE_COLOR1 = [0.5, 0.2, 0.2, 1.0]
        AMBIENT_COLOR1 = [0.1, 0, 0, 1.0]

        # тест глубины не справляется, строим поверхность от дальних вершин к ближним
        glEnable(GL_DEPTH_TEST)

        glClearColor(0, 0, 0, 0)
        glShadeModel(GL_FLAT)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHTING)

        # light: цвета источника
        glLightfv(GL_LIGHT0, GL_AMBIENT, AMBIENT_COLOR)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, DIFFUSE_COLOR )
        glEnable(GL_LIGHT0)

        glLightfv(GL_LIGHT1, GL_AMBIENT, AMBIENT_COLOR1)
        glLightfv(GL_LIGHT1, GL_DIFFUSE, DIFFUSE_COLOR1)
        glEnable(GL_LIGHT1)

        glLightModelf(GL_LIGHT_MODEL_TWO_SIDE, 1)

        # материал
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glColor3fv(MAT_COLOR)

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    #   v0 ---- v2
    #   |     / |
    #   |   /   |
    #   | /     |
    #   v1 ---- v3
    def paintGL(self):
        if Central.V(1, 1) is None:
            return
        try:
            self.paint()
        except:
            pass

    def paint(self):
        stamp = datetime.now().timestamp()  #######
        # save current model view matrix
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()

        # set camera position
        camY = math.sin(ss.view * math.pi / 180) * 1000
        camZ = math.cos(ss.view * math.pi / 180) * 1000
        glu.gluLookAt(0, camY, camZ,   0, 0, 0,    0, 1, 0)

        # light position
        ligX = math.sin(ss.light * math.pi / 180)
        ligZ = math.cos(ss.light * math.pi / 180)
        glLightfv(GL_LIGHT0, GL_POSITION, [0, ligX, ligZ, 0])
        glLightfv(GL_LIGHT1, GL_POSITION, [0, -ligX, -ligZ, 0])

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        w = self.model.width // 2
        h = self.model.height // 2
        d = ss.cell

        # строим поверхность от дальних вершин к ближним
        for x in range(w, -w - d, -d):
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

        # работаем с матрицей проекций
        glMatrixMode(GL_PROJECTION)
        # загрузка 1-матрицы
        glLoadIdentity()

        # режим ортогональной поекции
        z_from, z_to = -2000, 3000
        glOrtho(-side, side, -side, side, z_from, z_to)

        # работаем с матрицей наблюдения модели
        glMatrixMode(GL_MODELVIEW)
        # загрузка 1-матрицы
        glLoadIdentity()

    def z(self, x, y):
        return Central.V(x, y) * ss.kz

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
