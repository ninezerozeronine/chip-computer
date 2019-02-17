from eight_bit_computer import rom

romdatas = rom.get_all_romdata()
full_rom = rom.populate_empty_addresses(romdatas)
for romdata in full_rom:
    print romdata
print len(full_rom)