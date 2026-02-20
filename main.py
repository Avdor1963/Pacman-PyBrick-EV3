#!/usr/bin/env pybricks-micropython
"""
    Игра Пакман.
"""

# Эта программа требует LEGO EV3 MicroPython v2.0 или выше.
# Кликните левой кнопкой мыши на "Открыть руководство по расширению" на панели расширений EV3
#  для получения дополнительной информации.

import array
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

# Создаем объект EV3Brick для нашего контроллера EV3
ev3 = EV3Brick()
class pakman():
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
    def __init__(self, size: int, x: int, y: int, radius: int, rot: int, x_glaz: int, y_glaz: int, temp: int, napr: int):  
        """ Создаем нашего игрока "Пакмана".  """
        self.size    = size             # размер клетки игрового поля
        self.radius  = radius           # радиус пакмана
        self.x       = x * size         # начальные координаты клетки
        self.y       = y * size         # для вывода пакмана
        self.rot     = rot              # максимальный полуугол раскрытия рта пакмана (в пикселях), задает число фаз 
        self.x_glaz  = x_glaz           # координаты глаза пакмана
        self.y_glaz  = y_glaz           # относительно центра пакмана
        self.x_centr = size//2          # координаты центра пакмана, 
        self.y_centr = size//2          # относительно верхнего левого угла клетки пакмана 
        self.temp    = temp             # темп изменения фазы рта пакмана
        self.ct_temp = temp             # счетчик темпа
        self.napr    = napr             # начальное направление движения пакмана 0 - вверх, 1 - вправо, 2 - вниз, 3 - влево
        next_napr    = napr             # следующее направление движения пакмана, то есть в следующей клетке
        self.takt    = 0                # счетчик тактов
        #self.stop    = False           # признак остановки пакмана
        self.faza    = 0                # фаза отображения пакмана
        napr_faza    = 0                # 0 - раскрываем рот, 1 - закрываем рот
    
    def izm_napr(self, napr: int):
        """ Изменяем направление движения пакмана. """
        self.napr = napr

    def draw_pakman(self):
        """
        Перерисовываем пакмана в соответсвии с новым направлением движения и границами.
        """
        self.ct_temp -= 1
        if self.ct_temp == 0: 
            self.ct_temp = self.temp
            self.faza = self.faza + 1
            if self.faza == self.rot: self.faza = 0
        self.takt = self.takt + 1
        if self.takt == self.size:
            self.takt = 0
            self.faza = self.faza + 1
            if self.faza == self.rot: self.faza = 0
        # Стираем предыдущее изображение пакмана 
        ev3.screen.draw_box(self.x, self.y, self.x + self.size, self.y + self.size, 0, True, Color.WHITE)
        # Вычисляем новое положение пакмана
        # при движении вверх 
        if self.napr == 0:                  
            if kletka.border(self.y, 0):
                self.y_centr = 0
                self.stop = True
            self.y -= 1
        # при движении вправо 
        elif self.napr == 1:
            pass
        # при движении вниз 
        elif self.napr == 2:
            pass
        # при движении влево 
        elif self.napr == 3:
            pass

class kletka():
    """
    Клетка игрового поля. Задаем размер клетки и верхний левый угол. 
    Задаем границы клетки 0 - нет границы, то есть проход пакмана разрешен, 1 - есть граница, то есть проход пакмана запрещен  .
    """
    def __init__(self, size: int, x: int, y: int, up: int, right: int, down: int, left: int):
        """ Создаем клетку игрового поля размером в size и задаем состояние 4-х границ клетки """
        self.size   = size             # размер клетки
        self.x      = x * size         # координаты верхнего левого угла клетки
        self.y      = y * size         # относительно верхнего левого угла игрового поля
        self.up     = up               # граница сверху клетки
        self.right  = right            # граница справа клетки
        self.down   = down             # граница снизу клетки
        self.left   = left             # граница слева клетки
        
    def kletka(self):
        """ прорисовываем границы клетки """
        if self.up == 1:
            ev3.screen.draw_line(self.x,             self.y,             self.x + self.size, self.y            )
        elif self.right == 1:
            ev3.screen.draw_line(self.x + self.size, self.y,             self.x + self.size, self.y + self.size)
        elif self.down == 1:
            ev3.screen.draw_line(self.x,             self.y + self.size, self.x + self.size, self.y + self.size)
        elif self.left == 1:
            ev3.screen.draw_line(self.x + self.size, self.y,             self.x,             self.y + self.size)

    def is_border(self, x: int, y: int, napr: int) -> bool:
        if napr == 0:
            return self.up == 1 and y == self.y            
        elif napr == 1:
            return self.right == 1 and x == self.x + self.size
        elif napr == 2:
            return self.down == 1 and y == self.y + self.size
        elif napr == 3:
            return self.left == 1 and x == self.x

pole = []
for x in range(8):
    pole.append([])
    for y in range(11):
        pole[x].append(kletka(16, x, y, 0, 0, 0, 0))

