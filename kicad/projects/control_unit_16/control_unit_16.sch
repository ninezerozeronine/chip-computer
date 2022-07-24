EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr B 17000 11000
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
L sixteen-bit-computer:74HC161 U5
U 1 1 5FD857CC
P 3250 1600
F 0 "U5" H 3000 2250 50  0000 C CNN
F 1 "74HC161" H 3550 2250 50  0000 C CNN
F 2 "Package_DIP:DIP-16_W7.62mm" H 3250 1600 50  0001 C CNN
F 3 "https://www.ti.com/lit/ds/symlink/cd54hc163.pdf" H 3250 1600 50  0001 C CNN
	1    3250 1600
	1    0    0    -1  
$EndComp
$Comp
L sixteen-bit-computer:74HC138 U9
U 1 1 5FD88A13
P 5250 1400
F 0 "U9" H 5000 1850 50  0000 C CNN
F 1 "74HC138" H 5500 1850 50  0000 C CNN
F 2 "Package_DIP:DIP-16_W7.62mm" H 5250 1400 50  0001 C CNN
F 3 "https://www.ti.com/lit/ds/symlink/sn74hct138.pdf" H 5250 1400 50  0001 C CNN
	1    5250 1400
	1    0    0    -1  
$EndComp
$Comp
L Memory_EEPROM:28C256 U2
U 1 1 5FD89CDC
P 2250 8950
F 0 "U2" H 2000 10000 50  0000 C CNN
F 1 "28C256" H 2500 10000 50  0000 C CNN
F 2 "Package_DIP:DIP-28_W15.24mm_Socket" H 2250 8950 50  0001 C CNN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/doc0006.pdf" H 2250 8950 50  0001 C CNN
	1    2250 8950
	1    0    0    -1  
$EndComp
$Comp
L Memory_EEPROM:28C256 U6
U 1 1 5FD8ACCD
P 4550 8950
F 0 "U6" H 4300 10000 50  0000 C CNN
F 1 "28C256" H 4800 10000 50  0000 C CNN
F 2 "Package_DIP:DIP-28_W15.24mm_Socket" H 4550 8950 50  0001 C CNN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/doc0006.pdf" H 4550 8950 50  0001 C CNN
	1    4550 8950
	1    0    0    -1  
$EndComp
$Comp
L Memory_EEPROM:28C256 U10
U 1 1 5FD8B589
P 6850 8950
F 0 "U10" H 6600 10000 50  0000 C CNN
F 1 "28C256" H 7100 10000 50  0000 C CNN
F 2 "Package_DIP:DIP-28_W15.24mm_Socket" H 6850 8950 50  0001 C CNN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/doc0006.pdf" H 6850 8950 50  0001 C CNN
	1    6850 8950
	1    0    0    -1  
$EndComp
$Comp
L Memory_EEPROM:28C256 U11
U 1 1 5FD8C15B
P 9300 8950
F 0 "U11" H 9050 10000 50  0000 C CNN
F 1 "28C256" H 9550 10000 50  0000 C CNN
F 2 "Package_DIP:DIP-28_W15.24mm_Socket" H 9300 8950 50  0001 C CNN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/doc0006.pdf" H 9300 8950 50  0001 C CNN
	1    9300 8950
	1    0    0    -1  
$EndComp
$Comp
L sixteen-bit-computer:74HC173 U3
U 1 1 5FD8D05D
P 2400 6450
F 0 "U3" H 2150 7200 50  0000 C CNN
F 1 "74HC173" H 2650 7200 50  0000 C CNN
F 2 "Package_DIP:DIP-16_W7.62mm" H 2400 6450 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/cd74hc173.pdf" H 2400 6450 50  0001 C CNN
	1    2400 6450
	1    0    0    -1  
$EndComp
$Comp
L sixteen-bit-computer:Aux_connection J4
U 1 1 5FD8D921
P 11150 1500
F 0 "J4" H 11062 2125 50  0000 C CNN
F 1 "Aux_connection" H 11062 2034 50  0000 C CNN
F 2 "sixteen-bit-computer:aux-connection" H 11150 1500 50  0001 C CNN
F 3 "~" H 11150 1500 50  0001 C CNN
	1    11150 1500
	1    0    0    -1  
$EndComp
$Comp
L sixteen-bit-computer:Bus_connection J3
U 1 1 5FD8FB3B
P 9700 1800
F 0 "J3" H 9562 2725 50  0000 C CNN
F 1 "Bus_connection" H 9562 2634 50  0000 C CNN
F 2 "sixteen-bit-computer:bus-connection" H 9600 2200 50  0001 C CNN
F 3 "~" H 9600 2200 50  0001 C CNN
	1    9700 1800
	1    0    0    -1  
$EndComp
$Comp
L sixteen-bit-computer:Control_signal_backplane J2
U 1 1 5FD91862
P 9400 5450
F 0 "J2" H 9287 7175 50  0000 C CNN
F 1 "Control_signal_backplane" H 9287 7084 50  0000 C CNN
F 2 "sixteen-bit-computer:backplane-connector-single-row" H 9400 5450 50  0001 C CNN
F 3 "~" H 9400 5450 50  0001 C CNN
	1    9400 5450
	1    0    0    -1  
$EndComp
$Comp
L Device:LED D20
U 1 1 5FD956D3
P 6700 2150
F 0 "D20" H 6450 2100 50  0000 C CNN
F 1 "LED" H 6300 2100 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 6700 2150 50  0001 C CNN
F 3 "~" H 6700 2150 50  0001 C CNN
	1    6700 2150
	-1   0    0    -1  
$EndComp
$Comp
L Device:LED D19
U 1 1 5FD96F8F
P 6700 2000
F 0 "D19" H 6450 1950 50  0000 C CNN
F 1 "LED" H 6300 1950 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 6700 2000 50  0001 C CNN
F 3 "~" H 6700 2000 50  0001 C CNN
	1    6700 2000
	-1   0    0    -1  
$EndComp
$Comp
L Device:LED D18
U 1 1 5FD994D8
P 6700 1850
F 0 "D18" H 6450 1800 50  0000 C CNN
F 1 "LED" H 6300 1800 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 6700 1850 50  0001 C CNN
F 3 "~" H 6700 1850 50  0001 C CNN
	1    6700 1850
	-1   0    0    -1  
$EndComp
$Comp
L Device:LED D17
U 1 1 5FD994E2
P 6700 1700
F 0 "D17" H 6450 1650 50  0000 C CNN
F 1 "LED" H 6300 1650 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 6700 1700 50  0001 C CNN
F 3 "~" H 6700 1700 50  0001 C CNN
	1    6700 1700
	-1   0    0    -1  
$EndComp
$Comp
L Device:LED D16
U 1 1 5FD9D16A
P 6700 1550
F 0 "D16" H 6450 1500 50  0000 C CNN
F 1 "LED" H 6300 1500 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 6700 1550 50  0001 C CNN
F 3 "~" H 6700 1550 50  0001 C CNN
	1    6700 1550
	-1   0    0    -1  
$EndComp
$Comp
L Device:LED D15
U 1 1 5FD9D170
P 6700 1400
F 0 "D15" H 6450 1350 50  0000 C CNN
F 1 "LED" H 6300 1350 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 6700 1400 50  0001 C CNN
F 3 "~" H 6700 1400 50  0001 C CNN
	1    6700 1400
	-1   0    0    -1  
