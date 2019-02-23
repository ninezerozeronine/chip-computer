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

if __name__ == "__main__":
    sandbox()