Machine Code
============

00 DDD SSS - Copy instructions - Copy SSS to DDD
01 DDD [SSS] - Load instructions - Load memory contents at SSS into DDD
10 [DDD] SSS - Store instructions - Store SSS into memory at DDD
11 WWWW ZZ - ALU instructions - Do WWWW using ZZ (and sometimes B), and store the result in ZZ
00 110 CCC - Jump to an immediate value based on the result of the last test using the ALU (Pushes, Pops, Calls, Returns and other ALU operations will clobber the test results (Unless I AND bits 3, 4 and 5 (index starting at the right) of the op code and the alu write signal to enable a write to the flags register. But that will mean checking of other routine operations won't be possible))
00 111 CCC - Jump to an immediate value based on a test and check CCC between A and B register

Copy, Load and Store
====================
SSS = Source
DDD = Destination
WWWW = Operation
ZZ = Source/Dest

SSS/DDD - Source / Destination
000 = A
001 = B
010 = C
011 = D
100 = SP
101 = PC
110 = SP+/-
111 = Immediate

ALU
===
ZZ - Source / Destination
00 = A
01 = B
10 = C
11 = D

WWWW - ALU Operation
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

Checks
======
000: Check for equality to zero of the first value or last operation
001: Check for equality between the two values
010: Check if an addition resulted in a carry 
011: Check if subtraction resulted in a borrow 
100: Check if the first value is greater than the second value  
101: Check if the first value is greater than or equal to the second value 
110: Check if the first value is less than the second value
111: Check if the first value is less than or equal to the second value