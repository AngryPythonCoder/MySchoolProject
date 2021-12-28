def mask_0(x, y, value):
    if (x + y) % 2 == 0:
        return 1 - value
    
    else:
        return value
    
    
def mask_1(x, y, value):
    if y % 2 == 0:
        return 1 - value
    
    else:
        return value
        

def mask_2(x, y, value):
    if x % 3 == 0:
        return 1 - value
    
    else:
        return value
    
    
def mask_3(x, y, value):
    if (x + y) % 3 == 0:
        return 1 - value
    
    else:
        return value
    
    
def mask_4(x, y, value):
    if (x // 3 + y // 2) % 2 == 0:
        return 1 - value
    
    else:
        return value
    
    
def mask_5(x, y, value):
    if (x * y) % 2 + (x * y) % 3 == 0:
        return 1 - value
    
    else:
        return value


def mask_6(x, y, value):
    if ((x * y) % 2 + (x * y) % 3) % 2 == 0:
        return 1 - value
    
    else:
        return value
    
    
def mask_7(x, y, value):
    if ((x * y) % 3 + (x + y) % 2) % 2 == 0:
        return 1 - value
    
    else:
        return value
    
    
MASKS = [mask_0, mask_1, mask_2, mask_3, mask_4, mask_5, mask_6, mask_7]