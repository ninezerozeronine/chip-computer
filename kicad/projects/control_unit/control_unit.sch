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
P 4300 5400
F 0 "U3" H 4300 6681 50  0000 C CNN
F 1 "28C256" H 4300 6590 50  0000 C CNN
F 2 "Package_DIP:DIP-28_W15.24mm_Socket" H 4300 5400 50  0001 C CNN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/doc0006.pdf" H 4300 5400 50  0001 C CNN
	1    4300 5400
	1    0    0    -1  
$EndComp
$Comp
L Memory_EEPROM:28C256 U4
U 1 1 5E140592
P 2000 5400
F 0 "U4" H 2000 6681 50  0000 C CNN
F 1 "28C256" H 2000 6590 50  0000 C CNN
F 2 "Package_DIP:DIP-28_W15.24mm_Socket" H 2000 5400 50  0001 C CNN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/doc0006.pdf" H 2000 5400 50  0001 C CNN
	1    2000 5400
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x08_Female J7
U 1 1 5E25048F
P 4600 2250
F 0 "J7" V 4800 2200 50  0000 L CNN
F 1 "Conn_01x08_Female" V 4700 1850 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Horizontal" H 4600 2250 50  0001 C CNN
F 3 "~" H 4600 2250 50  0001 C CNN
	1    4600 2250
	0    1    -1   0   
$EndComp
$Comp
L Connector:Conn_01x16_Female J5
U 1 1 5E251504
P 3100 2000
F 0 "J5" V 3300 1900 50  0000 L CNN
F 1 "Conn_01x16_Female" V 3200 1550 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x16_P2.54mm_Horizontal" H 3100 2000 50  0001 C CNN
F 3 "~" H 3100 2000 50  0001 C CNN
	1    3100 2000
	0    1    -1   0   
$EndComp
$Comp
L Connector:Conn_01x04_Female J2
U 1 1 5E25238A
P 5200 750
F 0 "J2" V 5250 750 50  0000 L CNN
F 1 "Conn_01x04_Female" V 5350 450 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x04_P2.54mm_Horizontal" H 5200 750 50  0001 C CNN
F 3 "~" H 5200 750 50  0001 C CNN
	1    5200 750 
	0    1    -1   0   
$EndComp
$Comp
L Connector:Conn_01x08_Female J3
U 1 1 5E253BE4
P 1800 850
F 0 "J3" V 1850 750 50  0000 L CNN
F 1 "Conn_01x08_Female" V 1950 450 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Horizontal" H 1800 850 50  0001 C CNN
F 3 "~" H 1800 850 50  0001 C CNN
	1    1800 850 
	0    1    -1   0   
$EndComp
$Comp
L Connector:Conn_01x16_Female J6
U 1 1 5E2549B9
P 9500 2300
F 0 "J6" V 9550 2100 50  0000 L CNN
F 1 "Conn_01x16_Female" V 9650 1800 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x16_P2.54mm_Horizontal" H 9500 2300 50  0001 C CNN
F 3 "~" H 9500 2300 50  0001 C CNN
	1    9500 2300
	0    1    -1   0   
$EndComp
$Comp
L Connector:Conn_01x34_Male J4
U 1 1 5E25780B
P 4450 7650
F 0 "J4" V 4350 7650 50  0000 C CNN
F 1 "Conn_01x34_Male" V 4250 7650 50  0000 C CNN
F 2 "eight-bit-computer:backplane-connector" H 4450 7650 50  0001 C CNN
F 3 "~" H 4450 7650 50  0001 C CNN
	1    4450 7650
	0    1    -1   0   
$EndComp
$Comp
L eight-bit-computer:74HCT377 U5
U 1 1 5E2645FB
P 1600 1550
F 0 "U5" V 2100 1050 50  0000 C CNN
F 1 "74HCT377" V 2000 1050 50  0000 C CNN
F 2 "Package_DIP:DIP-20_W7.62mm_Socket" H 1600 1550 50  0001 C CNN
F 3 "http://www.ti.com/lit/gpn/sn74LS377" H 1600 1550 50  0001 C CNN
	1    1600 1550
	0    1    1    0   
$EndComp
$Comp
L eight-bit-computer:74HCT173 U7
U 1 1 5E268A7A
P 4700 1450
F 0 "U7" V 4550 400 50  0000 L CNN
F 1 "74HCT173" V 4450 250 50  0000 L CNN
F 2 "Package_DIP:DIP-16_W7.62mm_Socket" H 4700 1450 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/cd74hc173.pdf" H 4700 1450 50  0001 C CNN
	1    4700 1450
	0    1    1    0   
$EndComp
$Comp
L 74xx:74HCT04 U9
U 1 1 5E26993C
P 6100 1300
F 0 "U9" V 6150 1000 50  0000 C CNN
F 1 "74HCT04" V 6050 1000 50  0000 C CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket" H 6100 1300 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 6100 1300 50  0001 C CNN
	1    6100 1300
	0    1    1    0   
$EndComp
$Comp
L 74xx:74HCT04 U9
U 2 1 5E26A77F
P 6600 1300
F 0 "U9" V 6650 1550 50  0000 C CNN
F 1 "74HCT04" V 6550 1600 50  0000 C CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket" H 6600 1300 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 6600 1300 50  0001 C CNN
	2    6600 1300
	0    1    1    0   
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
P 6600 2100
F 0 "U6" V 7100 1500 50  0000 L CNN
F 1 "74HCT161" V 7000 1500 50  0000 L CNN
F 2 "Package_DIP:DIP-16_W7.62mm_Socket" H 6600 2100 50  0001 C CNN
F 3 "https://www.ti.com/lit/ds/symlink/cd54hc163.pdf" H 6600 2100 50  0001 C CNN
	1    6600 2100
	0    1    1    0   
