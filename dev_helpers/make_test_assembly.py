from sixteen_bit_computer import operations
# from sixteen_bit_computer.operations import call_return_ops, copy_op

import textwrap

def main():
    start = textwrap.dedent("""\
    &start
        NOOP

    """
    )
    res = start
    for op in operations.get_all_operations():
    # for op in [call_return_ops, copy_op]:
        res += op.gen_test_assembly()
        res += "\n"
    end = textwrap.dedent("""\
        JUMP &start
    """
    )
    res += end
    with open("test_all_instructions.asm", "w") as file:
        file.write(res)

if __name__ == "__main__":
    main()
