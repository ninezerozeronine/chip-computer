Input Sigs
==========
Opcode (8 bits)
Microcode Step (3 bits)
ALU Flags (4 bits) (Zero, Carry/compare, Equality, Negative)

15 in total

Control Sigs
============
A_IN
A_OUT
B_IN
B_OUT
C_IN
C_OUT
D_IN
D_OUT

ALU_STORE
ALU_OUT
ALU_S0
ALU_S1
ALU_S2
ALU_S3
ALU_CIN
ALU_M

ALU_FLAGS_STORE
ALU_INPUT_SEL
RAM_ADDR_IN
RAM_IN
RAM_OUT
PROGRAM_COUNTER_IN
PROGRAM_COUNTER_OUT
PROGRAM_COUNTER_COUNT

SP_IN
SP_OUT
INSTRUCTION_REGISTER_IN
PROGRAM_MEMORY_SELECT
STEP_COUNTER_RESET
HALT

30 in total

Instructions
============

In the instructions below

SRC / DST
^^^^^^^^^
A source/destination for an instruction. Can be one of:
    A
    B
    C
    D
    SP
    PC

CHECK
^^^
A check to perform on a test result
    ZZ == 0
    ZZ == B
    ZZ is negative (2's Compliment)
    ZZ <= B
    ZZ > B
    ZZ < B
    ZZ >= B

TASK
^^^^
An ALU task
    ZZ = ZZ + 1 
    ZZ = ZZ - 1  
    ZZ = A + B    
    ZZ = A - B  
    ZZ = A + B with carry from last addition  
    ZZ = A - B with borrow from last subtraction  
    ZZ = A AND B  
    ZZ = A OR B   
    ZZ = A NAND B 
    ZZ = A XOR B     
    ZZ = NOT A  
    ZZ = A << 1  
    ZZ = A << 1 with carry from last shift    
    Test ZZ and B (ZZ <= B, ZZ > B, ZZ == B)    
    Test ZZ and B (ZZ < B, ZZ >= B) 
    Test ZZ (ZZ == 0, ZZ is negative (2's compliment))

OPER
^^^^
An operand for an ALU task
    A
    B
    C
    D



COPY SRC DST
COPY (A, B, C, D, SP, PC) (A, B, C, D, SP, PC)
    Copy SSS into DST

LOAD [SRC] DST
LOAD [(A, B, C, D, SP, PC, #)] (A, B, C, D, SP, PC)
    Copy the value in memory at SRC to DST

STORE SRC [DST]
STORE (A, B, C, D, SP, PC) [(A, B, C, D, SP, PC, #)]
    Copy the value in SRC to memory at DST

POP DST
POP (A, B, C, D, SP, PC)
    Pop the value off the top of the stack into DST

PUSH SRC
PUSH (A, B ,C, D, SP, PC)
    Push the value in SRC on to the top of the stack

SET DST #
SET (A, B, C, D, SP, PC) #
    Set DST to an absolute value

SET_ZERO DST
SET_ZERO (A, B, C, D, SP, PC)
    Set DST to 0 (Saves a program byte!)

JUMP DST
JUMP (A, B, C, D, SP, PC, #)
    Set the program counter to a value.

JUMP_IF_TEST TTT #
JUMP_IF_TEST (ZERO, EQUAL, NEGATIVE, LTE, GT, LT, GTE) #
    If the result of the test that was done using the ALU was true, jump to #

JUMP_IF_FLAG FFF #
JUMP_IF_FLAG (ZERO, NEGATIVE, OVERFLOW, UNDERFLOW) #
    If the flag set by the ALU is true, jump to #

ALU TASK OPER
ALU (INCR, DECR, ADD, SUB, ADD_CARRY, SUB_BORROW, AND, OR, NAND, XOR, NOT, SHIFT, SHIFT_CARRY, TEST_LTE, TEST_GT, TEST_LT, TEST_GTE, TEST_ZERO, TEST_NEGATIVE) (A, B, C, D)
    Do the specified task using the given operand

CALL DST
CALL (A, B, C, D, SP, PC, #)
    Push the program counter, then set the program counter to a value.

RETURN
    Set the program counter to the value on top of the stack, then pop the value off the stack

PROGRAM_LOAD SRC
PROGRAM_LOAD [A, B, C, D, SP, PC, #)]
    Load the contents of program memory at SRC into the D register.

PROGRAM_STORE DST
PROGRAM_STORE [A, B, C, D, SP, PC, #)]
    Store the D register into program memory at DST.

NOOP
    Do nothing

HALT
    Halt the computer










COPY - Copy SSS into DDD
    00 SSS DDD
LOAD - Copy the value in memory at SSS to DDD
    01 [SSS] DDD
STORE - Copy the value in SSS to memory at DDD
    10 SSS [DDD]
POP - Decrement SP and copy the memory at SP into DDD
    Actually a load with the source set to [SP+/-]
    01 [110] DDD
PUSH - Copy SSS into memory at SP and increment SP
    Actually a store with the destination set to [SP+/-]
    10 SSS [110]
DATA - Set a DDD to a specific value
    Actually a copy from an immediate value to DDD
    00 111 DDD
JUMP - Set the program counter to a value.
    Actually a copy where the desination is PC
    00 SSS 101
JUMP_IF_TEST_RESULT - Conditionally jump to an immediate value based on a check (CCC) of the result of a test using the ALU
    00 110 TTT
JUMP_IF_FLAG - Conditionally jump to an immediate value based on the state of an ALU flag
    11 110 FFF
ALU - Perform the WWWW operation with the ALU where ZZ is a source, destination or both
    11 WWWW ZZ
CALL - Push the program counter, then set the program counter to a value. LLL has the same meaning as SSS/DDD
    Actually a load where the destination is SP+/-
    01 110 LLL
RETURN - Set the program counter to the value pointed at by the stack pointer, then increment the stack pointer
    Actually a POP into the PC which is actually a load from [SP+/-] to PC
    10 101 110
PROGRAM_LOAD - Load the contents of program memory at PPP into the D register. PPP has the same meaning as SSS/DDD
    01 [PPP] 111
PROGRAM_STORE - Store the D register into program memory at PPP.  PPP has the same meaning as SSS/DDD
    10 110 [PPP]
NOOP - Do nothing
    00 000 000
HALT - Halt the computer
    00 111 111

























Op codes
========

00 SSS DDD - Copy instructions - Copy SSS to DDD
01 [SSS] DDD - Load instructions - Load memory contents at SSS into DDD
10 SSS [DDD] - Store instructions - Store SSS into memory at DDD
11 WWWW ZZ - ALU instructions - Do WWWW using ZZ (and sometimes B), and store the result in ZZ

SSS = Source
DDD = Destination
WWWW = ALU Operation
ZZ = Source/Dest
CCC = Checks
RRR = Results

SSS/DDD - Source / Destination
000 = A
001 = B
010 = C
011 = D
100 = SP
101 = PC
110 = SP+/-
111 = Immediate

ZZ - Source / Destination
00 = A
01 = B
10 = C
11 = D

WWWW - ALU Operation
0000: ZZ = ZZ + 1
0001: ZZ = ZZ - 1
0010: ZZ = A + B
0011: ZZ = A - B
0100: ZZ = A + B with carry if last operation output a carry
0101: ZZ = A - B with borrow if last operation output a borrow
0110: ZZ = A AND B
0111: ZZ = A OR B 
1000: ZZ = A NAND B
1001: ZZ = A XOR B 
1010: ZZ = NOT A
1011: ZZ = A << 1
1100: ZZ = A << 1 with carry if last operation output a carry
1101: Test ZZ and B (ZZ <= B, ZZ > B, ZZ == B)
1110: Test ZZ and B (ZZ < B, ZZ >= B)
1111: Test ZZ (ZZ == 0, ZZ is negative (2's compliment))

TTT - Tests
Jump if test result:
000: ZZ == 0
001: ZZ == B
010: ZZ is negative (2's Compliment)
011: ZZ <= B
100: ZZ > B
101: ZZ < B
110: ZZ >= B
111: -

FFF - ALU Flags
000: Result was zero
001: Result was negative (2's Compliment)
010: Addition overflowed
011: Subtraction underflowed
100: -
101: -
110: -
111: -





Opcode Gaps
===========
Copying a register to itelf is meaningless
00 000 000 - NOOP
00 001 001
00 010 010
00 011 011
00 100 100
00 101 101
00 110 110
00 111 111 - HALT

A copy from SP+/- doesn't make sense, it only has a meaning when doing load or stores
00 110 XXX - Used by jump if test result

Storing SP+/- Not very meaningful - do you want to store the increment or decrement of SP?
10 110 [XXX] - Used by jump if flag

A copy to SP+/- doesn't make sense, it only has a meaning when doing load or stores
00 XXX 110 - 

A copy to an immediate value doesnt make sense, you can't write to an immediate value
00 XXX 111 - 

Loading into SP - Not very useful. Can be achieved with a load to a reg then a copy anyway.
01 [XXX] 100 - 

Loading into SP+/- doesn't make sense, SP+/- isn't somewhere you can store data
01 [XXX] 110 - Used by CALL

Loading into an immediate doeasn't make sense, you cant write to immediate values
01 [XXX] 111 - Used by PROGRAM_LOAD

Storing SP - Not very useful - that's what SP is there for. Can be achieved with a load to a reg then a copy anyway.
10 100 [XXX] - 

Storing immediate values - Simply not possible as a value needs be copied from one location in memory to another and we have no intermediate storage space
10 111 [XXX] - Used by PROGRAM_STORE



