#!/usr/bin/env pybricks-micropython
"""
    Игра ПАКМАН.
"""

# Эта программа требует LEGO EV3 MicroPython v2.0 или выше.
# Кликните левой кнопкой мыши на "Открыть руководство по расширению" на панели расширений EV3
#  для получения дополнительной информации.

from pybricks.hubs import EV3Brick
# from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                #  InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Button, Color #Port, Stop, Direction,
from pybricks.tools import wait#, StopWatch, DataLog
# from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import Font # SoundFile, ImageFile,

# Свой код начинаем писать здесь
from pakman import *

# функция паузы в игре. Можем поменять настройки игры. Также выход из игры.
def pauza():
    """ Пауза в игре """
    global IS_RUN
    print("пауза")
    if not ev3.buttons.pressed():                   # вначале ждем отпускания кнопки "E"
        pass
    print("пауза =====")
    # while not any(ev3.buttons.pressed()):            # затем ждем нажатия кнопки
    #     pass
    while not ev3.buttons.pressed() == [Button.UP]:
        if ev3.buttons.pressed() == [Button.DOWN]:   # если нажата кнопка "D"
            IS_RUN = False                          # то выходим из игры
    print("конец паузы ", IS_RUN)

# Создаем объект EV3Brick для нашего контроллера EV3
ev3 = EV3Brick()

# Выдаем начальный гудок от том, что наша программа запустилась.
# лучше оставить эту команду для проверки старта программы
ev3.speaker.beep()

ev3.screen.clear()
MyFont = Font(size=20, lang="ru")
ev3.screen.set_font(MyFont)

# создаем игровое поле
SIZE  = 16              # размер клетки игрового поля
MAX_X = 11              # количество клеток по горизонтали
MAX_Y = 8               # количество клеток по вертикали
X, Y  = 5, 3            # координаты пакмана в игровом поле по горизонтали и вертикали

pole = []               # игровое поле

for x in range(MAX_X):  # создаем игровое поле с внешними границами
    pole.append([])
    for y in range(MAX_Y):
        pole[x].append(kletka(SIZE, x, y, 0, 0, 0, 0))
        if  y == 0:          # верхняя граница
            pole[x][y].up = 1
        if x == MAX_X - 1: # правая граница
            pole[x][y].right = 1
        if y == MAX_Y - 1: # нижняя граница
            pole[x][y].down = 1
        if x == 0:         # левая граница
            pole[x][y].left = 1

#--------горизонтали -----------------
pole[1][0].down = 1; pole[1][1].up = 1
pole[2][0].down = 1; pole[2][1].up = 1
pole[3][0].down = 1; pole[3][1].up = 1
pole[4][0].down = 1; pole[4][1].up = 1
pole[6][0].down = 1; pole[6][1].up = 1
pole[7][0].down = 1; pole[7][1].up = 1
pole[8][0].down = 1; pole[8][1].up = 1
pole[9][0].down = 1; pole[9][1].up = 1
#-------------------------------------
pole[1][1].down = 1; pole[1][2].up = 1
pole[3][1].down = 1; pole[3][2].up = 1
pole[5][1].down = 1; pole[5][2].up = 1
pole[7][1].down = 1; pole[7][2].up = 1
pole[9][1].down = 1; pole[9][2].up = 1
#-------------------------------------
pole[1][2].down = 1; pole[1][3].up = 1
pole[2][2].down = 1; pole[2][3].up = 1
pole[3][2].down = 1; pole[3][3].up = 1
pole[4][2].down = 1; pole[4][3].up = 1
pole[6][2].down = 1; pole[6][3].up = 1
pole[7][2].down = 1; pole[7][3].up = 1
pole[8][2].down = 1; pole[8][3].up = 1
pole[9][2].down = 1; pole[9][3].up = 1
#-------------------------------------
pole[1][3].down = 1; pole[1][4].up = 1
pole[2][3].down = 1; pole[2][4].up = 1
pole[5][3].down = 1; pole[5][4].up = 1
pole[8][3].down = 1; pole[8][4].up = 1
pole[9][3].down = 1; pole[9][4].up = 1
#-------------------------------------
pole[1][4].down = 1; pole[1][5].up = 1
pole[2][4].down = 1; pole[2][5].up = 1
pole[3][4].down = 1; pole[3][5].up = 1
pole[4][4].down = 1; pole[4][5].up = 1
pole[6][4].down = 1; pole[6][5].up = 1
pole[7][4].down = 1; pole[7][5].up = 1
pole[8][4].down = 1; pole[8][5].up = 1
pole[9][4].down = 1; pole[9][5].up = 1
#-------------------------------------
pole[1][5].down = 1; pole[1][6].up = 1
pole[3][5].down = 1; pole[3][6].up = 1
pole[5][5].down = 1; pole[5][6].up = 1
pole[7][5].down = 1; pole[7][6].up = 1
pole[9][5].down = 1; pole[9][6].up = 1
#-------------------------------------
pole[1][6].down = 1; pole[1][7].up = 1
pole[2][6].down = 1; pole[2][7].up = 1
pole[3][6].down = 1; pole[3][7].up = 1
pole[4][6].down = 1; pole[4][7].up = 1
pole[6][6].down = 1; pole[6][7].up = 1
pole[7][6].down = 1; pole[7][7].up = 1
pole[8][6].down = 1; pole[8][7].up = 1
pole[9][6].down = 1; pole[9][7].up = 1
#----------вертикали---------------------
pole[0][1].right = 1; pole[1][1].left = 1
pole[0][6].right = 1; pole[1][6].left = 1
#----------------------------------------
pole[2][2].right = 1; pole[3][2].left = 1
pole[2][5].right = 1; pole[3][5].left = 1
#----------------------------------------
pole[3][3].right = 1; pole[4][3].left = 1
pole[3][4].right = 1; pole[4][4].left = 1
#----------------------------------------
pole[6][3].right = 1; pole[7][3].left = 1
pole[6][4].right = 1; pole[7][4].left = 1
#----------------------------------------
pole[7][2].right = 1; pole[8][2].left = 1
pole[7][5].right = 1; pole[8][5].left = 1
#-----------------------------------------
pole[9][1].right = 1; pole[10][1].left = 1
pole[9][6].right = 1; pole[10][6].left = 1
#-----------------------------------------
# рисуем игровое поле
for x in range(MAX_X):
    for y in range(MAX_Y):
        pole[x][y].dot = 1
        pole[x][y].draw_kletka()