$EndComp
$Comp
L eight-bit-computer:74HCT138 U8
U 1 1 5E2791CC
P 8050 2900
F 0 "U8" H 7650 2200 50  0000 R CNN
F 1 "74HCT138" H 7800 2300 50  0000 R CNN
F 2 "Package_DIP:DIP-16_W7.62mm_Socket" H 8050 2900 50  0001 C CNN
F 3 "https://www.ti.com/lit/ds/symlink/sn74hct138.pdf" H 8050 2900 50  0001 C CNN
	1    8050 2900
	1    0    0    -1  
$EndComp
$Comp
L Memory_EEPROM:28C256 U1
U 1 1 5E13E2C4
P 8750 5400
F 0 "U1" H 8750 6681 50  0000 C CNN
F 1 "28C256" H 8750 6590 50  0000 C CNN
F 2 "Package_DIP:DIP-28_W15.24mm_Socket" H 8750 5400 50  0001 C CNN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/doc0006.pdf" H 8750 5400 50  0001 C CNN
	1    8750 5400
	1    0    0    -1  
$EndComp
Text Label 8300 4500 2    50   ~ 0
MC_STEP_0
Entry Wire Line
	7750 4400 7850 4500
Entry Wire Line
	7750 4500 7850 4600
Entry Wire Line
	7750 4600 7850 4700
Entry Wire Line
	7750 4700 7850 4800
Entry Wire Line
	7750 4800 7850 4900
Entry Wire Line
	7750 4900 7850 5000
Entry Wire Line
	7750 5000 7850 5100
Entry Wire Line
	7750 5100 7850 5200
Entry Wire Line
	7750 5200 7850 5300
Entry Wire Line
	7750 5300 7850 5400
Entry Wire Line
	7750 5400 7850 5500
Entry Wire Line
	7750 5500 7850 5600
Entry Wire Line
	7750 5600 7850 5700
Entry Wire Line
	7750 5700 7850 5800
Entry Wire Line
	7750 5800 7850 5900
Text Label 8300 4600 2    50   ~ 0
MC_STEP_1
Text Label 8300 4700 2    50   ~ 0
MC_STEP_2
Text Label 8300 4800 2    50   ~ 0
MIR_FLAG_Z
Text Label 8300 4900 2    50   ~ 0
MIR_FLAG_N
Text Label 8300 5000 2    50   ~ 0
MIR_FLAG_C
Text Label 8300 5100 2    50   ~ 0
MIR_FLAG_E
Text Label 8300 5200 2    50   ~ 0
MIR_INST_0
Text Label 8300 5300 2    50   ~ 0
MIR_INST_1
Text Label 8300 5400 2    50   ~ 0
MIR_INST_2
Text Label 8300 5500 2    50   ~ 0
MIR_INST_3
Text Label 8300 5600 2    50   ~ 0
MIR_INST_4
Text Label 8300 5700 2    50   ~ 0
MIR_INST_5
Text Label 8300 5800 2    50   ~ 0
MIR_INST_6
Text Label 8300 5900 2    50   ~ 0
MIR_INST_7
Entry Wire Line
	9550 4500 9650 4600
Entry Wire Line
	9550 4600 9650 4700
Entry Wire Line
	9550 4700 9650 4800
Entry Wire Line
	9550 4800 9650 4900
Entry Wire Line
	9550 4900 9650 5000
Entry Wire Line
	9550 5000 9650 5100
Entry Wire Line
	9550 5100 9650 5200
Entry Wire Line
	9550 5200 9650 5300
Text Label 9200 4500 0    50   ~ 0
ROM_0_0
Text Label 9200 4600 0    50   ~ 0
ROM_0_1
Text Label 9200 4700 0    50   ~ 0
ROM_0_2
Text Label 9200 4800 0    50   ~ 0
ROM_0_3
Text Label 9200 4900 0    50   ~ 0
ROM_0_4
Text Label 9200 5000 0    50   ~ 0
ROM_0_5
Text Label 9200 5100 0    50   ~ 0
ROM_0_6
Text Label 9200 5200 0    50   ~ 0
ROM_0_7
$Comp
L Device:R_Network08_US RN1
U 1 1 5E2EBA2A
P 2600 3300
F 0 "RN1" H 2550 3650 50  0000 L CNN
F 1 "R_Network08_US" H 2300 3550 50  0000 L CNN
F 2 "Resistor_THT:R_Array_SIP9" V 3075 3300 50  0001 C CNN
F 3 "http://www.vishay.com/docs/31509/csc.pdf" H 2600 3300 50  0001 C CNN
	1    2600 3300
	-1   0    0    1   
$EndComp
$Comp
L Device:R_Network08_US RN2
U 1 1 5E2EC96E
P 9700 3850
F 0 "RN2" H 9600 4150 50  0000 L CNN
F 1 "R_Network08_US" H 9400 4050 50  0000 L CNN
F 2 "Resistor_THT:R_Array_SIP9" V 10175 3850 50  0001 C CNN
F 3 "http://www.vishay.com/docs/31509/csc.pdf" H 9700 3850 50  0001 C CNN
	1    9700 3850
	-1   0    0    1   
