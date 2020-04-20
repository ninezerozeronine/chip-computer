import itertools


def add_op():
    sigs = []
    for arg in ["A", "B", "C", "CONST_8"]:
        sigs.append(["ADD", arg])
    return sigs


def addc_op():
    sigs = []
    for arg in ["A", "B", "C", "CONST_8"]:
        sigs.append(["ADDC", arg])
    return sigs


def sub_op():
    sigs = []
    for arg in ["A", "B", "C", "CONST_8"]:
        sigs.append(["SUB", arg])
    return sigs


def subb_op():
    sigs = []
    for arg in ["A", "B", "C", "CONST_8"]:
        sigs.append(["SUBB", arg])
    return sigs


def lshift_op():
    sigs = []
    for arg in ["ACC", "A", "B", "C"]:
        sigs.append(["LSHIFT", arg])
    return sigs


def lshiftc_op():
    sigs = []
    for arg in ["ACC", "A", "B", "C"]:
        sigs.append(["LSHIFTC", arg])
    return sigs


def incr_op():
    sigs = []
    for arg in ["ACC", "A", "B", "C"]:
        sigs.append(["INCR", arg])
    return sigs


def decr_op():
    sigs = []
    for arg in ["ACC", "A", "B", "C"]:
        sigs.append(["DECR", arg])
    return sigs


def copy_op():
    sigs = []
    srcs = ["ACC", "A", "B", "C", "SP"]
    dests = ["ACC", "A", "B", "C", "SP"]
    for src, dest in itertools.product(srcs, dests):
        if src != dest:
            sigs.append(["COPY", src, dest])
    return sigs


def load_op():
    sigs = []
    srcs = ["CONST_16"]
    dests = ["ACC", "A", "B", "C", "SP"]
    for src, dest in itertools.product(srcs, dests):
        sigs.append(["LOAD", "[{0}]".format(src), dest])
    return sigs


def store_op():
    sigs = []
    srcs = ["ACC", "A", "B", "C"]
    dests = ["CONST_16"]
    for src, dest in itertools.product(srcs, dests):
        sigs.append(["STORE", src, "[{0}]".format(dest)])
    return sigs


def push_op():
    sigs = []
    for arg in ["ACC", "A", "B", "C"]:
        sigs.append(["PUSH", arg])
    return sigs


def pop_op():
    sigs = []
    for arg in ["ACC", "A", "B", "C"]:
        sigs.append(["POP", arg])
    return sigs


def set_op():
    sigs = []
    for arg in ["ACC", "A", "B", "C", "SP"]:
        sigs.append(["SET", arg, "CONST_8"])
    return sigs


def setzero_op():
    sigs = []
    for arg in ["ACC", "A", "B", "C"]:
        sigs.append(["SETZERO", arg])
    return sigs


def noop_op():
    return ["NOOP"]


def jump_op():
    sigs = []
    for arg in ["CONST_16"]:
        sigs.append(["JUMP", arg])
    return sigs


def comparison_jump_ops():
    sigs = []
    ops = [
        "JUMP_IF_LT_ACC",
        "JUMP_IF_LT_EQ_ACC",
        "JUMP_IF_EQ_ACC",
        "JUMP_IF_NEQ_ACC",
        "JUMP_IF_GT_EQ_ACC",
        "JUMP_IF_GT_ACC",
    ]
    args = [
        "A",
        "B",
        "C",
        "SP",
        "CONST_8",
    ]
    for op, arg in itertools.product(ops, args):
        sigs.append([op, arg, "CONST_16"])

    for arg in ["ACC", "A", "B", "C", "SP"]:
        sigs.append(["JUMP_IF_EQ_ZERO", arg, "CONST_16"])

    for arg in ["ACC", "A", "B", "C", "SP"]:
        sigs.append(["JUMP_IF_NEQ_ZERO", arg, "CONST_16"])

    return sigs


def jump_if_flag_ops():
    sigs = []
    ops = [
        "JUMP_IF_NEGATIVE_FLAG",
        "JUMP_IF_NOT_NEGATIVE_FLAG",
        "JUMP_IF_CARRYBORROW_FLAG",
        "JUMP_IF_NOT_CARRYBORROW_FLAG",
        "JUMP_IF_ZERO_FLAG",
        "JUMP_IF_NOT_ZERO_FLAG",
        ]
    for op in ops:
        sigs.append([op, "CONST_16"])
    return sigs


def skip_if_ops():
    sigs = []
    ops = [
        "SKIP_IF_LT_ACC",
        "SKIP_IF_LT_EQ_ACC",
        "SKIP_IF_EQ_ACC",
        "SKIP_IF_NEQ_ACC",
        "SKIP_IF_GT_EQ_ACC",
        "SKIP_IF_GT_ACC",
    ]
    args = [
        "A",
        "B",
        "C",
        "SP",
        "CONST_8",
    ]
    for op, arg in itertools.product(ops, args):
        sigs.append([op, arg])

    for arg in ["ACC", "A", "B", "C", "SP"]:
        sigs.append(["SKIP_IF_EQ_ZERO", arg])

    for arg in ["ACC", "A", "B", "C", "SP"]:
        sigs.append(["SKIP_IF_NEQ_ZERO", arg])

    return sigs


def call_op():
    return ["CALL", "CONST_16"]


def ret_op():
    return ["RETURN"]


def halt_op():
    return ["HALT"]


def logical_ops():
    sigs = []
    ops = [
        "AND",
        "NAND",
        "OR",
        "NOR",
        "XOR",
        "NXOR",
    ]
    args = ["A", "B", "C", "CONST_8"]
    for op, arg in itertools.product(ops, args):
        sigs.append([op, arg])

    for arg in ["ACC", "A", "B", "C"]:
        sigs.append(["NOT", arg])

    return sigs


def rot_left_op():
    sigs = []
    for arg in ["ACC", "A", "B", "C"]:
        sigs.append(["ROT_LEFT", arg])
    return sigs


def get_all_instructions():
    all_instrs = []
    all_ops = [
        add_op,
        addc_op,
        sub_op,
        subb_op,
        lshift_op,
        lshiftc_op,
        incr_op,
        decr_op,
        copy_op,
        load_op,
        store_op,
        push_op,
        pop_op,
        set_op,
        setzero_op,
        noop_op,
        jump_op,
        comparison_jump_ops,
        jump_if_flag_ops,
        skip_if_ops,
        call_op,
        ret_op,
        halt_op,
        logical_ops,
        rot_left_op
    ]
    for op in all_ops:
        all_instrs.extend(op())
    return all_instrs


print len(get_all_instructions())
