import tkinter
import time
import sys

from tkinter import *
from tkinter import scrolledtext, messagebox
from tkinter.ttk import Combobox, Notebook, Style
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from Gradient import make_data_lab_1, funct_consider
from SLSQP import make_data_lab_2, kp
from Rosenbrock_function import make_data_lab_3
from genetic_algorithm_l3 import GeneticAlgorithmL3
from pso import PSO
from functions import *



def main():
    window = Tk()

    window.iconbitmap(r'pic/hto.ico')


    width = window.winfo_screenwidth()
    height = window.winfo_screenheight()

    window.geometry("%dx%d" % (width, height))

    window.title("Оптимизация многоэкстремальных функций")

    fig = plt.figure(figsize=(14, 14))
    fig.add_subplot(projection='3d')

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH)

    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH)

    sky = "#DCF0F2"
    yellow = "#F2C84B"

    style = Style()

    style.theme_create("dummy", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1], "background": sky},
            "map": {"background": [("selected", yellow)],
                    "expand": [("selected", [1, 1, 1, 0])]}}})

    style.theme_use("dummy")

    tab_control = Notebook(window)

    # Лаба 1

    def draw_lab_1():
        fig.clf()

        x, y, z = make_data_lab_1()

        ax = fig.add_subplot(projection='3d')
        ax.plot_surface(x, y, z, rstride=5, cstride=5, alpha=0.5, cmap="inferno")
        canvas.draw()

        res_x = txt_1_tab_1.get()
        res_y = txt_2_tab_1.get()
        res_step = txt_3_tab_1.get()
        res_iterations = txt_4_tab_1.get()

        x_cs, y_cs, z_cs = funct_consider(float(res_x), float(res_y), float(res_step), int(res_iterations))

        for i in range(len(x_cs)):
            if i < (len(x_cs) - 1):
                ax.scatter(x_cs[i - 1], y_cs[i - 1], z_cs[i - 1], c="black", s=1, marker="s")
            else:
                ax.scatter(x_cs[i - 1], y_cs[i - 1], z_cs[i - 1], c="red")

            canvas.draw()
            txt_tab_1.insert(INSERT, f"{i}) ({round(x_cs[i], 2)})({round(y_cs[i], 2)}) = {z_cs[i]}\n")

            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            window.update()
            delay = txt_5_tab_1.get()
            time.sleep(float(delay))
        messagebox.showinfo('Уведомление', 'Готово')

    def delete_lab_1():
        txt_tab_1.delete(1.0, END)

    tab_1 = Frame(tab_control)
    tab_control.add(tab_1, text="LR1")

    main_f_tab_1 = LabelFrame(tab_1, text="Параметры")
    left_f_tab_1 = Frame(main_f_tab_1)
    right_f_tab_1 = Frame(main_f_tab_1)
    txt_f_tab_1 = LabelFrame(tab_1, text="Выполнение и результаты")

    lbl_1_tab_1 = Label(left_f_tab_1, text="X")
    lbl_2_tab_1 = Label(left_f_tab_1, text="Y")
    lbl_3_tab_1 = Label(left_f_tab_1, text="Начальный шаг")
    lbl_4_tab_1 = Label(left_f_tab_1, text="Число итераций")
    lbl_5_tab_1 = Label(tab_1, text="Функция Химмельблау")
    lbl_6_tab_1 = Label(left_f_tab_1, text="Задержка в секундах")

    txt_1_tab_1 = Entry(right_f_tab_1)
    txt_1_tab_1.insert(0, "-1")

    txt_2_tab_1 = Entry(right_f_tab_1)
    txt_2_tab_1.insert(0, "-1")

    txt_3_tab_1 = Entry(right_f_tab_1)
    txt_3_tab_1.insert(0, "0.5")

    txt_4_tab_1 = Entry(right_f_tab_1)
    txt_4_tab_1.insert(0, "100")

    txt_5_tab_1 = Entry(right_f_tab_1)
    txt_5_tab_1.insert(0, "0.5")

    txt_tab_1 = scrolledtext.ScrolledText(txt_f_tab_1)
    btn_del_tab_1 = Button(tab_1, text="Очистить", command=delete_lab_1)
    btn_tab_1 = Button(tab_1, text="Выполнить", foreground="black", background="#199917", command=draw_lab_1)

    lbl_5_tab_1.pack(side=TOP, padx=5, pady=5)
    main_f_tab_1.pack(side=TOP, padx=5, pady=5, fill=BOTH, expand=True)
    left_f_tab_1.pack(side=LEFT, fill=BOTH, expand=True)
    right_f_tab_1.pack(side=RIGHT, fill=BOTH, expand=True)

    lbl_1_tab_1.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    lbl_2_tab_1.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    lbl_3_tab_1.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    lbl_4_tab_1.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    lbl_6_tab_1.pack(side=TOP, padx=5, pady=5, fill=BOTH)

    txt_1_tab_1.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    txt_2_tab_1.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    txt_3_tab_1.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    txt_4_tab_1.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    txt_5_tab_1.pack(side=TOP, padx=5, pady=5, fill=BOTH)

    txt_tab_1.pack(padx=5, pady=5, fill=BOTH, expand=True)

    btn_tab_1.pack(side=BOTTOM, padx=5, pady=5, fill=BOTH, expand=True)
    txt_f_tab_1.pack(side=BOTTOM, padx=5, pady=5, fill=BOTH, expand=True)
    btn_del_tab_1.pack(side=BOTTOM, padx=5, pady=5, fill=BOTH, expand=True)

    # Лаба 2

    def draw_lab_2():
        fig.clf()

        x, y, z = make_data_lab_2()

        res_x = txt_1_tab_2.get()
        res_y = txt_2_tab_2.get()

        ax = fig.add_subplot(projection='3d')
        ax.plot_surface(x, y, z, rstride=5, cstride=5, alpha=0.5, cmap="inferno")
        canvas.draw()

        x_cs = []
        y_cs = []
        z_cs = []

        for i, point in kp(res_x, res_y):
            x_cs.append(point[0])
            y_cs.append(point[1])
            z_cs.append(point[2])

        for i in range(len(x_cs)):
            if i < (len(x_cs) - 1):
                ax.scatter(x_cs[i - 1], y_cs[i - 1], z_cs[i - 1], c="black", s=1, marker="s")
            else:
                ax.scatter(x_cs[i - 1], y_cs[i - 1], z_cs[i - 1], c="red")

            txt_tab_2.insert(INSERT, f"{i}) ({round(x_cs[i], 2)})({round(y_cs[i], 2)}) = {round(z_cs[i], 4)}\n")
            canvas.draw()
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            window.update()
            delay = txt_3_tab_2.get()
            time.sleep(float(delay))
        messagebox.showinfo('Уведомление', 'Готово')

    def delete_lab_2():
        txt_tab_2.delete(1.0, END)

    tab_2 = Frame(tab_control)
    tab_control.add(tab_2, text="LR2")

    main_f_tab_2 = LabelFrame(tab_2, text="Параметры")
    left_f_tab_2 = Frame(main_f_tab_2)
    right_f_tab_2 = Frame(main_f_tab_2)
    txt_f_tab_2 = LabelFrame(tab_2, text="Выполнение и результаты")

    lbl_1_tab_2 = Label(tab_2, text="Функция :\n2 * x₁² + 3 * x₂² + 4 * x₁ * x₂ - 6 * x₁ - 3 * x₂")
    lbl_2_tab_2 = Label(left_f_tab_2, text="X")
    lbl_3_tab_2 = Label(left_f_tab_2, text="Y")
    lbl_4_tab_2 = Label(left_f_tab_2, text="Задержка в секундах")

    txt_1_tab_2 = Entry(right_f_tab_2)
    txt_1_tab_2.insert(0, "10")

    txt_2_tab_2 = Entry(right_f_tab_2)
    txt_2_tab_2.insert(0, "10")

    txt_3_tab_2 = Entry(right_f_tab_2)
    txt_3_tab_2.insert(0, "0.5")

    txt_tab_2 = scrolledtext.ScrolledText(txt_f_tab_2)
    btn_del_tab_2 = Button(tab_2, text="Очистить", command=delete_lab_2)
    btn_tab_2 = Button(tab_2, text="Выполнить", foreground="black", background="#199917", command=draw_lab_2)

    lbl_1_tab_2.pack(side=TOP, padx=5, pady=5)
    main_f_tab_2.pack(side=TOP, padx=5, pady=5, fill=BOTH, expand=True)
    left_f_tab_2.pack(side=LEFT, fill=BOTH, expand=True)
    right_f_tab_2.pack(side=RIGHT, fill=BOTH, expand=True)

    lbl_2_tab_2.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    lbl_3_tab_2.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    lbl_4_tab_2.pack(side=TOP, padx=5, pady=5, fill=BOTH)

    txt_1_tab_2.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    txt_2_tab_2.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    txt_3_tab_2.pack(side=TOP, padx=5, pady=5, fill=BOTH)

    txt_tab_2.pack(padx=5, pady=5, fill=BOTH, expand=True)

    btn_tab_2.pack(side=BOTTOM, padx=5, pady=5, fill=BOTH, expand=True)
    txt_f_tab_2.pack(side=BOTTOM, padx=5, pady=5, fill=BOTH, expand=True)
    btn_del_tab_2.pack(side=BOTTOM, padx=5, pady=5, fill=BOTH, expand=True)

    # Лаба 3

    def draw_lab_3():
        fig.clf()

        x, y, z = make_data_lab_3()

        pop_number = int(txt_1_tab_3.get())
        iter_number = int(txt_2_tab_3.get())
        survive = float(txt_3_tab_3.get())
        mutation = float(txt_4_tab_3.get())
        delay = txt_5_tab_3.get()

        if combo_tab_3.get() == "Min":
            min_max = True
        else:
            min_max = False

        ax = fig.add_subplot(projection='3d')
        ax.plot_surface(x, y, z, rstride=5, cstride=5, alpha=0.5, cmap="inferno")
        canvas.draw()

        genetic = GeneticAlgorithmL3(rosenbrock_2, iter_number, min_max, mutation, survive, pop_number)
        genetic.generate_start_population(5, 5)

        for j in range(pop_number):
            ax.scatter(genetic.population[j][0], genetic.population[j][1], genetic.population[j][2], c="black", s=1,
                       marker="s")
        if min_max:
            gen_stat = list(genetic.statistic()[1])
        else:
            gen_stat = list(genetic.statistic()[0])

        ax.scatter(gen_stat[1][0], gen_stat[1][1], gen_stat[1][2], c="red")
        canvas.draw()
        window.update()

        # Эти 4 строки ниже это считай удалить точку/точки
        fig.clf()
        ax = fig.add_subplot(projection='3d')
        ax.plot_surface(x, y, z, rstride=5, cstride=5, alpha=0.5, cmap="inferno")
        canvas.draw()

        for i in range(50):
            for j in range(pop_number):
                ax.scatter(genetic.population[j][0], genetic.population[j][1], genetic.population[j][2], c="black", s=1,
                           marker="s")

            genetic.select()
            genetic.mutation(i)

            if min_max:
                gen_stat = list(genetic.statistic()[1])
            else:
                gen_stat = list(genetic.statistic()[0])

            ax.scatter(gen_stat[1][0], gen_stat[1][1], gen_stat[1][2], c="red")

            txt_tab_3.insert(INSERT,
                             f"{i}) ({round(gen_stat[1][0], 4)}) ({round(gen_stat[1][1], 4)}) = "
                             f" ({round(gen_stat[1][2], 4)})\n")

            canvas.draw()
            window.update()
            time.sleep(float(delay))

            fig.clf()
            ax = fig.add_subplot(projection='3d')
            ax.plot_surface(x, y, z, rstride=5, cstride=5, alpha=0.5, cmap="inferno")
            canvas.draw()

        for j in range(pop_number):
            ax.scatter(genetic.population[j][0], genetic.population[j][1], genetic.population[j][2], c="black", s=1,
                       marker="s")
        if min_max:
            gen_stat = list(genetic.statistic()[1])
        else:
            gen_stat = list(genetic.statistic()[0])

        ax.scatter(gen_stat[1][0], gen_stat[1][1], gen_stat[1][2], c="red")

        canvas.draw()
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        window.update()

        messagebox.showinfo('Уведомление', 'Готово')

    def delete_lab_3():
        txt_tab_3.delete(1.0, END)

    tab_3 = Frame(tab_control)
    tab_control.add(tab_3, text="LR3")

    main_f_tab_3 = LabelFrame(tab_3, text="Параметры")
    left_f_tab_3 = Frame(main_f_tab_3)
    right_f_tab_3 = Frame(main_f_tab_3)
    txt_f_tab_3 = LabelFrame(tab_3, text="Выполнение и результаты")

    lbl_1_tab_3 = Label(left_f_tab_3, text="Размер популяции")
    lbl_2_tab_3 = Label(left_f_tab_3, text="Количество итераций")
    lbl_3_tab_3 = Label(left_f_tab_3, text="Выживаемость")
    lbl_7_tab_3 = Label(left_f_tab_3, text="Шанс мутации")
    lbl_4_tab_3 = Label(left_f_tab_3, text="Выбор точки поиска")
    lbl_5_tab_3 = Label(left_f_tab_3, text="Задержка в секундах")
    lbl_6_tab_3 = Label(tab_3, text="Функция Розенброка")

    txt_1_tab_3 = Entry(right_f_tab_3)
    txt_1_tab_3.insert(0,"20")
    txt_2_tab_3 = Entry(right_f_tab_3)
    txt_2_tab_3.insert(0,"50")
    txt_3_tab_3 = Entry(right_f_tab_3)
    txt_3_tab_3.insert(0,"0.8")
    txt_4_tab_3 = Entry(right_f_tab_3)
    txt_4_tab_3.insert(0,"0.8")
    txt_5_tab_3 = Entry(right_f_tab_3)
    txt_5_tab_3.insert(0,"0.01")

    combo_tab_3 = Combobox(right_f_tab_3)
    combo_tab_3['values'] = ("Min", "Max")
    combo_tab_3.set("Min")

    txt_tab_3 = scrolledtext.ScrolledText(txt_f_tab_3)
    btn_del_tab_3 = Button(tab_3, text="Очистить", command=delete_lab_3)
    btn_tab_3 = Button(tab_3, text="Выполнить", foreground="black", background="#199917", command=draw_lab_3)

    lbl_6_tab_3.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    main_f_tab_3.pack(side=TOP, padx=5, pady=5, fill=BOTH, expand=True)
    left_f_tab_3.pack(side=LEFT, fill=BOTH, expand=True)
    right_f_tab_3.pack(side=RIGHT, fill=BOTH, expand=True)

    lbl_1_tab_3.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    lbl_2_tab_3.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    lbl_3_tab_3.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    lbl_7_tab_3.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    lbl_5_tab_3.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    #lbl_4_tab_3.pack(side=TOP, padx=5, pady=5, fill=BOTH)

    txt_1_tab_3.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    txt_2_tab_3.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    txt_3_tab_3.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    txt_4_tab_3.pack(side=TOP, padx=5, pady=5, fill=BOTH)  # задержка в секундах
    txt_5_tab_3.pack(side=TOP, padx=5, pady=5, fill=BOTH)  # шанс мутации
    #combo_tab_3.pack(side=TOP, padx=5, pady=5, fill=BOTH)

    txt_tab_3.pack(padx=5, pady=5, fill=BOTH, expand=True)

    btn_tab_3.pack(side=BOTTOM, padx=5, pady=5, fill=BOTH, expand=True)
    txt_f_tab_3.pack(side=BOTTOM, padx=5, pady=5, fill=BOTH, expand=True)
    btn_del_tab_3.pack(side=BOTTOM, padx=5, pady=5, fill=BOTH, expand=True)

    # Лаба 4

    def draw_lab_4():
        fig.clf()

        #x, y, z = make_data_lab_3()
        px = 5.0
        py = 5.0
        x, y, z = make_data_rastrigin(px, py)

        iter_number = int(txt_1_tab_4.get())
        particle_number = int(txt_2_tab_4.get())
        fi_p = float(txt_4_tab_4.get())
        fi_g = float(txt_5_tab_4.get())
        delay = txt_6_tab_4.get()

        ax = fig.add_subplot(projection='3d')
        ax.plot_surface(x, y, z, rstride=5, cstride=5, alpha=0.5, cmap="inferno")
        canvas.draw()

        psa_obj = PSO(rastrigin_2, particle_number, px, py, fi_p, fi_g)

        for particle in psa_obj.particles:
            ax.scatter(particle[0], particle[1], particle[2], c="black", s=1, marker="s")

        ax.scatter(psa_obj.generation_best[0], psa_obj.generation_best[1], psa_obj.generation_best[2], c="red")
        canvas.draw()
        window.update()

        # Эти 4 строки ниже это считай удалить точку/точки
        fig.clf()
        ax = fig.add_subplot(projection='3d')
        ax.plot_surface(x, y, z, rstride=5, cstride=5, alpha=0.5, cmap="inferno")
        canvas.draw()

        for i in range(iter_number):
            psa_obj.next_iteration()
            for particle in psa_obj.particles:
                ax.scatter(particle[0], particle[1], particle[2], c="black", s=1, marker="s")

            ax.scatter(psa_obj.generation_best[0], psa_obj.generation_best[1], psa_obj.generation_best[2], c="red")

            txt_tab_4.insert(INSERT,
                             f"{i + 1}) ({round(psa_obj.generation_best[0], 8)})"
                             f" ({round(psa_obj.generation_best[1], 8)}) = "
                             f" ({round(psa_obj.generation_best[2], 8)})\n")

            canvas.draw()
            window.update()
            time.sleep(float(delay))

            fig.clf()
            ax = fig.add_subplot(projection='3d')
            ax.plot_surface(x, y, z, rstride=5, cstride=5, alpha=0.5, cmap="inferno")
            canvas.draw()

        for particle in psa_obj.particles:
            ax.scatter(particle[0], particle[1], particle[2], c="black", s=1, marker="s")

        ax.scatter(psa_obj.generation_best[0], psa_obj.generation_best[1], psa_obj.generation_best[2], c="red")

        canvas.draw()
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        window.update()

        messagebox.showinfo('Уведомление', 'Готово')

    def delete_lab_4():
        txt_tab_4.delete(1.0, END)

    tab_4 = Frame(tab_control)
    tab_control.add(tab_4, text="LR4")

    main_f_tab_4 = LabelFrame(tab_4, text="Параметры")
    left_f_tab_4 = Frame(main_f_tab_4)
    right_f_tab_4 = Frame(main_f_tab_4)
    txt_f_tab_4 = LabelFrame(tab_4, text="Выполнените и результаты")

    lbl_1_tab_4 = Label(left_f_tab_4, text="Количество итераций")
    lbl_2_tab_4 = Label(left_f_tab_4, text="Количество частиц")
    lbl_4_tab_4 = Label(left_f_tab_4, text="Коэффициент g")
    lbl_5_tab_4 = Label(left_f_tab_4, text="Задержка в секундах")
    lbl_6_tab_4 = Label(tab_4, text="Функция Растригина")
    lbl_7_tab_4 = Label(left_f_tab_4, text="Коэффициент p")

    txt_1_tab_4 = Entry(right_f_tab_4)
    txt_1_tab_4.insert(0, "100")
    txt_2_tab_4 = Entry(right_f_tab_4)
    txt_2_tab_4.insert(0, "50")
    txt_4_tab_4 = Entry(right_f_tab_4)
    txt_4_tab_4.insert(0, "5")
    txt_5_tab_4 = Entry(right_f_tab_4)
    txt_5_tab_4.insert(0, "5")
    txt_6_tab_4 = Entry(right_f_tab_4)
    txt_6_tab_4.insert(0, "0.01")

    txt_tab_4 = scrolledtext.ScrolledText(txt_f_tab_4)
    btn_del_tab_4 = Button(tab_4, text="Очистить", command=delete_lab_4)
    btn_tab_4 = Button(tab_4, text="Выполнить", foreground="black", background="#199917", command=draw_lab_4)

    lbl_6_tab_4.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    main_f_tab_4.pack(side=TOP, padx=5, pady=5, fill=BOTH, expand=True)
    left_f_tab_4.pack(side=LEFT, fill=BOTH, expand=True)
    right_f_tab_4.pack(side=RIGHT, fill=BOTH, expand=True)

    lbl_1_tab_4.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    lbl_2_tab_4.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    lbl_7_tab_4.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    lbl_4_tab_4.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    lbl_5_tab_4.pack(side=TOP, padx=5, pady=5, fill=BOTH)

    txt_1_tab_4.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    txt_2_tab_4.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    txt_4_tab_4.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    txt_5_tab_4.pack(side=TOP, padx=5, pady=5, fill=BOTH)
    txt_6_tab_4.pack(side=TOP, padx=5, pady=5, fill=BOTH)

    txt_tab_4.pack(padx=5, pady=5, fill=BOTH, expand=True)

    btn_tab_4.pack(side=BOTTOM, padx=5, pady=5, fill=BOTH, expand=True)
    txt_f_tab_4.pack(side=BOTTOM, padx=5, pady=5, fill=BOTH, expand=True)
    btn_del_tab_4.pack(side=BOTTOM, padx=5, pady=5, fill=BOTH, expand=True)

    tab_control.pack(side=RIGHT, fill=BOTH, expand=True)
    window.mainloop()


if __name__ == '__main__':
    main()
