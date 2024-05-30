import random
import sympy
import sympy.ntheory

def mod_exp(val: int, exp: int, modulus: int):
    """Computes modular exponentiation.
    result = val^exp mod modulus.
    """
    return pow(val, exp, modulus)

def mod_inv(val: int, modulus: int):
    """Computes modular inverse.
    result = val^-1 mod modulus.
    """
    return mod_exp(val, modulus - 2, modulus)

def find_generator(modulus: int):
    return sympy.ntheory.primitive_root(modulus)

def root_of_unity(order: int, modulus: int):
    """Computes the nth root of unity.
    result = g^(order / modulus) mod modulus.
    """
    if ((modulus - 1) % order) != 0:
        raise ValueError('Order is not a factor of modulus - 1')
    
    generator = find_generator(modulus)
    if generator is None:
        raise ValueError('Generator not found')
    
    result = mod_exp(generator, (modulus - 1) // order, modulus)
    
    if result == 1:
        return root_of_unity(order, modulus)
    
    return result

def is_prime(number: int, num_trials: int = 200) -> bool:
    """Checks if a number is prime.
    Millar-Rabin primality test.
    """
    if number < 2: return False
    if number != 2 and number % 2 == 0: return False
    
    # Find largest odd factor of n - 1
    exp = number - 1
    while exp % 2 == 0:
        exp //= 2
        
    for _ in range(num_trials):
        rand = int(random.SystemRandom().randrange(1, number))
        new_exp = exp
        power = pow(rand, new_exp, number)
        while new_exp != number - 1 and power != 1 and power != number - 1:
            power = (power * power) % number
            new_exp *= 2
        if power != number - 1 and new_exp % 2 == 0:
            return False
        
    return True
    
