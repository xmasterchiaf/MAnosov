#!/usr/bin/env python
#coding: UTF-8
import sys

def rol(x, s):
    return (x << s | x >> (32 - s)) & 0xFFFFFFFF


def sha1(m):
    m = [ord(i) for i in m]

    # Шаг 1. Выравнивание потока
    bitLen = len(m) * 8
    m.append(0x80)
    zeroesNum = (56 - len(m) % 64 + 64) % 64
    m.extend([0] * zeroesNum)

    # Шаг 2. Добавление длины сообщения (в битах)
    for i in range(8):
        m.append((bitLen >> (7 - i) * 8) & 0xFF)

    blocks = []
    for i in range(len(m) / 4):
        bl = 0
        for k in range(4):
            bl |= m[i * 4 + k] << (3 - k) * 8
        blocks.append(bl)

    # Инициализация переменных
    h = [0] * 5
    h[0] = 0x67452301
    h[1] = 0xEFCDAB89
    h[2] = 0x98BADCFE
    h[3] = 0x10325476
    h[4] = 0xC3D2E1F0

    # Шаг 4. Вычисление в цикле
    for n in range(0, len(blocks), 16):
        w = [0] * 80
        w[0:16] = blocks[n:n+16]

        for i in range(16, 80):
            w[i] = rol(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1)

        a = h[0]
        b = h[1]
        c = h[2]
        d = h[3]
        e = h[4]

        # Основной цикл
        for i in range(80):
            if 0 <= i <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            elif 60 <= i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = rol(a, 5) + f + e + k + w[i]
            temp &= 0xFFFFFFFF
            e = d
            d = c
            c = rol(b, 30)
            b = a
            a = temp

        h[0] += a
        h[1] += b
        h[2] += c
        h[3] += d
        h[4] += e
        h = [i & 0xFFFFFFFF for i in h]

    # получение результата вычислений
    res = ""
    for i in h:
        res += "{:08x}".format(i)
    return res


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print ("Usage: sha1 file")
		sys.exit(1)
	file = open(sys.argv[1])
	data = file.read()
	print(sha1(data))