$EndComp
$Comp
L Device:R_Network04_US RN3
U 1 1 5E2ED15F
P 4300 3250
F 0 "RN3" H 4488 3296 50  0000 L CNN
F 1 "R_Network04_US" H 4488 3205 50  0000 L CNN
F 2 "Resistor_THT:R_Array_SIP5" V 4575 3250 50  0001 C CNN
F 3 "http://www.vishay.com/docs/31509/csc.pdf" H 4300 3250 50  0001 C CNN
	1    4300 3250
	-1   0    0    1   
$EndComp
Text Label 4750 4500 0    50   ~ 0
ROM_2_0
Text Label 4750 4600 0    50   ~ 0
ROM_2_1
Text Label 4750 4700 0    50   ~ 0
ROM_2_2
Text Label 4750 4800 0    50   ~ 0
ROM_2_3
Text Label 4750 4900 0    50   ~ 0
ROM_2_4
Text Label 4750 5000 0    50   ~ 0
ROM_2_5
Text Label 4750 5100 0    50   ~ 0
ROM_2_6
Text Label 4750 5200 0    50   ~ 0
ROM_2_7
Text Label 2450 4500 0    50   ~ 0
ROM_3_0
Text Label 2450 4600 0    50   ~ 0
ROM_3_1
Text Label 2450 4700 0    50   ~ 0
ROM_3_2
Text Label 2450 4800 0    50   ~ 0
ROM_3_3
Text Label 2450 4900 0    50   ~ 0
ROM_3_4
Text Label 2450 5000 0    50   ~ 0
ROM_3_5
Text Label 2450 5100 0    50   ~ 0
ROM_3_6
Text Label 2450 5200 0    50   ~ 0
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
NoConn ~ 6800 2600
Text Label 2100 3300 3    50   ~ 0
MIR_INST_0
Text Label 2000 3300 3    50   ~ 0
MIR_INST_1
Text Label 1900 3300 3    50   ~ 0
MIR_INST_2
Text Label 1800 3300 3    50   ~ 0
MIR_INST_3
Text Label 1700 3300 3    50   ~ 0
MIR_INST_4
Text Label 1600 3300 3    50   ~ 0
MIR_INST_5
Text Label 1500 3300 3    50   ~ 0
MIR_INST_6
Text Label 1400 3300 3    50   ~ 0
MIR_INST_7
Entry Wire Line
	2100 3750 2200 3850
Entry Wire Line
	2000 3750 2100 3850
Entry Wire Line
	1900 3750 2000 3850
Entry Wire Line
	1800 3750 1900 3850
Entry Wire Line
	1700 3750 1800 3850
Entry Wire Line
	1600 3750 1700 3850
Entry Wire Line
	1500 3750 1600 3850
Entry Wire Line
	1400 3750 1500 3850
Text Label 5300 3300 3    50   ~ 0
MIR_FLAG_Z
Text Label 5200 3300 3    50   ~ 0
MIR_FLAG_N
Text Label 5100 3300 3    50   ~ 0
MIR_FLAG_C
Text Label 5000 3300 3    50   ~ 0
MIR_FLAG_E
Entry Wire Line
	5300 3750 5400 3850
Entry Wire Line
	5200 3750 5300 3850
Entry Wire Line
	5100 3750 5200 3850
Entry Wire Line
	5000 3750 5100 3850
Text Label 7100 3300 3    50   ~ 0
MC_STEP_0
Text Label 7000 3300 3    50   ~ 0
MC_STEP_1
Text Label 6900 3300 3    50   ~ 0
MC_STEP_2
Entry Wire Line
	7100 3750 7200 3850
Entry Wire Line
	7000 3750 7100 3850
Entry Wire Line
	6900 3750 7000 3850
Wire Wire Line
	9150 4500 9550 4500
Wire Wire Line
	9150 4600 9550 4600
Wire Wire Line
	9150 4700 9550 4700
Wire Wire Line
	9150 4800 9550 4800
Wire Wire Line
	9150 4900 9550 4900
Wire Wire Line
	9550 5000 9150 5000
Wire Wire Line
	9150 5100 9550 5100
Wire Wire Line
	9150 5200 9550 5200
Wire Wire Line
	7850 4500 8350 4500
Wire Wire Line
	7850 4600 8350 4600
Wire Wire Line
	7850 4700 8350 4700
Wire Wire Line
	7850 4800 8350 4800
Wire Wire Line
	7850 4900 8350 4900
Wire Wire Line
	7850 5000 8350 5000
Wire Wire Line
	7850 5100 8350 5100
Wire Wire Line
	7850 5200 8350 5200
Wire Wire Line
	7850 5300 8350 5300
Wire Wire Line
	7850 5400 8350 5400
Wire Wire Line
	7850 5500 8350 5500
Wire Wire Line
	7850 5600 8350 5600
Wire Wire Line
	7850 5700 8350 5700
Wire Wire Line
	7850 5800 8350 5800
Wire Wire Line
	7850 5900 8350 5900
Entry Wire Line
	7400 4500 7500 4600
Entry Wire Line
	7400 4600 7500 4700
Entry Wire Line
	7400 4700 7500 4800
Entry Wire Line
	7400 4800 7500 4900
Entry Wire Line
	7400 4900 7500 5000
