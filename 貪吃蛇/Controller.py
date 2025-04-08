from typing import List
import pygame as pg
from Config import *
from Model import *
from random import *


def key_input(pressed_keys: List):
    """
    從 pygame 的鍵盤輸入判斷哪些按鍵被按下
    回傳方向
    """
    for key in pressed_keys:
        if key == pg.K_UP:
            movement = UP
            break
        if key == pg.K_DOWN:
            movement = DOWN
            break
        if key == pg.K_LEFT:
            movement = LEFT
            break
        if key == pg.K_RIGHT:
            movement = RIGHT
            break
        if key == pg.K_a:
            return "new"
    else:
        return None
    return movement


# 以下為大作業


def generate_wall(walls: List[Wall], player: Player, direction: int) -> None:
    """
    生成一個 `Wall` 的物件並加到 `walls` 裡面，不能與現有牆壁或玩家重疊
    新牆壁一定要與現有牆壁有接觸 (第一階段)，更好的話請讓牆壁朝著同個方向生長 (第二階段)
    無回傳值

    Keyword arguments:
    walls -- 牆壁物件的 list
    player -- 玩家物件
    direction -- 蛇的移動方向
    """

    wallx = 0
    wally = 0
    if len(walls) == 0:
        while 1:
            wallx = randint(0, 34) * 20
            wally = randint(0, 29) * 20
            if wallx == player.head_x and wally == player.head_y:
                continue
            walls.append(Wall((wallx, wally)))
            break
    else:
        if direction == 0:
            walls.append(Wall((walls[-1].pos_x, walls[-1].pos_y - SNAKE_SIZE)))
        elif direction == 1:
            walls.append(Wall((walls[-1].pos_x + SNAKE_SIZE, walls[-1].pos_y)))
        elif direction == 2:
            walls.append(Wall((walls[-1].pos_x, walls[-1].pos_y + SNAKE_SIZE)))
        elif direction == 3:
            walls.append(Wall((walls[-1].pos_x - SNAKE_SIZE, walls[-1].pos_y)))
    return direction


def generate_food(foods: List[Food], walls: List[Wall], player: Player) -> None:
    """
    在隨機位置生成一個 `Food` 的物件並加到 `foods` 裡面，不能與現有牆壁或玩家重疊
    無回傳值

    Keyword arguments:
    foods -- 食物物件的 list
    walls -- 牆壁物件的 list
    player -- 玩家物件
    """

    foodx = 0
    foody = 0
    while 1:
        foodx = randint(0, 34) * 20
        foody = randint(0, 29) * 20
        wf = 0
        sf = 0
        for i in range(player.length):
            if foodx == player.snake_list[i][0] and foody == player.snake_list[i][1]:
                sf = sf + 1
        for i in walls:
            if foodx == i.pos_x and foody == i.pos_y:
                wf = wf + 1
        if wf != 0 or sf != 0:
            continue
        foods.append(Food((foodx, foody)))
        break
    return


def generate_poison(walls: List[Wall], foods: List[Food], player: Player) -> None:
    """
    在隨機位置生成一個 `Poison` 的物件並回傳，不能與現有其他物件或玩家重疊
    無回傳值

    Keyword arguments:
    walls -- 牆壁物件的 list
    foods -- 食物物件的 list
    player -- 玩家物件
    """
    poix = 0
    poiy = 0
    while 1:
        poix = randint(0, 34) * 20
        poiy = randint(0, 29) * 20
        pf = 0
        pw = 0
        ps = 0
        for i in range(player.length):
            if poix == player.snake_list[i][0] and poiy == player.snake_list[i][1]:
                ps = ps + 1
        for i in walls:
            if poix == i.pos_x and poiy == i.pos_y:
                pw = pw + 1
        for i in foods:
            if poix == i.pos_x and poiy == i.pos_y:
                pf = pf + 1
        if pf != 0 or pw != 0:
            continue
        break
    return Poison((poix, poiy))


def generate_speedup(
    walls: List[Wall], foods: List[Food], player: Player, poison
) -> None:
    """
    吃到會FPS上升的方塊。
    """
    spx = 0
    spy = 0
    while 1:
        spx = randint(0, 34) * 20
        spy = randint(0, 29) * 20
        sf = 0
        sw = 0
        ss = 0
        sp = 0
        if spx == poison.pos_x and spy == poison.pos_y:
            continue
        for i in range(player.length):
            if spx == player.snake_list[i][0] and spy == player.snake_list[i][1]:
                ss = ss + 1
        for i in walls:
            if spx == i.pos_x and spy == i.pos_y:
                sw = sw + 1
        for i in foods:
            if spx == i.pos_x and spy == i.pos_y:
                sf = sf + 1
        if sf != 0 or sw != 0 or sp != 0 or ss != 0:
            continue
        break
    return Speedup((spx, spy))


def calculate_time_interval(player: Player, speedup) -> int:
    """
    根據蛇的長度，計算並回傳每一秒有幾幀
    蛇的長度每增加 4 幀數就 +1，從小到大，最大為 `TIME_INTERVAL_MAX`，最小為 `TIME_INTERVAL_MIN`
    """
    time = 0
    if player.length < 20:
        time = TIME_INTERVAL_MIN + player.length // 4 + speedup
    else:
        time = TIME_INTERVAL_MAX + speedup
    return time