$EndComp
$Comp
L Device:LED D14
U 1 1 5FD9D176
P 6700 1250
F 0 "D14" H 6450 1200 50  0000 C CNN
F 1 "LED" H 6300 1200 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 6700 1250 50  0001 C CNN
F 3 "~" H 6700 1250 50  0001 C CNN
	1    6700 1250
	-1   0    0    -1  
$EndComp
$Comp
L Device:LED D13
U 1 1 5FD9D17C
P 6700 1100
F 0 "D13" H 6450 1050 50  0000 C CNN
F 1 "LED" H 6300 1050 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 6700 1100 50  0001 C CNN
F 3 "~" H 6700 1100 50  0001 C CNN
	1    6700 1100
	-1   0    0    -1  
$EndComp
$Comp
L Device:LED D5
U 1 1 5FDA12E0
P 5650 3500
F 0 "D5" H 5400 3450 50  0000 C CNN
F 1 "LED" H 5250 3450 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 5650 3500 50  0001 C CNN
F 3 "~" H 5650 3500 50  0001 C CNN
	1    5650 3500
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D6
U 1 1 5FDA12E6
P 5650 3650
F 0 "D6" H 5400 3600 50  0000 C CNN
F 1 "LED" H 5250 3600 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 5650 3650 50  0001 C CNN
F 3 "~" H 5650 3650 50  0001 C CNN
	1    5650 3650
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D7
U 1 1 5FDA12EC
P 5650 3800
F 0 "D7" H 5400 3750 50  0000 C CNN
F 1 "LED" H 5250 3750 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 5650 3800 50  0001 C CNN
F 3 "~" H 5650 3800 50  0001 C CNN
	1    5650 3800
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D8
U 1 1 5FDA12F2
P 5650 3950
F 0 "D8" H 5400 3900 50  0000 C CNN
F 1 "LED" H 5250 3900 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 5650 3950 50  0001 C CNN
F 3 "~" H 5650 3950 50  0001 C CNN
	1    5650 3950
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D9
U 1 1 5FDA12F8
P 5650 4100
F 0 "D9" H 5400 4050 50  0000 C CNN
F 1 "LED" H 5250 4050 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 5650 4100 50  0001 C CNN
F 3 "~" H 5650 4100 50  0001 C CNN
	1    5650 4100
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D10
U 1 1 5FDA12FE
P 5650 4250
F 0 "D10" H 5400 4200 50  0000 C CNN
F 1 "LED" H 5250 4200 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 5650 4250 50  0001 C CNN
F 3 "~" H 5650 4250 50  0001 C CNN
	1    5650 4250
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D11
U 1 1 5FDA1304
P 5650 4400
F 0 "D11" H 5400 4350 50  0000 C CNN
F 1 "LED" H 5250 4350 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 5650 4400 50  0001 C CNN
F 3 "~" H 5650 4400 50  0001 C CNN
	1    5650 4400
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D12
U 1 1 5FDA130A
P 5650 4550
F 0 "D12" H 5400 4500 50  0000 C CNN
F 1 "LED" H 5250 4500 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 5650 4550 50  0001 C CNN
F 3 "~" H 5650 4550 50  0001 C CNN
	1    5650 4550
	-1   0    0    1   
$EndComp
$Comp
L Device:R_Network08_US RN3
U 1 1 5FDA3B23
P 7800 1500
F 0 "RN3" V 7183 1500 50  0000 C CNN
F 1 "R_Network08_US" V 7274 1500 50  0000 C CNN
F 2 "Resistor_THT:R_Array_SIP9" V 8275 1500 50  0001 C CNN
F 3 "http://www.vishay.com/docs/31509/csc.pdf" H 7800 1500 50  0001 C CNN
	1    7800 1500
	0    1    1    0   
$EndComp
$Comp
L Device:R_Network08_US RN2
U 1 1 5FDA7806
P 6700 3900
F 0 "RN2" V 6083 3900 50  0000 C CNN
F 1 "R_Network08_US" V 6174 3900 50  0000 C CNN
F 2 "Resistor_THT:R_Array_SIP9" V 7175 3900 50  0001 C CNN
F 3 "http://www.vishay.com/docs/31509/csc.pdf" H 6700 3900 50  0001 C CNN
	1    6700 3900
	0    1    1    0   
$EndComp
$Comp
L Device:R_Network04_US RN1
U 1 1 5FDA87EA
P 6950 6050
F 0 "RN1" V 6533 6050 50  0000 C CNN
F 1 "R_Network04_US" V 6624 6050 50  0000 C CNN
F 2 "Resistor_THT:R_Array_SIP5" V 7225 6050 50  0001 C CNN
F 3 "http://www.vishay.com/docs/31509/csc.pdf" H 6950 6050 50  0001 C CNN
	1    6950 6050
	0    1    1    0   
$EndComp
$Comp
L 74xx:74HC04 U1
U 1 1 5FDAA11A
P 1350 1600
F 0 "U1" H 1350 1917 50  0000 C CNN
F 1 "74HC04" H 1350 1826 50  0000 C CNN
F 2 "Package_DIP:DIP-14_W7.62mm" H 1350 1600 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 1350 1600 50  0001 C CNN
	1    1350 1600
	1    0    0    -1  
$EndComp
$Comp
L 74xx:74HC04 U1
U 2 1 5FDAB5DB
P 1350 2100
F 0 "U1" H 1350 2417 50  0000 C CNN
F 1 "74HC04" H 1350 2326 50  0000 C CNN
F 2 "Package_DIP:DIP-14_W7.62mm" H 1350 2100 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 1350 2100 50  0001 C CNN
	2    1350 2100
	1    0    0    -1  
$EndComp
$Comp
L 74xx:74HC04 U1
U 3 1 5FDACA10
P 12400 5200
F 0 "U1" H 12400 5517 50  0000 C CNN
F 1 "74HC04" H 12400 5426 50  0000 C CNN
F 2 "Package_DIP:DIP-14_W7.62mm" H 12400 5200 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 12400 5200 50  0001 C CNN
	3    12400 5200
	0    -1   -1   0   
$EndComp
$Comp
L 74xx:74HC04 U1
U 4 1 5FDAE4A7
P 13000 5200
F 0 "U1" H 13000 5517 50  0000 C CNN
F 1 "74HC04" H 13000 5426 50  0000 C CNN
F 2 "Package_DIP:DIP-14_W7.62mm" H 13000 5200 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 13000 5200 50  0001 C CNN
	4    13000 5200
	0    -1   -1   0   
$EndComp
$Comp
L 74xx:74HC04 U1
U 5 1 5FDAF775
P 13550 5200
F 0 "U1" H 13550 5517 50  0000 C CNN
F 1 "74HC04" H 13550 5426 50  0000 C CNN
F 2 "Package_DIP:DIP-14_W7.62mm" H 13550 5200 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 13550 5200 50  0001 C CNN
	5    13550 5200
	0    -1   -1   0   
$EndComp
$Comp
L 74xx:74HC04 U1
U 6 1 5FDB0B8C
P 14100 5200
F 0 "U1" H 14100 5517 50  0000 C CNN
F 1 "74HC04" H 14100 5426 50  0000 C CNN
F 2 "Package_DIP:DIP-14_W7.62mm" H 14100 5200 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 14100 5200 50  0001 C CNN
	6    14100 5200
	0    -1   -1   0   
