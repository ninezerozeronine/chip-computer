# Modes the panel can be in
# Allows single stepping of the CPU. The CPU is in full control
# of the peripherals.
PANEL_MODE_STEP = 100

# Running at a given frequency. The CPU is in full control of the
# peripherals.
PANEL_MODE_RUN = 101

# The CPU is stopped. Control of peripherals is given to the panel.
PANEL_MODE_STOP = 102

# The memory can be read manually by putting an address on the address
# bus.
PANEL_MODE_READ_MEMORY = 103


# Clock sources for the CPU
# The CPU is getting it's clock signals from the front panel
CPU_CLK_SRC_PANEL = 200

# The CPU is getting it's clock signal from the crystal
CPU_CLK_SRC_CRYSTAL = 201

# Maps panel modes to readable names
PANEL_MODE_TO_NAME = {
    PANEL_MODE_STEP: "Step",
    PANEL_MODE_RUN: "Run",
    PANEL_MODE_STOP: "Stop",
    PANEL_MODE_READ_MEMORY: "Read Memory"
}

# Maps clock modes to names
CLOCK_MODE_TO_NAME = {
    CPU_CLK_SRC_PANEL: "Custom frequency",
    CPU_CLK_SRC_CRYSTAL: "Crystal"
}

# Order is the same as defined in the micropython code
# The index is used as the ID
PRORGAMS = [
    "Dummy 1",
    "Dummy 2"
]