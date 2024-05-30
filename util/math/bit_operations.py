from math import log

def reverse_bits(value: int, width: int):
    """Reverses bits of an integer.
    """
    binary_val = '{:0{width}b}'.format(value, width=width)
    return int(binary_val[::-1], 2)

def bit_reverse_vec(values: list[int]):
    """Reverses the order of elements in a list.
    """
    result = [0] * len(values)
    for i in range(len(values)):
        result[i] = values[reverse_bits(i, int(log(len(values), 2)))]
        
    return result