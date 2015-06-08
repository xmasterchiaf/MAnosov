#!/usr/bin/env python
#coding: UTF-8
import sys


def gost(M):
    M = [ord(x) for x in M]
    h = [0] * 32
    Sum = [0] * 32
    L = [0] * 32

    for i in range(0, len(M) - 31, 32):
        Mi = M[i:i+32]
        h = f(h, Mi)
        Sum = controlSum(Sum, Mi)

    # вычисление длины сообщения
    L[(len(M) / 32) % 32] = 1
    
    if len(M) % 32:
        L[0] = (len(M) % 32) * 8
        Mi = M[-(len(M)%32):] + [0] * (32 - len(M) % 32)
        h = f(h, Mi)
        Sum = controlSum(Sum, Mi)

    h = f(h, L)
    h = f(h, Sum)

    res = ""
    for i in h:
        res += "{:02x}".format(i)
    return res.upper()

    
def f(Hin, m):
    keys = rKeys(Hin, m)

    S = []
    for i in range(4):
        tmp = Hin[i*8:(i+1)*8]
        tmp = E(tmp, keys[i])
        S += tmp

    res = psiN(S, 12)
    res = xor(m, res)
    res = psiN(res, 1)
    res = xor(Hin, res)
    res = psiN(res, 61)
    return res

def rKeys(U, V):
    C3 = [0x00, 0xff, 0x00, 0xff, 0x00, 0xff, 0x00, 0xff,
         0xff, 0x00, 0xff, 0x00, 0xff, 0x00, 0xff, 0x00, 
         0x00, 0xff, 0xff, 0x00, 0xff, 0x00, 0x00, 0xff, 
         0xff, 0x00, 0x00, 0x00, 0xff, 0xff, 0x00, 0xff]
    K = [0] * 4
    W = xor(U, V)
    K[0] = P(W)
    for j in range(1, 4):
        U = A(U)
        if j == 2:
            U = xor(U, C3)
        V = A(A(V))
        W = xor(U, V)
        K[j] = P(W)
    return K


def A(Y):
    res = [0] * 32
    res[:24] = Y[8:]
    for i in range(8):
        res[i + 24] = Y[i] ^ Y[i + 8]
    return res


def P(Y):
    res = [0] * 32
    for i in range(4):
        for k in range(1, 9):
            res[i + 1 + 4*(k-1) -1] = Y[8*i + k -1]
    return res


def E(D, K):    
    A = D[:4]
    B = D[4:]

    for i in 3*range(8) + range(7, -1, -1):
        tmp = EStep(A, K[i*4:(i+1)*4])
        tmp = xor(tmp, B)
        B = A
        A = tmp

    return B + A

	
def EStep(A, K):
    S = [
    [ 4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3 ],
    [ 14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9 ],
    [ 5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11 ],
    [ 7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3 ],
    [ 6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2 ],
    [ 4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 12, 15, 14 ],
    [ 13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12 ],
    [ 1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12 ]]

    res = [0] * 4
    c = 0
    for i in range(4):
        c += A[i] + K[i]
        res[i] = c & 0xFF
        c >>= 8

    for i in range(8):
        if i & 1:
            x = res[i >> 1] & 0xF0
        else:
            x = res[i >> 1] & 0x0F
        res[i >> 1] ^= x
        if i & 1:
            x >>= 4

        x = S[i][x]
        if i & 1:
            res[i >> 1] |= x << 4
        else:
            res[i >> 1] |= x << 0

    res = [res[3]] + res[:3]
    tmp = res[0] >> 5

    for i in range(1, 4):
        nTmp = res[i] >> 5
        res[i] = ((res[i] << 3) & 0xFF) | tmp
        tmp = nTmp
    res[0] = ((res[0] << 3) & 0xFF) | tmp
    return res


def psiN(Y, n):
    for i in range(n):
        tmp = [0, 0]
        for j in [1, 2, 3, 4, 13, 16]:
            tmp[0] ^= Y[2 * (j - 1)]
            tmp[1] ^= Y[2 * (j - 1) + 1]        
        Y = Y[2:] + tmp
    return Y


def controlSum(Sum, m):
    res = []
    c = 0
    for i in range(32):
        c += Sum[i] + m[i]
        res.append(c & 0xFF)
        c >>= 8
    return res


def xor(a, b):
    return [a[i] ^ b[i] for i in range(len(a))]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print ("Usage: gost file")
        sys.exit(1)
    file = open(sys.argv[1])
    data = file.read()
    print(gost(data))
