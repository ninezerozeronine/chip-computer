EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr USLetter 11000 8500
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Memory_EEPROM:28C256 U3
U 1 1 5E13FEAC
P 4300 4750
F 0 "U3" H 4300 6031 50  0000 C CNN
F 1 "28C256" H 4300 5940 50  0000 C CNN
F 2 "Package_DIP:DIP-28_W15.24mm_Socket" H 4300 4750 50  0001 C CNN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/doc0006.pdf" H 4300 4750 50  0001 C CNN
	1    4300 4750
	1    0    0    -1  
$EndComp
$Comp
L Memory_EEPROM:28C256 U4
U 1 1 5E140592
P 2000 4750
F 0 "U4" H 2000 6031 50  0000 C CNN
F 1 "28C256" H 2000 5940 50  0000 C CNN
F 2 "Package_DIP:DIP-28_W15.24mm_Socket" H 2000 4750 50  0001 C CNN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/doc0006.pdf" H 2000 4750 50  0001 C CNN
	1    2000 4750
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x08_Female J7
U 1 1 5E25048F
P 15100 3300
F 0 "J7" H 15128 3276 50  0000 L CNN
F 1 "Conn_01x08_Female" H 15128 3185 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Horizontal" H 15100 3300 50  0001 C CNN
F 3 "~" H 15100 3300 50  0001 C CNN
	1    15100 3300
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x16_Female J5
U 1 1 5E251504
P 14200 1950
F 0 "J5" H 14228 1926 50  0000 L CNN
F 1 "Conn_01x16_Female" H 14228 1835 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x16_P2.54mm_Horizontal" H 14200 1950 50  0001 C CNN
F 3 "~" H 14200 1950 50  0001 C CNN
	1    14200 1950
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x04_Female J2
U 1 1 5E25238A
P 12800 2650
F 0 "J2" H 12828 2626 50  0000 L CNN
F 1 "Conn_01x04_Female" H 12828 2535 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x04_P2.54mm_Horizontal" H 12800 2650 50  0001 C CNN
F 3 "~" H 12800 2650 50  0001 C CNN
	1    12800 2650
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x08_Female J3
U 1 1 5E253BE4
P 12850 1900
F 0 "J3" H 12878 1876 50  0000 L CNN
F 1 "Conn_01x08_Female" H 12878 1785 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Horizontal" H 12850 1900 50  0001 C CNN
F 3 "~" H 12850 1900 50  0001 C CNN
	1    12850 1900
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x16_Female J6
U 1 1 5E2549B9
P 14950 1950
F 0 "J6" H 14978 1926 50  0000 L CNN
F 1 "Conn_01x16_Female" H 14978 1835 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x16_P2.54mm_Horizontal" H 14950 1950 50  0001 C CNN
F 3 "~" H 14950 1950 50  0001 C CNN
	1    14950 1950
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x34_Male J4
U 1 1 5E25780B
P 4450 7650
F 0 "J4" V 4350 7650 50  0000 C CNN
F 1 "Conn_01x34_Male" V 4250 7650 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x34_P2.54mm_Horizontal" H 4450 7650 50  0001 C CNN
F 3 "~" H 4450 7650 50  0001 C CNN
	1    4450 7650
	0    1    -1   0   
$EndComp
$Comp
L Connector:Conn_01x08_Male J1
U 1 1 5E25493E
P 2100 7450
F 0 "J1" V 2027 7378 50  0000 C CNN
F 1 "Conn_01x08_Male" V 1936 7378 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x08_P2.54mm_Horizontal" H 2100 7450 50  0001 C CNN
F 3 "~" H 2100 7450 50  0001 C CNN
	1    2100 7450
	0    1    -1   0   
$EndComp
$Comp
L eight-bit-computer:74HCT377 U5
U 1 1 5E2645FB
P 1750 1050
F 0 "U5" H 1750 2031 50  0000 C CNN
F 1 "74HCT377" H 1750 1940 50  0000 C CNN
F 2 "Package_DIP:DIP-20_W7.62mm_Socket" H 1750 1050 50  0001 C CNN
F 3 "http://www.ti.com/lit/gpn/sn74LS377" H 1750 1050 50  0001 C CNN
	1    1750 1050
	0    1    1    0   
$EndComp
NoConn ~ 12300 -1650
$Comp
L eight-bit-computer:74HCT173 U7
U 1 1 5E268A7A
P 3700 1050
F 0 "U7" V 3654 1994 50  0000 L CNN
F 1 "74HCT173" V 3745 1994 50  0000 L CNN
F 2 "Package_DIP:DIP-16_W7.62mm_Socket" H 3700 1050 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/cd74hc173.pdf" H 3700 1050 50  0001 C CNN
	1    3700 1050
	0    1    1    0   
