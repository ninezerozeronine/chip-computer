from sixteen_bit_computer import operations
from sixteen_bit_computer.operations import call_return_ops, copy_op

def main():
    res = ""
    for op in [call_return_ops, copy_op]:
        res += op.gen_test_assembly()
    with open("test_all_instructions.asm", "w") as file:
        file.write(res)

if __name__ == "__main__":
    main()