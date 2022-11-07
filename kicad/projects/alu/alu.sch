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
L sixteen-bit-computer:Aux_connection J5
U 1 1 5F95F4FF
P 13950 5050
F 0 "J5" H 13862 5675 50  0000 C CNN
F 1 "Aux_connection" H 13862 5584 50  0000 C CNN
F 2 "sixteen-bit-computer:aux-connection" H 13950 5050 50  0001 C CNN
F 3 "~" H 13950 5050 50  0001 C CNN
	1    13950 5050
	1    0    0    -1  
$EndComp
$Comp
L sixteen-bit-computer:Bus_connection J4
U 1 1 5F96011F
P 6250 8050
F 0 "J4" H 6112 8975 50  0000 C CNN
F 1 "Bus_connection" H 6112 8884 50  0000 C CNN
F 2 "sixteen-bit-computer:bus-connection" H 6150 8450 50  0001 C CNN
F 3 "~" H 6150 8450 50  0001 C CNN
	1    6250 8050
	1    0    0    1   
$EndComp
$Comp
L sixteen-bit-computer:Control_signal_backplane J3
U 1 1 5F960B16
P 15850 5550
F 0 "J3" H 15737 7275 50  0000 C CNN
F 1 "Control_signal_backplane" H 15737 7184 50  0000 C CNN
F 2 "sixteen-bit-computer:backplane-connector-single-row-annotated" H 15850 5550 50  0001 C CNN
F 3 "~" H 15850 5550 50  0001 C CNN
	1    15850 5550
	1    0    0    -1  
$EndComp
$Comp
L sixteen-bit-computer:74HC157 U8
U 1 1 5F96E5D7
P 2800 4900
F 0 "U8" H 2500 5600 50  0000 C CNN
F 1 "74HC157" H 3050 5600 50  0000 C CNN
F 2 "Package_DIP:DIP-16_W7.62mm_Socket" H 2800 4850 50  0001 C CNN
F 3 "https://www.ti.com/lit/ds/symlink/sn74hct157.pdf" H 2800 4850 50  0001 C CNN
	1    2800 4900
	1    0    0    -1  
$EndComp
$Comp
L sixteen-bit-computer:74HC157 U10
U 1 1 5F96F80C
P 5250 4900
F 0 "U10" H 5000 5600 50  0000 C CNN
F 1 "74HC157" H 5500 5600 50  0000 C CNN
F 2 "Package_DIP:DIP-16_W7.62mm_Socket" H 5250 4850 50  0001 C CNN
F 3 "https://www.ti.com/lit/ds/symlink/sn74hct157.pdf" H 5250 4850 50  0001 C CNN
	1    5250 4900
	1    0    0    -1  
$EndComp
$Comp
L sixteen-bit-computer:74HC157 U11
U 1 1 5F970081
P 9800 4900
F 0 "U11" H 9550 5600 50  0000 C CNN
F 1 "74HC157" H 10050 5600 50  0000 C CNN
F 2 "Package_DIP:DIP-16_W7.62mm_Socket" H 9800 4850 50  0001 C CNN
F 3 "https://www.ti.com/lit/ds/symlink/sn74hct157.pdf" H 9800 4850 50  0001 C CNN
	1    9800 4900
	1    0    0    -1  
$EndComp
$Comp
L sixteen-bit-computer:74HC157 U9
U 1 1 5F9706EB
P 7550 4900
F 0 "U9" H 7250 5600 50  0000 C CNN
F 1 "74HC157" H 7800 5600 50  0000 C CNN
F 2 "Package_DIP:DIP-16_W7.62mm_Socket" H 7550 4850 50  0001 C CNN
F 3 "https://www.ti.com/lit/ds/symlink/sn74hct157.pdf" H 7550 4850 50  0001 C CNN
	1    7550 4900
	1    0    0    -1  
$EndComp
$Comp
L Device:LED D16
U 1 1 5F97105C
P 4050 6950
F 0 "D16" H 3800 6900 50  0000 C CNN
F 1 "LED" H 3600 6900 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 4050 6950 50  0001 C CNN
F 3 "~" H 4050 6950 50  0001 C CNN
	1    4050 6950
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D15
U 1 1 5F9815B5
P 4050 7100
F 0 "D15" H 3800 7050 50  0000 C CNN
F 1 "LED" H 3600 7050 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 4050 7100 50  0001 C CNN
F 3 "~" H 4050 7100 50  0001 C CNN
	1    4050 7100
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D14
U 1 1 5F981E12
P 4050 7250
F 0 "D14" H 3800 7200 50  0000 C CNN
F 1 "LED" H 3600 7200 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 4050 7250 50  0001 C CNN
F 3 "~" H 4050 7250 50  0001 C CNN
	1    4050 7250
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D13
U 1 1 5F982593
P 4050 7400
F 0 "D13" H 3800 7350 50  0000 C CNN
F 1 "LED" H 3600 7350 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 4050 7400 50  0001 C CNN
F 3 "~" H 4050 7400 50  0001 C CNN
	1    4050 7400
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D12
U 1 1 5F98323E
P 4050 7550
F 0 "D12" H 3800 7500 50  0000 C CNN
F 1 "LED" H 3600 7500 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 4050 7550 50  0001 C CNN
F 3 "~" H 4050 7550 50  0001 C CNN
	1    4050 7550
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D11
U 1 1 5F983248
P 4050 7700
F 0 "D11" H 3800 7650 50  0000 C CNN
F 1 "LED" H 3600 7650 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 4050 7700 50  0001 C CNN
F 3 "~" H 4050 7700 50  0001 C CNN
	1    4050 7700
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D10
U 1 1 5F983252
P 4050 7850
F 0 "D10" H 3800 7800 50  0000 C CNN
F 1 "LED" H 3600 7800 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 4050 7850 50  0001 C CNN
F 3 "~" H 4050 7850 50  0001 C CNN
	1    4050 7850
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D9
U 1 1 5F98325C
P 4050 8000
F 0 "D9" H 3800 7950 50  0000 C CNN
F 1 "LED" H 3600 7950 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 4050 8000 50  0001 C CNN
F 3 "~" H 4050 8000 50  0001 C CNN
	1    4050 8000
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D8
U 1 1 5F9873EE
P 4050 8150
F 0 "D8" H 3800 8100 50  0000 C CNN
F 1 "LED" H 3600 8100 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 4050 8150 50  0001 C CNN
F 3 "~" H 4050 8150 50  0001 C CNN
	1    4050 8150
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D7
U 1 1 5F9873F8
P 4050 8300
F 0 "D7" H 3800 8250 50  0000 C CNN
F 1 "LED" H 3600 8250 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 4050 8300 50  0001 C CNN
F 3 "~" H 4050 8300 50  0001 C CNN
	1    4050 8300
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D6
U 1 1 5F987402
P 4050 8450
F 0 "D6" H 3800 8400 50  0000 C CNN
F 1 "LED" H 3600 8400 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 4050 8450 50  0001 C CNN
F 3 "~" H 4050 8450 50  0001 C CNN
	1    4050 8450
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D5
U 1 1 5F98740C
P 4050 8600
F 0 "D5" H 3800 8550 50  0000 C CNN
F 1 "LED" H 3600 8550 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 4050 8600 50  0001 C CNN
F 3 "~" H 4050 8600 50  0001 C CNN
	1    4050 8600
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D4
U 1 1 5F987416
P 4050 8750
F 0 "D4" H 3800 8700 50  0000 C CNN
F 1 "LED" H 3600 8700 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 4050 8750 50  0001 C CNN
F 3 "~" H 4050 8750 50  0001 C CNN
	1    4050 8750
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D3
U 1 1 5F987420
P 4050 8900
F 0 "D3" H 3800 8850 50  0000 C CNN
F 1 "LED" H 3600 8850 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 4050 8900 50  0001 C CNN
F 3 "~" H 4050 8900 50  0001 C CNN
	1    4050 8900
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D2
U 1 1 5F98742A
P 4050 9050
F 0 "D2" H 3800 9000 50  0000 C CNN
F 1 "LED" H 3600 9000 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 4050 9050 50  0001 C CNN
F 3 "~" H 4050 9050 50  0001 C CNN
	1    4050 9050
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D1
U 1 1 5F987434
P 4050 9200
F 0 "D1" H 3800 9150 50  0000 C CNN
F 1 "LED" H 3600 9150 50  0000 C CNN
F 2 "sixteen-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 4050 9200 50  0001 C CNN
F 3 "~" H 4050 9200 50  0001 C CNN
	1    4050 9200
	-1   0    0    1   