$EndComp
$Comp
L 74xx:74HC04 U1
U 7 1 5FDB292F
P 11350 5000
F 0 "U1" H 11580 5046 50  0000 L CNN
F 1 "74HC04" H 11580 4955 50  0000 L CNN
F 2 "Package_DIP:DIP-14_W7.62mm" H 11350 5000 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 11350 5000 50  0001 C CNN
	7    11350 5000
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x16_Female J5
U 1 1 5FDB3728
P 12050 2850
F 0 "J5" V 12215 2780 50  0000 C CNN
F 1 "Conn_01x16_Female" V 12124 2780 50  0000 C CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x16_P2.54mm_Horizontal" H 12050 2850 50  0001 C CNN
F 3 "~" H 12050 2850 50  0001 C CNN
	1    12050 2850
	0    1    -1   0   
$EndComp
$Comp
L Connector:Conn_01x04_Female J1
U 1 1 5FDB6ECF
P 1050 5950
F 0 "J1" H 942 5525 50  0000 C CNN
F 1 "Conn_01x04_Female" H 942 5616 50  0000 C CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x04_P2.54mm_Horizontal" H 1050 5950 50  0001 C CNN
F 3 "~" H 1050 5950 50  0001 C CNN
	1    1050 5950
	-1   0    0    -1  
$EndComp
Text Label 1850 8050 2    50   ~ 0
BIN_STEP_0
Text Label 1850 8150 2    50   ~ 0
BIN_STEP_1
Text Label 1850 8250 2    50   ~ 0
BIN_STEP_2
Text Label 1850 8750 2    50   ~ 0
MIR_INST_0
Text Label 1850 8850 2    50   ~ 0
MIR_INST_1
Text Label 1850 8950 2    50   ~ 0
MIR_INST_2
Text Label 1850 9050 2    50   ~ 0
MIR_INST_3
Text Label 1850 9150 2    50   ~ 0
MIR_INST_4
Text Label 1850 9250 2    50   ~ 0
MIR_INST_5
Text Label 1850 9350 2    50   ~ 0
MIR_INST_6
Text Label 1850 9450 2    50   ~ 0
MIR_INST_7
Text Label 9700 8050 0    50   ~ 0
ROM_0_0
Text Label 9700 8150 0    50   ~ 0
ROM_0_1
Text Label 9700 8250 0    50   ~ 0
ROM_0_2
Text Label 9700 8350 0    50   ~ 0
ROM_0_3
Text Label 9700 8450 0    50   ~ 0
ROM_0_4
Text Label 9700 8550 0    50   ~ 0
ROM_0_5
Text Label 9700 8650 0    50   ~ 0
ROM_0_6
Text Label 9700 8750 0    50   ~ 0
ROM_0_7
Text Label 7250 8050 0    50   ~ 0
ROM_1_0
Text Label 7250 8150 0    50   ~ 0
ROM_1_1
Text Label 7250 8250 0    50   ~ 0
ROM_1_2
Text Label 7250 8350 0    50   ~ 0
ROM_1_3
Text Label 7250 8450 0    50   ~ 0
ROM_1_4
Text Label 7250 8550 0    50   ~ 0
ROM_1_5
Text Label 7250 8650 0    50   ~ 0
ROM_1_6
Text Label 7250 8750 0    50   ~ 0
ROM_1_7
Text Label 4950 8050 0    50   ~ 0
ROM_2_0
Text Label 4950 8150 0    50   ~ 0
ROM_2_1
Text Label 4950 8350 0    50   ~ 0
ROM_2_3
Text Label 4950 8250 0    50   ~ 0
ROM_2_2
Text Label 4950 8450 0    50   ~ 0
ROM_2_4
Text Label 4950 8550 0    50   ~ 0
ROM_2_5
Text Label 4950 8650 0    50   ~ 0
ROM_2_6
Text Label 4950 8750 0    50   ~ 0
ROM_2_7
Text Label 2650 8050 0    50   ~ 0
ROM_3_0
Text Label 2650 8150 0    50   ~ 0
ROM_3_1
Text Label 2650 8250 0    50   ~ 0
ROM_3_2
Text Label 2650 8450 0    50   ~ 0
ROM_3_4
Text Label 2650 8550 0    50   ~ 0
ROM_3_5
Text Label 2650 8650 0    50   ~ 0
ROM_3_6
Text Label 2650 8750 0    50   ~ 0
ROM_3_7
Text Label 4150 8750 2    50   ~ 0
MIR_INST_0
Text Label 4150 8850 2    50   ~ 0
MIR_INST_1
Text Label 4150 8950 2    50   ~ 0
MIR_INST_2
Text Label 4150 9050 2    50   ~ 0
MIR_INST_3
Text Label 4150 9150 2    50   ~ 0
MIR_INST_4
Text Label 4150 9250 2    50   ~ 0
MIR_INST_5
Text Label 4150 9350 2    50   ~ 0
MIR_INST_6
Text Label 4150 9450 2    50   ~ 0
MIR_INST_7
Text Label 6450 8750 2    50   ~ 0
MIR_INST_0
Text Label 6450 8850 2    50   ~ 0
MIR_INST_1
Text Label 6450 8950 2    50   ~ 0
MIR_INST_2
Text Label 6450 9050 2    50   ~ 0
MIR_INST_3
Text Label 6450 9150 2    50   ~ 0
MIR_INST_4
Text Label 6450 9250 2    50   ~ 0
MIR_INST_5
Text Label 6450 9350 2    50   ~ 0
MIR_INST_6
Text Label 6450 9450 2    50   ~ 0
MIR_INST_7
Text Label 8900 8750 2    50   ~ 0
MIR_INST_0
Text Label 8900 8850 2    50   ~ 0
MIR_INST_1
Text Label 8900 8950 2    50   ~ 0
MIR_INST_2
Text Label 8900 9050 2    50   ~ 0
MIR_INST_3
Text Label 8900 9150 2    50   ~ 0
MIR_INST_4
Text Label 8900 9250 2    50   ~ 0
MIR_INST_5
Text Label 8900 9350 2    50   ~ 0
MIR_INST_6
Text Label 8900 9450 2    50   ~ 0
MIR_INST_7
Text Label 1250 5850 0    50   ~ 0
EQUAL
Text Label 1250 5950 0    50   ~ 0
CARRY
Text Label 1250 6050 0    50   ~ 0
NEGATIVE
Text Label 1250 6150 0    50   ~ 0
ZERO
Text Label 2900 5850 0    50   ~ 0
MIR_EQUAL
Text Label 2900 5950 0    50   ~ 0
MIR_CARRY
Text Label 2900 6050 0    50   ~ 0
MIR_NEGATIVE
Text Label 2900 6150 0    50   ~ 0
MIR_ZERO
Text Label 1850 8350 2    50   ~ 0
MIR_EQUAL
Text Label 1850 8450 2    50   ~ 0
MIR_CARRY
Text Label 1850 8550 2    50   ~ 0
MIR_NEGATIVE
Text Label 1850 8650 2    50   ~ 0
MIR_ZERO
Text Label 4150 8350 2    50   ~ 0
MIR_EQUAL
Text Label 4150 8450 2    50   ~ 0
MIR_CARRY
Text Label 4150 8550 2    50   ~ 0
MIR_NEGATIVE
Text Label 4150 8650 2    50   ~ 0
MIR_ZERO
Text Label 6450 8350 2    50   ~ 0
MIR_EQUAL
Text Label 6450 8450 2    50   ~ 0
MIR_CARRY
Text Label 6450 8550 2    50   ~ 0
MIR_NEGATIVE
Text Label 6450 8650 2    50   ~ 0
MIR_ZERO
Text Label 8900 8350 2    50   ~ 0
MIR_EQUAL
Text Label 8900 8450 2    50   ~ 0
MIR_CARRY
Text Label 8900 8550 2    50   ~ 0
MIR_NEGATIVE
Text Label 8900 8650 2    50   ~ 0
MIR_ZERO
Wire Wire Line
	1250 5850 1900 5850
