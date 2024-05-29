import random
from typing import List

def sample_uniform(min: int, max: int, num: int) -> List[int]:    
    """Samples from a uniform distribution.
    """
    return [random.randrange(min, max) for _ in range(num)]

def sample_triangle(num: int) -> List[int]:
    """Samples from a discrete triangle distribution.
    Samples values from [-1, 0, 1] with probabilities [0.25, 0.5, 0.25] respectively.
    """
    sample = [0] * num
    for i in range(num):
        r = random.randrange(0, 4)
        if r == 0: sample[i] = -1
        elif r == 1: sample[i] = 1
        else: sample[i] = 0
        
    return sample

def sample_hamming_weight_vector(length: int, weight: int) -> List[int]:
    """Samples from a Hamming weight distribution.
    from the set [-1, 0, 1] s.t. the resulting vector has exactly h nonzero values.
    """
    samples = [0] * length
    total_weight = 0
    while total_weight < weight:
        index = random.randrange(0, length)
        if samples[index] == 0:
            samples[index] = random.choice([-1, 1])
            total_weight += 1
            
    return samples

def sample_random_complex_vector(length: int) -> List[complex]:
    """Samples a random complex vector.
    """
    return [complex(random.random() + random.random() * 1j) for _ in range(length)]

def sample_random_real_vector(length: int) -> List[float]:
    """Samples a random real vector.
    """
    return [random.random() for _ in range(length)]