$EndComp
$Comp
L 74xx:74HCT04 U9
U 1 1 5E26993C
P 14350 -1500
F 0 "U9" H 14350 -1183 50  0000 C CNN
F 1 "74HCT04" H 14350 -1274 50  0000 C CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket" H 14350 -1500 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 14350 -1500 50  0001 C CNN
	1    14350 -1500
	1    0    0    -1  
$EndComp
$Comp
L 74xx:74HCT04 U9
U 2 1 5E26A77F
P 15200 -1500
F 0 "U9" H 15200 -1183 50  0000 C CNN
F 1 "74HCT04" H 15200 -1274 50  0000 C CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket" H 15200 -1500 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 15200 -1500 50  0001 C CNN
	2    15200 -1500
	1    0    0    -1  
$EndComp
$Comp
L 74xx:74HCT04 U9
U 3 1 5E26B867
P 16100 -1500
F 0 "U9" H 16100 -1183 50  0000 C CNN
F 1 "74HCT04" H 16100 -1274 50  0000 C CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket" H 16100 -1500 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 16100 -1500 50  0001 C CNN
	3    16100 -1500
	1    0    0    -1  
$EndComp
$Comp
L 74xx:74HCT04 U9
U 4 1 5E26D36D
P 14350 -1050
F 0 "U9" H 14350 -733 50  0000 C CNN
F 1 "74HCT04" H 14350 -824 50  0000 C CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket" H 14350 -1050 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 14350 -1050 50  0001 C CNN
	4    14350 -1050
	1    0    0    -1  
$EndComp
$Comp
L 74xx:74HCT04 U9
U 5 1 5E26ED90
P 15200 -1050
F 0 "U9" H 15200 -733 50  0000 C CNN
F 1 "74HCT04" H 15200 -824 50  0000 C CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket" H 15200 -1050 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 15200 -1050 50  0001 C CNN
	5    15200 -1050
	1    0    0    -1  
$EndComp
$Comp
L 74xx:74HCT04 U9
U 6 1 5E270236
P 16050 -1000
F 0 "U9" H 16050 -683 50  0000 C CNN
F 1 "74HCT04" H 16050 -774 50  0000 C CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket" H 16050 -1000 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 16050 -1000 50  0001 C CNN
	6    16050 -1000
	1    0    0    -1  
$EndComp
$Comp
L 74xx:74HCT04 U9
U 7 1 5E271B70
P 16900 -1750
F 0 "U9" H 17130 -1704 50  0000 L CNN
F 1 "74HCT04" H 17130 -1795 50  0000 L CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket" H 16900 -1750 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 16900 -1750 50  0001 C CNN
	7    16900 -1750
	1    0    0    -1  
$EndComp
$Comp
L eight-bit-computer:74HCT161 U6
U 1 1 5E277071
P 5850 1050
F 0 "U6" V 5804 1894 50  0000 L CNN
F 1 "74HCT161" V 5895 1894 50  0000 L CNN
F 2 "Package_DIP:DIP-16_W7.62mm_Socket" H 5850 1050 50  0001 C CNN
F 3 "https://www.ti.com/lit/ds/symlink/cd54hc163.pdf" H 5850 1050 50  0001 C CNN
	1    5850 1050
	0    1    1    0   
$EndComp
$Comp
L eight-bit-computer:74HCT138 U8
U 1 1 5E2791CC
P 7900 1200
F 0 "U8" V 7946 456 50  0000 R CNN
F 1 "74HCT138" V 7855 456 50  0000 R CNN
F 2 "Package_DIP:DIP-16_W7.62mm_Socket" H 7900 1200 50  0001 C CNN
F 3 "https://www.ti.com/lit/ds/symlink/sn74hct138.pdf" H 7900 1200 50  0001 C CNN
	1    7900 1200
	0    -1   -1   0   
$EndComp
$Comp
L Memory_EEPROM:28C256 U1
U 1 1 5E13E2C4
P 8750 4750
F 0 "U1" H 8750 6031 50  0000 C CNN
F 1 "28C256" H 8750 5940 50  0000 C CNN
F 2 "Package_DIP:DIP-28_W15.24mm_Socket" H 8750 4750 50  0001 C CNN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/doc0006.pdf" H 8750 4750 50  0001 C CNN
	1    8750 4750
	1    0    0    -1  
$EndComp
Text Label 8300 3850 2    50   ~ 0
MC_STEP_0
Entry Wire Line
	7750 3750 7850 3850
Entry Wire Line
	7750 3850 7850 3950
Entry Wire Line
	7750 3950 7850 4050
Entry Wire Line
	7750 4050 7850 4150
Entry Wire Line
	7750 4150 7850 4250
Entry Wire Line
	7750 4250 7850 4350
Entry Wire Line
	7750 4350 7850 4450
Entry Wire Line
	7750 4450 7850 4550
Entry Wire Line
	7750 4550 7850 4650
Entry Wire Line
	7750 4650 7850 4750
Entry Wire Line
	7750 4750 7850 4850
