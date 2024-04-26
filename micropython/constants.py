# Modes the panel can be in
# Allows single stepping of the CPU. The CPU is in full control
# of the peripherals.
PANEL_MODE_STEP = 100

# Running at a given frequency. The CPU is in full control of the
# peripherals.
PANEL_MODE_RUN = 101

# The CPU is stopped. Control of peripherals is given to the panel.
PANEL_MODE_STOP = 102

# The memory can be read manually
PANEL_MODE_READ_MEMORY = 103


# Clock sources for the CPU
# The CPU is getting it's clock signals from the front panel
CPU_CLK_SRC_PANEL = 200

# The CPU is getting it's clock signal from the crystal
CPU_CLK_SRC_CRYSTAL = 201
