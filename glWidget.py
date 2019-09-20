from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QOpenGLWidget)
import OpenGL.GL as gl
from OpenGL import GLU as glu

class GLWidget(QOpenGLWidget):

    def __init__(self, parent, model):
        super().__init__(parent)
        self.model = model


    def initializeGL(self):
        gl.glClearColor(0, 0, 0, 0);
        gl.glShadeModel(gl.GL_SMOOTH);
        gl.glEnable(gl.GL_COLOR_MATERIAL);
        gl.glEnable(gl.GL_LIGHTING);
        ambientLight = [0.2, 0.2, 0.2, 1.0];
        diffuseLight = [0.5, 0.5, 0.5, 1.0];
        lightPos = [100, 100, 100, 0];
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_AMBIENT, ambientLight);
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, diffuseLight);
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, lightPos);
        gl.glEnable(gl.GL_LIGHT0);
        gl.glColorMaterial(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT_AND_DIFFUSE)

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT);
        gl.glColor3f(1.0, 2.0, 1.0);
        gl.glMatrixMode(gl.GL_MODELVIEW);
        gl.glPushMatrix();
        gl.glTranslatef(0.3, 0.3, 0.0);
        qobj = glu.gluNewQuadric();
        glu.gluQuadricOrientation(qobj, glu.GLU_OUTSIDE);
        glu.gluSphere(qobj, 0.67, 100, 100);
        gl.glPopMatrix();

    def resizeGL(self, width, height):
        side = min(width, height)
        if side < 0: return
        gl.glViewport((width - side) // 2, (height - side) // 2, side, side)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glScale(height / width, 1.0, 1.0);
        gl.glMatrixMode(gl.GL_MODELVIEW);

