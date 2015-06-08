#!/usr/bin/env python
#coding: UTF-8
import sys


def rol(x, s):
    return (x << s | x >> (32 - s)) & 0xFFFFFFFF
    
    
def inv(dword):
    res = 0
    res |= ((dword >> 0) & 0xFF) << 24
    res |= ((dword >> 8) & 0xFF) << 16
    res |= ((dword >> 16) & 0xFF) << 8
    res |= ((dword >> 24) & 0xFF) << 0
    return res
    

def ripemd160(m):
    m = [ord(i) for i in m]

    # Шаг 1. Выравнивание потока
    bitLen = len(m) * 8
    m.append(0x80)
    zeroesNum = (56 - len(m) % 64 + 64) % 64
    m.extend([0] * zeroesNum)

    # Шаг 2. Добавление длины сообщения (в битах)
    for i in range(8):
        m.append((bitLen >> i * 8) & 0xFF)

    blocks = []
    for i in range(len(m) / 4):
        bl = 0
        bl |= m[i * 4 + 0] << 0
        bl |= m[i * 4 + 1] << 8
        bl |= m[i * 4 + 2] << 16
        bl |= m[i * 4 + 3] << 24
        blocks.append(bl)

    # Шаг 3. Определение действующих функций и констант
    def f(j, x, y, z):
        if j < 16:
            return x ^ y ^ z

        if j < 32:
            return (x & y) | (~x & z)

        if j < 48:
            return (x | ~y) ^ z

        if j < 64:
            return (x & z) | (y & ~z)

        if j < 80:
            return x ^ (y | ~z)

    def K1(j):
        if j < 16:
            return 0x00000000

        if j < 32:
            return 0x5A827999

        if j < 48:
            return 0x6ED9EBA1

        if j < 64:
            return 0x8F1BBCDC

        if j < 80:
            return 0xA953FD4E

    def K2(j):
        if j < 16:
            return 0x50A28BE6

        if j < 32:
            return 0x5C4DD124

        if j < 48:
            return 0x6D703EF3

        if j < 64:
            return 0x7A6D76E9

        if j < 80:
            return 0x00000000
            
    R1 = [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8,
        3, 10, 14, 4, 9, 15, 8, 1, 2, 7, 0, 6, 13, 11, 5, 12,
        1, 9, 11, 10, 0, 8, 12, 4, 13, 3, 7, 15, 14, 5, 6, 2,
        4, 0, 5, 9, 7, 12, 2, 10, 14, 1, 3, 8, 11, 6, 15, 13
    ]

    R2 = [
        5, 14, 7, 0, 9, 2, 11, 4, 13, 6, 15, 8, 1, 10, 3, 12,
        6, 11, 3, 7, 0, 13, 5, 10, 14, 15, 8, 12, 4, 9, 1, 2,
        15, 5, 1, 3, 7, 14, 6, 9, 11, 8, 12, 2, 10, 0, 4, 13,
        8, 6, 4, 1, 3, 11, 15, 0, 5, 12, 2, 13, 9, 7, 10, 14,
        12, 15, 10, 4, 1, 5, 8, 7, 6, 2, 13, 14, 0, 3, 9, 11
    ]

    S1 = [
        11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8,
        7, 6, 8, 13, 11, 9, 7, 15, 7, 12, 15, 9, 11, 7, 13, 12,
        11, 13, 6, 7, 14, 9, 13, 15, 14, 8, 13, 6, 5, 12, 7, 5,
        11, 12, 14, 15, 14, 15, 9, 8, 9, 14, 5, 6, 8, 6, 5, 12,
        9, 15, 5, 11, 6, 8, 13, 12, 5, 12, 13, 14, 11, 8, 5, 6
    ]

    S2 = [
        8, 9, 9, 11, 13, 15, 15, 5, 7, 7, 8, 11, 14, 14, 12, 6,
        9, 13, 15, 7, 12, 8, 9, 11, 7, 7, 12, 7, 6, 15, 13, 11,
        9, 7, 15, 11, 8, 6, 6, 14, 12, 13, 5, 14, 13, 13, 7, 5,
        15, 5, 8, 11, 14, 14, 6, 14, 6, 9, 12, 9, 12, 5, 15, 8,
        8, 5, 12, 9, 12, 5, 14, 6, 8, 13, 6, 5, 15, 13, 11, 11
    ]

    h = [0] * 5
    h[0] = 0x67452301
    h[1] = 0xEFCDAB89
    h[2] = 0x98BADCFE
    h[3] = 0x10325476
    h[4] = 0xC3D2E1F0

    # Шаг 4. Вычисление в цикле
    for n in range(0, len(blocks), 16):
        x = blocks[n:n+16]

        A1 = h[0]
        B1 = h[1]
        C1 = h[2]
        D1 = h[3]
        E1 = h[4]

        A2 = h[0]
        B2 = h[1]
        C2 = h[2]
        D2 = h[3]
        E2 = h[4]

        for j in range(80):
            T = A1 + f(j, B1, C1, D1) + x[R1[j]] + K1(j)
            T &= 0xFFFFFFFF
            T = rol(T, S1[j]) + E1
            T &= 0xFFFFFFFF
            A1 = E1
            E1 = D1
            D1 = rol(C1, 10)
            C1 = B1
            B1 = T

            T = A2 + f(79 - j, B2, C2, D2) + x[R2[j]] + K2(j)
            T &= 0xFFFFFFFF
            T = rol(T, S2[j]) + E2
            T &= 0xFFFFFFFF
            A2 = E2
            E2 = D2
            D2 = rol(C2, 10)
            C2 = B2
            B2 = T

        T = h[1] + C1 + D2
        h[1] = h[2] + D1 + E2
        h[2] = h[3] + E1 + A2
        h[3] = h[4] + A1 + B2
        h[4] = h[0] + B1 + C2
        h[0] = T
        h = [i & 0xFFFFFFFF for i in h]

    # получение результата вычислений
    res = ""
    for i in h:
        res += "{:08x}".format(inv(i))
    return res


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print ("Usage: ripemd160 file")
		sys.exit(1)
	file = open(sys.argv[1])
	data = file.read()
	print(ripemd160(data))