$EndComp
$Comp
L 74xx:74HC04 U1
U 1 1 5F99EB01
P 1400 2600
F 0 "U1" H 1400 2917 50  0000 C CNN
F 1 "74HC04" H 1400 2826 50  0000 C CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket" H 1400 2600 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 1400 2600 50  0001 C CNN
	1    1400 2600
	1    0    0    -1  
$EndComp
$Comp
L 74xx:74HC04 U1
U 2 1 5F99F922
P 11550 2100
F 0 "U1" H 11550 2417 50  0000 C CNN
F 1 "74HC04" H 11550 2326 50  0000 C CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket" H 11550 2100 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 11550 2100 50  0001 C CNN
	2    11550 2100
	1    0    0    -1  
$EndComp
$Comp
L 74xx:74HC04 U1
U 3 1 5F9A188D
P 14950 1550
F 0 "U1" H 14950 1867 50  0000 C CNN
F 1 "74HC04" H 14950 1776 50  0000 C CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket" H 14950 1550 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 14950 1550 50  0001 C CNN
	3    14950 1550
	1    0    0    -1  
$EndComp
$Comp
L 74xx:74HC04 U1
U 4 1 5F9A32BA
P 14950 1000
F 0 "U1" H 14950 1317 50  0000 C CNN
F 1 "74HC04" H 14950 1226 50  0000 C CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket" H 14950 1000 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 14950 1000 50  0001 C CNN
	4    14950 1000
	1    0    0    -1  
$EndComp
$Comp
L 74xx:74HC04 U1
U 5 1 5F9A4E9B
P 14000 1550
F 0 "U1" H 14000 1867 50  0000 C CNN
F 1 "74HC04" H 14000 1776 50  0000 C CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket" H 14000 1550 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 14000 1550 50  0001 C CNN
	5    14000 1550
	1    0    0    -1  
$EndComp
$Comp
L 74xx:74HC04 U1
U 6 1 5F9A790D
P 14000 1000
F 0 "U1" H 14000 1317 50  0000 C CNN
F 1 "74HC04" H 14000 1226 50  0000 C CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket" H 14000 1000 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 14000 1000 50  0001 C CNN
	6    14000 1000
	1    0    0    -1  
$EndComp
$Comp
L 74xx:74HC04 U1
U 7 1 5F9A95E8
P 12500 1300
F 0 "U1" H 12730 1346 50  0000 L CNN
F 1 "74HC04" H 12730 1255 50  0000 L CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket" H 12500 1300 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 12500 1300 50  0001 C CNN
	7    12500 1300
	1    0    0    -1  
$EndComp
$Comp
L sixteen-bit-computer:74HCT245 U6
U 1 1 5F9AAB74
P 1800 9350
F 0 "U6" H 1550 10050 50  0000 C CNN
F 1 "74HCT245" H 2050 10050 50  0000 C CNN
F 2 "Package_DIP:DIP-20_W7.62mm_Socket" H 1450 9350 50  0001 C CNN
F 3 "" H 1450 9350 50  0001 C CNN
	1    1800 9350
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x16_Female J1
U 1 1 5F9AD90D
P 13100 3000
F 0 "J1" V 13150 2150 50  0000 L CNN
F 1 "ACC_CONTENTS" V 13150 3150 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x16_P2.54mm_Horizontal" H 13100 3000 50  0001 C CNN
F 3 "~" H 13100 3000 50  0001 C CNN
	1    13100 3000
	0    1    -1   0   
$EndComp
$Comp
L Device:C C2
U 1 1 5F9F7FBB
P 3950 2750
F 0 "C2" H 4065 2796 50  0000 L CNN
F 1 "0.1uF" H 4065 2705 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 3988 2600 50  0001 C CNN
F 3 "~" H 3950 2750 50  0001 C CNN
	1    3950 2750
	1    0    0    -1  
$EndComp
$Comp
L Device:C C3
U 1 1 5F9F984E
P 6150 2750
F 0 "C3" H 6265 2796 50  0000 L CNN
F 1 "0.1uF" H 6265 2705 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 6188 2600 50  0001 C CNN
F 3 "~" H 6150 2750 50  0001 C CNN
	1    6150 2750
	1    0    0    -1  
$EndComp
$Comp
L Device:C C5
U 1 1 5F9F9D5F
P 8450 2750
F 0 "C5" H 8565 2796 50  0000 L CNN
F 1 "0.1uF" H 8565 2705 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 8488 2600 50  0001 C CNN
F 3 "~" H 8450 2750 50  0001 C CNN
	1    8450 2750
	1    0    0    -1  
$EndComp
$Comp
L Device:C C9
U 1 1 5F9FA306
P 10800 2750
F 0 "C9" H 10915 2796 50  0000 L CNN
F 1 "0.1uF" H 10915 2705 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 10838 2600 50  0001 C CNN
F 3 "~" H 10800 2750 50  0001 C CNN
	1    10800 2750
	1    0    0    -1  
$EndComp
$Comp
L Device:C C8
U 1 1 5F9FAA0F
P 3800 5600
F 0 "C8" H 3915 5646 50  0000 L CNN
F 1 "0.1uF" H 3915 5555 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 3838 5450 50  0001 C CNN
F 3 "~" H 3800 5600 50  0001 C CNN
	1    3800 5600
	1    0    0    -1  
$EndComp
$Comp
L Device:C C10
U 1 1 5F9FB868
P 6250 5600
F 0 "C10" H 6365 5646 50  0000 L CNN
F 1 "0.1uF" H 6365 5555 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 6288 5450 50  0001 C CNN
F 3 "~" H 6250 5600 50  0001 C CNN
	1    6250 5600
	1    0    0    -1  
$EndComp
$Comp
L Device:C C11
U 1 1 5F9FBE7F
P 10800 5600
F 0 "C11" H 10915 5646 50  0000 L CNN
F 1 "0.1uF" H 10915 5555 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 10838 5450 50  0001 C CNN
F 3 "~" H 10800 5600 50  0001 C CNN
	1    10800 5600
	1    0    0    -1  
$EndComp
$Comp
L Device:C C7
U 1 1 5F9FC4C8
P 8550 5600
F 0 "C7" H 8665 5646 50  0000 L CNN
F 1 "0.1uF" H 8665 5555 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 8588 5450 50  0001 C CNN
F 3 "~" H 8550 5600 50  0001 C CNN
	1    8550 5600
	1    0    0    -1  
$EndComp
$Comp
L Device:C C6
U 1 1 5F9FCAC5
P 2950 9400
F 0 "C6" H 3065 9446 50  0000 L CNN
F 1 "0.1uF" H 3065 9355 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 2988 9250 50  0001 C CNN
F 3 "~" H 2950 9400 50  0001 C CNN
	1    2950 9400
	1    0    0    -1  
$EndComp
$Comp
L Device:C C1
U 1 1 5F9FD214
P 13300 1250
F 0 "C1" H 13415 1296 50  0000 L CNN
F 1 "0.1uF" H 13415 1205 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 13338 1100 50  0001 C CNN
F 3 "~" H 13300 1250 50  0001 C CNN
	1    13300 1250
	1    0    0    -1  
$EndComp
$Comp
L Device:C C4
U 1 1 5F9FE15C
P 3000 7250
F 0 "C4" H 3115 7296 50  0000 L CNN
F 1 "0.1uF" H 3115 7205 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 3038 7100 50  0001 C CNN
F 3 "~" H 3000 7250 50  0001 C CNN
	1    3000 7250
	1    0    0    -1  
$EndComp
$Comp
L Device:R_Network08_US RN1
U 1 1 5F9FF6F6
P 5200 7350
F 0 "RN1" V 4583 7350 50  0000 C CNN
F 1 "R_Network08_US" V 4674 7350 50  0000 C CNN
F 2 "Resistor_THT:R_Array_SIP9" V 5675 7350 50  0001 C CNN
F 3 "http://www.vishay.com/docs/31509/csc.pdf" H 5200 7350 50  0001 C CNN
	1    5200 7350
	0    1    1    0   
