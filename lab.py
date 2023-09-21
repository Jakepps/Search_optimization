import sys
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtOpenGL import *
from PyQt5 import *
from PyQt5.QtCore import QTimer
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np


class MyOpenGLWidget(QGLWidget):
    def __init__(self):
        super().__init__()
        self.rot_x = 0
        self.rot_y = 0
        self.rot_z = 0
        self.zoom = 1.0
        self.last_x = 0
        self.last_y = 0
        self.max_rot_x = 90
        self.min_rot_x = -90
        self.max_rot_y = 90
        self.min_rot_y = -90
        self.function_choice = "..."
        self.divisor = 1.0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateGL)
        self.timer.start(16)

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()
        gluLookAt(5, 5, 10, 0, 0, 0, 0, 0, 5)
        glTranslatef(0, 0, -5)

        glRotatef(self.rot_x, 1, 0, 0)
        glRotatef(self.rot_y, 0, 1, 0)
        glScalef(self.zoom, self.zoom, self.zoom)

        # Отрисовка осей XYZ
        # Ось X Красный цвет
        glColor3f(1.0, 0.0, 0.0)
        glLineWidth(5.0)
        glBegin(GL_LINES)
        glVertex3f(0, -5, 0)
        glVertex3f(-5, -5, 0)
        glEnd()

        # Ось Y Зеленый цвет
        glColor3f(0.0, 1.0, 0.0)
        glBegin(GL_LINES)
        glVertex3f(-5, -5, 0)
        glVertex3f(-5, 0, 0)
        glEnd()

        # Ось Z Синий цвет
        glColor3f(0.0, 0.0, 1.0)
        glBegin(GL_LINES)
        glVertex3f(-5, -5, 5)
        glVertex3f(-5, -5, 0)
        glVertex3f(0, 0, 0)
        glEnd()

        # Отрисовка сетки в плоскости XY
        glColor3f(0.5, 0.5, 0.5)
        glLineWidth(1.0)
        glBegin(GL_LINES)
        for i in np.arange(-5, 6, 1):
            glVertex3f(i, -5, 0)
            glVertex3f(i, 5, 0)
            glVertex3f(-5, i, 0)
            glVertex3f(5, i, 0)
        glEnd()


        # Отрисовка графика функции Химмельблау
        if self.function_choice == "Функция Химмельблау":
            glColor3f(0.0, 0.0, 1.0)
            glBegin(GL_POINTS)
            for x in np.arange(-5, 5, 0.1):
                for y in np.arange(-5, 5, 0.1):
                    z = (x ** 2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2
                    glVertex3f(x, y, z / 100)
            glEnd()

        if self.function_choice == "Z = Y":
            glColor3f(0.0, 0.0, 1.0)
            glBegin(GL_POINTS)
            for x in np.arange(0, 5, 0.1):
                for y in np.arange(0, 5, 0.1):
                    z = y
                    glVertex3f(x, y, z / self.divisor)
            glEnd()

        if self.function_choice == "Функция Букина":
            glColor3f(0.0, 0.0, 1.0)
            glBegin(GL_POINTS)
            for x in np.arange(-5, 5, 0.1):
                for y in np.arange(-5, 5, 0.1):
                    z = 100 * np.sqrt(abs(y - 0.01 * x**2)) + 0.01 * abs(x + 10)
                    glVertex3f(x, y, z / 100)
            glEnd()

        glFlush()

    def setFunctionChoice(self, choice):
        self.function_choice = choice
        self.updateGL()

    def mousePressEvent(self, event):
        self.last_x = event.x()
        self.last_y = event.y()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.last_x
        dy = event.y() - self.last_y
        self.last_x = event.x()
        self.last_y = event.y()

        self.rot_x += dy
        self.rot_y += dx

        self.rot_x = max(self.min_rot_x, min(self.max_rot_x, self.rot_x))
        self.rot_y = max(self.min_rot_y, min(self.max_rot_y, self.rot_y))

    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 120
        self.zoom *= 1.1**delta


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Оптимизация многоэкстремальных функций")
        self.setGeometry(300, 300, 1500, 800)

        central_widget = QSplitter(self)
        self.setCentralWidget(central_widget)

        self.opengl_widget = MyOpenGLWidget()
        central_widget.addWidget(self.opengl_widget)

        right_widget = QWidget(self)
        central_widget.addWidget(right_widget)

        layout = QVBoxLayout()

        # Виджет с вкладками
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)

        # Первая вкладка
        tab1 = QWidget()
        tab_widget.addTab(tab1, "1")

        settings_layout = QFormLayout()

        empty = QLabel('\n')
        settings_layout.setSpacing(10)

        # Элементы управления настройками
        beg_point = QLabel("Начальная точка")
        settings_layout.addRow(beg_point, empty)

        x_point = QLabel("X")
        x_input = QLineEdit("-1")

        y_point = QLabel("Y")
        y_input = QLineEdit("-1")

        settings_layout.addRow(x_point, x_input)
        settings_layout.addRow(y_point, y_input)

        beg_step = QLabel("Начальный шаг")
        begstep_input = QLineEdit("0.5")

        settings_layout.addRow(beg_step, begstep_input)

        count_iter = QLabel("Число итераций")
        countIter_input = QLineEdit("100")

        settings_layout.addRow(count_iter, countIter_input)


        delay = QLabel("Задержка")
        delay_input = QLineEdit("0.5")

        settings_layout.addRow(delay, delay_input)

        button = QPushButton("Выполнить")
        settings_layout.addWidget(button)

        tab1.setLayout(settings_layout)

        # Вторая вкладка
        tab2 = QWidget()
        tab_widget.addTab(tab2, "2")

        tab2_layout = QVBoxLayout()

        tab2_txt = QLabel("Некст")
        tab2_layout.addWidget(tab2_txt)

        tab2.setLayout(tab2_layout)

        # Виджет результатами
        result_layout = QVBoxLayout()
        res_groupbox = QGroupBox("Выполнение и результаты")

        res_input = QLineEdit()
        res_input.setFixedSize(300, 200) # надо как-то сделать чтобы он был большим и меня размер при изменении окна, хотя похуй, я нашел этому полезное применение
        res_input.setReadOnly(True)

        result_layout.addWidget(res_input)

        res_groupbox.setLayout(result_layout)
        layout.addWidget(res_groupbox)

        # Виджет с настройками графика
        setGraf_widget = QTabWidget()
        layout.addWidget(setGraf_widget)
        layout.setSpacing(20)

        setGraf = QWidget()

        group_box = QGroupBox("Функции и отображение ее графика")
        group_layout = QFormLayout()

        graf = QLabel("Функция")
        self.combo_box = QComboBox()
        self.combo_box.addItem("...")
        self.combo_box.addItem("Z = Y")
        self.combo_box.addItem("Функция Химмельблау")
        self.combo_box.addItem("Плоскость XY")
        self.combo_box.addItem("Функция Букина")
        self.combo_box.addItem("Функция Розенброкка")
        self.combo_box.addItem("Функция сферы")
        self.combo_box.addItem("Функция Растригина")
        self.combo_box.addItem("Функция для 2й лабы")
        group_layout.addRow(graf, self.combo_box)

        self.combo_box.currentIndexChanged.connect(self.handleComboBoxChange)

        xInter_label = QLabel("X интервал:")
        xInter_input = QLineEdit("(-5;5)")
        group_layout.addRow(xInter_label, xInter_input)

        yInter_label = QLabel("Y интервал:")
        yInter_input = QLineEdit("(-5;5)")
        group_layout.addRow(yInter_label, yInter_input)

        zScale = QLabel("Z масштаб:")
        self.zScale_input = QLineEdit("1")
        group_layout.addRow(zScale, self.zScale_input)

        self.zScale_input.textChanged.connect(self.updateZ)

        axes = QLabel("Оси")
        axes_check = QCheckBox()
        axes_check.setChecked(True)
        group_layout.addRow(axes, axes_check)

        axesyInter_label = QLabel("Ось X интервал:")
        axesyInter_input = QLineEdit("(-5;10)")
        group_layout.addRow(axesyInter_label, axesyInter_input)

        axesxInter_label = QLabel("Ось Y интервал:")
        axesxInter_input = QLineEdit("(-5;10)")
        group_layout.addRow(axesxInter_label, axesxInter_input)

        grid = QLabel("Сетка")
        grid_check = QCheckBox()
        grid_check.setChecked(True)
        group_layout.addRow(grid, grid_check)

        group_box.setLayout(group_layout)
        setGraf_layout = QVBoxLayout()
        setGraf_layout.addWidget(group_box)
        setGraf.setLayout(setGraf_layout)

        setGraf_widget.addTab(setGraf, "График")


        layout.addLayout(layout)
        central_widget.setLayout(layout)

        right_widget.setLayout(layout)

    def handleComboBoxChange(self):
        selected_text = self.combo_box.currentText()
        self.opengl_widget.setFunctionChoice(selected_text)

    def updateZ(self, text):
        text = self.zScale_input.text()
        try:
            self.divisor = float(text)
        except ValueError:
            self.divisor = 1.0


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
