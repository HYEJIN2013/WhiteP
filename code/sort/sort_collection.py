#!/usr/bin/python3
# -*- coding: utf-8 -*-

LIST_COUNT = 1000
LOOP_COUNT = 10000
MAX_NUM = 10000

def data_generate():
    import random
    return [ random.randint( 1, MAX_NUM) for _ in range( LIST_COUNT)]

def selection_sort_wai( data):
    '''
    この関数は配列を先頭から末尾に向かって、最小値を見つけて、それを先頭の要素と交換することを繰り返す
    '''
    for i in range( len( data)-1):
        for j in range( i+1, len( data)):
            if data[ i] > data[j]:
                data[i], data[j] = data[j], data[i]


def selection_sort( data):
    for i in range( len( data)-1):
        minimum = i

        for j in range( i+1, len( data)):
            if data[ minimum] > data[j]:
                minimum = j

        data[i], data[ minimum] = data[ minimum], data[i]

def bubble_sort_wai( data):
    '''
    この関数は配列の末尾から先頭に向かって、隣同士の要素を比較して、小さい方が前になるように交換することを繰り返す
    '''
    for i in range( len( data)-1, 0, -1):
        for j in range( i, 0, -1):
            if data[ j] < data[ j-1]:
                data[ j], data[ j-1] = data[ j-1], data[ j]

def bubble_sort( data):
    for i in range( len( data)):
        for t in range( 1, len( data) - i):
            if data[ t] < data[ t-1]:
                data[ t], data[ t-1] = data[ t-1], data[ t]
                
def insertion_sort( data):
    '''
    配列の末尾に1つずつ要素を挿入し、それより前にある要素が小さい限り、挿入位置を前に進めることを繰り返す
    '''
    for i in range( 1, len( data)):
        tmp = data[ i]
        if data[ i-1] > tmp:
            j = i
            while j > 0 and data[ j-1] > tmp:
                data[ j] = data[ j-1]
                j -= 1
            data[ j] = tmp

def shell_sort( data):
    '''
    適当な間隔を決めて挿入ソートを行うことを、間隔が1になるまで繰り返す
    '''
    gap = len( data)
    while gap > 0:
        for i in range( gap, len( data)):
            tmp = data[ i]
            j = i - gap
            while i >= 0 and tmp < data[ i]:
                pass
        gap //= 2

def merge_sort( data):
    '''
    配列を要素数が1つになるまで分割し、小さい方が前になるように結合することを繰り返す
    '''
    mid = len( data)
    if mid <= 1:
        # 要素が1以下ならそのまま返す
        return data

    # リストを分割して再帰ソート
    left = data[:(mid//2)]  #左半分
    right = data[(mid//2):] #右半分
    left = merge_sort( left)
    right = merge_sort( right)

    # 分割したリストを結合する
    array = []
    while len( left) != 0 and len( right) != 0:
        if left[ 0] < right[ 0]:
            array.append( left.pop( 0))
        else:
            array.append( right.pop( 0))

    # 左側にデータが残っていたらそのまま末尾にマージ
    if len( left) != 0:
        array.extend( left)
    # 右側にデータが残っていたらそのまま末尾にマージ
    elif len( right) != 0:
        array.extend( right)

    return array

def quick_sort( data):
    '''
    適当な基準値を決めて、配列の要素を基準値より大きいグループと小さいグループに分割することを繰り返す
    '''
    if len( data) < 1:
        return data

    pivot = data[ 0]
    left = []
    right = []
    for x in range( 1, len( data)):
        if data[ x] <= pivot:
            left.append( data[ x])
        else:
            right.append( data[ x])

    left = quick_sort( left)
    right = quick_sort( right)

    return left + [pivot] + right

def heap_sort( data):
    '''
    ヒープ(小さいデータほど上にある木構造で、木の根の要素が最小値となる)を構築し、最小値を取り出すたびにヒープを再構築することを繰り返す
    '''
    pass

if __name__ == '__main__':
    import time
    import sys
    
    # merge_sort TEST
    start = time.time()

    for _ in range( LOOP_COUNT):
        data = data_generate()
        merge_sort( data)
        print( '.', end='')
        sys.stdout.flush()

    end = time.time()
    print()
    print( 'merge_sort 経過時間:', ( end - start))