$EndComp
$Comp
L Device:R_Network08_US RN2
U 1 1 5FA03E7C
P 5200 8550
F 0 "RN2" V 4583 8550 50  0000 C CNN
F 1 "R_Network08_US" V 4674 8550 50  0000 C CNN
F 2 "Resistor_THT:R_Array_SIP9" V 5675 8550 50  0001 C CNN
F 3 "http://www.vishay.com/docs/31509/csc.pdf" H 5200 8550 50  0001 C CNN
	1    5200 8550
	0    1    1    0   
$EndComp
$Comp
L Connector:Conn_01x18_Female J2
U 1 1 5FA0675E
P 15300 3000
F 0 "J2" V 15350 2050 50  0000 L CNN
F 1 "RES_AEQB_CRYBRW_OUT" V 15350 2950 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x18_P2.54mm_Horizontal" H 15300 3000 50  0001 C CNN
F 3 "~" H 15300 3000 50  0001 C CNN
	1    15300 3000
	0    1    -1   0   
$EndComp
$Comp
L Device:R_US R1
U 1 1 5FA0CDAB
P 11150 3300
F 0 "R1" H 11218 3346 50  0000 L CNN
F 1 "1K" H 11218 3255 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 11190 3290 50  0001 C CNN
F 3 "~" H 11150 3300 50  0001 C CNN
	1    11150 3300
	1    0    0    -1  
$EndComp
$Comp
L power:VCC #PWR01
U 1 1 5FA0E4B4
P 15600 2150
F 0 "#PWR01" H 15600 2000 50  0001 C CNN
F 1 "VCC" H 15617 2323 50  0000 C CNN
F 2 "" H 15600 2150 50  0001 C CNN
F 3 "" H 15600 2150 50  0001 C CNN
	1    15600 2150
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR02
U 1 1 5FA1038F
P 15600 2500
F 0 "#PWR02" H 15600 2250 50  0001 C CNN
F 1 "GND" H 15605 2327 50  0000 C CNN
F 2 "" H 15600 2500 50  0001 C CNN
F 3 "" H 15600 2500 50  0001 C CNN
	1    15600 2500
	1    0    0    -1  
$EndComp
$Comp
L power:PWR_FLAG #FLG01
U 1 1 5FA12019
P 15600 2150
F 0 "#FLG01" H 15600 2225 50  0001 C CNN
F 1 "PWR_FLAG" V 15600 2278 50  0000 L CNN
F 2 "" H 15600 2150 50  0001 C CNN
F 3 "~" H 15600 2150 50  0001 C CNN
	1    15600 2150
	0    1    1    0   
$EndComp
$Comp
L power:PWR_FLAG #FLG02
U 1 1 5FA13D2F
P 15600 2500
F 0 "#FLG02" H 15600 2575 50  0001 C CNN
F 1 "PWR_FLAG" V 15600 2628 50  0000 L CNN
F 2 "" H 15600 2500 50  0001 C CNN
F 3 "~" H 15600 2500 50  0001 C CNN
	1    15600 2500
	0    1    1    0   
$EndComp
Text Label 15550 2150 2    50   ~ 0
VCC
Text Label 15550 2500 2    50   ~ 0
GND
Connection ~ 15600 2150
Connection ~ 15600 2500
Text Label 6350 8750 0    50   ~ 0
BUS_00
Text Label 6350 8650 0    50   ~ 0
BUS_01
Text Label 6350 8550 0    50   ~ 0
BUS_02
Text Label 6350 8450 0    50   ~ 0
BUS_03
Text Label 6350 8350 0    50   ~ 0
BUS_04
Text Label 6350 8250 0    50   ~ 0
BUS_05
Text Label 6350 8150 0    50   ~ 0
BUS_06
Text Label 6350 8050 0    50   ~ 0
BUS_07
Text Label 6350 7950 0    50   ~ 0
BUS_08
Text Label 6350 7850 0    50   ~ 0
BUS_09
Text Label 6350 7750 0    50   ~ 0
BUS_10
Text Label 6350 7650 0    50   ~ 0
BUS_11
Text Label 6350 7550 0    50   ~ 0
BUS_12
Text Label 6350 7450 0    50   ~ 0
BUS_13
Text Label 6350 7350 0    50   ~ 0
BUS_14
Text Label 6350 7250 0    50   ~ 0
BUS_15
Text Label 14150 4650 0    50   ~ 0
VCC
Wire Wire Line
	14150 4750 14150 4650
Wire Wire Line
	14150 4950 14150 4850