Wire Wire Line
	1250 5950 1900 5950
Wire Wire Line
	1250 6050 1900 6050
Wire Wire Line
	1250 6150 1900 6150
Text Label 9600 6650 0    50   ~ 0
STEP_RESET
Text Label 1050 1600 2    50   ~ 0
STEP_RESET
Text Label 1650 1600 0    50   ~ 0
~STEP_RESET
Text Label 11350 2000 0    50   ~ 0
RESET
Text Label 1050 2100 2    50   ~ 0
RESET
Text Label 1650 2100 0    50   ~ 0
~RESET
Wire Wire Line
	1650 2100 2750 2100
Wire Wire Line
	1650 1600 2750 1600
Text Label 11350 1800 0    50   ~ 0
CONTROL_CLOCK
Text Label 2300 1900 2    50   ~ 0
CONTROL_CLOCK
Wire Wire Line
	2750 1900 2300 1900
NoConn ~ 3750 1400
Text Label 3750 1100 0    50   ~ 0
BIN_STEP_0
Text Label 4150 8050 2    50   ~ 0
BIN_STEP_0
Text Label 4150 8150 2    50   ~ 0
BIN_STEP_1
Text Label 4150 8250 2    50   ~ 0
BIN_STEP_2
Text Label 6450 8050 2    50   ~ 0
BIN_STEP_0
Text Label 6450 8150 2    50   ~ 0
BIN_STEP_1
Text Label 6450 8250 2    50   ~ 0
BIN_STEP_2
Text Label 8900 8050 2    50   ~ 0
BIN_STEP_0
Text Label 8900 8150 2    50   ~ 0
BIN_STEP_1
Text Label 8900 8250 2    50   ~ 0
BIN_STEP_2
Text Label 3750 1200 0    50   ~ 0
BIN_STEP_1
Text Label 3750 1300 0    50   ~ 0
BIN_STEP_2
NoConn ~ 3750 1600
$Comp
L Device:C C4
U 1 1 5FE0D36E
P 2400 800
F 0 "C4" H 2200 850 50  0000 L CNN
F 1 "0.1uF" H 2100 750 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 2438 650 50  0001 C CNN
F 3 "~" H 2400 800 50  0001 C CNN
	1    2400 800 
	1    0    0    -1  
$EndComp
Wire Wire Line
	3250 2400 2400 2400
Wire Wire Line
	2400 2400 2400 1400
Wire Wire Line
	2400 650  2650 650 
Wire Wire Line
	3250 650  3250 800 
Wire Wire Line
	2750 1100 2750 1200
Wire Wire Line
	2750 1400 2400 1400
Connection ~ 2750 1400
Connection ~ 2750 1200
Wire Wire Line
	2750 1200 2750 1300
Connection ~ 2750 1300
Wire Wire Line
	2750 1300 2750 1400
Connection ~ 2400 1400
Wire Wire Line
	2400 1400 2400 950 
Wire Wire Line
	2750 1800 2650 1800
Connection ~ 2650 650 
Wire Wire Line
	2650 650  3250 650 
Wire Wire Line
	2650 650  2650 1700
Text Label 12750 3050 3    50   ~ 0
INST_00
Text Label 12650 3050 3    50   ~ 0
INST_01
Text Label 12550 3050 3    50   ~ 0
INST_02
Text Label 12450 3050 3    50   ~ 0
INST_03
Text Label 12350 3050 3    50   ~ 0
INST_04
Text Label 12250 3050 3    50   ~ 0
INST_05
Text Label 12150 3050 3    50   ~ 0
INST_06
Text Label 12050 3050 3    50   ~ 0
INST_07
NoConn ~ 11950 3050
NoConn ~ 11850 3050
NoConn ~ 11750 3050
NoConn ~ 11650 3050
NoConn ~ 11550 3050
NoConn ~ 11450 3050
NoConn ~ 11350 3050
NoConn ~ 11250 3050
Text Label 2850 650  0    50   ~ 0
VCC
Text Label 2850 2400 0    50   ~ 0
GND
$Comp
L Device:C C8
U 1 1 5FE2B52C
P 4450 900
F 0 "C8" H 4250 950 50  0000 L CNN
F 1 "0.1uF" H 4150 850 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 4488 750 50  0001 C CNN
F 3 "~" H 4450 900 50  0001 C CNN
	1    4450 900 
	1    0    0    -1  
$EndComp
Wire Wire Line
	4750 1700 4450 1700
Wire Wire Line
	4450 1700 4450 1050
Wire Wire Line
	4750 1800 4450 1800
Wire Wire Line
	4450 1800 4450 1700
Connection ~ 4450 1700
Wire Wire Line
	4450 1800 4450 2100
Wire Wire Line
	4450 2100 5250 2100
Connection ~ 4450 1800
Wire Wire Line
	4750 1600 4650 1600
Wire Wire Line
	4650 1600 4650 750 
Wire Wire Line
	4650 750  5250 750 
Wire Wire Line
	5250 750  5250 800 
Wire Wire Line
	4450 750  4650 750 
Connection ~ 4650 750 
Text Label 5100 750  0    50   ~ 0
VCC
Text Label 5000 2100 0    50   ~ 0
GND
Wire Wire Line
	3750 1100 4750 1100
Wire Wire Line
	3750 1200 4750 1200
Wire Wire Line
	3750 1300 4750 1300
Wire Wire Line
	5750 1100 6550 1100
Wire Wire Line
	5750 1200 6550 1200
Wire Wire Line
	6550 1200 6550 1250
Wire Wire Line
	5750 1300 6500 1300
Wire Wire Line
	6500 1300 6500 1400
Wire Wire Line
	6500 1400 6550 1400
Wire Wire Line
	5750 1400 6450 1400
Wire Wire Line
	6450 1400 6450 1550
Wire Wire Line
	6450 1550 6550 1550
Wire Wire Line
	5750 1500 6400 1500
Wire Wire Line
	6400 1500 6400 1700
Wire Wire Line
	6400 1700 6550 1700
Wire Wire Line
	5750 1600 6350 1600
Wire Wire Line
	6350 1600 6350 1850
Wire Wire Line
	6350 1850 6550 1850
Wire Wire Line
	5750 1700 6300 1700
Wire Wire Line
	6300 1700 6300 2000
Wire Wire Line
	6300 2000 6550 2000
Wire Wire Line
	6550 2150 6250 2150
Wire Wire Line
	6250 2150 6250 1800
Wire Wire Line
	6250 1800 5750 1800
Wire Wire Line
	6850 1100 7600 1100
Wire Wire Line
	6850 1250 7200 1250
Wire Wire Line
	7200 1250 7200 1200
Wire Wire Line
	7200 1200 7600 1200
Wire Wire Line
	6850 1400 7250 1400
Wire Wire Line
	7250 1400 7250 1300
Wire Wire Line
	7250 1300 7600 1300
Wire Wire Line
	6850 1550 7300 1550
