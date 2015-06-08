#!/usr/bin/env python
#coding: UTF-8

import sys
import mylib
import bigNumber.bigNumber as bigNumber

# генерация ключей RSA
# публичный ключ - e, n
# закрытый ключ - d
def keygen(efile, dfile, nfile, bits):
    p = mylib.genPrime(bits)
    q = mylib.genPrime(bits)
        
    n = p * q
    f = (p-1) * (q-1)
    e = bigNumber.bigNumber(65537)
    d = mylib.inv(e, f)

    mylib.writeNum(efile, e)
    mylib.writeNum(dfile, d)
    mylib.writeNum(nfile, n)

    print "Сгенерированы открытый ключ {} и {}".format(efile, nfile)
    print "              закрытый ключ {}".format(dfile)
    

def decrypt(cfile, dfile, nfile, rfile):
    c = mylib.readNum(cfile)
    d = mylib.readNum(dfile)
    n = mylib.readNum(nfile) 
    r = bigNumber.Pow(c, d, n) # cуть дешифрования
    mylib.writeNum(rfile, r)
    print "Число {} дешифровано. Результат - в {}".format(cfile, rfile)


def encrypt(mfile, efile, nfile, cfile):
    m = mylib.readNum(mfile)
    e = mylib.readNum(efile)
    n = mylib.readNum(nfile)
    if m >= n:
        print mfile, "- слишком велико для шифрования данным ключом"
        sys.exit(1)
    c =  bigNumber.Pow(m, e, n) # суть шифрования
    mylib.writeNum(cfile, c)
    print "Число {} зашифровано. Результат - в {}".format(mfile, cfile)
    
    
def getArgs():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['g', 'e', 'd'], help="g - генерация ключей, e - шифрование, d - дешифрование")
    parser.add_argument('-e', '--e_file', nargs='?', default="e.txt", help="Файл с/для числа e")
    parser.add_argument('-d', '--d_file', nargs='?', default="d.txt", help="Файл с/для числа d")
    parser.add_argument('-n', '--n_file', nargs='?', default="n.txt", help="Файл с/для числа n")
    parser.add_argument('-m', '--m_file', nargs='?', default="m.txt", help="Файл с числом m - числом, которое будет ЗАШИФРОВАНО")
    parser.add_argument('-c', '--c_file', nargs='?', default="c.txt", help="Файл с/для числа с - числа, которое будет ДЕШИФРОВАНО, результат ШИФРОВАНИЯ")
    parser.add_argument('-r', '--r_file', nargs='?', default="r.txt", help="Файл для числа r - результат ДЕШИФРОВАНИЯ")
    parser.add_argument('-l', '--lenght', nargs='?', default="64", help="Длина ключа в битах")
    return parser.parse_args()

    
if __name__ == "__main__":
    args = getArgs()
    if args.mode == 'e':
        encrypt(args.m_file, args.e_file, args.n_file, args.c_file)
    elif args.mode == 'd':
        decrypt(args.c_file, args.d_file, args.n_file, args.r_file)
    elif args.mode == 'g':
        keygen(args.e_file, args.d_file, args.n_file, int(args.lenght))
