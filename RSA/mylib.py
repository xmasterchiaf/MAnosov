#!/usr/bin/env python
#coding: UTF-8

import random
import sys
import bigNumber.bigNumber as bigNumber
bigNumber.initRandom() # инициализация генератора больших случайных чисел

# чтение числа из файла
def readNum(filename):
    try:
        f = open(filename)
    except:
        print "Не могу открыть файл {}".format(filename)
        sys.exit(1)
    numstr = f.read().rstrip("\n") # убираем перенос строки в конце
    n = bigNumber.bigNumber(numstr) # генерируем большое число из строки
    return n


# запись числа в файл
def writeNum(filename, n):
    open(filename, 'w').write(str(n)) # получаем строковое представление большого числа и записываем в файл
    

# получить простое число используя тест Ферма
# входной параметр - длина числа в битах
def genPrime(bits):
    P = bigNumber.GenerateRandomLen(bits) # библиотека генерирует случайное большое число
    while not FermaTest(P):
        P += 1
    return P

def FermaTest(n):
    for i in range(32): # число повторений теста
        #a = random.randint(1, n)
        a = bigNumber.GenerateRandomMax(n)
        if bigNumber.Pow(a, n-1, n) != 1:
            return False
    return True


# x = 1/a mod b
def inv(a, b):
    m = b            
    x1 = bigNumber.bigNumber(0)
    x2 = bigNumber.bigNumber(1)
    y1 = bigNumber.bigNumber(1)
    y2 = bigNumber.bigNumber(0)
    
    while b != 0:
        q = a / b
        r = a % b
        a = b
        b = r
        xx = x2 - x1 * q
        yy = y2 - y1 * q
        x2 = x1
        x1 = xx
        y2 = y1
        y1 = yy
    x = x2
    y = y2

    return (x + m) % m