ev3.screen.draw_line(0, 127, 175, 127, 1)       # нижняя строка
print("нарисовали поле")
# pr = input("нарисовали поле")

# создаем пакмана в центре игрового поля, движущегося вправо
pak_man = Pakman(SIZE, X, Y, SIZE // 2 - 1, 6, 4, 2, SIZE // 8, 1)

# начальная клетка в которой находится пакман
tek_kletka = pole[X][Y]

pak_man.draw_pakman()

IS_RUN = True               # признак запуска движения пакмана

while IS_RUN:
    # выполняем один такт движения пакмана
    in_kletka = pak_man.takt_pakman()           # флаг того, что пакман полностью вошел в клетку
    # если пакман вошел в клетку проверяем не упремся ли мы в стенку при текущем направлении движения
    if in_kletka:
        # перезадаем текущую клетку в которой находится пакман
        X = pak_man.x // pak_man.size
        Y = pak_man.y // pak_man.size
        tek_kletka = pole[X][Y]
        if tek_kletka.dot == 1:
            tek_kletka.dot = 0            # убираем точку с клетки, то есть съедаем её
            # если пакман в клетке с точкой то прибавляем очко
            pak_man.score += 1
            if pak_man.score == MAX_X * MAX_Y:
                IS_RUN = False
                ev3.screen.draw_text(0, 10, "ВЫ ВЫИГРАЛИ", Color.BLACK, Color.WHITE)
        pak_man.napr = pak_man.next_napr            # Только внутри клетки мы изменяем направление.
        # прорверяем упирается ли он в стенку
        if pak_man.napr == 0 and tek_kletka.up    or \
           pak_man.napr == 1 and tek_kletka.right or \
           pak_man.napr == 2 and tek_kletka.down  or \
           pak_man.napr == 3 and tek_kletka.left     \
           :
            # если упирается то останавливаем движение пакмана
            # if pak_man.next_napr != pak_man.napr:
            #     if pak_man.napr_izm == 0:
            #         pak_man.next_napr = pak_man.napr
            #         pak_man.napr_izm = 1
            #     else:
            pak_man.stop = True
        else:
            # иначе сбрасываем стоп пакмана,если он был, и продолжаем движение
            pak_man.stop = False
        #     pak_man.napr_izm = 0
    # проверяем нажатие кнопок блока EV3
    # if ev3.buttons.pressed():
    if any(ev3.buttons.pressed()):
        print(ev3.buttons.pressed())
        if   ev3.buttons.pressed() == [Button.CENTER]:
            pauza()
        elif ev3.buttons.pressed() == [Button.UP]:
            pak_man.izm_napr(0)
        elif ev3.buttons.pressed() == [Button.RIGHT]:
            pak_man.izm_napr(1)
        elif ev3.buttons.pressed() == [Button.DOWN]:
            pak_man.izm_napr(2)
        elif ev3.buttons.pressed() == [Button.LEFT]:
            pak_man.izm_napr(3)

    # такт игры
    wait(20)

wait(10000)