Wire Wire Line
	7300 1550 7300 1400
Wire Wire Line
	7300 1400 7600 1400
Wire Wire Line
	7600 1500 7350 1500
Wire Wire Line
	7350 1700 6850 1700
Wire Wire Line
	7350 1500 7350 1700
Wire Wire Line
	6850 1850 7400 1850
Wire Wire Line
	7400 1850 7400 1600
Wire Wire Line
	7400 1600 7600 1600
Wire Wire Line
	7600 1700 7450 1700
Wire Wire Line
	7450 1700 7450 2000
Wire Wire Line
	7450 2000 6850 2000
Wire Wire Line
	6850 2150 7500 2150
Wire Wire Line
	7500 2150 7500 1800
Wire Wire Line
	7500 1800 7600 1800
Text Label 8000 1100 0    50   ~ 0
VCC
Text Label 5750 1100 0    50   ~ 0
LIN_STEP_0
Text Label 5750 1200 0    50   ~ 0
LIN_STEP_1
Text Label 5750 1300 0    50   ~ 0
LIN_STEP_2
Text Label 5750 1400 0    50   ~ 0
LIN_STEP_3
Text Label 5750 1500 0    50   ~ 0
LIN_STEP_4
Text Label 5750 1600 0    50   ~ 0
LIN_STEP_5
Text Label 5750 1700 0    50   ~ 0
LIN_STEP_6
Text Label 5750 1800 0    50   ~ 0
LIN_STEP_7
$Comp
L sixteen-bit-computer:74HC245 U8
U 1 1 5FED6485
P 4600 3750
F 0 "U8" H 4400 4450 50  0000 C CNN
F 1 "74HC245" H 4850 4450 50  0000 C CNN
F 2 "Package_DIP:DIP-20_W7.62mm" H 4250 3750 50  0001 C CNN
F 3 "" H 4250 3750 50  0001 C CNN
	1    4600 3750
	1    0    0    -1  
$EndComp
Wire Wire Line
	3650 3100 3650 4550
$Comp
L Device:C C7
U 1 1 5FEE0F27
P 3650 2950
F 0 "C7" H 3450 3000 50  0000 L CNN
F 1 "0.1uF" H 3350 2900 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 3688 2800 50  0001 C CNN
F 3 "~" H 3650 2950 50  0001 C CNN
	1    3650 2950
	1    0    0    -1  
$EndComp
Wire Wire Line
	4050 3200 3950 3200
Wire Wire Line
	4050 3350 3850 3350
Wire Wire Line
	3650 4550 3950 4550
Wire Wire Line
	3950 4550 4600 4550
Connection ~ 3950 4550
Wire Wire Line
	3950 3200 3950 4550
Wire Wire Line
	3650 2800 3850 2800
Wire Wire Line
	3850 2800 4600 2800
Connection ~ 3850 2800
Wire Wire Line
	3850 3350 3850 2800
Wire Wire Line
	5150 3500 5500 3500
Wire Wire Line
	5150 3600 5500 3600
Wire Wire Line
	5500 3600 5500 3650
Wire Wire Line
	5150 3700 5450 3700
Wire Wire Line
	5450 3700 5450 3800
Wire Wire Line
	5450 3800 5500 3800
Wire Wire Line
	5150 3800 5400 3800
Wire Wire Line
	5400 3800 5400 3950
Wire Wire Line
	5400 3950 5500 3950
Wire Wire Line
	5150 3900 5350 3900
Wire Wire Line
	5350 3900 5350 4100
Wire Wire Line
	5350 4100 5500 4100
Wire Wire Line
	5150 4000 5300 4000
Wire Wire Line
	5300 4000 5300 4250
Wire Wire Line
	5300 4250 5500 4250
Wire Wire Line
	5150 4100 5250 4100
Wire Wire Line
	5250 4100 5250 4400
Wire Wire Line
	5250 4400 5500 4400
Wire Wire Line
	5500 4550 5200 4550
Wire Wire Line
	5200 4550 5200 4200
Wire Wire Line
	5200 4200 5150 4200
Wire Wire Line
	5800 3500 6500 3500
Wire Wire Line
	5800 3650 6150 3650
Wire Wire Line
	6150 3650 6150 3600
Wire Wire Line
	6150 3600 6500 3600
Wire Wire Line
	6500 3700 6200 3700
Wire Wire Line
	6200 3700 6200 3800
Wire Wire Line
	6200 3800 5800 3800
Wire Wire Line
	5800 3950 6250 3950
Wire Wire Line
	6250 3950 6250 3800
Wire Wire Line
	6250 3800 6500 3800
Wire Wire Line
	6500 3900 6300 3900
Wire Wire Line
	6300 3900 6300 4100
Wire Wire Line
	6300 4100 5800 4100
Wire Wire Line
	5800 4250 6350 4250
Wire Wire Line
	6350 4250 6350 4000
Wire Wire Line
	6350 4000 6500 4000
Wire Wire Line
	6500 4100 6400 4100
Wire Wire Line
	6400 4100 6400 4400
Wire Wire Line
	6400 4400 5800 4400
Wire Wire Line
	5800 4550 6450 4550
Wire Wire Line
	6450 4550 6450 4200
Wire Wire Line
	6450 4200 6500 4200
Text Label 6900 3500 0    50   ~ 0
GND
$Comp
L Device:LED D1
U 1 1 5FFC385A
P 6100 5850
F 0 "D1" H 5850 5800 50  0000 C CNN
F 1 "LED" H 5700 5800 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 6100 5850 50  0001 C CNN
F 3 "~" H 6100 5850 50  0001 C CNN
	1    6100 5850
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D2
U 1 1 5FFC3860
P 6100 6000
F 0 "D2" H 5850 5950 50  0000 C CNN
F 1 "LED" H 5700 5950 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 6100 6000 50  0001 C CNN
F 3 "~" H 6100 6000 50  0001 C CNN
	1    6100 6000
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D3
U 1 1 5FFC3866
P 6100 6150
F 0 "D3" H 5850 6100 50  0000 C CNN
F 1 "LED" H 5700 6100 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 6100 6150 50  0001 C CNN
F 3 "~" H 6100 6150 50  0001 C CNN
	1    6100 6150
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D4
U 1 1 5FFC386C
P 6100 6300
F 0 "D4" H 5850 6250 50  0000 C CNN
F 1 "LED" H 5700 6250 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 6100 6300 50  0001 C CNN
F 3 "~" H 6100 6300 50  0001 C CNN
	1    6100 6300
	-1   0    0    1   
$EndComp
Wire Wire Line
	3450 5450 3450 6900
$Comp
L Device:C C6
U 1 1 5FFC389D
P 3450 5300
F 0 "C6" H 3250 5350 50  0000 L CNN
F 1 "0.1uF" H 3150 5250 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 3488 5150 50  0001 C CNN
F 3 "~" H 3450 5300 50  0001 C CNN
	1    3450 5300
	1    0    0    -1  
$EndComp
Wire Wire Line
	4200 5550 4100 5550
Wire Wire Line
	4200 5700 4000 5700
Connection ~ 4100 6900
Wire Wire Line
	4100 5550 4100 6900
Wire Wire Line
	3450 5150 4000 5150
Wire Wire Line
	4000 5150 4750 5150
Connection ~ 4000 5150
Wire Wire Line
	4000 5700 4000 5150
Wire Wire Line
	5300 5850 5950 5850
Wire Wire Line
	5300 5950 5950 5950