Entry Wire Line
	7400 5000 7500 5100
Entry Wire Line
	7400 5100 7500 5200
Entry Wire Line
	7400 5200 7500 5300
Entry Wire Line
	2850 4500 2950 4600
Entry Wire Line
	2850 4600 2950 4700
Entry Wire Line
	2850 4700 2950 4800
Entry Wire Line
	2850 4800 2950 4900
Entry Wire Line
	2850 4900 2950 5000
Entry Wire Line
	2850 5000 2950 5100
Entry Wire Line
	2850 5100 2950 5200
Entry Wire Line
	2850 5200 2950 5300
Wire Wire Line
	2400 4500 2850 4500
Wire Wire Line
	2400 4600 2850 4600
Wire Wire Line
	2400 4700 2850 4700
Wire Wire Line
	2400 4800 2850 4800
Wire Wire Line
	2400 4900 2850 4900
Wire Wire Line
	2400 5000 2850 5000
Wire Wire Line
	2400 5100 2850 5100
Wire Wire Line
	2400 5200 2850 5200
Text Label 1500 4500 2    50   ~ 0
MC_STEP_0
Entry Wire Line
	950  4400 1050 4500
Entry Wire Line
	950  4500 1050 4600
Entry Wire Line
	950  4600 1050 4700
Entry Wire Line
	950  4700 1050 4800
Entry Wire Line
	950  4800 1050 4900
Entry Wire Line
	950  4900 1050 5000
Entry Wire Line
	950  5000 1050 5100
Entry Wire Line
	950  5100 1050 5200
Entry Wire Line
	950  5200 1050 5300
Entry Wire Line
	950  5300 1050 5400
Entry Wire Line
	950  5400 1050 5500
Entry Wire Line
	950  5500 1050 5600
Entry Wire Line
	950  5600 1050 5700
Entry Wire Line
	950  5700 1050 5800
Entry Wire Line
	950  5800 1050 5900
Text Label 1500 4600 2    50   ~ 0
MC_STEP_1
Text Label 1500 4700 2    50   ~ 0
MC_STEP_2
Text Label 1500 4800 2    50   ~ 0
MIR_FLAG_Z
Text Label 1500 4900 2    50   ~ 0
MIR_FLAG_N
Text Label 1500 5000 2    50   ~ 0
MIR_FLAG_C
Text Label 1500 5100 2    50   ~ 0
MIR_FLAG_E
Text Label 1500 5200 2    50   ~ 0
MIR_INST_0
Text Label 1500 5300 2    50   ~ 0
MIR_INST_1
Text Label 1500 5400 2    50   ~ 0
MIR_INST_2
Text Label 1500 5500 2    50   ~ 0
MIR_INST_3
Text Label 1500 5600 2    50   ~ 0
MIR_INST_4
Text Label 1500 5700 2    50   ~ 0
MIR_INST_5
Text Label 1500 5800 2    50   ~ 0
MIR_INST_6
Text Label 1500 5900 2    50   ~ 0
MIR_INST_7
Wire Wire Line
	1050 4500 1600 4500
Wire Wire Line
	1050 4600 1600 4600
Wire Wire Line
	1050 4700 1600 4700
Wire Wire Line
	1050 4800 1600 4800
Wire Wire Line
	1050 4900 1600 4900
Wire Wire Line
	1050 5000 1600 5000
Wire Wire Line
	1050 5100 1600 5100
Wire Wire Line
	1050 5200 1600 5200
Wire Wire Line
	1050 5300 1600 5300
Wire Wire Line
	1050 5400 1600 5400
Wire Wire Line
	1050 5500 1600 5500
Wire Wire Line
	1050 5600 1600 5600
Wire Wire Line
	1050 5700 1600 5700
Wire Wire Line
	1050 5800 1600 5800
Wire Wire Line
	1050 5900 1600 5900
Entry Wire Line
	5150 4500 5250 4600
Entry Wire Line
	5150 4600 5250 4700
Entry Wire Line
	5150 4700 5250 4800
Entry Wire Line
	5150 4800 5250 4900
Entry Wire Line
	5150 4900 5250 5000
Entry Wire Line
	5150 5000 5250 5100
Entry Wire Line
	5150 5100 5250 5200
Entry Wire Line
	5150 5200 5250 5300
Wire Wire Line
	4700 4500 5150 4500
Wire Wire Line
	4700 4600 5150 4600
Wire Wire Line
	4700 4700 5150 4700
Wire Wire Line
	4700 4800 5150 4800
Wire Wire Line
	4700 4900 5150 4900
Wire Wire Line
	4700 5000 5150 5000
Wire Wire Line
	4700 5100 5150 5100
Wire Wire Line
	4700 5200 5150 5200
Text Label 3750 4500 2    50   ~ 0
MC_STEP_0
Entry Wire Line
	3200 4400 3300 4500
Entry Wire Line
	3200 4500 3300 4600
Entry Wire Line
	3200 4600 3300 4700
Entry Wire Line
	3200 4700 3300 4800
Entry Wire Line
	3200 4800 3300 4900
Entry Wire Line
	3200 4900 3300 5000
Entry Wire Line
	3200 5000 3300 5100
Entry Wire Line
	3200 5100 3300 5200
Entry Wire Line
	3200 5200 3300 5300
Entry Wire Line
	3200 5300 3300 5400
Entry Wire Line
	3200 5400 3300 5500
