"""
Tokens define the atomic parts of assembly code.

Tokens are of different types, and one type can have varying values. E.g.
A number type can have a value of 34, or 16.



"""



class Token():
    pass

class CONSTANT(Token):
    pass

class ALIAS(CONSTANT):
    pass

class NUMBER(CONSTANT):
    pass

class LABEL(CONSTANT):
    pass

class VARIABLE(CONSTANT):
    pass



class ASCII(Token):
    pass


class ANCHOR(Token):
    pass




class INSTRUCTION(Token):
    pass

class LOAD(INSTRUCTION):
    pass

class STORE(INSTRUCTION):
    pass




class MODULE(Token):
    pass

class A(MODULE):
    pass

class B(MODULE):
    pass

class C(MODULE):
    pass




class MEMREF(Token):
    pass

class M_A(MEMREF):
    pass

class M_B(MEMREF):
    pass