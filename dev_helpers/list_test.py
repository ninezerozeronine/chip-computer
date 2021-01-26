from copy import deepcopy


class MyClass():
    def __init__(self, my_list):
        self.my_list = deepcopy(my_list)

    def get_list(self):
        return self.my_list


class OtherClass():
    FOO = 8

    def __init__(self, num):
        self._num = num

    @property
    def num(self):
        print("Getting num")
        return self._num

    def print_num(self):
        print(type(self.num))
        print(self.num)
        print(f"FOO: {self.FOO}")
        self.FOO = self.FOO + 1


def make_obj(input_list):

    obj = MyClass(input_list)
    return obj


a = [1, 2, 3]
obj = make_obj(a)
a[0] = 9


print(a)
print(obj.my_list)

b = obj.get_list()
b[2] = 7
print(obj.my_list)

c = OtherClass(5)
d = OtherClass(10)
c.print_num()
d.print_num()
c.print_num()
d.print_num()

print(type(4))