Entry Wire Line
	3200 5500 3300 5600
Entry Wire Line
	3200 5600 3300 5700
Entry Wire Line
	3200 5700 3300 5800
Entry Wire Line
	3200 5800 3300 5900
Text Label 3750 4600 2    50   ~ 0
MC_STEP_1
Text Label 3750 4700 2    50   ~ 0
MC_STEP_2
Text Label 3750 4800 2    50   ~ 0
MIR_FLAG_Z
Text Label 3750 4900 2    50   ~ 0
MIR_FLAG_N
Text Label 3750 5000 2    50   ~ 0
MIR_FLAG_C
Text Label 3750 5100 2    50   ~ 0
MIR_FLAG_E
Text Label 3750 5200 2    50   ~ 0
MIR_INST_0
Text Label 3750 5300 2    50   ~ 0
MIR_INST_1
Text Label 3750 5400 2    50   ~ 0
MIR_INST_2
Text Label 3750 5500 2    50   ~ 0
MIR_INST_3
Text Label 3750 5600 2    50   ~ 0
MIR_INST_4
Text Label 3750 5700 2    50   ~ 0
MIR_INST_5
Text Label 3750 5800 2    50   ~ 0
MIR_INST_6
Text Label 3750 5900 2    50   ~ 0
MIR_INST_7
Wire Wire Line
	3300 4500 3900 4500
Wire Wire Line
	3300 4600 3900 4600
Wire Wire Line
	3300 4700 3900 4700
Wire Wire Line
	3300 4800 3900 4800
Wire Wire Line
	3300 4900 3900 4900
Wire Wire Line
	3300 5000 3900 5000
Wire Wire Line
	3300 5100 3900 5100
Wire Wire Line
	3300 5200 3900 5200
Wire Wire Line
	3300 5300 3900 5300
Wire Wire Line
	3300 5400 3900 5400
Wire Wire Line
	3300 5500 3900 5500
Wire Wire Line
	3300 5600 3900 5600
Wire Wire Line
	3300 5700 3900 5700
Wire Wire Line
	3300 5800 3900 5800
Wire Wire Line
	3300 5900 3900 5900
Wire Wire Line
	6950 5200 7400 5200
Wire Wire Line
	6950 5100 7400 5100
Wire Wire Line
	6950 5000 7400 5000
Wire Wire Line
	6950 4900 7400 4900
Wire Wire Line
	6950 4800 7400 4800
Wire Wire Line
	6950 4700 7400 4700
Wire Wire Line
	6950 4600 7400 4600
Wire Wire Line
	6950 4500 7400 4500
Wire Wire Line
	5600 5900 6150 5900
Wire Wire Line
	5600 5800 6150 5800
Wire Wire Line
	5600 5700 6150 5700
Wire Wire Line
	5600 5600 6150 5600
Wire Wire Line
	5600 5500 6150 5500
Wire Wire Line
	5600 5400 6150 5400
Wire Wire Line
	5600 5300 6150 5300
Wire Wire Line
	5600 5200 6150 5200
Wire Wire Line
	5600 5100 6150 5100
Wire Wire Line
	5600 5000 6150 5000
Wire Wire Line
	5600 4900 6150 4900
Wire Wire Line
	5600 4800 6150 4800
Wire Wire Line
	5600 4700 6150 4700
Wire Wire Line
	5600 4600 6150 4600
Wire Wire Line
	5600 4500 6150 4500
Text Label 6050 5900 2    50   ~ 0
MIR_INST_7
Text Label 6050 5800 2    50   ~ 0
MIR_INST_6
Text Label 6050 5700 2    50   ~ 0
MIR_INST_5
Text Label 6050 5600 2    50   ~ 0
MIR_INST_4
Text Label 6050 5500 2    50   ~ 0
MIR_INST_3
Text Label 6050 5400 2    50   ~ 0
MIR_INST_2
Text Label 6050 5300 2    50   ~ 0
MIR_INST_1
Text Label 6050 5200 2    50   ~ 0
MIR_INST_0
Text Label 6050 5100 2    50   ~ 0
MIR_FLAG_E
Text Label 6050 5000 2    50   ~ 0
MIR_FLAG_C
Text Label 6050 4900 2    50   ~ 0
MIR_FLAG_N
Text Label 6050 4800 2    50   ~ 0
MIR_FLAG_Z
Text Label 6050 4700 2    50   ~ 0
MC_STEP_2
Text Label 6050 4600 2    50   ~ 0
MC_STEP_1
Entry Wire Line
	5500 5800 5600 5900
Entry Wire Line
	5500 5700 5600 5800
Entry Wire Line
	5500 5600 5600 5700
Entry Wire Line
	5500 5500 5600 5600
Entry Wire Line
	5500 5400 5600 5500
Entry Wire Line
	5500 5300 5600 5400
Entry Wire Line
	5500 5200 5600 5300
Entry Wire Line
	5500 5100 5600 5200
Entry Wire Line
	5500 5000 5600 5100
Entry Wire Line
	5500 4900 5600 5000
Entry Wire Line
	5500 4800 5600 4900
Entry Wire Line
	5500 4700 5600 4800
Entry Wire Line
	5500 4600 5600 4700
Entry Wire Line
	5500 4500 5600 4600
Entry Wire Line
	5500 4400 5600 4500