Text Label 14150 4850 0    50   ~ 0
GND
NoConn ~ 14150 5150
NoConn ~ 14150 5350
NoConn ~ 14150 5550
Text Label 16050 5250 0    50   ~ 0
S0
Text Label 16050 5350 0    50   ~ 0
S1
Text Label 16050 5450 0    50   ~ 0
S2
Text Label 16050 5550 0    50   ~ 0
S3
Text Label 2250 2000 2    50   ~ 0
S0
Text Label 2250 2100 2    50   ~ 0
S1
Text Label 2250 2200 2    50   ~ 0
S2
Text Label 2250 2300 2    50   ~ 0
S3
Text Label 4500 2000 2    50   ~ 0
S0
Text Label 4500 2100 2    50   ~ 0
S1
Text Label 4500 2200 2    50   ~ 0
S2
Text Label 4500 2300 2    50   ~ 0
S3
Text Label 6750 2000 2    50   ~ 0
S0
Text Label 6750 2100 2    50   ~ 0
S1
Text Label 6750 2200 2    50   ~ 0
S2
Text Label 6750 2300 2    50   ~ 0
S3
Text Label 9050 2000 2    50   ~ 0
S0
Text Label 9050 2100 2    50   ~ 0
S1
Text Label 9050 2200 2    50   ~ 0
S2
Text Label 9050 2300 2    50   ~ 0
S3
Text Label 3450 1400 0    50   ~ 0
RES_00
Text Label 3450 1500 0    50   ~ 0
RES_01
Text Label 3450 1600 0    50   ~ 0
RES_02
Text Label 3450 1700 0    50   ~ 0
RES_03
Text Label 5700 1400 0    50   ~ 0
RES_04
Text Label 5700 1500 0    50   ~ 0
RES_05
Text Label 5700 1600 0    50   ~ 0
RES_06
Text Label 5700 1700 0    50   ~ 0
RES_07
Text Label 7950 1400 0    50   ~ 0
RES_08
Text Label 7950 1500 0    50   ~ 0
RES_09
Text Label 7950 1600 0    50   ~ 0
RES_10
Text Label 7950 1700 0    50   ~ 0
RES_11
Text Label 10250 1400 0    50   ~ 0
RES_12
Text Label 10250 1500 0    50   ~ 0
RES_13
Text Label 10250 1600 0    50   ~ 0
RES_14
Text Label 10250 1700 0    50   ~ 0
RES_15
NoConn ~ 10250 2400
NoConn ~ 10250 2500
NoConn ~ 7950 2400
NoConn ~ 7950 2500
NoConn ~ 5700 2400
NoConn ~ 5700 2500
NoConn ~ 3450 2400
NoConn ~ 3450 2500
Text Label 13800 3200 3    50   ~ 0
ACC_00
Text Label 13700 3200 3    50   ~ 0
ACC_01
Text Label 13600 3200 3    50   ~ 0
ACC_02
Text Label 13500 3200 3    50   ~ 0
ACC_03
Text Label 13400 3200 3    50   ~ 0
ACC_04
Text Label 13200 3200 3    50   ~ 0
ACC_06
Text Label 13300 3200 3    50   ~ 0
ACC_05
Text Label 13100 3200 3    50   ~ 0
ACC_07
Text Label 13000 3200 3    50   ~ 0
ACC_08
Text Label 12900 3200 3    50   ~ 0
ACC_09
Text Label 12800 3200 3    50   ~ 0
ACC_10
Text Label 12700 3200 3    50   ~ 0
ACC_11
Text Label 12600 3200 3    50   ~ 0
ACC_12
Text Label 12500 3200 3    50   ~ 0
ACC_13
Text Label 12400 3200 3    50   ~ 0
ACC_14
Text Label 12300 3200 3    50   ~ 0
ACC_15
Text Label 1250 9800 2    50   ~ 0
RES_00
Text Label 1250 9700 2    50   ~ 0
RES_01
Text Label 1250 9600 2    50   ~ 0
RES_02
Text Label 1250 9500 2    50   ~ 0
RES_03
Text Label 1250 9400 2    50   ~ 0
RES_04
Text Label 1250 9300 2    50   ~ 0
RES_05
Text Label 1250 9200 2    50   ~ 0
RES_06
Text Label 1250 9100 2    50   ~ 0
RES_07
Text Label 1250 7650 2    50   ~ 0
RES_08
Text Label 1250 7550 2    50   ~ 0
RES_09
Text Label 1250 7450 2    50   ~ 0
RES_10
Text Label 1250 7350 2    50   ~ 0
RES_11
Text Label 1250 7250 2    50   ~ 0
RES_12
Text Label 1250 7150 2    50   ~ 0
RES_13
Text Label 1250 7050 2    50   ~ 0
RES_14
Text Label 1250 6950 2    50   ~ 0
RES_15
Text Label 3300 4750 0    50   ~ 0
SEL_00
Text Label 3300 4850 0    50   ~ 0
SEL_01
Text Label 3300 4950 0    50   ~ 0
SEL_02
Text Label 3300 5050 0    50   ~ 0
SEL_03
Text Label 5750 4750 0    50   ~ 0
SEL_04
Text Label 5750 4850 0    50   ~ 0
SEL_05
Text Label 5750 4950 0    50   ~ 0
SEL_06
Text Label 5750 5050 0    50   ~ 0
SEL_07
Text Label 8050 4750 0    50   ~ 0
SEL_08
Text Label 8050 4850 0    50   ~ 0
SEL_09
Text Label 8050 4950 0    50   ~ 0
SEL_10
Text Label 10300 4750 0    50   ~ 0
SEL_12
Text Label 10300 4850 0    50   ~ 0
SEL_13
Text Label 10300 4950 0    50   ~ 0
SEL_14
Text Label 10300 5050 0    50   ~ 0
SEL_15
Text Label 8050 5050 0    50   ~ 0
SEL_11
Text Label 16050 5150 0    50   ~ 0
A_IS_BUS
Text Label 16050 5650 0    50   ~ 0
M
Text Label 16050 5750 0    50   ~ 0
CARRY_IN
Text Label 1100 2600 2    50   ~ 0
CARRY_IN
Text Label 2250 2600 2    50   ~ 0
CARRY_IN_BAR
Text Label 2250 2500 2    50   ~ 0
M
Text Label 4500 2500 2    50   ~ 0
M
Text Label 6750 2500 2    50   ~ 0
M
Text Label 9050 2500 2    50   ~ 0
M
Text Label 2300 4350 2    50   ~ 0
ACC_00
Text Label 2300 4450 2    50   ~ 0
ACC_01
Text Label 2300 4550 2    50   ~ 0
ACC_02
Text Label 2300 4650 2    50   ~ 0
ACC_03
Text Label 4750 4350 2    50   ~ 0
ACC_04
Text Label 4750 4550 2    50   ~ 0
ACC_06
Text Label 4750 4450 2    50   ~ 0
ACC_05
Text Label 4750 4650 2    50   ~ 0
ACC_07
Text Label 7050 4350 2    50   ~ 0
ACC_08
Text Label 7050 4450 2    50   ~ 0
ACC_09
Text Label 7050 4550 2    50   ~ 0
ACC_10
Text Label 7050 4650 2    50   ~ 0
ACC_11
Text Label 9300 4350 2    50   ~ 0
ACC_12
Text Label 9300 4450 2    50   ~ 0
ACC_13
Text Label 9300 4550 2    50   ~ 0
ACC_14
Text Label 9300 4650 2    50   ~ 0
ACC_15
Text Label 9050 1200 2    50   ~ 0
SEL_12
Text Label 9050 1300 2    50   ~ 0
SEL_13
Text Label 9050 1400 2    50   ~ 0
SEL_14
Text Label 9050 1500 2    50   ~ 0
SEL_15
Text Label 6750 1200 2    50   ~ 0
SEL_08
Text Label 6750 1300 2    50   ~ 0
SEL_09
Text Label 6750 1400 2    50   ~ 0
SEL_10
Text Label 6750 1500 2    50   ~ 0
SEL_11
Text Label 4500 1200 2    50   ~ 0
SEL_04
Text Label 4500 1300 2    50   ~ 0
SEL_05
Text Label 4500 1400 2    50   ~ 0
SEL_06
Text Label 4500 1500 2    50   ~ 0
SEL_07
Text Label 2250 1200 2    50   ~ 0
SEL_00
Text Label 2250 1300 2    50   ~ 0
SEL_01
Text Label 2250 1400 2    50   ~ 0
SEL_02
Text Label 2250 1500 2    50   ~ 0
SEL_03
Wire Wire Line
	1700 2600 2250 2600
Wire Wire Line
	3450 2100 4300 2100
Wire Wire Line
	4300 2100 4300 2600
Wire Wire Line
	4300 2600 4500 2600
Wire Wire Line
	5700 2100 6550 2100
Wire Wire Line
	6550 2100 6550 2600
Wire Wire Line
	6550 2600 6750 2600
Wire Wire Line
	7950 2100 8850 2100
Wire Wire Line
	3450 2200 3700 2200
Wire Wire Line
	3700 2200 3700 3150
Wire Wire Line
	3700 3150 5950 3150
Wire Wire Line
	11150 3150 11150 3000
Wire Wire Line
	11150 2200 10250 2200
Wire Wire Line
	7950 2200 8200 2200
Wire Wire Line
	8200 2200 8200 3150
Wire Wire Line
	8200 3150 11150 3150
Wire Wire Line
	5700 2200 5950 2200
Wire Wire Line
	5950 2200 5950 3150
Connection ~ 11150 3150
Wire Wire Line
	5950 3150 8200 3150
Connection ~ 5950 3150
Connection ~ 8200 3150
Text Label 2850 2900 3    50   ~ 0
GND
Text Label 5100 2900 3    50   ~ 0
GND
Text Label 7350 2900 3    50   ~ 0
GND
Text Label 9650 2900 3    50   ~ 0
GND
Wire Wire Line
	11250 2100 10250 2100
Text Label 12050 2100 0    50   ~ 0
CARRY_BORROW_OUT
Text Label 11150 3450 3    50   ~ 0
VCC
Text Label 11600 3000 0    50   ~ 0
A_EQ_B
Wire Wire Line
	11150 3000 11600 3000
Connection ~ 11150 3000
Wire Wire Line
	11150 3000 11150 2200
Wire Wire Line
	11850 2100 12050 2100
Text Label 9650 900  1    50   ~ 0
VCC
Text Label 7350 900  1    50   ~ 0
VCC
Text Label 5100 900  1    50   ~ 0
VCC
Text Label 2850 900  1    50   ~ 0
VCC
Wire Wire Line
	3950 2600 3950 900 
Wire Wire Line
	3950 900  2850 900 
Wire Wire Line
	3950 2900 2850 2900
Wire Wire Line
	6150 2600 6150 900 
Wire Wire Line
	6150 900  5100 900 
Wire Wire Line
	6150 2900 5100 2900
Wire Wire Line
	8450 2600 8450 900 
Wire Wire Line
	8450 900  7350 900 
Wire Wire Line
	8450 2900 7350 2900
Wire Wire Line
	10800 2600 10800 900 
Wire Wire Line
	10800 900  9650 900 
Wire Wire Line
	10800 2900 9650 2900
Wire Wire Line
	2300 5350 1900 5350
Wire Wire Line
	1900 5350 1900 5750
Wire Wire Line
	1900 5750 2800 5750
Wire Wire Line
	4750 5350 4350 5350
Wire Wire Line
	4350 5350 4350 5750
Wire Wire Line
	4350 5750 5250 5750
Wire Wire Line
	7050 5350 6650 5350
Wire Wire Line
	6650 5350 6650 5750
Wire Wire Line
	9300 5350 8900 5350
Wire Wire Line
	8900 5350 8900 5750
