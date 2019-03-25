from pprint import pprint

from eight_bit_computer import rom, utils

def sandbox():

    # rom_path = r"E:\dev\8bit-74-series-computer\logisim\roms"
    # rom.write_logisim_roms(rom_path)

    # romdatas = rom.get_rom()
    # print romdatas[0]
    # print romdatas[1]
    # print romdatas[2]
    # print romdatas[3]
    # print romdatas[4]

    romdatas = rom.get_rom()
    slices = rom.slice_rom(romdatas)
    slice_index = 1
    romdata_chunks = utils.chunker(slices[slice_index], 16)
    count = 0
    for sixteen_index, romdata_chunk in enumerate(romdata_chunks):
        for line_index, romdata in enumerate(romdata_chunk):
            print "{hex_sixteen_index:04X} {sixteen_index:03} {line_index:04} {count:05} {romdata}".format(
                hex_sixteen_index=sixteen_index*16,
                sixteen_index=sixteen_index,
                line_index=line_index+1,
                count=count,
                romdata=romdata,
            )
            count += 1

    print romdatas[128]

    logisim_string = rom.rom_slice_to_logisim_string(slices[slice_index])
    print logisim_string

    # romdatas = rom.get_defined_romdata()
    # full_rom = rom.populate_empty_addresses(romdatas)
    # for romdata in full_rom:
    #     print romdata
    # print len(full_rom)

def file_test():
    with open("test.py") as file:
        lines = file.read().splitlines()

    for line in lines[:10]:
        print line
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
    return {"a":1, "b":2}

def dict_ref_test_2():
    a = get_dict()
    a["a"] = "foo"
    print a
    b = get_dict()
    b["a"] = "bar"
    print a
    print b

if __name__ == "__main__":
    # sandbox()
    # file_test()
    # dict_ref_test()
    dict_ref_test_2()
