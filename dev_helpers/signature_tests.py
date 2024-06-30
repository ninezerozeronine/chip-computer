from enum import Enum

class INS(Enum):
    NOOP = 1
    JUMP = 2
    LOAD = 3


class MOD(Enum):
    A = 1
    B = 2
    C = 3


class E_CONST(Enum):
    CONST = 1


class MEM(Enum):
    A = 1
    B = 2
    CONST = 3


def test_enums():
    test = {
        (INS.NOOP,): "NOOP",
        (INS.JUMP, E_CONST.CONST): "JUMP CONST",
        (INS.LOAD, MEM.A, MOD.A): "LOAD [A] A",
        (INS.LOAD, MOD.A, MEM.A): "LOAD A [A]",
    }

    for key, value in test.iteritems():
        print key, ": ", value

    print (INS.LOAD, MOD.A, MEM.A) == (INS.LOAD, MOD.A, MEM.A)
    print (INS.LOAD, MOD.A, MEM.A) == (INS.LOAD, MEM.A, MOD.A)

    print test[(INS.LOAD, MOD.A, MEM.A)]








# class LOAD():
#     pass

# class NOOP():
#     pass

# class JUMP():
#     pass


# class A():
#     pass

# class B():
#     pass


# class CONSTANT():
#     pass


class Instruction():
    pass

NOOP = Instruction()
JUMP = Instruction()
LOAD = Instruction()



class Module():
    pass

A = Module()
B = Module()
C = Module()


class Constant():
    pass

CONST = Constant()


# Would be nice but means you have to use awkward M([A]) syntax.
# class M(tuple):
#     pass

class M:
    def __init__(self, location):
        self._location = location


    def __eq__(self, other):
        if not isinstance(other, M):
            return False
        return self._location == other._location


    def __hash__(self):
        return hash(("M", (self._location)))


    @property
    def location(self):
        return self._location





def test_classes():
    test = {
        (LOAD, M(A), A): "LOAD [A] A",
        (LOAD, M(A), A): "LOAD [A] A (2)",
        (LOAD, A, M(A)): "LOAD A [A]",
        (NOOP,): "NOOP",
        (JUMP, CONST): "JUMP CONST",
    }

    for key, value in test.iteritems():
        print key, ": ", value

    print (LOAD, M(A), A) == (LOAD, M(A), A)
    print (LOAD, M(A), A) == (LOAD, A, M(A))

    a = (LOAD, M(A), A)
    b = (LOAD, M(A), A)
    print a == b
    print a is b

    print hash(A)
    print hash(M(A))
    print hash(M(A))

test_classes()