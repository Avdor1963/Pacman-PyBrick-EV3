"""
    Игра Пакман.
"""

# Эта программа требует LEGO EV3 MicroPython v2.0 или выше.
# Кликните левой кнопкой мыши на "Открыть руководство по расширению" на панели расширений EV3
#  для получения дополнительной информации.

from pybricks.hubs import EV3Brick
# from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
#                                  InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Color #Port, Stop, Direction, Button,
#from pybricks.tools import wait, StopWatch, DataLog
# from pybricks.robotics import DriveBase
# from pybricks.media.ev3dev import SoundFile, ImageFile

# Создаем объект EV3Brick для нашего контроллера EV3
ev3 = EV3Brick()
class Pakman():
    """
    Пакман - игровой персонаж на экране EV3. Занимает одну клетку 16х16 пикселей игрового поля 11 на 7 клеток.
    Передвигается строго по горизонтали и вертикали. Направление задается (0 - вверх, 1 - вправо, 2 - вниз, 3 - влево)
    соответсвующими кнопками контроллера EV3. Изменять направление может только по клеткам игрового поля, то есть 
    при получении команды сменить направление движения пакман должен дойти до средины клетки и только тогда
    повернуть в нужном направлении, если это разрешено границами игрового поля и межклеточными границами.
    Пакман рисуется в виде закрашенного круга с открытым глазом и с раскрываемым по фазам ртом. Глаз и рот пакмана
    рисуются, в зависимости от направления движения пакмана. Фаза раскрытия рта изменяется с заданным тактом temp, 
    координата движения пакмана изменяется на 1 пиксель раз в такт (при вызове функции draw_pakman). Сдвиг пакмана 
    осуществялся стиранием предыдущего изображения пакмана и рисованием нового. Пакман может остановится, если упрется 
    в границу игрового поля или межклеточную границу. При этом он не перестает раскрывать и закрывать рот.
    """
    def __init__(self, size: int, x: int, y: int, radius: int, rot: int, s_glaz: int, l_glaz: int, temp: int, napr: int):
        """ Создаем нашего игрока "Пакмана".  """
        self.size      = size             # размер клетки игрового поля
        self.radius    = radius           # радиус пакмана
        self.x         = x * size         # начальные координаты клетки
        self.y         = y * size         # для вывода пакмана
        self.rot       = rot              # максимальный полуугол раскрытия рта пакмана (в пикселях), задает число фаз
        self.s_glaz    = s_glaz           # смещение координат глаза пакмана
        self.l_glaz    = l_glaz           # относительно центра пакмана и его размер в пикселях
        self.x_centr   = size // 2        # координаты центра пакмана,
        self.y_centr   = size // 2        # относительно верхнего левого угла клетки пакмана
        self.temp      = temp             # темп изменения фазы рта пакмана
        self.ct_temp   = temp             # счетчик темпа
        self.napr      = napr             # начальное направление движения пакмана 0 - вверх, 1 - вправо, 2 - вниз, 3 - влево
        self.next_napr = napr             # следующее направление движения пакмана, то есть в следующей клетке
        self.takt      = 0                # счетчик тактов
        self.stop      = False            # признак остановки пакмана, задаем из внешней программы, когда пакман упирается в стенку
        self.faza      = 0                # фаза отображения пакмана
        self.napr_faza = 0                # 0 - раскрываем рот, 1 - закрываем рот
        self.score     = 0                # счет съеденных точек пакмана

    def izm_napr(self, napr: int):
        """ 
        Изменяем направление движения пакмана при полном вхождении пакмана в следующую клетку игрового поля.
        """
        self.next_napr = napr

    def draw_pakman(self):
        """
        Перерисовываем пакмана в соответсвии с новым направлением движения.
        """
        # общий для всех направлений заполненный круг
        ev3.screen.draw_circle(self.x + self.x_centr, self.y + self.y_centr, self.radius, True, Color.BLACK)       # внешний обод
        # ev3.screen.draw_circle(self.x + self.x_centr, self.y + self.y_centr, self.radius-1, True, Color.RED)          # заполнение

        # рисуем глаз пакмана
        if self.napr == 0:      # ртом вверх
            ev3.screen.draw_box(self.x + self.x_centr - self.s_glaz,               self.y + self.y_centr + self.s_glaz - self.l_glaz,
                                self.x + self.x_centr - self.s_glaz + self.l_glaz, self.y + self.y_centr + self.s_glaz,
                                1, True, Color.WHITE)
        elif self.napr == 1:    # ртом вправо
            ev3.screen.draw_box(self.x + self.x_centr - self.s_glaz, self.y + self.y_centr - self.s_glaz,
                                self.x + self.x_centr - self.s_glaz + self.l_glaz, self.y + self.y_centr - self.s_glaz + self.l_glaz,
                                1, True, Color.WHITE)
        elif self.napr == 2:    # ртом вниз
            ev3.screen.draw_box(self.x + self.x_centr - self.s_glaz,               self.y + self.y_centr - self.s_glaz,
                                self.x + self.x_centr - self.s_glaz + self.l_glaz, self.y + self.y_centr - self.s_glaz + self.l_glaz,
                                1, True, Color.WHITE)
        elif self.napr == 3:    # ртом влево
            ev3.screen.draw_box(self.x + self.x_centr + self.s_glaz - self.l_glaz, self.y + self.y_centr - self.s_glaz,
                                self.x + self.x_centr + self.s_glaz,               self.y + self.y_centr - self.s_glaz + self.l_glaz,
                                1, True, Color.WHITE)

        # прорисовываем фазу раскрытия рта
        if self.napr == 0:      # ртом вверх
            # print("0")
            for f in range(-self.faza, self.faza+1):
                # print("0 f - ", f)
                ev3.screen.draw_line(self.x + self.x_centr,               self.y + self.y_centr - 1,
                                     self.x + self.x_centr + f,           self.y + self.y_centr - self.radius,
                                        1, Color.WHITE)
        elif self.napr == 1:    # ртом вправо
            # print("1")
            for f in range(-self.faza, self.faza+1):
                # print("1 f - ", f)
                ev3.screen.draw_line(self.x + self.x_centr + 1,           self.y + self.y_centr,
                                     self.x + self.x_centr + self.radius, self.y + self.y_centr + f,
                                        1, Color.WHITE)
        elif self.napr == 2:    # ртом вниз
            # print("2")
            for f in range(-self.faza, self.faza+1):
                # print("2 f - ", f)
                ev3.screen.draw_line(self.x + self.x_centr,               self.y + self.y_centr + 1,
                                     self.x + self.x_centr + f,           self.y + self.y_centr + self.radius,
                                        1, Color.WHITE)
        elif self.napr == 3:        # ртом влево
            # print("3")
            for f in range(-self.faza, self.faza+1):
                # print("3 f - ", f)
                ev3.screen.draw_line(self.x + self.x_centr - 1,           self.y + self.y_centr,
                                     self.x + self.x_centr - self.radius, self.y + self.y_centr + f,
                                        1, Color.WHITE)

    def takt_pakman(self):
        """
        Один такт движения пакмана в соответсвии с новым направлением движения и границами.
        """
        # вычисляем фазу раскрытия/закрытия рта
        self.ct_temp -= 1                   # отсчитываем такт фазы
        if self.ct_temp == 0:
            # print("nf=", self.napr_faza, "f=", self.faza, "rot=", self.rot)
            self.ct_temp = self.temp        # перезадаем счетчик темпа изменения фаз пакмана
            if self.napr_faza == 0:         # если раскрываем рот
                self.faza += 1              # то увеличиваем фазу
                if self.faza == self.rot:   # если полностью раскрыли рот,
                    self.napr_faza = 1      # то меняем фазу на закрытие рта
            elif self.napr_faza == 1:       # если закрываем рот
                self.faza -= 1              # то уменьшаем фазу
                if self.faza == 0:          # если полностью закрыли рот,
                    self.napr_faza = 0      # то меняем фазу на открытие рта
            # print("nf=", self.napr_faza, "f=", self.faza, "rot=", self.rot)

        # Стираем предыдущее изображение пакмана
        ev3.screen.draw_box(self.x + 1, self.y + 1, self.x + self.size - 1, self.y + self.size - 1, 0, True, Color.WHITE)
        # Вычисляем новое положение пакмана
        if not self.stop:
            # при движении вверх
            if self.napr == 0:
                self.y -= 1
            # при движении вправо
            elif self.napr == 1:
                self.x += 1
            # при движении вниз
            elif self.napr == 2:
                self.y += 1
            # при движении влево
            elif self.napr == 3:
                self.x -= 1

        # Выводим пакмана в новом положении
        self.draw_pakman()

        # print("t=", self.takt, "n=", self.napr, "x=", self.x, "y=", self.y, "nn=", self.next_napr, "stop=", self.stop,
            #   "tf=", self.ct_temp, "f=", self.faza, "nf=", self.napr_faza)

        # отслеживаем полное попадание в клетку игрового поля при движении пакмана
        self.takt = self.takt + 1
        if self.takt == self.size or self.stop:     # при стопе каждый такт начальный так как мы уже стоим в клетке
            self.takt = 0
            self.napr = self.next_napr              # только сейчас меняем направление движения пакмана
            return True                             # и сообщаем, что пакман полностью вдвинулся в клетку игрового поля
        return False                                # иначе сообщаем, что мы еще в движении

