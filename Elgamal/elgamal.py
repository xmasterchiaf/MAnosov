#!/usr/bin/env python
#coding: UTF-8

import sys
import random
import mylib
import bigNumber.bigNumber as bigNumber

# генерация ключей для схемы Эль-Гамаля
# публичный ключ - p, g, y
# закрытый ключ - x
def keygen(pfile, gfile, yfile, xfile, bits):
    p = mylib.genPrime(bits)
    g = bigNumber.GenerateRandomMax(p)
    x = bigNumber.GenerateRandomMax(p-1)
    y = bigNumber.Pow(g, x, p)

    mylib.writeNum(pfile, p)
    mylib.writeNum(gfile, g)
    mylib.writeNum(yfile, y)
    mylib.writeNum(xfile, x)

    print "Сгенерированы открытый ключ {}, {}, {}".format(pfile, gfile, yfile)
    print "              закрытый ключ {}".format(xfile)
    

def decrypt(pfile, xfile, afile, bfile, rfile):
    p = mylib.readNum(pfile)
    x = mylib.readNum(xfile)
    a = mylib.readNum(afile)
    b = mylib.readNum(bfile)
    
    r = (b * bigNumber.Pow(a, p - 1 - x, p)) % p # суть дешифрования
    mylib.writeNum(rfile, r)
    print "Числа {}, {} дешифрованы. Результат - в {}".format(afile, bfile, rfile)


def encrypt(pfile, gfile, yfile, mfile, afile, bfile):
    p = mylib.readNum(pfile)
    g = mylib.readNum(gfile)
    y = mylib.readNum(yfile)
    m = mylib.readNum(mfile)

    # суть шифрования
    if m >= p:
        print "{} - слишком велико для шифрования данным ключом".format(mfile)
        sys.exit(1)
    k = bigNumber.GenerateRandomMax(p-1)
    a = bigNumber.Pow(g, k, p)
    b = bigNumber.Pow(y, k, p)
    b = (b * m) % p

    mylib.writeNum(afile, a)
    mylib.writeNum(bfile, b)
    print "Число {} зашифровано. Результат - в {}, {}".format(mfile, afile, bfile)
    
    
def getArgs():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['g', 'e', 'd'], help="g - генерация ключей, e - шифрование, d - дешифрование")
    parser.add_argument('-p', '--p_file', nargs='?', default="p.txt", help="Файл с/для числа p")
    parser.add_argument('-g', '--g_file', nargs='?', default="g.txt", help="Файл с/для числа g")
    parser.add_argument('-y', '--y_file', nargs='?', default="y.txt", help="Файл с/для числа y")
    parser.add_argument('-x', '--x_file', nargs='?', default="x.txt", help="Файл с/для числа x")
    parser.add_argument('-m', '--m_file', nargs='?', default="m.txt", help="Файл с числом m - числом, которое будет ЗАШИФРОВАНО")
    parser.add_argument('-a', '--a_file', nargs='?', default="a.txt", help="Файл с/для числа a - числа, которое будет ДЕШИФРОВАНО, результат ШИФРОВАНИЯ")
    parser.add_argument('-b', '--b_file', nargs='?', default="b.txt", help="Файл с/для числа b - числа, которое будет ДЕШИФРОВАНО, результат ШИФРОВАНИЯ")
    parser.add_argument('-r', '--r_file', nargs='?', default="r.txt", help="Файл для числа r - результат ДЕШИФРОВАНИЯ")
    parser.add_argument('-l', '--lenght', nargs='?', default="64", help="Длина ключа в битах")
    return parser.parse_args()


if __name__ == "__main__":
    args = getArgs()
    if args.mode == 'e':
        encrypt(args.p_file, args.g_file, args.y_file, args.m_file, args.a_file, args.b_file)
    elif args.mode == 'd':
        decrypt(args.p_file, args.x_file, args.a_file, args.b_file, args.r_file)
    elif args.mode == 'g':
        keygen(args.p_file, args.g_file, args.y_file, args.x_file, int(args.lenght))
