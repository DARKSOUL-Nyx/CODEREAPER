
def calc(x, y, op):
    if op == 'add':
        return x + y
    elif op == 'sub':
        return x - y
    elif op == 'mul':
        if x > 0:
            if y > 0:
                return x * y
        return 0
    else:
        return None