class kletka():
    """
    Клетка игрового поля. Задаем размер клетки и верхний левый угол. 
    Задаем границы клетки 0 - нет границы, то есть проход пакмана разрешен, 1 - есть граница, то есть проход пакмана запрещен  .
    """
    def __init__(self, size: int, x: int, y: int, up: int, right: int, down: int, left: int):
        """ Создаем клетку игрового поля размером в size и задаем состояние 4-х границ клетки """
        self.size   = size             # размер клетки
        self.xk     = x                # координаты клетки
        self.yk     = y                # в игровом поле
        self.x      = x * size         # координаты верхнего левого угла клетки
        self.y      = y * size         # относительно верхнего левого угла игрового поля
        self.up     = up               # граница сверху клетки
        self.right  = right            # граница справа клетки
        self.down   = down             # граница снизу клетки
        self.left   = left             # граница слева клетки
        self.dot    = 0                # наличие точки в клетке, которую пакман должен съесть

    def draw_kletka(self):
        """ прорисовываем границы клетки """
        if self.up == 1:
            ev3.screen.draw_line(self.x,             self.y,             self.x + self.size, self.y            )
        if self.right == 1:
            ev3.screen.draw_line(self.x + self.size, self.y,             self.x + self.size, self.y + self.size)
        if self.down == 1:
            ev3.screen.draw_line(self.x,             self.y + self.size, self.x + self.size, self.y + self.size)
        if self.left == 1:
            ev3.screen.draw_line(self.x,             self.y,             self.x,             self.y + self.size)
        if self.dot == 1:
            ev3.screen.draw_box(self.x + self.size // 2 - 1, self.y + self.size // 2 - 1,
                                self.x + self.size // 2 + 1, self.y + self.size // 2 + 1, 0, True)

        # print("x = ", self.x, " - y = ", self.y, self.up, self.right, self.down, self.left)
        # pr = input("нарисовали черту")

    def is_border(self, x: int, y: int, napr: int) -> bool:
        """ Проверяем, что имеет ли клетка в которой находится или в которую полностью вдвинулся пакман
            границу по направлению движения пакмана или нет. Если нет, то пакман может двигаться в эту сторону.                        . 
        """
        if napr == 0:
            return self.up == 1 and y == self.y
        elif napr == 1:
            return self.right == 1 and x == self.x + self.size
        elif napr == 2:
            return self.down == 1 and y == self.y + self.size
        elif napr == 3:
            return self.left == 1 and x == self.x
