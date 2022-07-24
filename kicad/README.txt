templates
    KiCad templates for boards in the computer
    https://docs.kicad-pcb.org/5.1/en/kicad/kicad.html#project_templates

symbol_libs
    Symbol libraries shared between the KiCad project.
    The templates are set up to point to these.

projects
    A folder to contain the KiCad projects.
    Each board is it's own project.

footprint_libs
    Footprint libraries shared between the KiCad projects.
    The templates are set up to point to these.


Library referncing is achieved via the KiCad variable replacement in the project library settings:
    ${KIPRJMOD}\..\..\symbol_libs\eight-bit-computer.lib
    ${KIPRJMOD}\..\..\footprint_libs\eight-bit-computer.pretty