Wire Wire Line
	5950 5950 5950 6000
Wire Wire Line
	5300 6050 5900 6050
Wire Wire Line
	5900 6050 5900 6150
Wire Wire Line
	5900 6150 5950 6150
Wire Wire Line
	5300 6150 5850 6150
Wire Wire Line
	5850 6150 5850 6300
Wire Wire Line
	5850 6300 5950 6300
Wire Wire Line
	6250 5850 6750 5850
Wire Wire Line
	6250 6000 6600 6000
Wire Wire Line
	6600 6000 6600 5950
Wire Wire Line
	6600 5950 6750 5950
Wire Wire Line
	6750 6050 6650 6050
Wire Wire Line
	6650 6050 6650 6150
Wire Wire Line
	6650 6150 6250 6150
Wire Wire Line
	6250 6300 6700 6300
Wire Wire Line
	6700 6300 6700 6150
Wire Wire Line
	6700 6150 6750 6150
Text Label 7150 5850 0    50   ~ 0
GND
Wire Wire Line
	2900 5850 4200 5850
Wire Wire Line
	4200 5950 2900 5950
Wire Wire Line
	2900 6050 4200 6050
Wire Wire Line
	4200 6150 2900 6150
Wire Wire Line
	4100 6900 4750 6900
Wire Wire Line
	4200 6550 3750 6550
Text Label 1650 6850 2    50   ~ 0
CONTROL_CLOCK
Wire Wire Line
	1900 7050 1800 7050
Wire Wire Line
	1800 7050 1800 7350
Wire Wire Line
	1900 6350 1800 6350
Wire Wire Line
	1800 6350 1800 6450
Connection ~ 1800 7050
Wire Wire Line
	1900 6450 1800 6450
Connection ~ 1800 6450
Wire Wire Line
	1800 6450 1800 6650
Wire Wire Line
	1900 6650 1800 6650
Connection ~ 1800 6650
Wire Wire Line
	1800 6650 1800 6750
Wire Wire Line
	1900 6750 1800 6750
Connection ~ 1800 6750
Wire Wire Line
	1800 6750 1800 7050
Text Label 4350 2800 0    50   ~ 0
VCC
Text Label 4350 4550 0    50   ~ 0
GND
Text Label 4550 5150 0    50   ~ 0
VCC
Text Label 4550 6900 0    50   ~ 0
GND
$Comp
L Device:C C3
U 1 1 60092834
P 1800 5600
F 0 "C3" H 1600 5650 50  0000 L CNN
F 1 "0.1uF" H 1500 5550 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 1838 5450 50  0001 C CNN
F 3 "~" H 1800 5600 50  0001 C CNN
	1    1800 5600
	1    0    0    -1  
$EndComp
Wire Wire Line
	1800 5450 2400 5450
Wire Wire Line
	2400 5450 2400 5550
Wire Wire Line
	1800 7350 2400 7350
Wire Wire Line
	1800 5750 1800 6350
Connection ~ 1800 6350
Text Label 2150 5450 0    50   ~ 0
VCC
Text Label 2150 7350 0    50   ~ 0
GND
Wire Wire Line
	1650 6850 1900 6850
Text Label 2250 10150 2    50   ~ 0
GND
Text Label 2250 7750 2    50   ~ 0
VCC
$Comp
L Device:C C1
U 1 1 60228310
P 1050 8950
F 0 "C1" H 850 9000 50  0000 L CNN
F 1 "0.1uF" H 750 8900 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 1088 8800 50  0001 C CNN
F 3 "~" H 1050 8950 50  0001 C CNN
	1    1050 8950
	1    0    0    -1  
$EndComp
$Comp
L Device:C C5
U 1 1 60229DB3
P 3400 8950
F 0 "C5" H 3200 9000 50  0000 L CNN
F 1 "0.1uF" H 3100 8900 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 3438 8800 50  0001 C CNN
F 3 "~" H 3400 8950 50  0001 C CNN
	1    3400 8950
	1    0    0    -1  
$EndComp
$Comp
L Device:C C9
U 1 1 6022A560
P 5700 8950
F 0 "C9" H 5500 9000 50  0000 L CNN
F 1 "0.1uF" H 5400 8900 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 5738 8800 50  0001 C CNN
F 3 "~" H 5700 8950 50  0001 C CNN
	1    5700 8950
	1    0    0    -1  
$EndComp
$Comp
L Device:C C10
U 1 1 6022AF52
P 8150 8950
F 0 "C10" H 7900 9000 50  0000 L CNN
F 1 "0.1uF" H 7850 8900 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 8188 8800 50  0001 C CNN
F 3 "~" H 8150 8950 50  0001 C CNN
	1    8150 8950
	1    0    0    -1  
$EndComp
Wire Wire Line
	1850 9650 1300 9650
Wire Wire Line
	1850 9750 1300 9750
Wire Wire Line
	1300 9750 1300 9850
Wire Wire Line
	1850 9850 1300 9850
Connection ~ 1300 9850
Wire Wire Line
	1050 7750 1300 7750
Wire Wire Line
	2250 7750 2250 7850
Wire Wire Line
	1300 7750 1300 9650
Connection ~ 1300 7750
Wire Wire Line
	1300 7750 2250 7750
Wire Wire Line
	1050 7750 1050 8800
Wire Wire Line
	4550 7850 4550 7750
Wire Wire Line
	4550 7750 3600 7750
Wire Wire Line
	3600 9650 4150 9650
Wire Wire Line
	4150 9750 3600 9750
Wire Wire Line
	3600 10150 4550 10150
Wire Wire Line
	4550 10150 4550 10050
Wire Wire Line
	4150 9850 3600 9850
Wire Wire Line
	3600 9750 3600 9850
Connection ~ 3600 9850
Wire Wire Line
	3600 9850 3600 10150
Wire Wire Line
	3600 7750 3600 9650
Wire Wire Line
	3600 7750 3400 7750
Wire Wire Line
	3400 7750 3400 8800
Connection ~ 3600 7750
Wire Wire Line
	3400 9100 3400 10150
Wire Wire Line
	3400 10150 3600 10150
Connection ~ 3600 10150
Wire Wire Line
	1050 10150 1300 10150
Wire Wire Line
	2250 10150 2250 10050
Wire Wire Line
	1050 9100 1050 10150
Wire Wire Line
	1300 9850 1300 10150
Connection ~ 1300 10150
Wire Wire Line
	1300 10150 2250 10150
Text Label 4550 10150 2    50   ~ 0
GND
Text Label 4550 7750 2    50   ~ 0
VCC
Wire Wire Line
	6850 7750 5900 7750
Wire Wire Line
	5900 7750 5900 9650
Wire Wire Line
	5900 9650 6450 9650
Wire Wire Line
	6450 9750 5900 9750
Wire Wire Line
	5900 9750 5900 9850
Wire Wire Line
	5900 10150 6850 10150
Wire Wire Line
	6850 10150 6850 10050
Wire Wire Line
	6450 9850 5900 9850
Connection ~ 5900 9850
Wire Wire Line
	5900 9850 5900 10150
Wire Wire Line
	5700 9100 5700 10150
Wire Wire Line
	5700 10150 5900 10150
Connection ~ 5900 10150
Wire Wire Line
	5700 8800 5700 7750
Wire Wire Line
	5700 7750 5900 7750
