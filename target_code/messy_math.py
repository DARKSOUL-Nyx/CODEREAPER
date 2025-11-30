def do_math_stuff(a, b, op):
    if op == 'add':
        return a + b
    elif op == 'sub':
        return a - b
    elif op == 'mul':
        if a > 0:
            if b > 0:
                return a * b
            else:
                return 0
        else:
            return 0
    elif op == 'div':
        if b != 0:
            return a / b
        else:
            return "Error"
    # ... Imagine 50 more nested if-statements here ...
    else:
        return 0