Entry Wire Line
	7750 4850 7850 4950
Entry Wire Line
	7750 4950 7850 5050
Entry Wire Line
	7750 5050 7850 5150
Entry Wire Line
	7750 5150 7850 5250
Text Label 8300 3950 2    50   ~ 0
MC_STEP_1
Text Label 8300 4050 2    50   ~ 0
MC_STEP_2
Text Label 8300 4150 2    50   ~ 0
MIR_FLAG_Z
Text Label 8300 4250 2    50   ~ 0
MIR_FLAG_N
Text Label 8300 4350 2    50   ~ 0
MIR_FLAG_C
Text Label 8300 4450 2    50   ~ 0
MIR_FLAG_E
Text Label 8300 4550 2    50   ~ 0
MIR_INST_0
Text Label 8300 4650 2    50   ~ 0
MIR_INST_1
Text Label 8300 4750 2    50   ~ 0
MIR_INST_2
Text Label 8300 4850 2    50   ~ 0
MIR_INST_3
Text Label 8300 4950 2    50   ~ 0
MIR_INST_4
Text Label 8300 5050 2    50   ~ 0
MIR_INST_5
Text Label 8300 5150 2    50   ~ 0
MIR_INST_6
Text Label 8300 5250 2    50   ~ 0
MIR_INST_7
Entry Wire Line
	9550 3850 9650 3950
Entry Wire Line
	9550 3950 9650 4050
Entry Wire Line
	9550 4050 9650 4150
Entry Wire Line
	9550 4150 9650 4250
Entry Wire Line
	9550 4250 9650 4350
Entry Wire Line
	9550 4350 9650 4450
Entry Wire Line
	9550 4450 9650 4550
Entry Wire Line
	9550 4550 9650 4650
Text Label 9200 3850 0    50   ~ 0
ROM_0_0
Text Label 9200 3950 0    50   ~ 0
ROM_0_1
Text Label 9200 4050 0    50   ~ 0
ROM_0_2
Text Label 9200 4150 0    50   ~ 0
ROM_0_3
Text Label 9200 4250 0    50   ~ 0
ROM_0_4
Text Label 9200 4350 0    50   ~ 0
ROM_0_5
Text Label 9200 4450 0    50   ~ 0
ROM_0_6
Text Label 9200 4550 0    50   ~ 0
ROM_0_7
$Comp
L Device:R_Network08_US RN1
U 1 1 5E2EBA2A
P 9900 1400
F 0 "RN1" H 10288 1446 50  0000 L CNN
F 1 "R_Network08_US" H 10288 1355 50  0000 L CNN
F 2 "Resistor_THT:R_Array_SIP9" V 10375 1400 50  0001 C CNN
F 3 "http://www.vishay.com/docs/31509/csc.pdf" H 9900 1400 50  0001 C CNN
	1    9900 1400
	1    0    0    -1  
$EndComp
$Comp
L Device:R_Network08_US RN2
U 1 1 5E2EC96E
P 9900 2000
F 0 "RN2" H 10288 2046 50  0000 L CNN
F 1 "R_Network08_US" H 10288 1955 50  0000 L CNN
F 2 "Resistor_THT:R_Array_SIP9" V 10375 2000 50  0001 C CNN
F 3 "http://www.vishay.com/docs/31509/csc.pdf" H 9900 2000 50  0001 C CNN
	1    9900 2000
	1    0    0    -1  
$EndComp
$Comp
L Device:R_Network04_US RN3
U 1 1 5E2ED15F
P 9800 850
F 0 "RN3" H 9988 896 50  0000 L CNN
F 1 "R_Network04_US" H 9988 805 50  0000 L CNN
F 2 "Resistor_THT:R_Array_SIP5" V 10075 850 50  0001 C CNN
F 3 "http://www.vishay.com/docs/31509/csc.pdf" H 9800 850 50  0001 C CNN
	1    9800 850 
	1    0    0    -1  
$EndComp
Text Label 4750 3850 0    50   ~ 0
ROM_2_0
Text Label 4750 3950 0    50   ~ 0
ROM_2_1
Text Label 4750 4050 0    50   ~ 0
ROM_2_2
Text Label 4750 4150 0    50   ~ 0
ROM_2_3
Text Label 4750 4250 0    50   ~ 0
ROM_2_4
Text Label 4750 4350 0    50   ~ 0
ROM_2_5
Text Label 4750 4450 0    50   ~ 0
ROM_2_6
Text Label 4750 4550 0    50   ~ 0
ROM_2_7
Text Label 2450 3850 0    50   ~ 0
ROM_3_0
Text Label 2450 3950 0    50   ~ 0
ROM_3_1
Text Label 2450 4050 0    50   ~ 0
ROM_3_2
Text Label 2450 4150 0    50   ~ 0
ROM_3_3
Text Label 2450 4250 0    50   ~ 0
ROM_3_4
Text Label 2450 4350 0    50   ~ 0
ROM_3_5
Text Label 2450 4450 0    50   ~ 0
ROM_3_6
Text Label 2450 4550 0    50   ~ 0
ROM_3_7
Text Label 6050 7350 1    50   ~ 0
ROM_0_0
Text Label 5950 7350 1    50   ~ 0
ROM_0_1
Text Label 5850 7350 1    50   ~ 0
ROM_0_2
Text Label 5750 7350 1    50   ~ 0
ROM_0_3
Text Label 5650 7350 1    50   ~ 0
ROM_0_4
Text Label 5550 7350 1    50   ~ 0
ROM_0_5
Text Label 5450 7350 1    50   ~ 0
ROM_0_6
Text Label 5350 7350 1    50   ~ 0
ROM_0_7
Entry Wire Line
	5950 6900 6050 7000
