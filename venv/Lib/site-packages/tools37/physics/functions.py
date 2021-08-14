from numbers import Real
from tools37.algebra import Polynom
from .Circle import Circle
from .Line import Line
from tools37.geom import VectorBase


def elastic_collision(v1: Real, m1: Real, v2: Real, m2: Real):
    """Calculate the resulting speeds after an elastic collision"""
    if m1 == m2:
        return v2, v1

    if m1 == float('inf'):
        return v1, 2 * v1 - v2

    if m2 == float('inf'):
        return 2 * v2 - v1, v2

    m = m1 + m2
    n1 = ((m1 - m2) * v1 + 2 * m2 * v2) / m
    n2 = ((m2 - m1) * v2 + 2 * m1 * v1) / m
    return n1, n2


def circle_circle_collision(circle1: Circle, circle2: Circle):
    t1 = Polynom(circle1.position, circle1.speed)
    t2 = Polynom(circle2.position, circle2.speed)
    rt = t1 - t2
    err = rt ** 2 - (circle1.radius + circle2.radius) ** 2
    if err(0) >= 0:
        for t in err.solve():
            yield t, rt(t)


def circle_line_collision(circle: Circle, line: Line):
    t1 = Polynom(circle.position, circle.speed)
    t2 = Polynom(line.origin, line.speed)
    rt = t1 - t2
    ex = line.delta.__unit__()
    ey = ex.__orth__()

    err = (rt * ey) ** 2 - circle.radius ** 2
    for t in err.solve():
        if 0 <= rt(t) * ex <= 2 * abs(line.delta):
            yield t, (rt(t) * ey) * ey
