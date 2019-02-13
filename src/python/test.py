import utils

# Good
# bitdefs = [
#     utils.BitDef(end=3, start=0, value="101X"),
#     utils.BitDef(end=7, start=4, value="0000")
# ]

bitdefs = [
    utils.BitDef(end=3, start=2, value="00"),
    utils.BitDef(end=5, start=4, value="11"),
    utils.BitDef(end=7, start=6, value="XX")
]

# Gaps
# bitdefs = [
#     utils.BitDef(end=2, start=0, value="111"),
#     utils.BitDef(end=7, start=4, value="0000")
# ]

# Overlap
# bitdefs = [
#     utils.BitDef(end=3, start=0, value="1111"),
#     utils.BitDef(end=7, start=2, value="000000")
# ]

for bitdef in bitdefs:
    print bitdef


print "limits", utils.bitdef_limits(bitdefs)
print "overlap", utils.bitdefs_overlap(bitdefs)
print "gaps", utils.bitdefs_have_gaps(bitdefs)
print "join", utils.join_bitdefs(bitdefs)