Entry Wire Line
	5850 6900 5950 7000
Entry Wire Line
	5750 6900 5850 7000
Entry Wire Line
	5650 6900 5750 7000
Entry Wire Line
	5550 6900 5650 7000
Entry Wire Line
	5450 6900 5550 7000
Entry Wire Line
	5350 6900 5450 7000
Entry Wire Line
	5250 6900 5350 7000
Text Label 5250 7350 1    50   ~ 0
ROM_1_0
Text Label 5150 7350 1    50   ~ 0
ROM_1_1
Text Label 5050 7350 1    50   ~ 0
ROM_1_2
Text Label 4950 7350 1    50   ~ 0
ROM_1_3
Text Label 4850 7350 1    50   ~ 0
ROM_1_4
Text Label 4750 7350 1    50   ~ 0
ROM_1_5
Text Label 4650 7350 1    50   ~ 0
ROM_1_6
Text Label 4550 7350 1    50   ~ 0
ROM_1_7
Text Label 4450 7350 1    50   ~ 0
ROM_2_0
Text Label 4350 7350 1    50   ~ 0
ROM_2_1
Text Label 4250 7350 1    50   ~ 0
ROM_2_2
Text Label 4150 7350 1    50   ~ 0
ROM_2_3
Text Label 4050 7350 1    50   ~ 0
ROM_2_4
Text Label 3950 7350 1    50   ~ 0
ROM_2_5
Text Label 3850 7350 1    50   ~ 0
ROM_2_6
Text Label 3750 7350 1    50   ~ 0
ROM_2_7
Text Label 3650 7350 1    50   ~ 0
ROM_3_0
Text Label 3550 7350 1    50   ~ 0
ROM_3_1
Text Label 3450 7350 1    50   ~ 0
ROM_3_2
Text Label 3350 7350 1    50   ~ 0
ROM_3_3
Text Label 3250 7350 1    50   ~ 0
ROM_3_4
Text Label 3150 7350 1    50   ~ 0
ROM_3_5
Text Label 3050 7350 1    50   ~ 0
ROM_3_6
Text Label 2950 7350 1    50   ~ 0
ROM_3_7
Entry Wire Line
	5150 6900 5250 7000
Entry Wire Line
	5050 6900 5150 7000
Entry Wire Line
	4950 6900 5050 7000
Entry Wire Line
	4850 6900 4950 7000
Entry Wire Line
	4750 6900 4850 7000
Entry Wire Line
	4650 6900 4750 7000
Entry Wire Line
	4550 6900 4650 7000
Entry Wire Line
	4450 6900 4550 7000
Entry Wire Line
	4350 6900 4450 7000
Entry Wire Line
	4250 6900 4350 7000
Entry Wire Line
	4150 6900 4250 7000
Entry Wire Line
	4050 6900 4150 7000
Entry Wire Line
	3950 6900 4050 7000
Entry Wire Line
	3850 6900 3950 7000
Entry Wire Line
	3750 6900 3850 7000
Entry Wire Line
	3650 6900 3750 7000
Entry Wire Line
	3550 6900 3650 7000
Entry Wire Line
	3450 6900 3550 7000
Entry Wire Line
	3350 6900 3450 7000
Entry Wire Line
	3250 6900 3350 7000
Entry Wire Line
	3150 6900 3250 7000
Entry Wire Line
	3050 6900 3150 7000
Entry Wire Line
	2950 6900 3050 7000
Entry Wire Line
	2850 6900 2950 7000
NoConn ~ 6050 1550
Text Label 2250 1600 3    50   ~ 0
MIR_INST_0
Text Label 2150 1600 3    50   ~ 0
MIR_INST_1
Text Label 2050 1600 3    50   ~ 0
MIR_INST_2
Text Label 1950 1600 3    50   ~ 0
MIR_INST_3
Text Label 1850 1600 3    50   ~ 0
MIR_INST_4
Text Label 1750 1600 3    50   ~ 0
MIR_INST_5
Text Label 1650 1600 3    50   ~ 0
MIR_INST_6
Text Label 1550 1600 3    50   ~ 0
MIR_INST_7
Entry Wire Line
	2250 2050 2350 2150