Connection ~ 5900 7750
Text Label 6850 7750 2    50   ~ 0
VCC
Text Label 9300 7750 2    50   ~ 0
VCC
Wire Wire Line
	6850 7750 6850 7850
Wire Wire Line
	9300 7850 9300 7750
Wire Wire Line
	9300 7750 8350 7750
Wire Wire Line
	8350 7750 8350 9650
Wire Wire Line
	8350 9650 8900 9650
Wire Wire Line
	8900 9750 8350 9750
Wire Wire Line
	8350 9750 8350 9850
Wire Wire Line
	8350 10150 9300 10150
Wire Wire Line
	9300 10150 9300 10050
Connection ~ 8350 9850
Wire Wire Line
	8350 9850 8350 10150
Wire Wire Line
	8350 7750 8150 7750
Wire Wire Line
	8150 7750 8150 8800
Connection ~ 8350 7750
Wire Wire Line
	8150 9100 8150 10150
Wire Wire Line
	8150 10150 8350 10150
Connection ~ 8350 10150
Text Label 6850 10150 2    50   ~ 0
GND
Text Label 9300 10150 2    50   ~ 0
GND
Wire Wire Line
	8350 9850 8900 9850
Text Label 9600 3950 0    50   ~ 0
ROM_0_0
Text Label 9600 4050 0    50   ~ 0
ROM_0_1
Text Label 9600 4150 0    50   ~ 0
ROM_0_2
Text Label 9600 4250 0    50   ~ 0
ROM_0_3
Text Label 9600 4350 0    50   ~ 0
ROM_0_4
Text Label 9600 4450 0    50   ~ 0
ROM_0_5
Text Label 9600 4550 0    50   ~ 0
ROM_0_6
Text Label 9600 4650 0    50   ~ 0
ROM_0_7
Text Label 9600 4750 0    50   ~ 0
ROM_1_0
Text Label 9600 4850 0    50   ~ 0
ROM_1_1
Text Label 9600 4950 0    50   ~ 0
ROM_1_2
Text Label 9600 5050 0    50   ~ 0
ROM_1_3
Text Label 9600 5150 0    50   ~ 0
ROM_1_4
Text Label 9600 5250 0    50   ~ 0
ROM_1_5
Text Label 9600 5350 0    50   ~ 0
ROM_1_6
Text Label 9600 5450 0    50   ~ 0
ROM_1_7
Text Label 9600 5550 0    50   ~ 0
ROM_2_0
Text Label 9600 5650 0    50   ~ 0
ROM_2_1
Text Label 9600 5850 0    50   ~ 0
ROM_2_3
Text Label 9600 5750 0    50   ~ 0
ROM_2_2
Text Label 9600 5950 0    50   ~ 0
ROM_2_4
Text Label 9600 6050 0    50   ~ 0
ROM_2_5
Text Label 9600 6150 0    50   ~ 0
ROM_2_6
Text Label 9600 6250 0    50   ~ 0
ROM_2_7
Text Label 9600 6350 0    50   ~ 0
ROM_3_0
Text Label 9600 6450 0    50   ~ 0
ROM_3_1
Text Label 9600 6550 0    50   ~ 0
ROM_3_2
Text Label 9600 6750 0    50   ~ 0
ROM_3_4
Text Label 9600 6850 0    50   ~ 0
ROM_3_5
Text Label 9600 6950 0    50   ~ 0
ROM_3_6
Text Label 9600 7050 0    50   ~ 0
ROM_3_7
Text Label 2650 8350 0    50   ~ 0
STEP_RESET
NoConn ~ 9800 1100
NoConn ~ 9800 1200
NoConn ~ 9800 1300
NoConn ~ 9800 1400
NoConn ~ 9800 1500
NoConn ~ 9800 1600
NoConn ~ 9800 1700
NoConn ~ 9800 1800
NoConn ~ 9800 1900
NoConn ~ 9800 2000
NoConn ~ 9800 2100
NoConn ~ 9800 2200
NoConn ~ 9800 2300
NoConn ~ 9800 2400
NoConn ~ 9800 2500
NoConn ~ 9800 2600
Wire Wire Line
	11350 1100 11350 1200
Wire Wire Line
	11350 1300 11350 1400
NoConn ~ 11350 1600
$Comp
L power:GND #PWR0101
U 1 1 606CDBFC
P 12000 1400
F 0 "#PWR0101" H 12000 1150 50  0001 C CNN
F 1 "GND" H 12005 1227 50  0000 C CNN
F 2 "" H 12000 1400 50  0001 C CNN
F 3 "" H 12000 1400 50  0001 C CNN
	1    12000 1400
	1    0    0    -1  
$EndComp
$Comp
L power:PWR_FLAG #FLG0101
U 1 1 606CF370
P 11700 1400
F 0 "#FLG0101" H 11700 1475 50  0001 C CNN
F 1 "PWR_FLAG" H 11700 1573 50  0000 C CNN
F 2 "" H 11700 1400 50  0001 C CNN
F 3 "~" H 11700 1400 50  0001 C CNN
	1    11700 1400
	-1   0    0    1   
$EndComp
$Comp
L Device:CP C12
U 1 1 606E4D6D
P 12300 1250
F 0 "C12" H 12418 1296 50  0000 L CNN
F 1 "33uF" H 12418 1205 50  0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D6.3mm_P2.50mm" H 12338 1100 50  0001 C CNN
F 3 "~" H 12300 1250 50  0001 C CNN
	1    12300 1250
	1    0    0    -1  
$EndComp
$Comp
L Device:CP C13
U 1 1 606E63B5
P 12700 1250
F 0 "C13" H 12818 1296 50  0000 L CNN
F 1 "33uF" H 12818 1205 50  0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D6.3mm_P2.50mm" H 12738 1100 50  0001 C CNN
F 3 "~" H 12700 1250 50  0001 C CNN
	1    12700 1250
	1    0    0    -1  
$EndComp
$Comp
L Device:CP C14
U 1 1 606E6A8A
P 13100 1250
F 0 "C14" H 13218 1296 50  0000 L CNN
F 1 "33uF" H 13218 1205 50  0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D6.3mm_P2.50mm" H 13138 1100 50  0001 C CNN
F 3 "~" H 13100 1250 50  0001 C CNN
	1    13100 1250
	1    0    0    -1  
$EndComp
Connection ~ 11350 1100
Connection ~ 11700 1100
Connection ~ 12000 1100
Wire Wire Line
	12000 1100 12300 1100
Connection ~ 12300 1100
Wire Wire Line
	12300 1100 12700 1100
Connection ~ 12700 1100
Wire Wire Line
	12700 1100 13100 1100
Wire Wire Line
	13100 1400 12700 1400
Connection ~ 11350 1400
Connection ~ 11700 1400
Wire Wire Line
	11700 1400 11350 1400
Connection ~ 12000 1400
Wire Wire Line
	12000 1400 11700 1400
Connection ~ 12300 1400
Wire Wire Line
	12300 1400 12000 1400
Connection ~ 12700 1400
Wire Wire Line
	12700 1400 12300 1400
Wire Wire Line
	11700 1100 12000 1100
$Comp
L power:VCC #PWR0102
U 1 1 606CC509
P 12000 1100
F 0 "#PWR0102" H 12000 950 50  0001 C CNN
F 1 "VCC" H 12017 1273 50  0000 C CNN
F 2 "" H 12000 1100 50  0001 C CNN
F 3 "" H 12000 1100 50  0001 C CNN
	1    12000 1100
	1    0    0    -1  
