"""
Things to test with oscilloscope

 - Interference between lines with HC chips on both ends.
  - Signals going the same way.
  - Signals going different ways.
  - Ground next to it.
 - The effect of an LED + resistor on a data line.
 - Compare bus line + inactive buffers to regular signal line.
 - What effect logic level shifters have on the signal.



"""

import sys
import os
from pprint import pprint
import textwrap
import random
from itertools import product

sys.path.append(os.path.abspath("../src"))
print(sys.path)
from sixteen_bit_computer import main


def sandbox():
    pass
    # rom_path = r"E:\dev\8bit-74-series-computer\logisim\roms"
    # rom.write_logisim_roms(rom_path)

    # romdatas = rom.get_rom()
    # print romdatas[0]
    # print romdatas[1]
    # print romdatas[2]
    # print romdatas[3]
    # print romdatas[4]

    # romdatas = rom.get_rom()
    # print("done")
    # slices = rom.slice_rom(romdatas)
    # slice_index = 1
    # romdata_chunks = rom.chunker(slices[slice_index], 16)
    # count = 0
    # for sixteen_index, romdata_chunk in enumerate(romdata_chunks):
    #     for line_index, romdata in enumerate(romdata_chunk):
    #         print("{hex_sixteen_index:04X} {sixteen_index:03} {line_index:04} {count:05} {romdata}".format(
    #             hex_sixteen_index=sixteen_index*16,
    #             sixteen_index=sixteen_index,
    #             line_index=line_index+1,
    #             count=count,
    #             romdata=romdata,
    #         ))
    #         count += 1

    # print(romdatas[128])

    # logisim_string = rom.rom_slice_to_logisim_string(slices[slice_index])
    # print(logisim_string)

    # romdatas = rom.get_defined_romdata()
    # full_rom = rom.populate_empty_addresses(romdatas)
    # for romdata in full_rom:
    #     print romdata
    # print len(full_rom)


def file_test():
    with open("test.py") as file:
        lines = file.read().splitlines()

    for line in lines[:10]:
        print(line)
        # print line.endswith("\n")


def modify(my_list):
    my_list[0]["new"] = "foo"
    my_list[1]["existing"].append("bar")


def dict_ref_test():
    a = [
        {
            "hello": 1
        },
        {
            "existing": ["baz"]
        },
    ]
    pprint(a)
    modify(a)
    pprint(a)


def get_dict():
    return {"a": 1, "b": 2}


def dict_ref_test_2():
    a = get_dict()
    a["a"] = "foo"
    print(a)
    b = get_dict()
    b["a"] = "bar"
    print(a)
    print(b)


def assemble_test():
    main.assemble("../programs/fibbonaci.asm")

def try_dedent():
    a = textwrap.dedent(
        """\
        FOO
            BAR
        HELLO
        WORLD
        """
    )

    print(a)
    print(a.splitlines())

def create_copy_tests():
    """
    &copy_<index>
        SET SRC #random
        SET ACC #random
        COPY SRC DEST
        JUMP_IF_EQ_ACC DEST &copy_<index + 1>
        HALT


    """
    sources = ("ACC", "A", "B", "C", "SP")
    destinations = ("ACC", "A", "B", "C", "SP")
    lines = []
    index = 0
    for src, dest in product(sources, destinations):
        if (src != dest):
            num = random.randint(0, 65535)
            if dest == "ACC":
                lines.append("&copy_{index}".format(index=index))
                lines.append("    SET {src} #{num}".format(src=src, num=num))
                lines.append("    COPY {src} ACC".format(src=src))
                lines.append("    JUMP_IF_ACC_EQ #{num} &copy_{index_plus_one}".format(num=num, index_plus_one=index+1))
                lines.append("    HALT")
                lines.append("")
            else:    
                lines.append("&copy_{index}".format(index=index))
                if src != "ACC":
                    lines.append("    SET {src} #{num}".format(src=src, num=num))
                lines.append("    SET ACC #{num}".format(num=num))
                lines.append("    COPY {src} {dest}".format(src=src, dest=dest))
                lines.append("    JUMP_IF_ACC_EQ {dest} &copy_{index_plus_one}".format(dest=dest, index_plus_one=index+1))
                lines.append("    HALT")
                lines.append("")

            index += 1

    print("\n".join(lines))

def create_load_tests():
    """

    $v_load_<index> #<random>
    &load_<index>
        SET A $v_load_<index>
        LOAD [A] ACC
        JUMP_IF_ACC_EQ #<random> &load_<index + 1>
        HALT

    $v_load_<index> #<random>
    &load_<index>
        SET A $v_load_<index>
        LOAD [A] A
        SET ACC #<random>
        JUMP_IF_ACC_EQ A &load_<index + 1>
        HALT

    $v_load_<index> #<random>
    &load_<index>
        LOAD [$v_load_<index>] ACC
        JUMP_IF_ACC_EQ #<random> &load_<index + 1>
        HALT

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



if __name__ == "__main__":
    # sandbox()
    # file_test()
    # dict_ref_test()
    # dict_ref_test_2()
    # assemble_test()
    # main.create_roms(directory="./test_roms")
    # try_dedent()
    # create_copy_tests()
    create_load_tests()
    create_store_tests()
