# coding: utf-8
# license: GPLv3

from Data.solar_vis import *
from Data.solar_model import *
from Data.solar_input import *
from Data.solar_statistic import *
import thorpy
import time
import numpy as np

class Time:
    timer = None

    model_time = 0
    """Физическое время от начала расчёта.
    Тип: float"""

    time_scale = 1000.0
    """Шаг по времени при моделировании.
    Тип: float"""


class Core:
    alive = True
    statistic_maneger = StatisticManager()

    perform_execution = False
    """Флаг цикличности выполнения расчёта"""

    space_objects = []
    """Список космических объектов."""

    @staticmethod
    def pause_execution():
        Core.perform_execution = False

    @staticmethod
    def start_execution():
        """Обработчик события нажатия на кнопку Start.
        Запускает циклическое исполнение функции execution.
        """
        Core.perform_execution = True

    @staticmethod
    def stop_execution():
        """Обработчик события нажатия на кнопку Start.
        Останавливает циклическое исполнение функции execution.
        """
        Core.alive = False

    @staticmethod
    def statistic_execution():
        Core.statistic_maneger.get()


def execution(delta):
    """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
    а также обновляя их положение на экране.
    Цикличность выполнения зависит от значения глобальной переменной perform_execution.
    При perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
    """
    recalculate_space_objects_positions([dr.obj for dr in Core.space_objects], delta)
    Time.model_time += delta



def open_file():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """

    Core.statistic_maneger = StatisticManager()
    in_filename = "Input/solar_system.txt"
    Core.space_objects = read_space_objects_data_from_file(in_filename)
    max_distance = max([max(abs(obj.obj.x), abs(obj.obj.y)) for obj in Core.space_objects])
    calculate_scale_factor(max_distance)


def handle_events(events, menu):
    for event in events:
        menu.react(event)
        if event.type == pg.QUIT:
            Core.alive = False


def slider_to_real(val):
    return np.exp(5 + val)


def slider_reaction(event):
    Time.time_scale = slider_to_real(event.el.get_value())


def init_ui(screen):
    slider = thorpy.SliderX(100, (-10, 10), "Simulation speed")
    slider.user_func = slider_reaction
    button_stop = thorpy.make_button("Quit", func=Core.stop_execution)
    button_pause = thorpy.make_button("Pause", func=Core.pause_execution)
    button_play = thorpy.make_button("Play", func=Core.start_execution)
    button_statistic = thorpy.make_button("Statistic", func=Core.statistic_execution)
    timer = thorpy.OneLineText("Seconds passed")

    button_load = thorpy.make_button(text="Load a file", func=open_file)

    box = thorpy.Box(elements=[
        slider,
        button_pause,
        button_stop,
        button_play,
        button_load,
        button_statistic,
        timer])
    reaction1 = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                                reac_func=slider_reaction,
                                event_args={"id": thorpy.constants.EVENT_SLIDE},
                                params={},
                                reac_name="slider reaction")
    box.add_reaction(reaction1)

    menu = thorpy.Menu(box)
    for element in menu.get_population():
        element.surface = screen

    box.set_topleft((0, 0))
    box.blit()
    box.update()
    return menu, box, timer


def main():
    """Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
    """

    print('Modelling started!')

    pg.init()

    width = 1000
    height = 700
    screen = pg.display.set_mode((width, height))
    last_time = time.perf_counter()
    drawer = Drawer(screen)
    menu, box, timer = init_ui(screen)
    Core.perform_execution = True
    last_time_statistic = 0
    while Core.alive:
        handle_events(pg.event.get(), menu)
        cur_time = time.perf_counter()
        if Core.perform_execution:
            execution((cur_time - last_time) * Time.time_scale)
            text = "%d seconds passed" % (int(Time.model_time))
            timer.set_text(text)
            if (cur_time - last_time_statistic) * Time.time_scale > 1000 * 100:
                Core.statistic_maneger.add(Core.space_objects, (cur_time - last_time) * Time.time_scale)
                last_time_statistic = cur_time

        last_time = cur_time
        drawer.update(Core.space_objects, box)
        time.sleep(1.0 / 60)

    print('Modelling finished!')


if __name__ == "__main__":
    main()