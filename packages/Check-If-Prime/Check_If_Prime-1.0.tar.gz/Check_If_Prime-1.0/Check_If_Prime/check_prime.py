def check_prime(num) -> bool:
    """checks whether the given number is prime or not

    Args:
                    num (int)): positive integer

    Returns:
                    bool: True if num is prime else False
    """
    
    if num > 1:
        for i in range(2, num):
            if (num % i) == 0:
                return False
    return True