Entry Wire Line
	2150 2050 2250 2150
Entry Wire Line
	2050 2050 2150 2150
Entry Wire Line
	1950 2050 2050 2150
Entry Wire Line
	1850 2050 1950 2150
Entry Wire Line
	1750 2050 1850 2150
Entry Wire Line
	1650 2050 1750 2150
Entry Wire Line
	1550 2050 1650 2150
Text Label 4300 1600 3    50   ~ 0
MIR_FLAG_Z
Text Label 4200 1600 3    50   ~ 0
MIR_FLAG_N
Text Label 4100 1600 3    50   ~ 0
MIR_FLAG_C
Text Label 4000 1600 3    50   ~ 0
MIR_FLAG_E
Entry Wire Line
	4300 2050 4400 2150
Entry Wire Line
	4200 2050 4300 2150
Entry Wire Line
	4100 2050 4200 2150
Entry Wire Line
	4000 2050 4100 2150
Text Label 6350 1750 3    50   ~ 0
MC_STEP_0
Text Label 6250 1750 3    50   ~ 0
MC_STEP_1
Text Label 6150 1750 3    50   ~ 0
MC_STEP_2
Entry Wire Line
	6350 2200 6450 2300
Entry Wire Line
	6250 2200 6350 2300
Entry Wire Line
	6150 2200 6250 2300
Wire Wire Line
	9150 3850 9550 3850
Wire Wire Line
	9150 3950 9550 3950
Wire Wire Line
	9150 4050 9550 4050
Wire Wire Line
	9150 4150 9550 4150
Wire Wire Line
	9150 4250 9550 4250
Wire Wire Line
	9550 4350 9150 4350
Wire Wire Line
	9150 4450 9550 4450
Wire Wire Line
	9150 4550 9550 4550
Wire Wire Line
	7850 3850 8350 3850
Wire Wire Line
	7850 3950 8350 3950
Wire Wire Line
	7850 4050 8350 4050
Wire Wire Line
	7850 4150 8350 4150
Wire Wire Line
	7850 4250 8350 4250
Wire Wire Line
	7850 4350 8350 4350
Wire Wire Line
	7850 4450 8350 4450
Wire Wire Line
	7850 4550 8350 4550
Wire Wire Line
	7850 4650 8350 4650
Wire Wire Line
	7850 4750 8350 4750
Wire Wire Line
	7850 4850 8350 4850
Wire Wire Line
	7850 4950 8350 4950
Wire Wire Line
	7850 5050 8350 5050
Wire Wire Line
	7850 5150 8350 5150
Wire Wire Line
	7850 5250 8350 5250
Entry Wire Line
	7400 3850 7500 3950
Entry Wire Line
	7400 3950 7500 4050
Entry Wire Line
	7400 4050 7500 4150
Entry Wire Line
	7400 4150 7500 4250
Entry Wire Line
	7400 4250 7500 4350
Entry Wire Line
	7400 4350 7500 4450
Entry Wire Line
	7400 4450 7500 4550
Entry Wire Line
	7400 4550 7500 4650
Entry Wire Line
	2850 3850 2950 3950
Entry Wire Line
	2850 3950 2950 4050
Entry Wire Line
	2850 4050 2950 4150
Entry Wire Line
	2850 4150 2950 4250
Entry Wire Line
	2850 4250 2950 4350
Entry Wire Line
	2850 4350 2950 4450
Entry Wire Line
	2850 4450 2950 4550
Entry Wire Line
	2850 4550 2950 4650
Wire Wire Line
	2400 3850 2850 3850
Wire Wire Line
	2400 3950 2850 3950
Wire Wire Line
	2400 4050 2850 4050
Wire Wire Line
	2400 4150 2850 4150
Wire Wire Line
	2400 4250 2850 4250
Wire Wire Line
	2400 4350 2850 4350
Wire Wire Line
	2400 4450 2850 4450
Wire Wire Line
	2400 4550 2850 4550
Text Label 1500 3850 2    50   ~ 0
MC_STEP_0
Entry Wire Line
	950  3750 1050 3850
Entry Wire Line
	950  3850 1050 3950
Entry Wire Line
	950  3950 1050 4050
Entry Wire Line
	950  4050 1050 4150
Entry Wire Line
	950  4150 1050 4250
Entry Wire Line
	950  4250 1050 4350
Entry Wire Line
	950  4350 1050 4450
Entry Wire Line
	950  4450 1050 4550
Entry Wire Line
	950  4550 1050 4650
Entry Wire Line
	950  4650 1050 4750
Entry Wire Line
	950  4750 1050 4850
Entry Wire Line
	950  4850 1050 4950
Entry Wire Line
	950  4950 1050 5050
Entry Wire Line
	950  5050 1050 5150