Wire Wire Line
	8900 5750 9800 5750
Text Label 2300 5450 2    50   ~ 0
A_IS_BUS
Text Label 4750 5450 2    50   ~ 0
A_IS_BUS
Text Label 7050 5450 2    50   ~ 0
A_IS_BUS
Text Label 9300 5450 2    50   ~ 0
A_IS_BUS
Text Label 2800 5750 3    50   ~ 0
GND
Text Label 5250 5750 3    50   ~ 0
GND
Text Label 7550 5750 3    50   ~ 0
GND
Text Label 9800 5750 3    50   ~ 0
GND
Text Label 9800 4050 1    50   ~ 0
VCC
Text Label 7550 4050 1    50   ~ 0
VCC
Text Label 5250 4050 1    50   ~ 0
VCC
Text Label 2800 4050 1    50   ~ 0
VCC
Wire Wire Line
	2800 4050 3800 4050
Wire Wire Line
	3800 4050 3800 5450
Wire Wire Line
	3800 5750 2800 5750
Connection ~ 2800 5750
Wire Wire Line
	5250 4050 6250 4050
Wire Wire Line
	6250 4050 6250 5450
Wire Wire Line
	6250 5750 5250 5750
Connection ~ 5250 5750
Wire Wire Line
	7550 4050 8550 4050
Wire Wire Line
	8550 4050 8550 5450
Wire Wire Line
	6650 5750 7550 5750
Connection ~ 7550 5750
Wire Wire Line
	7550 5750 8550 5750
Wire Wire Line
	9800 4050 10800 4050
Wire Wire Line
	10800 4050 10800 5450
Wire Wire Line
	10800 5750 9800 5750
Connection ~ 9800 5750
Text Label 2350 9800 0    50   ~ 0
RES_BUF_00
Text Label 2350 9700 0    50   ~ 0
RES_BUF_01
Text Label 2350 9600 0    50   ~ 0
RES_BUF_02
Text Label 2350 9500 0    50   ~ 0
RES_BUF_03
Text Label 2350 9400 0    50   ~ 0
RES_BUF_04
Text Label 2350 9300 0    50   ~ 0
RES_BUF_05
Text Label 2350 9200 0    50   ~ 0
RES_BUF_06
Text Label 2350 9100 0    50   ~ 0
RES_BUF_07
Text Label 2350 7650 0    50   ~ 0
RES_BUF_08
Text Label 2350 7550 0    50   ~ 0
RES_BUF_09
Text Label 2350 7450 0    50   ~ 0
RES_BUF_10
Text Label 2350 7350 0    50   ~ 0
RES_BUF_11
Text Label 2350 7250 0    50   ~ 0
RES_BUF_12
Text Label 2350 7150 0    50   ~ 0
RES_BUF_13
Text Label 2350 7050 0    50   ~ 0
RES_BUF_14
Text Label 2350 6950 0    50   ~ 0
RES_BUF_15
Wire Wire Line
	1250 8950 1000 8950
Wire Wire Line
	1000 8950 1000 8400
Wire Wire Line
	1000 8400 1800 8400
Text Label 1800 10150 3    50   ~ 0
GND
Text Label 1800 8000 3    50   ~ 0
GND
Text Label 1800 6250 1    50   ~ 0
VCC
Text Label 1800 8400 1    50   ~ 0
VCC
Wire Wire Line
	1250 6800 1000 6800
Wire Wire Line
	1000 6800 1000 6250
Wire Wire Line
	3000 6250 3000 7100
Wire Wire Line
	3000 7400 3000 8000
Wire Wire Line
	3000 8000 1800 8000
Wire Wire Line
	1800 8400 2950 8400
Wire Wire Line
	2950 8400 2950 9250
Connection ~ 1800 8400
Wire Wire Line
	2950 9550 2950 10150
Wire Wire Line
	2950 10150 1800 10150
Text Label 3900 8000 2    50   ~ 0
RES_BUF_08
Text Label 3900 7850 2    50   ~ 0
RES_BUF_09
Text Label 3900 7700 2    50   ~ 0
RES_BUF_10
Text Label 3900 7550 2    50   ~ 0
RES_BUF_11
Text Label 3900 7400 2    50   ~ 0
RES_BUF_12
Text Label 3900 7250 2    50   ~ 0
RES_BUF_13
Text Label 3900 7100 2    50   ~ 0
RES_BUF_14
Text Label 3900 6950 2    50   ~ 0
RES_BUF_15
Text Label 3900 9200 2    50   ~ 0
RES_BUF_00
Text Label 3900 9050 2    50   ~ 0
RES_BUF_01
Text Label 3900 8900 2    50   ~ 0
RES_BUF_02
Text Label 3900 8750 2    50   ~ 0
RES_BUF_03
Text Label 3900 8600 2    50   ~ 0
RES_BUF_04
Text Label 3900 8450 2    50   ~ 0
RES_BUF_05
Text Label 3900 8300 2    50   ~ 0
RES_BUF_06
Text Label 3900 8150 2    50   ~ 0
RES_BUF_07
Wire Wire Line
	4200 6950 5000 6950
Wire Wire Line
	4200 7100 4600 7100
Wire Wire Line
	4600 7100 4600 7050
Wire Wire Line
	4600 7050 5000 7050
Wire Wire Line
	4200 7250 4650 7250
Wire Wire Line
	4650 7250 4650 7150
Wire Wire Line
	4650 7150 5000 7150
Wire Wire Line
	4200 7400 4700 7400
Wire Wire Line
	4700 7400 4700 7250
Wire Wire Line
	4700 7250 5000 7250
Wire Wire Line
	4200 7550 4750 7550
Wire Wire Line
	4750 7550 4750 7350
Wire Wire Line
	4750 7350 5000 7350
Wire Wire Line
	4200 7700 4800 7700
Wire Wire Line
	4800 7700 4800 7450
Wire Wire Line
	4800 7450 5000 7450
Wire Wire Line
	5000 7550 4850 7550
Wire Wire Line
	4850 7550 4850 7850
Wire Wire Line
	4850 7850 4200 7850
Wire Wire Line
	4200 8000 4900 8000
Wire Wire Line
	4900 8000 4900 7650
Wire Wire Line
	4900 7650 5000 7650
Wire Wire Line
	4200 8150 5000 8150
Wire Wire Line
	4200 8300 4600 8300
Wire Wire Line
	4600 8300 4600 8250
Wire Wire Line
	4600 8250 5000 8250
Wire Wire Line
	4200 8450 4650 8450
Wire Wire Line
	4650 8450 4650 8350
Wire Wire Line
	4650 8350 5000 8350
Wire Wire Line
	4200 8600 4700 8600
Wire Wire Line
	4700 8600 4700 8450
Wire Wire Line
	4700 8450 5000 8450
Wire Wire Line
	4200 8750 4750 8750
Wire Wire Line
	4750 8750 4750 8550
Wire Wire Line
	4750 8550 5000 8550
Wire Wire Line
	4200 8900 4800 8900
Wire Wire Line
	4800 8900 4800 8650
Wire Wire Line
	4800 8650 5000 8650
Wire Wire Line
	5000 8750 4850 8750
Wire Wire Line
	4850 8750 4850 9050
Wire Wire Line
	4850 9050 4200 9050
Wire Wire Line
	4200 9200 4900 9200
Wire Wire Line
	4900 9200 4900 8850
Wire Wire Line
	4900 8850 5000 8850
Text Label 5400 6950 0    50   ~ 0
GND
Text Label 5400 8150 0    50   ~ 0
GND
Text Label 12500 800  1    50   ~ 0
VCC
Text Label 12500 1800 3    50   ~ 0
GND
Wire Wire Line
	12500 800  13300 800 
Wire Wire Line
	13300 800  13300 1100
Wire Wire Line
	13300 1400 13300 1800
Wire Wire Line
	13300 1800 12500 1800
Wire Wire Line
	13300 1800 13700 1800
