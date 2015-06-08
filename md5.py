#!/usr/bin/env python
#coding: UTF-8
import sys
from math import sin, fabs

def F(x, y, z):
    return (x & y) | (~x & z)

def G(x, y, z):
    return (x & z) | (~z & y)

def H(x, y, z):
    return x ^ y ^ z

def I(x, y, z):
    return y ^ (~z | x)


def T(i):
    return int(0x100000000 * fabs(sin(i)))

# циклический сдвиг влево
def rol(x, s):
    return (x << s | x >> (32-s)) & 0xFFFFFFFF

# [F abcd k s i] a = b + ((a + F(b,c,d) + X[k] + T[i]) <<< s)
def md5Operator(Fun, a, b, c, d, x, s, ti):
    a = (a + Fun(b, c, d) + x + ti) & 0xFFFFFFFF
    a = rol(a, s)
    a = (a + b) & 0xFFFFFFFF
    return a


def inv(dword):
    res = 0
    res |= ((dword >> 0) & 0xFF) << 24
    res |= ((dword >> 8) & 0xFF) << 16
    res |= ((dword >> 16) & 0xFF) << 8
    res |= ((dword >> 24) & 0xFF) << 0
    return res


def md5(m):
    m = [ord(i) for i in m]

    # Шаг 1. Выравнивание потока
    bitLen = len(m) * 8
    m.append(0x80)
    zeroesNum = (56 - len(m) % 64 + 64) % 64
    m.extend([0] * zeroesNum)

    # Шаг 2. Добавление длины сообщения (в битах)
    for i in range(8):
        m.append((bitLen >> i * 8) & 0xFF)
    
    # Шаг 3. Инициализация буфера
    a = 0x67452301
    b = 0xEFCDAB89
    c = 0x98BADCFE
    d = 0x10325476

    # объединение байт в блоки по 32 бита
    blocks = []
    for i in range(len(m) / 4):
        bl = 0
        bl |= m[i * 4 + 0] << 0
        bl |= m[i * 4 + 1] << 8
        bl |= m[i * 4 + 2] << 16
        bl |= m[i * 4 + 3] << 24
        blocks.append(bl)

    # Шаг 4. Вычисление в цикле
    for n in range(0, len(blocks), 16):
        chunk = blocks[n:n+16]

        AA = a
        BB = b
        CC = c
        DD = d

        # параметры для каждого раунда - s, k (и её шаг), функция
        params = [
            ((7, 12, 17, 22), 0, 1, F),
            ((5,  9, 14, 20), 1, 5, G),
            ((4, 11, 16, 23), 5, 3, H),
            ((6, 10, 15, 21), 0, 7, I)
        ]

        i = 1
        for round in range(4): # число раундов
            S, k, step, Func = params[round]
            for j in range(4): # в каждом раунде по 16 операций
                a = md5Operator(Func, a, b, c, d, chunk[k], S[0], T(i))
                i += 1
                k = (k + step) % 16
                
                d = md5Operator(Func, d, a, b, c, chunk[k], S[1], T(i))
                i += 1
                k = (k + step) % 16
                
                c = md5Operator(Func, c, d, a, b, chunk[k], S[2], T(i))
                i += 1
                k = (k + step) % 16
                
                b = md5Operator(Func, b, c, d, a, chunk[k], S[3], T(i))
                i += 1
                k = (k + step) % 16

        a = AA + a
        b = BB + b
        c = CC + c
        d = DD + d

    # получение результата вычислений
    res = ""
    for i in [a, b, c, d]:
        res += "{:08x}".format(inv(i))
    return res


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print ("Usage: md5 file")
		sys.exit(1)
	file = open(sys.argv[1])
	data = file.read()
	print(md5(data))
