from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QOpenGLWidget)
import OpenGL.GL as gl
from OpenGL import GLU as glu


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
        diffuseLight = [0.5, 0.5, 0.5, 1.0];
        lightPos = [300, 0, 100, 0];
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_AMBIENT, ambientLight);
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, diffuseLight);
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, lightPos);
        gl.glEnable(gl.GL_LIGHT0);
        gl.glColorMaterial(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT_AND_DIFFUSE)

        print(gl.glGetString(gl.GL_EXTENSIONS))

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glColor3f(1.0, 0.0, 0.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPushMatrix()
        gl.glEnable(gl.GL_CULL_FACE)


        gl.glBegin(gl.GL_TRIANGLE_STRIP)

        gl.glVertex3f(0, 100, 0)      # V0
        gl.glVertex3f(0, 0, 0)        # V1
        gl.glVertex3f(100, 100, 400)    # V2

        gl.glColor3f(0.0, 1.0, 0.0);
        gl.glVertex3f(100, 0, 0)      # V3

        gl.glColor3f(0.0, 0.0, 1.0);
        gl.glVertex3f(200, 100, 0)    # V4

        gl.glColor3f(1.0, 0.0, 0.0);
        gl.glVertex3f(200, 0, 0)      # V5


        gl.glEnd()

        gl.glPopMatrix();

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