Entry Wire Line
	950  5150 1050 5250
Text Label 1500 3950 2    50   ~ 0
MC_STEP_1
Text Label 1500 4050 2    50   ~ 0
MC_STEP_2
Text Label 1500 4150 2    50   ~ 0
MIR_FLAG_Z
Text Label 1500 4250 2    50   ~ 0
MIR_FLAG_N
Text Label 1500 4350 2    50   ~ 0
MIR_FLAG_C
Text Label 1500 4450 2    50   ~ 0
MIR_FLAG_E
Text Label 1500 4550 2    50   ~ 0
MIR_INST_0
Text Label 1500 4650 2    50   ~ 0
MIR_INST_1
Text Label 1500 4750 2    50   ~ 0
MIR_INST_2
Text Label 1500 4850 2    50   ~ 0
MIR_INST_3
Text Label 1500 4950 2    50   ~ 0
MIR_INST_4
Text Label 1500 5050 2    50   ~ 0
MIR_INST_5
Text Label 1500 5150 2    50   ~ 0
MIR_INST_6
Text Label 1500 5250 2    50   ~ 0
MIR_INST_7
Wire Wire Line
	1050 3850 1600 3850
Wire Wire Line
	1050 3950 1600 3950
Wire Wire Line
	1050 4050 1600 4050
Wire Wire Line
	1050 4150 1600 4150
Wire Wire Line
	1050 4250 1600 4250
Wire Wire Line
	1050 4350 1600 4350
Wire Wire Line
	1050 4450 1600 4450
Wire Wire Line
	1050 4550 1600 4550
Wire Wire Line
	1050 4650 1600 4650
Wire Wire Line
	1050 4750 1600 4750
Wire Wire Line
	1050 4850 1600 4850
Wire Wire Line
	1050 4950 1600 4950
Wire Wire Line
	1050 5050 1600 5050
Wire Wire Line
	1050 5150 1600 5150
Wire Wire Line
	1050 5250 1600 5250
Entry Wire Line
	5150 3850 5250 3950
Entry Wire Line
	5150 3950 5250 4050
Entry Wire Line
	5150 4050 5250 4150
Entry Wire Line
	5150 4150 5250 4250
Entry Wire Line
	5150 4250 5250 4350
Entry Wire Line
	5150 4350 5250 4450
Entry Wire Line
	5150 4450 5250 4550
Entry Wire Line
	5150 4550 5250 4650
Wire Wire Line
	4700 3850 5150 3850
Wire Wire Line
	4700 3950 5150 3950
Wire Wire Line
	4700 4050 5150 4050
Wire Wire Line
	4700 4150 5150 4150
Wire Wire Line
	4700 4250 5150 4250
Wire Wire Line
	4700 4350 5150 4350
Wire Wire Line
	4700 4450 5150 4450
Wire Wire Line
	4700 4550 5150 4550
Text Label 3750 3850 2    50   ~ 0
MC_STEP_0
Entry Wire Line
	3200 3750 3300 3850
Entry Wire Line
	3200 3850 3300 3950
Entry Wire Line
	3200 3950 3300 4050
Entry Wire Line
	3200 4050 3300 4150
Entry Wire Line
	3200 4150 3300 4250
Entry Wire Line
	3200 4250 3300 4350
Entry Wire Line
	3200 4350 3300 4450
Entry Wire Line
	3200 4450 3300 4550
Entry Wire Line
	3200 4550 3300 4650
Entry Wire Line
	3200 4650 3300 4750
Entry Wire Line
	3200 4750 3300 4850
Entry Wire Line
	3200 4850 3300 4950
Entry Wire Line
	3200 4950 3300 5050
Entry Wire Line
	3200 5050 3300 5150
Entry Wire Line
	3200 5150 3300 5250
Text Label 3750 3950 2    50   ~ 0
MC_STEP_1
Text Label 3750 4050 2    50   ~ 0
MC_STEP_2
Text Label 3750 4150 2    50   ~ 0
MIR_FLAG_Z
Text Label 3750 4250 2    50   ~ 0
MIR_FLAG_N
Text Label 3750 4350 2    50   ~ 0
MIR_FLAG_C
Text Label 3750 4450 2    50   ~ 0
MIR_FLAG_E
Text Label 3750 4550 2    50   ~ 0
MIR_INST_0
Text Label 3750 4650 2    50   ~ 0
MIR_INST_1
Text Label 3750 4750 2    50   ~ 0
MIR_INST_2
Text Label 3750 4850 2    50   ~ 0
MIR_INST_3
Text Label 3750 4950 2    50   ~ 0
MIR_INST_4
Text Label 3750 5050 2    50   ~ 0
MIR_INST_5
Text Label 3750 5150 2    50   ~ 0
MIR_INST_6
Text Label 3750 5250 2    50   ~ 0
MIR_INST_7
Wire Wire Line
	3300 3850 3900 3850
