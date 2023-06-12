result = lambda p: p[0][0]
rest = lambda p: p[0][1]


def digits_to_int(digits):
    return int(''.join(digits))


def cons(x, xs):
    if isinstance(x, str) and xs == []:
        return x
    if isinstance(xs, str):
        return str(x) + xs  # ensure x is converted to a string
    return [x] + xs


class Parser:
    def __rshift__(self, other):
        return Seq(self, other)

    def __xor__(self, other):
        return OrElse(self, other)

    def parse(self, inp):
        raise NotImplementedError("Subclasses must implement the parse method.")


class Seq(Parser):
    def __init__(self, parser, and_then):
        self.parser = parser
        self.and_then = and_then

    def parse(self, inp):
        p = self.parser.parse(inp)
        if p != []:
            return self.and_then(result(p)).parse(rest(p))

        return []


class OrElse(Parser):
    def __init__(self, parser1, parser2):
        self.parser1 = parser1
        self.parser2 = parser2

    def parse(self, inp):
        p = self.parser1.parse(inp)
        if p != []:
            return p

        return self.parser2.parse(inp)


class ParseItem(Parser):
    def parse(self, inp):
        if inp == "":
            return []
        return [(inp[0], inp[1:])]


class Return(Parser):
    def __init__(self, x):
        self.x = x

    def parse(self, inp):
        return [(self.x, inp)]


class Fail(Parser):
    def parse(self, inp):
        return []


###############################
# Below this line, no parsers #
# may override "parse".       #
###############################

# Generic combinators

class ParseSome(Parser):
    def __init__(self, parser):
        self.parser = parser >> (lambda x: \
                                 (ParseSome(parser) ^ Return([])) >> (lambda xs: \
                                 Return(cons(x, xs))))

    def parse(self, inp):
        return self.parser.parse(inp)


class ParseIf(Parser):
    def __init__(self, pred):
        self.pred = pred
        self.parser = ParseItem() >> (lambda c: \
                                      Return(c) if self.pred(c) else Fail())

    def parse(self, inp):
        return self.parser.parse(inp)


class ParseChar(Parser):
    """
    >>> ParseChar('-').parse("-89abc")
    [('-', '89abc')]
    >>> ParseChar('a').parse("89")
    []
    >>> ParseChar('a').parse("abc")
    [('a', 'bc')]
    """

    def __init__(self, c):
        self.parser = ParseIf(lambda x: c == x)

    def parse(self, inp):
        return self.parser.parse(inp)


class ParseDigit(Parser):
    """
    >>> ParseDigit().parse("89abc")
    [('8', '9abc')]
    >>> ParseDigit().parse("a89b")
    []
    """

    def __init__(self):
        self.parser = ParseIf(lambda c: c in "0123456789")

    def parse(self, inp):
        return self.parser.parse(inp)


class ParsePositiveInteger(Parser):
    def __init__(self):
        super().__init__()
        # Convert list of digits to an integer
        self.parser = ParseSome(ParseDigit()) >> (lambda digits: Return(digits_to_int(digits)))

    def parse(self, inp):
        return self.parser.parse(inp)


class ParseSpace(Parser):
    def __init__(self):
        super().__init__()
        self.parser = ParseSome(ParseChar(' '))

    def parse(self, inp):
        return self.parser.parse(inp)


class ParseNewline(Parser):
    def __init__(self):
        super().__init__()
        self.parser = ParseSome(ParseChar('\n'))

    def parse(self, inp):
        return self.parser.parse(inp)


class ParseNameOfTask(Parser):
    def __init__(self):
        super().__init__()
        self.parser = (ParseChar('T') >>
                       lambda _: ParseChar('a') >>
                       lambda _: ParseChar('s') >>
                       lambda _: ParseChar('k') >>
                       lambda _: (ParsePositiveInteger() ^ Return('')) >>
                       lambda n: (ParseSpace() ^ ParseNewline()) >>
                       lambda _: Return('Task' + str(n)))

    def parse(self, inp):
        return self.parser.parse(inp)


class ParseTask(Parser):
    def __init__(self):
        super().__init__()
        self.parser = (ParseNameOfTask() >>
                       lambda name: ParseChar('t') >>
                       lambda _: ParseChar('a') >>
                       lambda _: ParseChar('k') >>
                       lambda _: ParseChar('e') >>
                       lambda _: ParseChar('s') >>
                       lambda _: ParseSpace() >>
                       lambda _: ParsePositiveInteger() >>
                       lambda duration: ParseChar('n') >>
                       lambda _: ParseChar('e') >>
                       lambda _: ParseChar('d') >>
                       lambda _: ParseChar('s') >>
                       lambda _: ParseSpace() >>
                       lambda _: (ParsePositiveInteger() ^ Return('')) >>
                       lambda dependency: ParseNewline() >>
                       lambda _: Return((name, duration, dependency)))

    def parse(self, inp):
        return self.parser.parse(inp)


class ParseListOfTasks(Parser):
    def __init__(self):
        super().__init__()
        self.parser = ((ParseTask() >>
                        lambda task: (ParseListOfTasks() ^ Return([])) >>
                        lambda rest: Return(cons(task, rest))) ^ Return([]))

    def parse(self, inp):
        return self.parser.parse(inp)
