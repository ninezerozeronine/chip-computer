Assembly
========

COPY - Copy SSS into DDD
    00 DDD SSS
LOAD - Copy the value in memory at SSS to DDD
    01 DDD [SSS]
STORE - Copy the value in SSS to memory at DDD
    10 [DDD] SSS
POP - Decrement SP and copy the memory at SP into DDD
    Actually a load with the source set to [SP+/-]
    01 DDD 110
PUSH - Copy DDD into memory at SP and increment SP
    Actually a store with the destination set to [SP+/-]
    10 110 SSS
DATA - Set a DDD to a specific value
    Actually a copy from an immediate value to DDD
    00 DDD 1113
JUMP - Set the program counter to a value. JJJ has the same meaning as SSS/DDD
    Actually a copy where the desination is PC
    00 101 JJJ
CONDITIONAL_JUMP - Conditionally jump to an immediate value based on a check (CCC) of the result of the last test using the ALU
    Uses the unused move instruction with the destination as SP+/-
    00 110 CCC
TEST_AND_CONDITONAL_JUMP - Conditionally jump to an immediate value based on a check (CCC) of a test between A and B register
    Uses the unused move instruction with the destination as Immediate
    00 111 CCC
ALU - Perform the WWWW operation with the ALU where ZZ is a source, destination or both
    11 WWWW ZZ

	0000: ZZ = 0 
	0001: ZZ = ZZ + 1
	0010: ZZ = ZZ - 1
	0011: ZZ = A + B
	0100: ZZ = A - B
	0101: ZZ = A + B with carry
	0110: ZZ = A - B with borrow
	0111: ZZ = A AND B
	1000: ZZ = A OR B 
	1001: ZZ = A NAND B
	1010: ZZ = A XOR B 
	1011: ZZ = NOT A 
	1100: ZZ = A < 1
	1101: ZZ = A < 1 with carry 
	1110: Test ZZ and B (Greater than or equal to or less than and all other non size comparison tests) 
	1111: Test ZZ and B (Less than or equal to or greater than and all other non size comparison tests)

CALL - Push the program counter, then set the program counter to a value. LLL has the same meaning as SSS/DDD
    Actually a load where the destination is PC+/-
    01 110 LLL
RETURN - Set the program counter to the value pointed at by the stack pointer, then increment the stack pointer
    Actually a POP into the PC which is actually a load from [SP+/-] to PC
    10 101 110
PROGRAM_LOAD - Load the contents of program memory at PPP into the D register. PPP has the same meaning as SSS/DDD
    01 111 PPP
PROGRAM_STORE - Store the D register into program memory at PPP
    10 PPP 110
NOOP - Do nothing
    00 000 000
HALT - Halt the computer
    00 111 111