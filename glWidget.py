from model.Central import Central
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QOpenGLWidget)
import OpenGL.GL as gl
# from OpenGL import GLU as glu
# from OpenGL import GLUT as glut


class GLWidget(QOpenGLWidget):



    def __init__(self, parent, model):
        super().__init__(parent)
        self.model = model

    def initializeGL(self):
        # MAT_COLOR = [0.6, 0.6, 1.0]
        # DIFFUSE_COLOR = [0.7, 0.7, 0.7, 1.0]
        # AMBIENT_COLOR = [0.3, 0.3, 0.3, 1.0]

        MAT_COLOR = [1, 1, 1]
        DIFFUSE_COLOR = [0.4, 0.4, 1, 1.0]
        AMBIENT_COLOR = [0.2, 0.2, 0.2, 1.0]
        POSITION = [0, 0, 400, 1]

        gl.glClearColor(0, 0, 0, 0);
        gl.glShadeModel(gl.GL_SMOOTH);
        gl.glEnable(gl.GL_COLOR_MATERIAL);
        gl.glEnable(gl.GL_LIGHTING);
        # цвета источника
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_AMBIENT, AMBIENT_COLOR);
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, DIFFUSE_COLOR );
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_SPECULAR, [1, 1, 1, 1.0]);

        # позиция источника
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, POSITION);
        gl.glEnable(gl.GL_LIGHT0);

        # материал
        gl.glColorMaterial(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT_AND_DIFFUSE)
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_AMBIENT_AND_DIFFUSE, [0.9, 0.9, 0.9, 1.0])
        gl.glColor3fv(MAT_COLOR)

        print(gl.glGetString(gl.GL_EXTENSIONS))

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPushMatrix()
        gl.glEnable(gl.GL_CULL_FACE)

        w = self.model.width // 2
        h = self.model.height // 2
        d = self.model.cell
        k = self.model.K * 4
        if not k:
            return

        for y in range(h, -h, -d):
            x = -w
            v0 = [x, y, Central.V(x, y) * k]
            v1 = [x, y - d, Central.V(x, y - d) * k]
            gl.glBegin(gl.GL_TRIANGLE_STRIP)

            n0 = [0, 0, 1]
            gl.glNormal3fv(n0)
            gl.glVertex3fv(v0)

            n1 = [0, 0, 1]
            gl.glNormal3fv(n1)
            gl.glVertex3fv(v1)

            for x in range(-w + d, w + d, d):
                v2 = [x, y, Central.V(x, y) * k]
                v3 = [x, y - d, Central.V(x, y - d) * k]
                n2 = normcrossprod(v0, v1, v2)
                n3 = normcrossprod(v1, v3, v2)

                gl.glNormal3fv(n2)
                gl.glVertex3fv(v2)

                gl.glNormal3fv(n3)
                gl.glVertex3fv(v3)

                v0, v1 = v2, v3
            gl.glEnd()

        gl.glPopMatrix()

    def resizeGL(self, width, height):
        side = min(width, height) / 2
        if side < 0:
            return
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()

        gl.glOrtho(-side, side, -side, side, -side, side)

        gl.glMatrixMode(gl.GL_MODELVIEW);
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