Text Label 6050 4500 2    50   ~ 0
MC_STEP_0
Text Label 7000 5200 0    50   ~ 0
ROM_1_7
Text Label 7000 5100 0    50   ~ 0
ROM_1_6
Text Label 7000 5000 0    50   ~ 0
ROM_1_5
Text Label 7000 4900 0    50   ~ 0
ROM_1_4
Text Label 7000 4800 0    50   ~ 0
ROM_1_3
Text Label 7000 4700 0    50   ~ 0
ROM_1_2
Text Label 7000 4600 0    50   ~ 0
ROM_1_1
Text Label 7000 4500 0    50   ~ 0
ROM_1_0
$Comp
L Memory_EEPROM:28C256 U2
U 1 1 5E13F5AB
P 6550 5400
F 0 "U2" H 6550 6681 50  0000 C CNN
F 1 "28C256" H 6550 6590 50  0000 C CNN
F 2 "Package_DIP:DIP-28_W15.24mm_Socket" H 6550 5400 50  0001 C CNN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/doc0006.pdf" H 6550 5400 50  0001 C CNN
	1    6550 5400
	1    0    0    -1  
$EndComp
Wire Wire Line
	7000 2600 7000 2700
Wire Wire Line
	6900 2600 6900 2800
Wire Wire Line
	7100 2600 7550 2600
Wire Wire Line
	7000 2700 7550 2700
Wire Wire Line
	6900 2800 7550 2800
Connection ~ 7100 2600
Connection ~ 7000 2700
Connection ~ 6900 2800
Wire Wire Line
	7100 2600 7100 3750
Wire Wire Line
	7000 2700 7000 3750
Wire Wire Line
	6900 2800 6900 3750
Wire Wire Line
	5100 3750 5100 2600
Wire Wire Line
	5200 3750 5200 2550
Wire Wire Line
	5300 3750 5300 2500
Wire Wire Line
	2100 2050 2100 2250
Wire Wire Line
	2000 3750 2000 2300
Wire Wire Line
	1900 2050 1900 2350
Wire Wire Line
	1800 3750 1800 2400
Wire Wire Line
	1700 2050 1700 2450
Wire Wire Line
	1600 3750 1600 2500
Wire Wire Line
	1500 2050 1500 2550
Wire Wire Line
	1400 3750 1400 2600
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
	950  4050 3200 4050
Connection ~ 5500 4050
Wire Bus Line
	5500 4050 7750 4050
Connection ~ 3200 4050
Wire Bus Line
	3200 4050 5500 4050
Connection ~ 950  4050
$Comp
L power:GND #PWR02
U 1 1 5E43A29B
P 2000 6500
F 0 "#PWR02" H 2000 6250 50  0001 C CNN
F 1 "GND" H 2005 6327 50  0000 C CNN
F 2 "" H 2000 6500 50  0001 C CNN
F 3 "" H 2000 6500 50  0001 C CNN
	1    2000 6500
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR04
U 1 1 5E43C2C3
P 4300 6500
F 0 "#PWR04" H 4300 6250 50  0001 C CNN
F 1 "GND" V 4305 6372 50  0000 R CNN
F 2 "" H 4300 6500 50  0001 C CNN
F 3 "" H 4300 6500 50  0001 C CNN
	1    4300 6500
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR07
U 1 1 5E43D144
P 6550 6500
F 0 "#PWR07" H 6550 6250 50  0001 C CNN
F 1 "GND" V 6555 6372 50  0000 R CNN
F 2 "" H 6550 6500 50  0001 C CNN
F 3 "" H 6550 6500 50  0001 C CNN
	1    6550 6500
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR09
U 1 1 5E440B33
P 8750 6500
F 0 "#PWR09" H 8750 6250 50  0001 C CNN
F 1 "GND" V 8755 6372 50  0000 R CNN
F 2 "" H 8750 6500 50  0001 C CNN
F 3 "" H 8750 6500 50  0001 C CNN
	1    8750 6500
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR08
U 1 1 5E44B31E
P 7100 1600
F 0 "#PWR08" H 7100 1350 50  0001 C CNN
F 1 "GND" V 7105 1472 50  0000 R CNN
F 2 "" H 7100 1600 50  0001 C CNN
F 3 "" H 7100 1600 50  0001 C CNN
	1    7100 1600
	0    -1   -1   0   
$EndComp
Connection ~ 6900 1600
Wire Wire Line
	6900 1600 6800 1600
Connection ~ 7000 1600
Wire Wire Line
	7000 1600 6900 1600
Connection ~ 7100 1600
Wire Wire Line
	7100 1600 7000 1600
$Comp
L power:VCC #PWR06
U 1 1 5E457189
P 6400 1600
F 0 "#PWR06" H 6400 1450 50  0001 C CNN
F 1 "VCC" H 6417 1773 50  0000 C CNN
F 2 "" H 6400 1600 50  0001 C CNN
F 3 "" H 6400 1600 50  0001 C CNN
	1    6400 1600
	1    0    0    -1  
$EndComp
Wire Wire Line
	6400 1600 6500 1600
$Comp
L Connector:Conn_01x11_Male J1
U 1 1 5E46E5E4
P 1950 7650
F 0 "J1" V 1877 7628 50  0000 C CNN
F 1 "Conn_01x11_Male" V 1786 7628 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x11_P2.54mm_Horizontal" H 1950 7650 50  0001 C CNN
F 3 "~" H 1950 7650 50  0001 C CNN
	1    1950 7650
	0    1    -1   0   