Connection ~ 13300 1800
NoConn ~ 14300 1000
NoConn ~ 14300 1550
NoConn ~ 15250 1000
NoConn ~ 15250 1550
NoConn ~ 16050 4050
NoConn ~ 16050 4150
NoConn ~ 16050 4250
NoConn ~ 16050 4350
NoConn ~ 16050 4450
NoConn ~ 16050 4550
NoConn ~ 16050 4650
NoConn ~ 16050 4750
NoConn ~ 16050 4850
NoConn ~ 16050 4950
NoConn ~ 16050 5050
NoConn ~ 16050 5850
NoConn ~ 16050 5950
NoConn ~ 16050 6050
NoConn ~ 16050 6150
NoConn ~ 16050 6250
NoConn ~ 16050 6350
NoConn ~ 16050 6450
NoConn ~ 16050 6650
NoConn ~ 16050 6550
NoConn ~ 16050 6750
NoConn ~ 16050 6850
NoConn ~ 16050 6950
NoConn ~ 16050 7050
NoConn ~ 16050 7150
Text Label 14500 3200 3    50   ~ 0
CARRY_BORROW_OUT
Text Label 14400 3200 3    50   ~ 0
A_EQ_B
Wire Wire Line
	8850 2600 9050 2600
Wire Wire Line
	8850 2100 8850 2600
$Comp
L sixteen-bit-computer:74LS181 U2
U 1 1 5FEA7109
P 2850 1900
F 0 "U2" H 2500 2750 50  0000 C CNN
F 1 "74LS181" H 3100 2750 50  0000 C CNN
F 2 "Package_DIP:DIP-24_W15.24mm_Socket" H 2850 1900 50  0001 C CNN
F 3 "74xx/74F181.pdf" H 2850 1900 50  0001 C CNN
	1    2850 1900
	1    0    0    -1  
$EndComp
$Comp
L sixteen-bit-computer:74LS181 U3
U 1 1 5FEA96F4
P 5100 1900
F 0 "U3" H 4750 2750 50  0000 C CNN
F 1 "74LS181" H 5350 2750 50  0000 C CNN
F 2 "Package_DIP:DIP-24_W15.24mm_Socket" H 5100 1900 50  0001 C CNN
F 3 "74xx/74F181.pdf" H 5100 1900 50  0001 C CNN
	1    5100 1900
	1    0    0    -1  
$EndComp
$Comp
L sixteen-bit-computer:74LS181 U5
U 1 1 5FEAAD52
P 7350 1900
F 0 "U5" H 7000 2750 50  0000 C CNN
F 1 "74LS181" H 7600 2750 50  0000 C CNN
F 2 "Package_DIP:DIP-24_W15.24mm_Socket" H 7350 1900 50  0001 C CNN
F 3 "74xx/74F181.pdf" H 7350 1900 50  0001 C CNN
	1    7350 1900
	1    0    0    -1  
$EndComp
$Comp
L sixteen-bit-computer:74LS181 U7
U 1 1 5FEACAD4
P 9650 1900
F 0 "U7" H 9300 2750 50  0000 C CNN
F 1 "74LS181" H 9900 2750 50  0000 C CNN
F 2 "Package_DIP:DIP-24_W15.24mm_Socket" H 9650 1900 50  0001 C CNN
F 3 "74xx/74F181.pdf" H 9650 1900 50  0001 C CNN
	1    9650 1900
	1    0    0    -1  
$EndComp
$Comp
L Device:CP C12
U 1 1 5FC1FB19
P 14950 2300
F 0 "C12" H 15068 2346 50  0000 L CNN
F 1 "33uF" H 15068 2255 50  0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D6.3mm_P2.50mm" H 14988 2150 50  0001 C CNN
F 3 "~" H 14950 2300 50  0001 C CNN
	1    14950 2300
	1    0    0    -1  
$EndComp
Wire Wire Line
	14950 2150 15600 2150
Wire Wire Line
	14950 2450 14950 2500
Wire Wire Line
	14950 2500 15600 2500
$Comp
L Device:CP C14
U 1 1 5FC812BA
P 14500 2300
F 0 "C14" H 14618 2346 50  0000 L CNN
F 1 "33uF" H 14618 2255 50  0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D6.3mm_P2.50mm" H 14538 2150 50  0001 C CNN
F 3 "~" H 14500 2300 50  0001 C CNN
	1    14500 2300
	1    0    0    -1  
$EndComp
$Comp
L Device:CP C13
U 1 1 5FC81852
P 14050 2300
F 0 "C13" H 14168 2346 50  0000 L CNN
F 1 "33uF" H 14168 2255 50  0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D6.3mm_P2.50mm" H 14088 2150 50  0001 C CNN
F 3 "~" H 14050 2300 50  0001 C CNN
	1    14050 2300
	1    0    0    -1  
$EndComp
Wire Wire Line
	14050 2150 14500 2150
Connection ~ 14950 2150
Connection ~ 14500 2150
Wire Wire Line
	14500 2150 14950 2150
Wire Wire Line
	14950 2500 14500 2500
Wire Wire Line
	14050 2500 14050 2450
Connection ~ 14950 2500
Wire Wire Line
	14500 2450 14500 2500
Connection ~ 14500 2500
Wire Wire Line
	14500 2500 14050 2500
Connection ~ 13700 1550
Wire Wire Line
	13700 1550 13700 1800
Wire Wire Line
	13700 1000 13700 1550
Wire Wire Line
	13700 1800 14650 1800
Wire Wire Line
	14650 1800 14650 1550
Connection ~ 13700 1800
Connection ~ 14650 1550
Wire Wire Line
	14650 1550 14650 1000
$Comp
L sixteen-bit-computer:74HC245 U12
U 1 1 62EA6F4C
P 8150 7200
F 0 "U12" H 7900 7900 50  0000 C CNN
F 1 "74HC245" H 8400 7900 50  0000 C CNN
F 2 "Package_DIP:DIP-20_W7.62mm_Socket" H 7800 7200 50  0001 C CNN
F 3 "https://www.ti.com/lit/ds/symlink/cd74hc245.pdf" H 7800 7200 50  0001 C CNN
	1    8150 7200
	1    0    0    -1  
$EndComp
$Comp
L sixteen-bit-computer:74HC245 U13
U 1 1 62EA86E3
P 8150 9350
F 0 "U13" H 7900 10050 50  0000 C CNN
F 1 "74HC245" H 8400 10050 50  0000 C CNN
F 2 "Package_DIP:DIP-20_W7.62mm_Socket" H 7800 9350 50  0001 C CNN
F 3 "https://www.ti.com/lit/ds/symlink/cd74hc245.pdf" H 7800 9350 50  0001 C CNN
	1    8150 9350
	1    0    0    -1  
$EndComp
Wire Wire Line
	6350 8750 6700 8750
Wire Wire Line
	6700 8750 6700 9800
Wire Wire Line
	6700 9800 7600 9800
Wire Wire Line
	7600 9700 6750 9700
Wire Wire Line
	6750 9700 6750 8650
Wire Wire Line
	6750 8650 6350 8650
Wire Wire Line
	6350 8550 6800 8550
Wire Wire Line
	6800 8550 6800 9600
Wire Wire Line
	6800 9600 7600 9600
Wire Wire Line
	7600 9500 6850 9500
Wire Wire Line
	6850 9500 6850 8450
Wire Wire Line
	6850 8450 6350 8450
Wire Wire Line
	6350 8350 6900 8350
Wire Wire Line
	6900 8350 6900 9400
Wire Wire Line
	6900 9400 7600 9400
Wire Wire Line
	7600 9300 6950 9300
Wire Wire Line
	6950 9300 6950 8250
Wire Wire Line
	6950 8250 6350 8250
Wire Wire Line
	6350 8150 7000 8150
Wire Wire Line
	7000 8150 7000 9200
Wire Wire Line
	7000 9200 7600 9200
Wire Wire Line
	7600 9100 7050 9100
Wire Wire Line
	7050 9100 7050 8050
Wire Wire Line
	7050 8050 6350 8050
Wire Wire Line
	6350 7950 7050 7950
Wire Wire Line
	7050 7950 7050 7650
Wire Wire Line
	7050 7650 7600 7650
Wire Wire Line
	7600 7550 7000 7550
Wire Wire Line
	7000 7550 7000 7850
Wire Wire Line
	7000 7850 6350 7850
Wire Wire Line
	6350 7750 6950 7750
Wire Wire Line
	6950 7750 6950 7450
Wire Wire Line
	6950 7450 7600 7450
