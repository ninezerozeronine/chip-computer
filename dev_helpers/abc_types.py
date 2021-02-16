from abc import ABC


class Base(ABC):
    pass


class Inh(Base):
    pass


A = Inh()
print(type(A))
print(Inh)
print(type(Inh))
print(isinstance(A, Inh))
print(isinstance(A, Base))
