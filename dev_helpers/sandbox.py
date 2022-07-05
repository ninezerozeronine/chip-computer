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


if __name__ == "__main__":
    # sandbox()
    # file_test()
    # dict_ref_test()
    # dict_ref_test_2()
    # assemble_test()
    # main.create_roms(directory="./test_roms")
    # try_dedent()
    create_copy_tests()
