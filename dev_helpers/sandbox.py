import sys
import os
from pprint import pprint

sys.path.append(os.path.abspath("../src"))

from eight_bit_computer import rom, main
from eight_bit_computer.simulator import core
from eight_bit_computer.simulator.register import Register
from eight_bit_computer.simulator.constant import Constant


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
    print "done"
    slices = rom.slice_rom(romdatas)
    slice_index = 1
    romdata_chunks = rom.chunker(slices[slice_index], 16)
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
    return {"a": 1, "b": 2}


def dict_ref_test_2():
    a = get_dict()
    a["a"] = "foo"
    print a
    b = get_dict()
    b["a"] = "bar"
    print a
    print b


def assemble_test():
    main.assemble("../programs/fibbonaci.asm")


class Channel_dev(object):
    def __init__(self):
        self.state = 0


class Port_dev(object):
    def __init__(self, channels):
        self.channels = channels


class Connection_dev(object):
    def __init__(self, ports):
        self.ports = ports

    def incr_channel(self):
        self.ports[0].channels[0].state += 1


class Module_dev(object):
    def __init__(self):
        chan = Channel_dev()
        self.port = Port_dev(channels=[chan])


def contention_test():
    p1 = core.Port("one", channels=[core.Channel(mode=core.MODE["OUTPUT"])])
    p2 = core.Port("two", channels=[core.Channel(mode=core.MODE["INPUT"])])
    conn = core.Connection([p1, p2])
    print conn.ports_in_contention()


def conn_test():
    module = Module_dev()
    connection = Connection_dev([module.port])
    connection2 = Connection_dev([module.port])
    print module.port
    print module.port.channels
    print module.port.channels[0]
    print module.port.channels[0].state
    connection.incr_channel()
    print module.port.channels[0].state
    connection2.incr_channel()
    print module.port.channels[0].state


class SimpleSim(object):
    def __init__(self):
        self.zeros = [
            core.STATE["LOW"],
            core.STATE["LOW"],
            core.STATE["LOW"],
            core.STATE["LOW"],
            core.STATE["LOW"],
            core.STATE["LOW"],
            core.STATE["LOW"],
            core.STATE["LOW"],

        ]
        self.ones = [
            core.STATE["HIGH"],
            core.STATE["HIGH"],
            core.STATE["HIGH"],
            core.STATE["HIGH"],
            core.STATE["HIGH"],
            core.STATE["HIGH"],
            core.STATE["HIGH"],
            core.STATE["HIGH"],
        ]
        self.modules = {}
        self.modules["reg"] = Register("A")
        self.modules["clock"] = Constant("clock", bitwidth=1)
        self.modules["input_enable"] = Constant("input_enable", bitwidth=1)
        self.modules["output_enable"] = Constant("output_enable", bitwidth=1)
        self.modules["data"] = Constant("data", bitwidth=8)

        self.modules["clock"].output.states = [core.STATE["LOW"]]
        self.modules["input_enable"].output.states = [core.STATE["LOW"]]
        self.modules["output_enable"].output.states = [core.STATE["LOW"]]
        self.modules["data"].output.states = self.zeros

        self.connections = [
            core.Connection(ports=[
                self.modules["data"].output,
                self.modules["reg"].data,
            ]),
            core.Connection(ports=[
                self.modules["clock"].output,
                self.modules["reg"].clock,
            ]),
            core.Connection(ports=[
                self.modules["input_enable"].output,
                self.modules["reg"].input_enable,
            ]),
            core.Connection(ports=[
                self.modules["output_enable"].output,
                self.modules["reg"].output_enable,
            ]),
        ]

    def update(self):
        for connection in self.connections:
            for port in connection.ports:
                connection.propagate_to_inputs()

        for module in self.modules.values():
            module.update()

    def print_reg(self):
        print "---"
        print "contents:",
        states = []
        for channel in self.modules["reg"].contents.channels:
            states.append(str(channel.state))
        print "".join(states)

        print "input_enable:",
        print self.modules["reg"].input_enable.states[0]

        print "output_enable:",
        print self.modules["reg"].output_enable.states[0]

        print "clock:",
        print self.modules["reg"].clock.states[0]
        print "---"

    def test(self):
        self.update()
        self.print_reg()
        self.modules["input_enable"].output.states = [core.STATE["HIGH"]]
        self.update()
        self.print_reg()
        self.modules["clock"].output.states = [core.STATE["HIGH"]]
        self.update()
        self.print_reg()
        self.modules["data"].output.states = self.ones
        self.update()
        self.print_reg()
        self.modules["clock"].output.states = [core.STATE["LOW"]]
        self.update()
        self.print_reg()
        self.modules["clock"].output.states = [core.STATE["HIGH"]]
        self.update()
        self.print_reg()
        self.modules["output_enable"].output.states = [core.STATE["LOW"]]
        self.update()
        self.print_reg()
        self.update()
        self.print_reg()

def sim_test():
    sim = SimpleSim()
    sim.test()


if __name__ == "__main__":
    # sandbox()
    # file_test()
    # dict_ref_test()
    # dict_ref_test_2()
    # assemble_test()
    # main.create_roms(directory="./test_roms")
    # conn_test()
    # contention_test()
    sim_test()



























