import math
from datetime import datetime
from model.Central import Central
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QOpenGLWidget)
import OpenGL.GL as gl
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
        AMBIENT_COLOR = [0.3, 0.3, 0.3, 1.0]


        gl.glClearColor(0, 0, 0, 0)
        gl.glShadeModel(gl.GL_SMOOTH)
        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glEnable(gl.GL_LIGHTING)

        # light: цвета источника
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_AMBIENT, AMBIENT_COLOR)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, DIFFUSE_COLOR )


        gl.glEnable(gl.GL_LIGHT0)

        # материал
        gl.glColorMaterial(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT_AND_DIFFUSE)
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_AMBIENT_AND_DIFFUSE, [0.9, 0.9, 0.9, 1.0])
        gl.glColor3fv(MAT_COLOR)

    def z(self, x, y):
        return Central.V(x, y) * self.kz


    #   v0 ---- v2
    #   |     / |
    #   |   /   |
    #   | /     |
    #   v1 ---- v3
    def paintGL(self):
        stamp = datetime.now().timestamp()  #######

        if not self.model.K:
            return



        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPushMatrix()
         # camera
        camY = math.sin(self.view * math.pi / 180) * 1000
        camZ = math.cos(self.view * math.pi / 180) * 1000
        glu.gluLookAt(0, camY, camZ, 0,0,0, 0,1,0)

        # light position
        posX = math.sin(self.light * math.pi / 180)
        posZ = math.cos(self.light * math.pi / 180)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, [posX, 0, posZ, 0])


        w = self.model.width // 2
        h = self.model.height // 2
        d = self.cell


        gl.glBegin(gl.GL_TRIANGLES)
        for x in range(-w, w + d, d):
            for y in range(-h, h + d, d):
                v0 = [x, y, self.z(x, y)]
                v1 = [x, y - d, self.z(x, y - d)]
                v2 = [x + d, y, self.z(x + d, y)]
                v3 = [x + d, y - d, self.z(x + d, y - d)]
                n012 = normcrossprod(v0, v1, v2)
                n132 = normcrossprod(v1, v3, v2)
                # v0v1v2
                gl.glNormal3fv(n012)
                gl.glVertex3fv(v0)
                gl.glVertex3fv(v1)
                gl.glVertex3fv(v2)
                # v1v2v3
                gl.glNormal3fv(n132)
                gl.glVertex3fv(v1)
                gl.glVertex3fv(v3)
                gl.glVertex3fv(v2)

        gl.glEnd()
        gl.glPopMatrix()
        print(f"paintGL: {datetime.now().timestamp() - stamp}")  #######


    def resizeGL(self, width, height):
        side = min(width, height) / 2
        if side < 0:
            return
        gl.glViewport(0, 0, width, height)
        # текущая матрица - проекций
        gl.glMatrixMode(gl.GL_PROJECTION)
        # загрузка 1-матрицы
        gl.glLoadIdentity()

        gl.glOrtho(-side, side, -side, side, -1000, 2000)
        #glu.gluPerspective(45.0, width / height, 0, 1000 )

        # текущая матрица - наблюдения модели
        gl.glMatrixMode(gl.GL_MODELVIEW)
        # загрузка 1-матрицы
        gl.glLoadIdentity()


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