Wire Wire Line
	7600 7350 6900 7350
Wire Wire Line
	6900 7350 6900 7650
Wire Wire Line
	6900 7650 6350 7650
Wire Wire Line
	6350 7550 6850 7550
Wire Wire Line
	6850 7550 6850 7250
Wire Wire Line
	6850 7250 7600 7250
Wire Wire Line
	7600 7150 6800 7150
Wire Wire Line
	6800 7150 6800 7450
Wire Wire Line
	6800 7450 6350 7450
Wire Wire Line
	6350 7350 6750 7350
Wire Wire Line
	6750 7350 6750 7050
Wire Wire Line
	6750 7050 7600 7050
Wire Wire Line
	7600 6950 6700 6950
Wire Wire Line
	6700 6950 6700 7250
Wire Wire Line
	6700 7250 6350 7250
Text Label 8700 6950 0    50   ~ 0
BUS_BUF_15
Text Label 8700 7050 0    50   ~ 0
BUS_BUF_14
Text Label 8700 7150 0    50   ~ 0
BUS_BUF_13
Text Label 8700 7250 0    50   ~ 0
BUS_BUF_12
Text Label 8700 7350 0    50   ~ 0
BUS_BUF_11
Text Label 8700 7450 0    50   ~ 0
BUS_BUF_10
Text Label 8700 7550 0    50   ~ 0
BUS_BUF_09
Text Label 8700 7650 0    50   ~ 0
BUS_BUF_08
Text Label 8700 9100 0    50   ~ 0
BUS_BUF_07
Text Label 8700 9200 0    50   ~ 0
BUS_BUF_06
Text Label 8700 9300 0    50   ~ 0
BUS_BUF_05
Text Label 8700 9400 0    50   ~ 0
BUS_BUF_04
Text Label 8700 9500 0    50   ~ 0
BUS_BUF_03
Text Label 8700 9600 0    50   ~ 0
BUS_BUF_02
Text Label 8700 9700 0    50   ~ 0
BUS_BUF_01
Text Label 8700 9800 0    50   ~ 0
BUS_BUF_00
Text Label 8150 8000 3    50   ~ 0
GND
Text Label 8150 8400 1    50   ~ 0
VCC
Text Label 8150 10150 3    50   ~ 0
GND
Text Label 8150 6250 1    50   ~ 0
VCC
Wire Wire Line
	7600 6650 7400 6650
Wire Wire Line
	7400 6650 7400 8000
Wire Wire Line
	7400 8000 8150 8000
$Comp
L Device:C C15
U 1 1 63056294
P 9450 7300
F 0 "C15" H 9565 7346 50  0000 L CNN
F 1 "0.1uF" H 9565 7255 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 9488 7150 50  0001 C CNN
F 3 "~" H 9450 7300 50  0001 C CNN
	1    9450 7300
	1    0    0    -1  
$EndComp
$Comp
L Device:C C16
U 1 1 63061E70
P 9450 9450
F 0 "C16" H 9565 9496 50  0000 L CNN
F 1 "0.1uF" H 9565 9405 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 9488 9300 50  0001 C CNN
F 3 "~" H 9450 9450 50  0001 C CNN
	1    9450 9450
	1    0    0    -1  
$EndComp
Wire Wire Line
	8150 8000 9450 8000
Wire Wire Line
	9450 8000 9450 7450
Connection ~ 8150 8000
Wire Wire Line
	9450 7150 9450 6250
Wire Wire Line
	9450 6250 8150 6250
Wire Wire Line
	7600 6800 7500 6800
Wire Wire Line
	7500 6800 7500 6250
Wire Wire Line
	7500 6250 8150 6250
Connection ~ 8150 6250
Wire Wire Line
	7600 8950 7500 8950
Wire Wire Line
	7500 8950 7500 8400
Wire Wire Line
	7500 8400 8150 8400
Wire Wire Line
	8150 8400 9450 8400
Wire Wire Line
	9450 8400 9450 9300
Connection ~ 8150 8400
Wire Wire Line
	9450 9600 9450 10150
Wire Wire Line
	9450 10150 8150 10150
Wire Wire Line
	7600 8800 7400 8800
Wire Wire Line
	7400 8800 7400 10150
Wire Wire Line
	7400 10150 8150 10150
Connection ~ 8150 10150
Text Label 9050 1900 2    50   ~ 0
BUS_BUF_15
Text Label 9050 1800 2    50   ~ 0
BUS_BUF_14
Text Label 9050 1700 2    50   ~ 0
BUS_BUF_13
Text Label 9050 1600 2    50   ~ 0
BUS_BUF_12
Text Label 6750 1900 2    50   ~ 0
BUS_BUF_11
Text Label 6750 1800 2    50   ~ 0
BUS_BUF_10
Text Label 6750 1700 2    50   ~ 0
BUS_BUF_09
Text Label 6750 1600 2    50   ~ 0
BUS_BUF_08
Text Label 4500 1900 2    50   ~ 0
BUS_BUF_07
Text Label 4500 1800 2    50   ~ 0
BUS_BUF_06
Text Label 4500 1700 2    50   ~ 0
BUS_BUF_05
Text Label 4500 1600 2    50   ~ 0
BUS_BUF_04
Text Label 2250 1900 2    50   ~ 0
BUS_BUF_03
Text Label 2250 1800 2    50   ~ 0
BUS_BUF_02
Text Label 2250 1700 2    50   ~ 0
BUS_BUF_01
Text Label 2250 1600 2    50   ~ 0
BUS_BUF_00
Text Label 10250 2100 0    50   ~ 0
CARRY_BORROW_OUT_BAR
Text Label 2300 5150 2    50   ~ 0
BUS_BUF_03
Text Label 2300 5050 2    50   ~ 0
BUS_BUF_02
Text Label 2300 4950 2    50   ~ 0
BUS_BUF_01
Text Label 2300 4850 2    50   ~ 0
BUS_BUF_00
Text Label 4750 5150 2    50   ~ 0
BUS_BUF_07
Text Label 4750 5050 2    50   ~ 0
BUS_BUF_06
Text Label 4750 4950 2    50   ~ 0
BUS_BUF_05
Text Label 4750 4850 2    50   ~ 0
BUS_BUF_04
Text Label 7050 5150 2    50   ~ 0
BUS_BUF_11
Text Label 7050 5050 2    50   ~ 0
BUS_BUF_10
Text Label 7050 4950 2    50   ~ 0
BUS_BUF_09
Text Label 7050 4850 2    50   ~ 0
BUS_BUF_08
Text Label 9300 5150 2    50   ~ 0
BUS_BUF_15
Text Label 9300 5050 2    50   ~ 0
BUS_BUF_14
Text Label 9300 4950 2    50   ~ 0
BUS_BUF_13
Text Label 9300 4850 2    50   ~ 0
BUS_BUF_12
$Comp
L Connector:Conn_01x02_Female J6
U 1 1 62F464B6
P 11450 950
F 0 "J6" V 11500 750 50  0000 L CNN
F 1 "TOP_POWER" V 11500 900 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x02_P2.54mm_Horizontal" H 11450 950 50  0001 C CNN
F 3 "~" H 11450 950 50  0001 C CNN
	1    11450 950 
	0    1    -1   0   
$EndComp
Text Label 11450 1150 3    50   ~ 0
VCC
Text Label 11350 1150 3    50   ~ 0
GND
Text Label 12550 4650 2    50   ~ 0
VCC
Text Label 12550 5200 2    50   ~ 0
GND
$Comp
L Connector:Conn_01x03_Male J7
U 1 1 62F6F8F1
P 12750 4750
F 0 "J7" H 12600 4650 50  0000 L CNN
F 1 "LED_CONTROL" H 12200 4750 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Horizontal" H 12750 4750 50  0001 C CNN
F 3 "~" H 12750 4750 50  0001 C CNN
	1    12750 4750
	-1   0    0    -1  
$EndComp
$Comp
L Device:R_US R2
U 1 1 62F7CD19
P 12250 4900
F 0 "R2" H 12318 4946 50  0000 L CNN
F 1 "10K" H 12318 4855 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 12290 4890 50  0001 C CNN
F 3 "~" H 12250 4900 50  0001 C CNN
	1    12250 4900
	1    0    0    -1  
