import sys
from PyQt5.QtWidgets import *
from PyQt5.QtOpenGL import *
from PyQt5 import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class MyOpenGLWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Устанавливаем цвет для рисования (красный)
        glColor3f(1.0, 0.0, 0.0)

        # Рисуем треугольник
        glBegin(GL_TRIANGLES)
        glVertex2f(-0.5, -0.5)
        glVertex2f(0.5, -0.5)
        glVertex2f(0.0, 0.5)
        glEnd()

        # Завершаем рисование
        glFlush()

# Ваш класс MyOpenGLWidget остается без изменений

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Оптимизация многоэкстремальных функций")
        self.setGeometry(300, 300, 1500, 800)

        central_widget = QSplitter(self)
        self.setCentralWidget(central_widget)

        opengl_widget = MyOpenGLWidget()
        central_widget.addWidget(opengl_widget)

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
        settings_layout.setSpacing(20)

        # Элементы управления настройками
        beg_point = QLabel("Начальная точка")
        settings_layout.addRow(beg_point, empty)

        x_point = QLabel("X")
        x_input = QLineEdit()

        y_point = QLabel("Y")
        y_input = QLineEdit()

        settings_layout.addRow(x_point, x_input)
        settings_layout.addRow(y_point, y_input)

        beg_step = QLabel("Начальный шаг")
        begstep_input = QLineEdit()

        settings_layout.addRow(beg_step,begstep_input)

        button = QPushButton("Выполнить")
        settings_layout.addWidget(button)

        tab1.setLayout(settings_layout)

        # Вторая вкладка
        tab2 = QWidget()
        tab_widget.addTab(tab2, "2")

        tab2_layout = QVBoxLayout()

        tab2_txt = QLabel("Некст говно")
        tab2_layout.addWidget(tab2_txt)

        tab2.setLayout(tab2_layout)

        # Виджет результатами
        result_layout = QVBoxLayout()
        res_groupbox = QGroupBox("Выполнение и результаты")

        res_input1 = QLineEdit()
        res_input1.setFixedSize(750, 200) # надо как-то сделать чтобы он был большим и меня размер при изменении окна

        result_layout.addWidget(res_input1)

        res_groupbox.setLayout(result_layout)
        layout.addWidget(res_groupbox)

        # Виджет с настройками графика
        setGraf_widget = QTabWidget()
        layout.addWidget(setGraf_widget)
        layout.setSpacing(20)

        setGraf = QWidget()

        group_box = QGroupBox("Функции и отображение ее графика")
        group_layout = QFormLayout()

        xInter_label = QLabel("X интервал:")
        xInter_input = QLineEdit()
        group_layout.addRow(xInter_label, xInter_input)

        yInter_label = QLabel("Y интервал:")
        yInter_input = QLineEdit()
        group_layout.addRow(yInter_label, yInter_input)

        combo_box = QComboBox()
        combo_box.addItem("График 1")
        combo_box.addItem("График 2")
        group_layout.addWidget(combo_box)

        group_box.setLayout(group_layout)
        setGraf_layout = QVBoxLayout()
        setGraf_layout.addWidget(group_box)
        setGraf.setLayout(setGraf_layout)

        setGraf_widget.addTab(setGraf, "График")

        layout.addLayout(layout)
        central_widget.setLayout(layout)

        right_widget.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
