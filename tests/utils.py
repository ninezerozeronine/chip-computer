from itertools import product

def create_load_tests():
    """

    # Module as an address into ACC
    $v_load_<index> #<random>
    &load_<index>
        SET A $v_load_<index>
        LOAD [A] ACC
        JUMP_IF_ACC_EQ #<random> &load_<index + 1>
        HALT

    # Module as an address into a non ACC module
    $v_load_<index> #<random>
    &load_<index>
        SET A $v_load_<index>
        LOAD [A] A
        SET ACC #<random>
        JUMP_IF_ACC_EQ A &load_<index + 1>
        HALT

    # Constant address into ACC
    $v_load_<index> #<random>
    &load_<index>
        LOAD [$v_load_<index>] ACC
        JUMP_IF_ACC_EQ #<random> &load_<index + 1>
        HALT

    # Constant address into a non ACC module
    $v_load_<index> #<random>
    &load_<index>
        LOAD [$v_load_<index>] C
        SET ACC #<random>
        JUMP_IF_ACC_EQ C &load_<index + 1>
        HALT

    """
    sources = ("[ACC]", "[A]", "[B]", "[C]", "[SP]")
    destinations = ("ACC", "A", "B", "C")
    lines = []
    index = 0
    for src, dest in product(sources, destinations):
        num = random.randint(0, 65535)
        if dest == "ACC":
            lines.append(f"$v_load_{index} #{num}")
            lines.append(f"&load_{index}")
            lines.append(f"    SET {src[1:-1]} $v_load_{index}")
            lines.append(f"    LOAD {src} {dest}")
            lines.append(f"    JUMP_IF_ACC_EQ #{num} &load_{index + 1}")
            lines.append(f"    HALT")
            lines.append("")
        else:
            lines.append(f"$v_load_{index} #{num}")
            lines.append(f"&load_{index}")
            lines.append(f"    SET {src[1:-1]} $v_load_{index}")
            lines.append(f"    LOAD {src} {dest}")
            lines.append(f"    SET ACC #{num}")
            lines.append(f"    JUMP_IF_ACC_EQ {dest} &load_{index + 1}")
            lines.append(f"    HALT")
            lines.append("")

        index += 1

    for dest in destinations:
        num = random.randint(0, 65535)
        if dest == "ACC":
            lines.append(f"$v_load_{index} #{num}")
            lines.append(f"&load_{index}")
            lines.append(f"    LOAD [$v_load_{index}] {dest}")
            lines.append(f"    JUMP_IF_ACC_EQ #{num} &load_{index + 1}")
            lines.append(f"    HALT")
            lines.append("")
        else:
            lines.append(f"$v_load_{index} #{num}")
            lines.append(f"&load_{index}")
            lines.append(f"    LOAD [$v_load_{index}] {dest}")
            lines.append(f"    SET ACC #{num}")
            lines.append(f"    JUMP_IF_ACC_EQ {dest} &load_{index + 1}")
            lines.append(f"    HALT")
            lines.append("")

        index += 1

    print("\n".join(lines))


def create_store_tests():
    """

    Same source and dest
        $v_store_<index>
        &store_<index>
            SET C $v_store_<index>
            STORE C [C]
            LOAD [C] ACC
            JUMP_IF_ACC_EQ $v_store_<index> &store_<index + 1>
            HALT


    Different Source and Dest
        $v_store_<index>
        &store_<index>
            SET C #<random>
            SET A $v_store_<index>
            STORE C [A]
            LOAD [A] ACC
            JUMP_IF_ACC_EQ #<random> &store_<index + 1>
            HALT

    Dest is constant
        $v_store_<index>
        &store_<index>
            SET C #<random>
            STORE C [$v_store_<index>]
            LOAD [$v_store_<index>] ACC
            JUMP_IF_ACC_EQ #<random> &store_<index + 1>
            HALT


    """
    sources = ("ACC", "A", "B", "C", "SP")
    destinations = ("[ACC]", "[A]", "[B]", "[C]", "[SP]")
    lines = []
    index = 0
    for src in sources:
        for dest in destinations:
            if dest[1:-1] == src:
                # E.g. STORE B [B]
                lines.append(f"$v_store_{index}")
                lines.append(f"&store_{index}")
                lines.append(f"    SET {src} $v_store_{index}")
                lines.append(f"    STORE {src} {dest}")
                lines.append(f"    LOAD {dest} ACC")
                lines.append(f"    JUMP_IF_ACC_EQ $v_store_{index} &store_{index + 1}")
                lines.append(f"    HALT")
                lines.append("")
            else:
                # E.g. STORE C [SP]
                num = random.randint(0, 65535)
                lines.append(f"$v_store_{index}")
                lines.append(f"&store_{index}")
                lines.append(f"    SET {src} #{num}")
                lines.append(f"    SET {dest[1:-1]} $v_store_{index}")
                lines.append(f"    STORE {src} {dest}")
                lines.append(f"    LOAD {dest} ACC")
                lines.append(f"    JUMP_IF_ACC_EQ #{num} &store_{index + 1}")
                lines.append(f"    HALT")
                lines.append("")

            index += 1

        # E.g. STORE C [#123]
        num = random.randint(0, 65535)
        lines.append(f"$v_store_{index}")
        lines.append(f"&store_{index}")
        lines.append(f"    SET {src} #{num}")
        lines.append(f"    STORE {src} [$v_store_{index}]")
        lines.append(f"    LOAD [$v_store_{index}] ACC")
        lines.append(f"    JUMP_IF_ACC_EQ #{num} &store_{index + 1}")
        lines.append(f"    HALT")
        lines.append("")

        index += 1

    print("\n".join(lines))