Wire Wire Line
	3300 3950 3900 3950
Wire Wire Line
	3300 4050 3900 4050
Wire Wire Line
	3300 4150 3900 4150
Wire Wire Line
	3300 4250 3900 4250
Wire Wire Line
	3300 4350 3900 4350
Wire Wire Line
	3300 4450 3900 4450
Wire Wire Line
	3300 4550 3900 4550
Wire Wire Line
	3300 4650 3900 4650
Wire Wire Line
	3300 4750 3900 4750
Wire Wire Line
	3300 4850 3900 4850
Wire Wire Line
	3300 4950 3900 4950
Wire Wire Line
	3300 5050 3900 5050
Wire Wire Line
	3300 5150 3900 5150
Wire Wire Line
	3300 5250 3900 5250
Wire Wire Line
	6950 4550 7400 4550
Wire Wire Line
	6950 4450 7400 4450
Wire Wire Line
	6950 4350 7400 4350
Wire Wire Line
	6950 4250 7400 4250
Wire Wire Line
	6950 4150 7400 4150
Wire Wire Line
	6950 4050 7400 4050
Wire Wire Line
	6950 3950 7400 3950
Wire Wire Line
	6950 3850 7400 3850
Wire Wire Line
	5600 5250 6150 5250
Wire Wire Line
	5600 5150 6150 5150
Wire Wire Line
	5600 5050 6150 5050
Wire Wire Line
	5600 4950 6150 4950
Wire Wire Line
	5600 4850 6150 4850
Wire Wire Line
	5600 4750 6150 4750
Wire Wire Line
	5600 4650 6150 4650
Wire Wire Line
	5600 4550 6150 4550
Wire Wire Line
	5600 4450 6150 4450
Wire Wire Line
	5600 4350 6150 4350
Wire Wire Line
	5600 4250 6150 4250
Wire Wire Line
	5600 4150 6150 4150
Wire Wire Line
	5600 4050 6150 4050
Wire Wire Line
	5600 3950 6150 3950
Wire Wire Line
	5600 3850 6150 3850
Text Label 6050 5250 2    50   ~ 0
MIR_INST_7
Text Label 6050 5150 2    50   ~ 0
MIR_INST_6
Text Label 6050 5050 2    50   ~ 0
MIR_INST_5
Text Label 6050 4950 2    50   ~ 0
MIR_INST_4
Text Label 6050 4850 2    50   ~ 0
MIR_INST_3
Text Label 6050 4750 2    50   ~ 0
MIR_INST_2
Text Label 6050 4650 2    50   ~ 0
MIR_INST_1
Text Label 6050 4550 2    50   ~ 0
MIR_INST_0
Text Label 6050 4450 2    50   ~ 0
MIR_FLAG_E
Text Label 6050 4350 2    50   ~ 0
MIR_FLAG_C
Text Label 6050 4250 2    50   ~ 0
MIR_FLAG_N
Text Label 6050 4150 2    50   ~ 0
MIR_FLAG_Z
Text Label 6050 4050 2    50   ~ 0
MC_STEP_2
Text Label 6050 3950 2    50   ~ 0
MC_STEP_1
Entry Wire Line
	5500 5150 5600 5250
Entry Wire Line
	5500 5050 5600 5150
Entry Wire Line
	5500 4950 5600 5050
Entry Wire Line
	5500 4850 5600 4950
Entry Wire Line
	5500 4750 5600 4850
Entry Wire Line
	5500 4650 5600 4750
Entry Wire Line
	5500 4550 5600 4650
Entry Wire Line
	5500 4450 5600 4550
Entry Wire Line
	5500 4350 5600 4450
Entry Wire Line
	5500 4250 5600 4350
Entry Wire Line
	5500 4150 5600 4250
Entry Wire Line
	5500 4050 5600 4150
Entry Wire Line
	5500 3950 5600 4050
Entry Wire Line
	5500 3850 5600 3950
Entry Wire Line
	5500 3750 5600 3850
Text Label 6050 3850 2    50   ~ 0
MC_STEP_0
Text Label 7000 4550 0    50   ~ 0
ROM_1_7
Text Label 7000 4450 0    50   ~ 0
ROM_1_6
Text Label 7000 4350 0    50   ~ 0
ROM_1_5
Text Label 7000 4250 0    50   ~ 0
ROM_1_4
Text Label 7000 4150 0    50   ~ 0
ROM_1_3
Text Label 7000 4050 0    50   ~ 0
ROM_1_2
Text Label 7000 3950 0    50   ~ 0
ROM_1_1
Text Label 7000 3850 0    50   ~ 0
ROM_1_0
$Comp
L Memory_EEPROM:28C256 U2
U 1 1 5E13F5AB
P 6550 4750
F 0 "U2" H 6550 6031 50  0000 C CNN
F 1 "28C256" H 6550 5940 50  0000 C CNN
F 2 "Package_DIP:DIP-28_W15.24mm_Socket" H 6550 4750 50  0001 C CNN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/doc0006.pdf" H 6550 4750 50  0001 C CNN
	1    6550 4750
	1    0    0    -1  