# Выдаем начальный гудок от том, что наша программа запустилась. 
# лучше оставить эту команду для проверки старта программы
ev3.speaker.beep()
# Свой код начинаем писать здесь
ev3.screen.clear()
while True:
    ev3.screen.draw_circle(80, 80, 9, False, Color.BLACK)
    ev3.screen.draw_circle(80, 80, 8, False, Color.BLACK)
    ev3.screen.draw_circle(80, 80, 7, True, Color.RED)
    ev3.screen.draw_box(76, 76, 78, 78, 1, True, Color.BLACK)
    ev3.screen.draw_line(82, 80, 89, 80, 1, Color.BLACK)
    # while not ev3.buttons.pressed():
    #     pass
    wait(200)
    ev3.screen.draw_circle(80, 80, 9, False, Color.BLACK)
    ev3.screen.draw_circle(80, 80, 8, False, Color.BLACK)
    ev3.screen.draw_circle(80, 80, 7, True, Color.RED)
    ev3.screen.draw_box(76, 76, 78, 78, 1, True, Color.BLACK)
    ev3.screen.draw_line(82, 80, 89, 79, 1, Color.BLACK)
    ev3.screen.draw_line(82, 80, 89, 80, 1, Color.WHITE)
    ev3.screen.draw_line(82, 80, 89, 81, 1, Color.BLACK)
    wait(200)
    ev3.screen.draw_circle(80, 80, 9, False, Color.BLACK)
    ev3.screen.draw_circle(80, 80, 8, False, Color.BLACK)
    ev3.screen.draw_circle(80, 80, 7, True, Color.RED)
    ev3.screen.draw_box(76, 76, 78, 78, 1, True, Color.BLACK)
    ev3.screen.draw_line(81, 80, 89, 78, 1, Color.BLACK)
    ev3.screen.draw_line(81, 80, 89, 79, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 80, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 81, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 82, 1, Color.BLACK)
    wait(200)
    ev3.screen.draw_circle(80, 80, 9, False, Color.BLACK)
    ev3.screen.draw_circle(80, 80, 8, False, Color.BLACK)
    ev3.screen.draw_circle(80, 80, 7, True, Color.RED)
    ev3.screen.draw_box(76, 76, 78, 78, 1, True, Color.BLACK)
    ev3.screen.draw_line(81, 80, 89, 77, 1, Color.BLACK)
    ev3.screen.draw_line(81, 80, 89, 78, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 79, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 80, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 81, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 82, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 83, 1, Color.BLACK)
    wait(200)
    ev3.screen.draw_circle(80, 80, 9, False, Color.BLACK)
    ev3.screen.draw_circle(80, 80, 8, False, Color.BLACK)
    ev3.screen.draw_circle(80, 80, 7, True, Color.RED)
    ev3.screen.draw_box(76, 76, 78, 78, 1, True, Color.BLACK)
    ev3.screen.draw_line(81, 80, 89, 76, 1, Color.BLACK)
    ev3.screen.draw_line(81, 80, 89, 77, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 78, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 79, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 80, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 81, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 82, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 83, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 84, 1, Color.BLACK)
    wait(200)
    ev3.screen.draw_circle(80, 80, 9, False, Color.BLACK)
    ev3.screen.draw_circle(80, 80, 8, False, Color.BLACK)
    ev3.screen.draw_circle(80, 80, 7, True, Color.RED)
    ev3.screen.draw_box(76, 76, 78, 78, 1, True, Color.BLACK)
    ev3.screen.draw_line(81, 80, 89, 75, 1, Color.BLACK)
    ev3.screen.draw_line(81, 80, 89, 76, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 77, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 78, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 79, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 80, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 81, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 82, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 83, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 84, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 85, 1, Color.BLACK)
    wait(200)
    ev3.screen.draw_circle(80, 80, 9, False, Color.BLACK)
    ev3.screen.draw_circle(80, 80, 8, False, Color.BLACK)
    ev3.screen.draw_circle(80, 80, 7, True, Color.RED)
    ev3.screen.draw_box(76, 76, 78, 78, 1, True, Color.BLACK)
    ev3.screen.draw_line(81, 80, 89, 76, 1, Color.BLACK)
    ev3.screen.draw_line(81, 80, 89, 77, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 78, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 79, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 80, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 81, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 82, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 83, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 84, 1, Color.BLACK)
    wait(200)
    ev3.screen.draw_circle(80, 80, 9, False, Color.BLACK)
    ev3.screen.draw_circle(80, 80, 8, False, Color.BLACK)
    ev3.screen.draw_circle(80, 80, 7, True, Color.RED)
    ev3.screen.draw_box(76, 76, 78, 78, 1, True, Color.BLACK)
    ev3.screen.draw_line(81, 80, 89, 77, 1, Color.BLACK)
    ev3.screen.draw_line(81, 80, 89, 78, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 79, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 80, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 81, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 82, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 83, 1, Color.BLACK)
    wait(200)
    ev3.screen.draw_circle(80, 80, 9, False, Color.BLACK)
    ev3.screen.draw_circle(80, 80, 8, False, Color.BLACK)
    ev3.screen.draw_circle(80, 80, 7, True, Color.RED)
    ev3.screen.draw_box(76, 76, 78, 78, 1, True, Color.BLACK)
    ev3.screen.draw_line(81, 80, 89, 78, 1, Color.BLACK)
    ev3.screen.draw_line(81, 80, 89, 79, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 80, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 81, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 82, 1, Color.BLACK)
    wait(200)
    ev3.screen.draw_circle(80, 80, 9, False, Color.BLACK)
    ev3.screen.draw_circle(80, 80, 8, False, Color.BLACK)
    ev3.screen.draw_circle(80, 80, 7, True, Color.RED)
    ev3.screen.draw_box(76, 76, 78, 78, 1, True, Color.BLACK)
    ev3.screen.draw_line(81, 80, 89, 79, 1, Color.BLACK)
    ev3.screen.draw_line(81, 80, 89, 80, 1, Color.WHITE)
    ev3.screen.draw_line(81, 80, 89, 81, 1, Color.BLACK)
    wait(200)
    ev3.screen.draw_circle(80, 80, 9, False, Color.BLACK)
    ev3.screen.draw_circle(80, 80, 8, False, Color.BLACK)
    ev3.screen.draw_circle(80, 80, 7, True, Color.RED)
    ev3.screen.draw_box(76, 76, 78, 78, 1, True, Color.BLACK)
    ev3.screen.draw_line(82, 80, 89, 80, 1, Color.BLACK)
    wait(200)
