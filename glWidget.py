from model.Central import Central
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QOpenGLWidget)
import OpenGL.GL as gl
from OpenGL import GLU as glu
from OpenGL import GLUT as glut


class GLWidget(QOpenGLWidget):

    def __init__(self, parent, model):
        super().__init__(parent)
        self.model = model


    def initializeGL(self):
        gl.glClearColor(0, 0, 0, 0);
        gl.glShadeModel(gl.GL_FLAT);
        gl.glEnable(gl.GL_COLOR_MATERIAL);
        gl.glEnable(gl.GL_LIGHTING);
        ambientLight = [0.2, 0.2, 0.2, 1.0];
        diffuseLight = [0.99, 0.99, 0.99, 1.0];
        lightPos = [0, 0, 1000, 0];
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_AMBIENT, ambientLight);
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, diffuseLight);
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, lightPos);
        gl.glEnable(gl.GL_LIGHT0);
        gl.glColorMaterial(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT_AND_DIFFUSE)

        gl.glMaterialfv(gl.GL_FRONT, gl.GL_AMBIENT_AND_DIFFUSE, [0.3, 0.3, 0.3, 1.0])

        print(gl.glGetString(gl.GL_EXTENSIONS))

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glColor3f(0.6, 0.6, 1.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPushMatrix()
        gl.glEnable(gl.GL_CULL_FACE)

        w = self.model.width // 2
        h = self.model.height // 2
        d = self.model.cell
        k = self.model.K * 4
        if not k:
            return

        for y in range(-h, h, d):
            x = -w
            gl.glBegin(gl.GL_TRIANGLE_STRIP)
            v0 = [x, y, Central.V(x, y) * k]
            v1 = [x, y - d, Central.V(x, y - d) * k]
            gl.glVertex3fv(v0)  # V0
            gl.glVertex3fv(v1)  # V1

            for x in range(-w + 1, w, d):
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


# void normalize(float v[3])
# {
#    GLfloat d = sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2]);
#    if (d == 0.0) {
#       error("zero length vector");
#       return;
#    }
#    v[0] /= d;
#    v[1] /= d;
#    v[2] /= d;
# }
#
# void normcrossprod(float v1[3], float v2[3], float out[3])
# {
#    out[0] = v1[1]*v2[2] - v1[2]*v2[1];
#    out[1] = v1[2]*v2[0] - v1[0]*v2[2];
#    out[2] = v1[0]*v2[1] - v1[1]*v2[0];
#    normalize(out);
# }