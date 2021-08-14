from numbers import Real

from .Coords import Coords


class BoundingBox:
    """
        BoundingBox represent a rectangle in 2 dimensions

        nw ── n ── ne   yi
        │     │     │    │
        w ─── c ─── e    y
        │     │     │    │
        sw ── s ── se   yf

        xi ── x ── xf

        where dx == x - xi == xf - x
              dy == y - yi == yf - y
              d  == Coords(dx, dy)
    """

    x: Real
    y: Real
    dx: Real
    dy: Real
    xi: Real
    yi: Real
    xf: Real
    yf: Real

    @property
    def nw(self) -> Coords:
        return Coords(self.xi, self.yi)

    @nw.setter
    def nw(self, value: Coords):
        self.xi, self.yi = value

    @property
    def ne(self) -> Coords:
        return Coords(self.xf, self.yi)

    @ne.setter
    def ne(self, value: Coords):
        self.xf, self.yi = value

    @property
    def sw(self) -> Coords:
        return Coords(self.xi, self.yf)

    @sw.setter
    def sw(self, value: Coords):
        self.xi, self.yf = value

    @property
    def se(self) -> Coords:
        return Coords(self.xf, self.yf)

    @se.setter
    def se(self, value: Coords):
        self.xf, self.yf = value

    @property
    def n(self) -> Coords:
        return Coords(self.x, self.yi)

    @n.setter
    def n(self, value: Coords):
        self.x, self.yi = value

    @property
    def s(self) -> Coords:
        return Coords(self.x, self.yf)

    @s.setter
    def s(self, value: Coords):
        self.x, self.yf = value

    @property
    def w(self) -> Coords:
        return Coords(self.xi, self.y)

    @w.setter
    def w(self, value: Coords):
        self.xi, self.y = value

    @property
    def e(self) -> Coords:
        return Coords(self.xf, self.y)

    @e.setter
    def e(self, value: Coords):
        self.xf, self.y = value

    @property
    def c(self) -> Coords:
        return Coords(self.x, self.y)

    @c.setter
    def c(self, value: Coords):
        self.x, self.y = value

    @property
    def d(self) -> Coords:
        return Coords(self.dx, self.dy)

    @d.setter
    def d(self, value: Coords):
        self.dx, self.dy = value
