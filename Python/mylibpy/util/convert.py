# -*- utf-8 -*-

def to_bcd(n):
    """整数値をBCDに変換"""
    if n < 0:
        return None

    result = 0
    shift = len(str(n)) -1
    for s in str(n):
        b = int(s,16)
        result |= (b << (4 * shift))
        shift -= 1
    return result

def extract_bytes(datas, start, end):
    """指定範囲のバイト情報を削除する"""
    array = bytearray(datas)
    del array[start:end]
    buffer = bytes(array)
    return buffer

if __name__ == '__main__':
    pass