$EndComp
Text Label 11600 4750 0    50   ~ 0
LED_CONTROL
Wire Wire Line
	11600 4750 12250 4750
Text Label 700  6650 0    50   ~ 0
LED_CONTROL
Wire Wire Line
	1800 6250 3000 6250
Wire Wire Line
	1000 6250 1800 6250
Connection ~ 1800 6250
$Comp
L sixteen-bit-computer:74HCT245 U4
U 1 1 5F9AC31C
P 1800 7200
F 0 "U4" H 1550 7900 50  0000 C CNN
F 1 "74HCT245" H 2050 7900 50  0000 C CNN
F 2 "Package_DIP:DIP-20_W7.62mm_Socket" H 1450 7200 50  0001 C CNN
F 3 "" H 1450 7200 50  0001 C CNN
	1    1800 7200
	1    0    0    -1  
$EndComp
Wire Wire Line
	700  6650 1250 6650
Text Label 650  8800 0    50   ~ 0
LED_CONTROL
Wire Wire Line
	650  8800 1250 8800
Connection ~ 12250 4750
$Comp
L sixteen-bit-computer:74HCT245 U14
U 1 1 64944998
P 11250 7650
F 0 "U14" H 11000 8350 50  0000 C CNN
F 1 "74HCT245" H 11500 8350 50  0000 C CNN
F 2 "Package_DIP:DIP-20_W7.62mm_Socket" H 10900 7650 50  0001 C CNN
F 3 "" H 10900 7650 50  0001 C CNN
	1    11250 7650
	1    0    0    -1  
$EndComp
$Comp
L Device:C C17
U 1 1 6494499E
P 12550 7650
F 0 "C17" H 12665 7696 50  0000 L CNN
F 1 "0.1uF" H 12665 7605 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 12588 7500 50  0001 C CNN
F 3 "~" H 12550 7650 50  0001 C CNN
	1    12550 7650
	1    0    0    -1  
$EndComp
$Comp
L Device:C C18
U 1 1 649449A4
P 15200 7700
F 0 "C18" H 15315 7746 50  0000 L CNN
F 1 "0.1uF" H 15315 7655 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 15238 7550 50  0001 C CNN
F 3 "~" H 15200 7700 50  0001 C CNN
	1    15200 7700
	1    0    0    -1  
$EndComp
Text Label 10700 8100 2    50   ~ 0
RES_00
Text Label 10700 8000 2    50   ~ 0
RES_01
Text Label 10700 7900 2    50   ~ 0
RES_02
Text Label 10700 7800 2    50   ~ 0
RES_03
Text Label 10700 7700 2    50   ~ 0
RES_04
Text Label 10700 7600 2    50   ~ 0
RES_05
Text Label 10700 7500 2    50   ~ 0
RES_06
Text Label 10700 7400 2    50   ~ 0
RES_07
Text Label 13350 8100 2    50   ~ 0
RES_08
Text Label 13350 8000 2    50   ~ 0
RES_09
Text Label 13350 7900 2    50   ~ 0
RES_10
Text Label 13350 7800 2    50   ~ 0
RES_11
Text Label 13350 7700 2    50   ~ 0
RES_12
Text Label 13350 7600 2    50   ~ 0
RES_13
Text Label 13350 7500 2    50   ~ 0
RES_14
Text Label 13350 7400 2    50   ~ 0
RES_15
Text Label 11800 8100 0    50   ~ 0
RES_HCT_BUF_00
Text Label 11800 8000 0    50   ~ 0
RES_HCT_BUF_01
Text Label 11800 7900 0    50   ~ 0
RES_HCT_BUF_02
Text Label 11800 7800 0    50   ~ 0
RES_HCT_BUF_03
Text Label 11800 7700 0    50   ~ 0
RES_HCT_BUF_04
Text Label 11800 7600 0    50   ~ 0
RES_HCT_BUF_05
Text Label 11800 7500 0    50   ~ 0
RES_HCT_BUF_06
Text Label 11800 7400 0    50   ~ 0
RES_HCT_BUF_07
Text Label 14450 8100 0    50   ~ 0
RES_HCT_BUF_08
Text Label 14450 8000 0    50   ~ 0
RES_HCT_BUF_09
Text Label 14450 7900 0    50   ~ 0
RES_HCT_BUF_10
Text Label 14450 7800 0    50   ~ 0
RES_HCT_BUF_11
Text Label 14450 7700 0    50   ~ 0
RES_HCT_BUF_12
Text Label 14450 7600 0    50   ~ 0
RES_HCT_BUF_13
Text Label 14450 7500 0    50   ~ 0
RES_HCT_BUF_14
Text Label 14450 7400 0    50   ~ 0
RES_HCT_BUF_15
Wire Wire Line
	10700 7250 10450 7250
Wire Wire Line
	10450 7250 10450 6700
Wire Wire Line
	10450 6700 11250 6700
Text Label 11250 8450 3    50   ~ 0
GND
Text Label 13900 8450 3    50   ~ 0
GND
Text Label 13900 6700 1    50   ~ 0
VCC
Text Label 11250 6700 1    50   ~ 0
VCC
Wire Wire Line
	13350 7250 13100 7250
Wire Wire Line
	13100 7250 13100 6700
Wire Wire Line
	15200 6700 15200 7550
Wire Wire Line
	15200 7850 15200 8450
Wire Wire Line
	15200 8450 13900 8450
Wire Wire Line
	11250 6700 12550 6700
Wire Wire Line
	12550 6700 12550 7500
Connection ~ 11250 6700
Wire Wire Line
	12550 7800 12550 8450
Wire Wire Line
	12550 8450 11250 8450
Wire Wire Line
	13900 6700 15200 6700
Wire Wire Line
	13100 6700 13900 6700
Connection ~ 13900 6700
$Comp
L sixteen-bit-computer:74HCT245 U15
U 1 1 649449DF
P 13900 7650
F 0 "U15" H 13650 8350 50  0000 C CNN
F 1 "74HCT245" H 14150 8350 50  0000 C CNN
F 2 "Package_DIP:DIP-20_W7.62mm_Socket" H 13550 7650 50  0001 C CNN
F 3 "" H 13550 7650 50  0001 C CNN
	1    13900 7650
	1    0    0    -1  
$EndComp
Wire Wire Line
	13350 7100 12950 7100
Wire Wire Line
	12950 7100 12950 8450
Wire Wire Line
	12950 8450 13900 8450
Connection ~ 13900 8450
Wire Wire Line
	10700 7100 10250 7100
Wire Wire Line
	10250 7100 10250 8450
Wire Wire Line
	10250 8450 11250 8450
Connection ~ 11250 8450
Wire Wire Line
	12250 4750 12550 4750
Wire Wire Line
	12250 5050 12550 5050
Wire Wire Line
	12550 5050 12550 5200
Wire Wire Line
	12550 5050 12550 4850
Connection ~ 12550 5050
Text Label 16100 3200 3    50   ~ 0
RES_HCT_BUF_00
Text Label 16000 3200 3    50   ~ 0
RES_HCT_BUF_01
Text Label 15900 3200 3    50   ~ 0
RES_HCT_BUF_02
Text Label 15800 3200 3    50   ~ 0
RES_HCT_BUF_03
Text Label 15700 3200 3    50   ~ 0
RES_HCT_BUF_04
Text Label 15600 3200 3    50   ~ 0
RES_HCT_BUF_05
Text Label 15500 3200 3    50   ~ 0
RES_HCT_BUF_06
Text Label 15400 3200 3    50   ~ 0
RES_HCT_BUF_07
Text Label 15300 3200 3    50   ~ 0
RES_HCT_BUF_08
Text Label 15200 3200 3    50   ~ 0
RES_HCT_BUF_09
Text Label 15100 3200 3    50   ~ 0
RES_HCT_BUF_10
Text Label 15000 3200 3    50   ~ 0
RES_HCT_BUF_11
Text Label 14900 3200 3    50   ~ 0
RES_HCT_BUF_12
Text Label 14800 3200 3    50   ~ 0
RES_HCT_BUF_13
Text Label 14700 3200 3    50   ~ 0
RES_HCT_BUF_14
Text Label 14600 3200 3    50   ~ 0
RES_HCT_BUF_15
$EndSCHEMATC