$EndComp
NoConn ~ 6600 2600
Text Label 2750 7350 1    50   ~ 0
CONTROL_CLOCK
Wire Wire Line
	2750 7450 2750 7350
Text Label 1100 600  2    50   ~ 0
CONTROL_CLOCK
Wire Wire Line
	1100 600  1200 500 
Wire Wire Line
	1200 500  1200 1050
Wire Wire Line
	1200 500  4300 500 
Wire Wire Line
	4300 500  4300 950 
Connection ~ 1200 500 
Wire Wire Line
	4300 500  6300 500 
Wire Wire Line
	6300 500  6300 1600
Connection ~ 4300 500 
Text Label 1450 7350 1    50   ~ 0
MASTER_RESET
Wire Wire Line
	1450 7450 1450 7350
Text Label 6100 900  2    50   ~ 0
MASTER_RESET
Wire Wire Line
	6100 900  6100 1000
$Comp
L Connector:Conn_01x01_Female J8
U 1 1 5E54AF22
P 6600 800
F 0 "J8" V 6538 712 50  0000 R CNN
F 1 "Conn_01x01_Female" V 6447 712 50  0000 R CNN
F 2 "Connector_Wire:SolderWirePad_1x01_Drill0.8mm" H 6600 800 50  0001 C CNN
F 3 "~" H 6600 800 50  0001 C CNN
	1    6600 800 
	0    -1   -1   0   
$EndComp
Connection ~ 6400 1600
NoConn ~ 2850 7450
$Comp
L power:GND #PWR01
U 1 1 5E58C888
P 800 1050
F 0 "#PWR01" H 800 800 50  0001 C CNN
F 1 "GND" V 805 922 50  0000 R CNN
F 2 "" H 800 1050 50  0001 C CNN
F 3 "" H 800 1050 50  0001 C CNN
	1    800  1050
	0    1    1    0   
$EndComp
Wire Wire Line
	800  1550 800  1050
Wire Wire Line
	1100 1050 800  1050
Connection ~ 800  1050
Wire Wire Line
	3800 2200 3800 2250
Wire Wire Line
	3800 2250 2100 2250
Connection ~ 2100 2250
Wire Wire Line
	2100 2250 2100 3750
Wire Wire Line
	3600 2200 3600 2300
Connection ~ 2000 2300
Wire Wire Line
	2000 2300 2000 2050
Wire Wire Line
	3400 2200 3400 2350
Wire Wire Line
	3400 2350 1900 2350
Connection ~ 1900 2350
Wire Wire Line
	1900 2350 1900 3750
Wire Wire Line
	3200 2200 3200 2400
Wire Wire Line
	3200 2400 1800 2400
Connection ~ 1800 2400
Wire Wire Line
	1800 2400 1800 2050
Wire Wire Line
	3000 2200 3000 2450
Wire Wire Line
	3000 2450 1700 2450
Connection ~ 1700 2450
Wire Wire Line
	1700 2450 1700 3750
Wire Wire Line
	1600 2500 2800 2500
Wire Wire Line
	2800 2500 2800 2200
Connection ~ 1600 2500
Wire Wire Line
	1600 2500 1600 2050
Wire Wire Line
	2600 2200 2600 2550
Wire Wire Line
	2600 2550 1500 2550
Connection ~ 1500 2550
Wire Wire Line
	1500 2550 1500 3750
Wire Wire Line
	2400 2200 2400 2600
Wire Wire Line
	2400 2600 1400 2600
Connection ~ 1400 2600
Wire Wire Line
	1400 2600 1400 2050
Wire Wire Line
	3700 2200 3700 3100
Wire Wire Line
	3700 3100 3000 3100
Wire Wire Line
	2000 2300 3600 2300
Wire Wire Line
	3500 2200 3500 3050
Wire Wire Line
	2900 3050 2900 3100
Wire Wire Line
	3300 2200 3300 3000
Wire Wire Line
	3300 3000 2800 3000
Wire Wire Line
	2800 3000 2800 3100
Wire Wire Line
	3100 2200 3100 2950
Wire Wire Line
	3100 2950 2700 2950
Wire Wire Line
	2700 2950 2700 3100
Wire Wire Line
	2900 2200 2900 2900
Wire Wire Line
	2900 2900 2600 2900
Wire Wire Line
	2600 2900 2600 3100
Wire Wire Line
	2900 3050 3500 3050
Wire Wire Line
	2700 2200 2700 2850
Wire Wire Line
	2700 2850 2500 2850
Wire Wire Line
	2500 2850 2500 3100
Wire Wire Line
	2500 2200 2500 2800
Wire Wire Line
	2500 2800 2400 2800
Wire Wire Line
	2400 2800 2400 3100
Wire Wire Line
	2300 2200 2300 3100
Wire Wire Line
	4900 2450 4900 2500
Wire Wire Line
	4900 2500 5300 2500
Wire Wire Line
	5200 2550 4700 2550
Wire Wire Line
	4700 2550 4700 2450
Wire Wire Line
	5100 2600 4500 2600
Wire Wire Line
	4500 2600 4500 2450
Wire Wire Line
	5000 2650 4300 2650
Wire Wire Line
	4300 2650 4300 2450
Wire Wire Line
	4200 2450 4200 3050
Wire Wire Line
	4800 3050 4500 3050
Wire Wire Line
	4800 2450 4800 3050