$EndComp
Wire Wire Line
	11350 1100 11700 1100
$Comp
L power:PWR_FLAG #FLG0102
U 1 1 606CAA2A
P 11700 1100
F 0 "#FLG0102" H 11700 1175 50  0001 C CNN
F 1 "PWR_FLAG" H 11700 1273 50  0000 C CNN
F 2 "" H 11700 1100 50  0001 C CNN
F 3 "~" H 11700 1100 50  0001 C CNN
	1    11700 1100
	1    0    0    -1  
$EndComp
Text Label 11450 1100 0    50   ~ 0
VCC
Text Label 11450 1400 0    50   ~ 0
GND
$Comp
L Device:C C11
U 1 1 607AA190
P 10950 5000
F 0 "C11" H 10700 5050 50  0000 L CNN
F 1 "0.1uF" H 10650 4950 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 10988 4850 50  0001 C CNN
F 3 "~" H 10950 5000 50  0001 C CNN
	1    10950 5000
	1    0    0    -1  
$EndComp
Wire Wire Line
	11350 4500 10950 4500
Wire Wire Line
	10950 4500 10950 4850
Wire Wire Line
	10950 5150 10950 5500
Wire Wire Line
	10950 5500 11350 5500
Wire Wire Line
	11350 5500 12400 5500
Connection ~ 11350 5500
Connection ~ 12400 5500
Wire Wire Line
	12400 5500 13000 5500
Connection ~ 13000 5500
Wire Wire Line
	13000 5500 13550 5500
Connection ~ 13550 5500
Wire Wire Line
	13550 5500 14100 5500
NoConn ~ 14100 4900
NoConn ~ 13550 4900
NoConn ~ 13000 4900
NoConn ~ 12400 4900
Text Label 11100 5500 0    50   ~ 0
GND
Text Label 11150 4500 0    50   ~ 0
VCC
Wire Wire Line
	2750 1700 2650 1700
Connection ~ 2650 1700
Wire Wire Line
	2650 1700 2650 1800
$Comp
L Device:R_Network08_US RN4
U 1 1 60897A38
P 6250 7100
F 0 "RN4" V 5633 7100 50  0000 C CNN
F 1 "R_Network08_US" V 5724 7100 50  0000 C CNN
F 2 "Resistor_THT:R_Array_SIP9" V 6725 7100 50  0001 C CNN
F 3 "http://www.vishay.com/docs/31509/csc.pdf" H 6250 7100 50  0001 C CNN
	1    6250 7100
	0    1    1    0   
$EndComp
$Comp
L sixteen-bit-computer:74HC245 U7
U 1 1 5FFC3890
P 4750 6100
F 0 "U7" H 4550 6800 50  0000 C CNN
F 1 "74HC245" H 5000 6800 50  0000 C CNN
F 2 "Package_DIP:DIP-20_W7.62mm" H 4400 6100 50  0001 C CNN
F 3 "" H 4400 6100 50  0001 C CNN
	1    4750 6100
	1    0    0    -1  
$EndComp
Wire Wire Line
	5300 6250 5500 6250
Wire Wire Line
	5500 6250 5500 6700
Wire Wire Line
	5500 6700 6050 6700
Wire Wire Line
	6050 6800 5450 6800
Wire Wire Line
	5450 6800 5450 6350
Wire Wire Line
	5450 6350 5300 6350
Wire Wire Line
	5300 6450 5400 6450
Wire Wire Line
	5400 6450 5400 6900
Wire Wire Line
	5400 6900 6050 6900
Wire Wire Line
	6050 7000 5350 7000
Wire Wire Line
	5350 7000 5350 6550
Wire Wire Line
	5350 6550 5300 6550
Wire Wire Line
	3450 6900 4100 6900
Wire Wire Line
	3750 6550 3750 7100
Wire Wire Line
	3750 7100 6050 7100
Wire Wire Line
	6050 7200 3700 7200
Wire Wire Line
	3700 7200 3700 6450
Wire Wire Line
	3700 6450 4200 6450
Wire Wire Line
	3650 6350 3650 7300
Wire Wire Line
	3650 7300 6050 7300
Wire Wire Line
	3650 6350 4200 6350
Wire Wire Line
	6050 7400 3600 7400
Wire Wire Line
	3600 7400 3600 6250
Wire Wire Line
	3600 6250 4200 6250
Text Label 6450 6700 0    50   ~ 0
GND
Text Label 2350 4800 0    50   ~ 0
GND
Text Label 2300 3200 0    50   ~ 0
VCC
Wire Wire Line
	4050 3500 3100 3500
Wire Wire Line
	3100 3600 4050 3600
Wire Wire Line
	4050 3700 3100 3700
Wire Wire Line
	3100 3800 4050 3800
Wire Wire Line
	4050 3900 3100 3900
Wire Wire Line
	3100 4000 4050 4000
Wire Wire Line
	4050 4100 3100 4100
Wire Wire Line
	3100 4200 4050 4200
Wire Wire Line
	1500 4400 2100 4400
Wire Wire Line
	1650 4500 1650 4800
Connection ~ 1650 4500
Wire Wire Line
	2100 4500 1650 4500
Wire Wire Line
	1650 4800 2600 4800
Wire Wire Line
	1650 3500 1650 4500
Wire Wire Line
	1650 3200 2600 3200
$Comp
L Device:C C2
U 1 1 5FECB829
P 1650 3350
F 0 "C2" H 1450 3400 50  0000 L CNN
F 1 "0.1uF" H 1350 3300 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 1688 3200 50  0001 C CNN
F 3 "~" H 1650 3350 50  0001 C CNN
	1    1650 3350
	1    0    0    -1  
$EndComp
Text Label 1500 4400 2    50   ~ 0
CONTROL_CLOCK
Text Label 3100 3500 0    50   ~ 0
MIR_INST_7
Text Label 3100 3600 0    50   ~ 0
MIR_INST_6
Text Label 3100 3700 0    50   ~ 0
MIR_INST_5
Text Label 3100 3800 0    50   ~ 0
MIR_INST_4
Text Label 3100 3900 0    50   ~ 0
MIR_INST_3
Text Label 3100 4000 0    50   ~ 0
MIR_INST_2
Text Label 3100 4100 0    50   ~ 0
MIR_INST_1
Text Label 3100 4200 0    50   ~ 0
MIR_INST_0
Text Label 2100 3500 2    50   ~ 0
INST_07
Text Label 2100 3600 2    50   ~ 0
INST_06
Text Label 2100 3700 2    50   ~ 0
INST_05
Text Label 2100 3800 2    50   ~ 0
INST_04
Text Label 2100 3900 2    50   ~ 0
INST_03
Text Label 2100 4000 2    50   ~ 0
INST_02
Text Label 2100 4100 2    50   ~ 0
INST_01
Text Label 2100 4200 2    50   ~ 0
INST_00
$Comp
L sixteen-bit-computer:74HC377 U4
U 1 1 5FD843AB
P 2600 4000
F 0 "U4" H 2350 4650 50  0000 C CNN
F 1 "74HC377" H 2850 4650 50  0000 C CNN
F 2 "Package_DIP:DIP-20_W7.62mm" H 2600 4000 50  0001 C CNN
F 3 "http://www.ti.com/lit/gpn/sn74LS377" H 2600 4000 50  0001 C CNN
	1    2600 4000
	1    0    0    -1  
$EndComp
$EndSCHEMATC
