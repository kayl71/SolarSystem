# coding: utf-8
# license: GPLv3


class SolarObj:
    def __init__(self, m=1, x=0, y=0, Vx=0, Vy=0, Fx=0, Fy=0, R=5, color="red"):
        """
        :param m: Масса
        :param x: Координата **x**
        :param y: Координата **y**
        :param Vx: Скорость по оси **x**
        :param Vy: Скорость по оси **y**
        :param Fx: Сила по оси **x**
        :param Fy: Сила по оси **y**
        :param R: Радиус объекта
        :param color: Цвет объекта
        """
        self.m = m
        self.x = x
        self.y = y
        self.Vx = Vx
        self.Vy = Vy
        self.Fx = Fx
        self.Fy = Fy
        self.R = R
        self.color = color


class Star(SolarObj):
    """Тип данных, описывающий звезду.
    Содержит массу, координаты, скорость звезды,
    а также визуальный радиус звезды в пикселах и её цвет.
    """

    def __init__(self, *args, **kwargs):
        """
        Объект типа type = "star"
        """
        super().__init__(*args, **kwargs)


class Planet(SolarObj):
    """Тип данных, описывающий планету.
    Содержит массу, координаты, скорость планеты,
    а также визуальный радиус планеты в пикселах и её цвет
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
