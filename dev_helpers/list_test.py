from copy import deepcopy


class MyClass():
    def __init__(self, my_list):
        self.my_list = deepcopy(my_list)

    def get_list(self):
        return self.my_list


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
