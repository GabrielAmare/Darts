from typing import List, TypeVar, Dict, Callable

__all__ = ["ReprTable", "make_chart"]


def make_chart(ih: str, iv: str, oh: str, ov: str,
               ihd: str = '1', ivd: str = '1', ohd: str = '1', ovd: str = '1') -> str:
    """
        This function create a chart from it's parameters

        ih : the type of inside horizontal lines
        iv : the type of inside vertical lines
        oh : the type of outside horizontal lines
        ov : the type of outside vertical lines

        ihd : the dotting of inside horizontal lines
        ivd : the dotting of inside vertical lines
        ohd : the dotting of outside horizontal lines
        ovd : the dotting of outside vertical lines

        types :
            S -> Simple line
            B -> Bold line
            D -> Double line

        dotting :
            1 -> line non splited
            2 -> line splited in 2
            3 -> line splited in 3
            4 -> line splited in 4

        the chart is constitued in 16 characters :
            [00] top left corner
            [01] top intersection
            [02] top horizontal bar
            [03] top right corner
            [04] left intersection
            [05] middle intersection
            [06] inside horizontal bar
            [07] right intersection
            [08] left vertical bar
            [09] inside vertical bar
            [10] fill char
            [11] right vertical bar
            [12] bottom left corner
            [13] bottom intersection
            [14] bottom horizontal bar
            [15] bottom right corner
    """
    assert ih in ('S', 'B', 'D'), f"invalid value ih={ih!r} should be in ('S', 'B', 'D')"
    assert iv in ('S', 'B', 'D'), f"invalid value iv={iv!r} should be in ('S', 'B', 'D')"
    assert oh in ('S', 'B', 'D'), f"invalid value oh={oh!r} should be in ('S', 'B', 'D')"
    assert ov in ('S', 'B', 'D'), f"invalid value ov={ov!r} should be in ('S', 'B', 'D')"

    assert ihd in ('1', '2', '3', '4'), f"invalid value ihd={ihd!r} should be in ('1', '2', '3', '4')"
    assert ivd in ('1', '2', '3', '4'), f"invalid value ivd={ivd!r} should be in ('1', '2', '3', '4')"
    assert ohd in ('1', '2', '3', '4'), f"invalid value ohd={ohd!r} should be in ('1', '2', '3', '4')"
    assert ovd in ('1', '2', '3', '4'), f"invalid value ovd={ovd!r} should be in ('1', '2', '3', '4')"

    assert oh + ov not in ('DB', 'BD'), "cannot cross Double and Bold"
    assert oh + iv not in ('DB', 'BD'), "cannot cross Double and Bold"
    assert ih + ov not in ('DB', 'BD'), "cannot cross Double and Bold"
    assert ih + iv not in ('DB', 'BD'), "cannot cross Double and Bold"

    assert ih != 'D' or ihd == '1', "cannot dot Double"
    assert iv != 'D' or ivd == '1', "cannot dot Double"
    assert oh != 'D' or ohd == '1', "cannot dot Double"
    assert ov != 'D' or ovd == '1', "cannot dot Double"

    c = ''
    c += {'SS': '┌', 'SD': '╓', 'SB': '┎', 'DS': '╒', 'DD': '╔', 'DB': '╳', 'BS': '┍', 'BD': '╳', 'BB': '┏'}[oh + ov]
    c += {'SS': '┬', 'SD': '╥', 'SB': '┰', 'DS': '╤', 'DD': '╦', 'DB': '╳', 'BS': '┯', 'BD': '╳', 'BB': '┳'}[oh + iv]
    c += {'S1': '─', 'S2': '╌', 'S3': '┄', 'S4': '┈', 'B1': '━', 'B2': '╍', 'B3': '┅', 'B4': '┉', 'D1': '═'}[oh + ohd]
    c += {'SS': '┐', 'SD': '╖', 'SB': '┒', 'DS': '╕', 'DD': '╗', 'DB': '╳', 'BS': '┑', 'BD': '╳', 'BB': '┓'}[oh + ov]
    c += {'SS': '├', 'SD': '╟', 'SB': '┠', 'DS': '╞', 'DD': '╠', 'DB': '╳', 'BS': '┝', 'BD': '╳', 'BB': '┣'}[ih + ov]
    c += {'SS': '┼', 'SD': '╫', 'SB': '╂', 'DS': '╪', 'DD': '╬', 'DB': '╳', 'BS': '┿', 'BD': '╳', 'BB': '╋'}[ih + iv]
    c += {'S1': '─', 'S2': '╌', 'S3': '┄', 'S4': '┈', 'B1': '━', 'B2': '╍', 'B3': '┅', 'B4': '┉', 'D1': '═'}[ih + ihd]
    c += {'SS': '┤', 'SD': '╢', 'SB': '┨', 'DS': '╡', 'DD': '╣', 'DB': '╳', 'BS': '┥', 'BD': '╳', 'BB': '┫'}[ih + ov]
    c += {'S1': '│', 'S2': '╎', 'S3': '┆', 'S4': '┊', 'B1': '┃', 'B2': '╏', 'B3': '┇', 'B4': '┋', 'D1': '║', }[ov + ovd]
    c += {'S1': '│', 'S2': '╎', 'S3': '┆', 'S4': '┊', 'B1': '┃', 'B2': '╏', 'B3': '┇', 'B4': '┋', 'D1': '║', }[iv + ivd]
    c += ' '
    c += {'S1': '│', 'S2': '╎', 'S3': '┆', 'S4': '┊', 'B1': '┃', 'B2': '╏', 'B3': '┇', 'B4': '┋', 'D1': '║', }[ov + ovd]
    c += {'SS': '└', 'SD': '╙', 'SB': '┖', 'DS': '╘', 'DD': '╚', 'DB': '╳', 'BS': '┕', 'BD': '╳', 'BB': '┗'}[oh + ov]
    c += {'SS': '┴', 'SD': '╨', 'SB': '┸', 'DS': '╧', 'DD': '╩', 'DB': '╳', 'BS': '┷', 'BD': '╳', 'BB': '┻'}[oh + iv]
    c += {'S1': '─', 'S2': '╌', 'S3': '┄', 'S4': '┈', 'B1': '━', 'B2': '╍', 'B3': '┅', 'B4': '┉', 'D1': '═'}[oh + ohd]
    c += {'SS': '┘', 'SD': '╜', 'SB': '┚', 'DS': '╛', 'DD': '╝', 'DB': '╳', 'BS': '┙', 'BD': '╳', 'BB': '┛'}[oh + ov]

    return c