$EndComp
Wire Wire Line
	6250 1550 6250 1650
Wire Wire Line
	6150 1550 6150 1700
Wire Wire Line
	6350 1600 7100 1600
Wire Wire Line
	6250 1650 7100 1650
Wire Wire Line
	6150 1700 7100 1700
Wire Wire Line
	6350 1550 6350 1600
Connection ~ 6350 1600
Connection ~ 6250 1650
Connection ~ 6150 1700
Wire Wire Line
	6350 1600 6350 2200
Wire Wire Line
	6250 1650 6250 2200
Wire Wire Line
	6150 1700 6150 2200
Wire Wire Line
	4000 1550 4000 2050
Wire Wire Line
	4100 2050 4100 1550
Wire Wire Line
	4200 2050 4200 1550
Wire Wire Line
	4300 2050 4300 1550
Wire Wire Line
	2250 1550 2250 2050
Wire Wire Line
	2150 2050 2150 1550
Wire Wire Line
	2050 1550 2050 2050
Wire Wire Line
	1950 2050 1950 1550
Wire Wire Line
	1850 1550 1850 2050
Wire Wire Line
	1750 2050 1750 1550
Wire Wire Line
	1650 1550 1650 2050
Wire Wire Line
	1550 2050 1550 1550
Wire Wire Line
	6050 7000 6050 7450
Wire Wire Line
	5950 7000 5950 7450
Wire Wire Line
	5850 7000 5850 7450
Wire Wire Line
	5750 7000 5750 7450
Wire Wire Line
	5650 7000 5650 7450
Wire Wire Line
	5550 7000 5550 7450
Wire Wire Line
	5450 7000 5450 7450
Wire Wire Line
	5350 7000 5350 7450
Wire Wire Line
	5250 7000 5250 7450
Wire Wire Line
	5150 7000 5150 7450
Wire Wire Line
	5050 7000 5050 7450
Wire Wire Line
	4950 7000 4950 7450
Wire Wire Line
	4850 7000 4850 7450
Wire Wire Line
	4750 7000 4750 7450
Wire Wire Line
	4650 7000 4650 7450
Wire Wire Line
	4550 7000 4550 7450
Wire Wire Line
	4450 7000 4450 7450
Wire Wire Line
	4350 7000 4350 7450
Wire Wire Line
	4250 7000 4250 7450
Wire Wire Line
	4150 7000 4150 7450
Wire Wire Line
	4050 7000 4050 7450
Wire Wire Line
	3950 7000 3950 7450
Wire Wire Line
	3850 7000 3850 7450
Wire Wire Line
	3750 7000 3750 7450
Wire Wire Line
	3650 7000 3650 7450
Wire Wire Line
	3550 7000 3550 7450
Wire Wire Line
	3450 7000 3450 7450
Wire Wire Line
	3350 7000 3350 7450
Wire Wire Line
	3250 7000 3250 7450
Wire Wire Line
	3150 7000 3150 7450
Wire Wire Line
	3050 7000 3050 7450
Wire Wire Line
	2950 7000 2950 7450
Wire Bus Line
	9650 6700 5950 6700
Wire Bus Line
	5950 6700 5950 6900
Wire Bus Line
	7500 6650 5150 6650
Wire Bus Line
	5150 6650 5150 6900
Wire Bus Line
	5250 6600 4350 6600
Wire Bus Line
	4350 6600 4350 6900
Wire Bus Line
	2850 6900 2950 6900
Connection ~ 2950 6900
Wire Bus Line
	4400 2300 4400 2150
Wire Bus Line
	950  3400 3200 3400
Connection ~ 5500 3400
Wire Bus Line
	5500 3400 7750 3400
Connection ~ 3200 3400
Wire Bus Line
	3200 3400 5500 3400
Wire Bus Line
	950  3400 950  2150
Wire Bus Line
	4400 2300 6450 2300
Wire Bus Line
	5250 6900 5950 6900
Wire Bus Line
	4450 6900 5150 6900
Wire Bus Line
	3650 6900 4350 6900
Wire Bus Line
	2950 6900 3550 6900
Wire Bus Line
	9650 3950 9650 6700
Wire Bus Line
	7500 3950 7500 6650
Wire Bus Line
	5250 3950 5250 6600
Wire Bus Line
	2950 3950 2950 6900
Wire Bus Line
	7750 3400 7750 5150
Wire Bus Line
	950  2150 4400 2150
Wire Bus Line
	950  3400 950  5150
Wire Bus Line
	3200 3400 3200 5150
Wire Bus Line
	5500 3400 5500 5150
Connection ~ 950  3400
$EndSCHEMATC