Wire Wire Line
	4600 3000 4400 3000
Wire Wire Line
	4400 3000 4400 3050
Wire Wire Line
	4600 2450 4600 3000
Wire Wire Line
	4400 2950 4300 2950
Wire Wire Line
	4300 2950 4300 3050
Wire Wire Line
	4400 2450 4400 2950
Connection ~ 5000 2650
Wire Wire Line
	5000 2650 5000 3750
Connection ~ 5100 2600
Connection ~ 5200 2550
Connection ~ 5300 2500
Wire Wire Line
	5000 1950 5000 2650
Wire Wire Line
	5300 1950 5300 2500
Wire Wire Line
	5200 1950 5200 2550
Wire Wire Line
	5100 1950 5100 2600
Wire Bus Line
	950  4050 950  3850
Wire Wire Line
	8550 2600 10200 2600
Wire Wire Line
	10200 2600 10200 2500
Wire Wire Line
	8550 2700 10000 2700
Wire Wire Line
	10000 2700 10000 2500
Wire Wire Line
	8550 2800 9800 2800
Wire Wire Line
	9800 2800 9800 2500
Wire Wire Line
	8550 2900 9600 2900
Wire Wire Line
	9600 2900 9600 2500
Wire Wire Line
	8550 3000 9400 3000
Wire Wire Line
	9400 3000 9400 2500
Wire Wire Line
	9200 2500 9200 3100
Wire Wire Line
	9200 3100 8550 3100
Wire Wire Line
	8550 3200 9000 3200
Wire Wire Line
	9000 3200 9000 2500
Wire Wire Line
	8800 2500 8800 3300
Wire Wire Line
	8800 3300 8550 3300
Wire Wire Line
	10100 2500 10100 3650
Wire Wire Line
	9900 2500 9900 2950
Wire Wire Line
	9900 2950 10000 2950
Wire Wire Line
	10000 2950 10000 3650
Wire Wire Line
	9700 2500 9700 3000
Wire Wire Line
	9700 3000 9900 3000
Wire Wire Line
	9900 3000 9900 3650
Wire Wire Line
	9800 3650 9800 3100
Wire Wire Line
	9800 3100 9500 3100
Wire Wire Line
	9500 3100 9500 2500
Wire Wire Line
	9300 2500 9300 3200
Wire Wire Line
	9300 3200 9700 3200
Wire Wire Line
	9700 3200 9700 3650
Wire Wire Line
	9600 3650 9600 3300
Wire Wire Line
	9600 3300 9100 3300
Wire Wire Line
	9100 3300 9100 2500
Wire Wire Line
	8900 2500 8900 3400
Wire Wire Line
	8900 3400 9500 3400
Wire Wire Line
	9500 3400 9500 3650
Wire Wire Line
	9400 3650 9400 3500
Wire Wire Line
	9400 3500 8700 3500
Wire Wire Line
	8700 3500 8700 2500
$Comp
L power:GND #PWR03
U 1 1 5EF04E27
P 4100 950
F 0 "#PWR03" H 4100 700 50  0001 C CNN
F 1 "GND" H 4200 800 50  0000 R CNN
F 2 "" H 4100 950 50  0001 C CNN
F 3 "" H 4100 950 50  0001 C CNN
	1    4100 950 
	-1   0    0    1   
$EndComp
$Comp
L power:GND #PWR05
U 1 1 5EF05A4B
P 4800 950
F 0 "#PWR05" H 4800 700 50  0001 C CNN
F 1 "GND" H 4900 800 50  0000 R CNN
F 2 "" H 4800 950 50  0001 C CNN
F 3 "" H 4800 950 50  0001 C CNN
	1    4800 950 
	-1   0    0    1   
$EndComp
Wire Wire Line
	4400 950  4500 950 
Connection ~ 4800 950 
Connection ~ 4500 950 
Wire Wire Line
	4500 950  4700 950 
Connection ~ 4700 950 
Wire Wire Line
	4700 950  4800 950 
Wire Wire Line
	2000 6500 1600 6500
Wire Wire Line
	1600 6500 1600 6300
Connection ~ 1600 6300
Wire Wire Line
	1600 6300 1600 6200
Connection ~ 2000 6500
Wire Wire Line
	4300 6500 3900 6500
Wire Wire Line
	3900 6500 3900 6300
Connection ~ 4300 6500
Connection ~ 3900 6300
Wire Wire Line
	3900 6300 3900 6200
Wire Wire Line
	6550 6500 6150 6500
Wire Wire Line
	6150 6500 6150 6300
Connection ~ 6550 6500
Connection ~ 6150 6300
Wire Wire Line
	6150 6300 6150 6200
Wire Bus Line
	5250 6900 5950 6900
Wire Bus Line
	4450 6900 5150 6900
Wire Bus Line
	3650 6900 4350 6900
Wire Bus Line
	2950 6900 3550 6900
Wire Bus Line
	5250 4600 5250 6600
Wire Bus Line
	2950 4600 2950 6900
Wire Bus Line
	7500 4600 7500 6650
Wire Bus Line
	9650 4600 9650 6700
Wire Bus Line
	7750 4050 7750 5800
Wire Bus Line
	950  3850 7200 3850
Wire Bus Line
	950  4050 950  5800
Wire Bus Line
	3200 4050 3200 5800
Wire Bus Line
	5500 4050 5500 5800
$EndSCHEMATC