K = TypeVar("K")


class ReprTable:
    SIMPLE = make_chart(*'SSSS')
    DOUBLE = make_chart(*'DDDD')
    BOLD = make_chart(*'BBBB')

    DOUBLE_OUT = make_chart(*'SSDD')
    BOLD_OUT = make_chart(*'SSBB')

    DOUBLE_IN = make_chart(*'DDSS')
    BOLD_IN = make_chart(*'BBSS')

    DOUBLE_H = make_chart(*'DSDS')
    DOUBLE_V = make_chart(*'SDSD')

    BOLD_H = make_chart(*'BSBS')
    BOLD_V = make_chart(*'SBSB')

    @classmethod
    def from_items(cls, items: List[K], config: Dict[str, Callable[[K], str]]):
        labels, functions = zip(*config.items())
        return cls([labels] + [[function(item) for function in functions] for item in items])

    def __init__(self, data: List[List[str]], padx: int = 1, pady: int = 0, chart: str = BOLD_OUT):
        self.data: List[List[str]] = data
        self.padx: int = padx
        self.pady: int = pady

        self.chart: str = chart
        self.widths: List[int] = [
            max([
                max([
                    len(line) for line in cell.split('\n')
                ], default=0)
                for cell in col
            ], default=0)
            for col in zip(*self.data)
        ]
        self.heights: List[int] = [
            max([
                len(cell.split('\n'))
                for cell in row
            ], default=0)
            for row in self.data
        ]

    def get_box(self, text: str, width: int, height: int) -> List[str]:
        lines = text.split('\n')
        empty = width * self.chart[10]
        lines.extend((height - len(lines)) * [empty])
        return self.pady * [empty] + [
            self.padx * self.chart[10] + line.ljust(width, self.chart[10]) + self.padx * self.chart[10]
            for line in lines
        ] + self.pady * [empty]

    def __str__(self):
        start_line = self.chart[0] + self.chart[1].join(
            (width + 2 * self.padx) * self.chart[2]
            for width in self.widths
        ) + self.chart[3]
        sep_line = self.chart[4] + self.chart[5].join(
            (width + 2 * self.padx) * self.chart[6]
            for width in self.widths
        ) + self.chart[7]
        end_line = self.chart[12] + self.chart[13].join(
            (width + 2 * self.padx) * self.chart[14]
            for width in self.widths
        ) + self.chart[15]

        return '\n'.join([
            start_line,
            ('\n' + sep_line + '\n').join(
                '\n'.join(
                    self.chart[8] + self.chart[9].join(
                        text.ljust((width + 2 * self.padx), self.chart[10])
                        for width, text in zip(self.widths, nrow)
                    ) + self.chart[11]
                    for nrow in zip(*(
                        self.get_box(text, width, height)
                        for text, width in zip(row, self.widths)
                    ))
                )
                for row, height in zip(self.data, self.heights)
            ),
            end_line
        ])


if __name__ == '__main__':
    data = [
        ["first name", "last name", "deceased"],
        ["Barack", "Obama", "N"],
        ["Joe", "Biden", "N"],
        ["Michael", "Jackson", "Y"],
        ["John", "Doe", "?"],
        ["John", "Fitzgerald\nKennedy", "Y"],
        ["Someone", "-/-", "-/-"],
    ]

    table = ReprTable(data, chart=make_chart(*'SBSD4321'))

    print(table)
