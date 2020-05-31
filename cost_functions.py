def distance(pos1, pos2):
    x_diff = abs(pos1[0], pos2[0])
    y_diff = abs(pos1[1], pos2[1])
    return x_diff + y_diff

def g(position, start):
    return distance(position, start)

def h(position, end):
    return distance(position, end)

def f(position, start, end):
    return g(position, start) + h(position, end)