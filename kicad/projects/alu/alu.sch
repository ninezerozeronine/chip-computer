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
L eight-bit-computer:Aux_connection J5
U 1 1 5F95F4FF
P 13600 7650
F 0 "J5" H 13512 8275 50  0000 C CNN
F 1 "Aux_connection" H 13512 8184 50  0000 C CNN
F 2 "eight-bit-computer:aux-connection" H 13600 7650 50  0001 C CNN
F 3 "~" H 13600 7650 50  0001 C CNN
	1    13600 7650
	1    0    0    -1  
$EndComp
$Comp
L eight-bit-computer:Bus_connection J4
U 1 1 5F96011F
P 12500 7500
F 0 "J4" H 12362 8425 50  0000 C CNN
F 1 "Bus_connection" H 12362 8334 50  0000 C CNN
F 2 "eight-bit-computer:bus-connection" H 12400 7900 50  0001 C CNN
F 3 "~" H 12400 7900 50  0001 C CNN
	1    12500 7500
	1    0    0    -1  
$EndComp
$Comp
L eight-bit-computer:Control_signal_backplane J3
U 1 1 5F960B16
P 15000 7200
F 0 "J3" H 14887 8925 50  0000 C CNN
F 1 "Control_signal_backplane" H 14887 8834 50  0000 C CNN
F 2 "eight-bit-computer:backplane-connector-single-row-annotated" H 15000 7200 50  0001 C CNN
F 3 "~" H 15000 7200 50  0001 C CNN
	1    15000 7200
	1    0    0    -1  
$EndComp
$Comp
L eight-bit-computer:74HCT157 U8
U 1 1 5F96E5D7
P 2800 4900
F 0 "U8" H 2500 5600 50  0000 C CNN
F 1 "74HCT157" H 3050 5600 50  0000 C CNN
F 2 "Package_DIP:DIP-16_W7.62mm_Socket" H 2800 4850 50  0001 C CNN
F 3 "https://www.ti.com/lit/ds/symlink/sn74hct157.pdf" H 2800 4850 50  0001 C CNN
	1    2800 4900
	1    0    0    -1  
$EndComp
$Comp
L eight-bit-computer:74HCT157 U10
U 1 1 5F96F80C
P 5250 4900
F 0 "U10" H 5000 5600 50  0000 C CNN
F 1 "74HCT157" H 5500 5600 50  0000 C CNN
F 2 "Package_DIP:DIP-16_W7.62mm_Socket" H 5250 4850 50  0001 C CNN
F 3 "https://www.ti.com/lit/ds/symlink/sn74hct157.pdf" H 5250 4850 50  0001 C CNN
	1    5250 4900
	1    0    0    -1  
$EndComp
$Comp
L eight-bit-computer:74HCT157 U11
U 1 1 5F970081
P 9800 4900
F 0 "U11" H 9550 5600 50  0000 C CNN
F 1 "74HCT157" H 10050 5600 50  0000 C CNN
F 2 "Package_DIP:DIP-16_W7.62mm_Socket" H 9800 4850 50  0001 C CNN
F 3 "https://www.ti.com/lit/ds/symlink/sn74hct157.pdf" H 9800 4850 50  0001 C CNN
	1    9800 4900
	1    0    0    -1  
$EndComp
$Comp
L eight-bit-computer:74HCT157 U9
U 1 1 5F9706EB
P 7550 4900
F 0 "U9" H 7250 5600 50  0000 C CNN
F 1 "74HCT157" H 7800 5600 50  0000 C CNN
F 2 "Package_DIP:DIP-16_W7.62mm_Socket" H 7550 4850 50  0001 C CNN
F 3 "https://www.ti.com/lit/ds/symlink/sn74hct157.pdf" H 7550 4850 50  0001 C CNN
	1    7550 4900
	1    0    0    -1  
$EndComp
$Comp
L Device:LED D16
U 1 1 5F97105C
P 5000 7050
F 0 "D16" H 4750 7000 50  0000 C CNN
F 1 "LED" H 4550 7000 50  0000 C CNN
F 2 "eight-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 5000 7050 50  0001 C CNN
F 3 "~" H 5000 7050 50  0001 C CNN
	1    5000 7050
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D15
U 1 1 5F9815B5
P 5000 7200
F 0 "D15" H 4750 7150 50  0000 C CNN
F 1 "LED" H 4550 7150 50  0000 C CNN
F 2 "eight-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 5000 7200 50  0001 C CNN
F 3 "~" H 5000 7200 50  0001 C CNN
	1    5000 7200
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D14
U 1 1 5F981E12
P 5000 7350
F 0 "D14" H 4750 7300 50  0000 C CNN
F 1 "LED" H 4550 7300 50  0000 C CNN
F 2 "eight-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 5000 7350 50  0001 C CNN
F 3 "~" H 5000 7350 50  0001 C CNN
	1    5000 7350
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D13
U 1 1 5F982593
P 5000 7500
F 0 "D13" H 4750 7450 50  0000 C CNN
F 1 "LED" H 4550 7450 50  0000 C CNN
F 2 "eight-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 5000 7500 50  0001 C CNN
F 3 "~" H 5000 7500 50  0001 C CNN
	1    5000 7500
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D12
U 1 1 5F98323E
P 5000 7650
F 0 "D12" H 4750 7600 50  0000 C CNN
F 1 "LED" H 4550 7600 50  0000 C CNN
F 2 "eight-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 5000 7650 50  0001 C CNN
F 3 "~" H 5000 7650 50  0001 C CNN
	1    5000 7650
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D11
U 1 1 5F983248
P 5000 7800
F 0 "D11" H 4750 7750 50  0000 C CNN
F 1 "LED" H 4550 7750 50  0000 C CNN
F 2 "eight-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 5000 7800 50  0001 C CNN
F 3 "~" H 5000 7800 50  0001 C CNN
	1    5000 7800
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D10
U 1 1 5F983252
P 5000 7950
F 0 "D10" H 4750 7900 50  0000 C CNN
F 1 "LED" H 4550 7900 50  0000 C CNN
F 2 "eight-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 5000 7950 50  0001 C CNN
F 3 "~" H 5000 7950 50  0001 C CNN
	1    5000 7950
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D9
U 1 1 5F98325C
P 5000 8100
F 0 "D9" H 4750 8050 50  0000 C CNN
F 1 "LED" H 4550 8050 50  0000 C CNN
F 2 "eight-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 5000 8100 50  0001 C CNN
F 3 "~" H 5000 8100 50  0001 C CNN
	1    5000 8100
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D8
U 1 1 5F9873EE
P 5000 8250
F 0 "D8" H 4750 8200 50  0000 C CNN
F 1 "LED" H 4550 8200 50  0000 C CNN
F 2 "eight-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 5000 8250 50  0001 C CNN
F 3 "~" H 5000 8250 50  0001 C CNN
	1    5000 8250
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D7
U 1 1 5F9873F8
P 5000 8400
F 0 "D7" H 4750 8350 50  0000 C CNN
F 1 "LED" H 4550 8350 50  0000 C CNN
F 2 "eight-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 5000 8400 50  0001 C CNN
F 3 "~" H 5000 8400 50  0001 C CNN
	1    5000 8400
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D6
U 1 1 5F987402
P 5000 8550
F 0 "D6" H 4750 8500 50  0000 C CNN
F 1 "LED" H 4550 8500 50  0000 C CNN
F 2 "eight-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 5000 8550 50  0001 C CNN
F 3 "~" H 5000 8550 50  0001 C CNN
	1    5000 8550
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D5
U 1 1 5F98740C
P 5000 8700
F 0 "D5" H 4750 8650 50  0000 C CNN
F 1 "LED" H 4550 8650 50  0000 C CNN
F 2 "eight-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 5000 8700 50  0001 C CNN
F 3 "~" H 5000 8700 50  0001 C CNN
	1    5000 8700
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D4
U 1 1 5F987416
P 5000 8850
F 0 "D4" H 4750 8800 50  0000 C CNN
F 1 "LED" H 4550 8800 50  0000 C CNN
F 2 "eight-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 5000 8850 50  0001 C CNN
F 3 "~" H 5000 8850 50  0001 C CNN
	1    5000 8850
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D3
U 1 1 5F987420
P 5000 9000
F 0 "D3" H 4750 8950 50  0000 C CNN
F 1 "LED" H 4550 8950 50  0000 C CNN
F 2 "eight-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 5000 9000 50  0001 C CNN
F 3 "~" H 5000 9000 50  0001 C CNN
	1    5000 9000
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D2
U 1 1 5F98742A
P 5000 9150
F 0 "D2" H 4750 9100 50  0000 C CNN
F 1 "LED" H 4550 9100 50  0000 C CNN
F 2 "eight-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 5000 9150 50  0001 C CNN
F 3 "~" H 5000 9150 50  0001 C CNN
	1    5000 9150
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D1
U 1 1 5F987434
P 5000 9300
F 0 "D1" H 4750 9250 50  0000 C CNN
F 1 "LED" H 4550 9250 50  0000 C CNN
F 2 "eight-bit-computer:LED_D5.0mm_Horizontal_O3.81mm_Z3.0mm" H 5000 9300 50  0001 C CNN
F 3 "~" H 5000 9300 50  0001 C CNN
	1    5000 9300
	-1   0    0    1   
$EndComp
$Comp
L 74xx:74HCT04 U1
U 1 1 5F99EB01
P 1400 2600
F 0 "U1" H 1400 2917 50  0000 C CNN
F 1 "74HCT04" H 1400 2826 50  0000 C CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket" H 1400 2600 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 1400 2600 50  0001 C CNN
	1    1400 2600
	1    0    0    -1  
$EndComp
$Comp
L 74xx:74HCT04 U1
U 2 1 5F99F922
P 14550 3250
F 0 "U1" H 14550 3567 50  0000 C CNN
F 1 "74HCT04" H 14550 3476 50  0000 C CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket" H 14550 3250 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 14550 3250 50  0001 C CNN
	2    14550 3250
	1    0    0    -1  
$EndComp
$Comp
L 74xx:74HCT04 U1
U 3 1 5F9A188D
P 14550 2700
F 0 "U1" H 14550 3017 50  0000 C CNN
F 1 "74HCT04" H 14550 2926 50  0000 C CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket" H 14550 2700 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 14550 2700 50  0001 C CNN
	3    14550 2700
	1    0    0    -1  
$EndComp
$Comp
L 74xx:74HCT04 U1
U 4 1 5F9A32BA
P 14550 2200
F 0 "U1" H 14550 2517 50  0000 C CNN
F 1 "74HCT04" H 14550 2426 50  0000 C CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket" H 14550 2200 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 14550 2200 50  0001 C CNN
	4    14550 2200
	1    0    0    -1  
$EndComp
$Comp
L 74xx:74HCT04 U1
U 5 1 5F9A4E9B
P 14550 1700
F 0 "U1" H 14550 2017 50  0000 C CNN
F 1 "74HCT04" H 14550 1926 50  0000 C CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket" H 14550 1700 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 14550 1700 50  0001 C CNN
	5    14550 1700
	1    0    0    -1  
$EndComp
$Comp
L 74xx:74HCT04 U1
U 6 1 5F9A790D
P 14550 1200
F 0 "U1" H 14550 1517 50  0000 C CNN
F 1 "74HCT04" H 14550 1426 50  0000 C CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket" H 14550 1200 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 14550 1200 50  0001 C CNN
	6    14550 1200
	1    0    0    -1  
$EndComp
$Comp
L 74xx:74HCT04 U1
U 7 1 5F9A95E8
P 13050 1300
F 0 "U1" H 13280 1346 50  0000 L CNN
F 1 "74HCT04" H 13280 1255 50  0000 L CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket" H 13050 1300 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 13050 1300 50  0001 C CNN
	7    13050 1300
	1    0    0    -1  
$EndComp
$Comp
L eight-bit-computer:74HCT245 U6
U 1 1 5F9AAB74
P 2750 9450
F 0 "U6" H 2500 10150 50  0000 C CNN
F 1 "74HCT245" H 3000 10150 50  0000 C CNN
F 2 "Package_DIP:DIP-20_W7.62mm_Socket" H 2400 9450 50  0001 C CNN
F 3 "" H 2400 9450 50  0001 C CNN
	1    2750 9450
	1    0    0    -1  
$EndComp
$Comp
L eight-bit-computer:74HCT245 U4
U 1 1 5F9AC31C
P 2750 7300
F 0 "U4" H 2500 8000 50  0000 C CNN
F 1 "74HCT245" H 3000 8000 50  0000 C CNN
F 2 "Package_DIP:DIP-20_W7.62mm_Socket" H 2400 7300 50  0001 C CNN
F 3 "" H 2400 7300 50  0001 C CNN
	1    2750 7300
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x16_Female J1
U 1 1 5F9AD90D
P 12650 4500
F 0 "J1" V 12700 3650 50  0000 L CNN
F 1 "ACC_CONTENTS" V 12700 4650 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x16_P2.54mm_Horizontal" H 12650 4500 50  0001 C CNN
F 3 "~" H 12650 4500 50  0001 C CNN
	1    12650 4500
	0    1    -1   0   
$EndComp
$Comp
L Device:C C2
U 1 1 5F9F7FBB
P 3950 1850
F 0 "C2" H 4065 1896 50  0000 L CNN
F 1 "0.1uF" H 4065 1805 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 3988 1700 50  0001 C CNN
F 3 "~" H 3950 1850 50  0001 C CNN
	1    3950 1850
	1    0    0    -1  
$EndComp
$Comp
L Device:C C3
U 1 1 5F9F984E
P 6150 1850
F 0 "C3" H 6265 1896 50  0000 L CNN
F 1 "0.1uF" H 6265 1805 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 6188 1700 50  0001 C CNN
F 3 "~" H 6150 1850 50  0001 C CNN
	1    6150 1850
	1    0    0    -1  
$EndComp
$Comp
L Device:C C5
U 1 1 5F9F9D5F
P 8450 1850
F 0 "C5" H 8565 1896 50  0000 L CNN
F 1 "0.1uF" H 8565 1805 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 8488 1700 50  0001 C CNN
F 3 "~" H 8450 1850 50  0001 C CNN
	1    8450 1850
	1    0    0    -1  
$EndComp
$Comp
L Device:C C9
U 1 1 5F9FA306
P 10800 1850
F 0 "C9" H 10915 1896 50  0000 L CNN
F 1 "0.1uF" H 10915 1805 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 10838 1700 50  0001 C CNN
F 3 "~" H 10800 1850 50  0001 C CNN
	1    10800 1850
	1    0    0    -1  
$EndComp
$Comp
L Device:C C8
U 1 1 5F9FAA0F
P 3800 4850
F 0 "C8" H 3915 4896 50  0000 L CNN
F 1 "0.1uF" H 3915 4805 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 3838 4700 50  0001 C CNN
F 3 "~" H 3800 4850 50  0001 C CNN
	1    3800 4850
	1    0    0    -1  
$EndComp
$Comp
L Device:C C10
U 1 1 5F9FB868
P 6250 4900
F 0 "C10" H 6365 4946 50  0000 L CNN
F 1 "0.1uF" H 6365 4855 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 6288 4750 50  0001 C CNN
F 3 "~" H 6250 4900 50  0001 C CNN
	1    6250 4900
	1    0    0    -1  
$EndComp
$Comp
L Device:C C11
U 1 1 5F9FBE7F
P 10800 4900
F 0 "C11" H 10915 4946 50  0000 L CNN
F 1 "0.1uF" H 10915 4855 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 10838 4750 50  0001 C CNN
F 3 "~" H 10800 4900 50  0001 C CNN
	1    10800 4900
	1    0    0    -1  
$EndComp
$Comp
L Device:C C7
U 1 1 5F9FC4C8
P 8550 4850
F 0 "C7" H 8665 4896 50  0000 L CNN
F 1 "0.1uF" H 8665 4805 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 8588 4700 50  0001 C CNN
F 3 "~" H 8550 4850 50  0001 C CNN
	1    8550 4850
	1    0    0    -1  
$EndComp
$Comp
L Device:C C6
U 1 1 5F9FCAC5
P 3900 9500
F 0 "C6" H 4015 9546 50  0000 L CNN
F 1 "0.1uF" H 4015 9455 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 3938 9350 50  0001 C CNN
F 3 "~" H 3900 9500 50  0001 C CNN
	1    3900 9500
	1    0    0    -1  
$EndComp
$Comp
L Device:C C1
U 1 1 5F9FD214
P 13850 1250
F 0 "C1" H 13965 1296 50  0000 L CNN
F 1 "0.1uF" H 13965 1205 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 13888 1100 50  0001 C CNN
F 3 "~" H 13850 1250 50  0001 C CNN
	1    13850 1250
	1    0    0    -1  
$EndComp
$Comp
L Device:C C4
U 1 1 5F9FE15C
P 3950 7350
F 0 "C4" H 4065 7396 50  0000 L CNN
F 1 "0.1uF" H 4065 7305 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.7mm_W2.5mm_P5.00mm" H 3988 7200 50  0001 C CNN
F 3 "~" H 3950 7350 50  0001 C CNN
	1    3950 7350
	1    0    0    -1  
$EndComp
$Comp
L Device:R_Network08_US RN1
U 1 1 5F9FF6F6
P 6150 7450
F 0 "RN1" V 5533 7450 50  0000 C CNN
F 1 "R_Network08_US" V 5624 7450 50  0000 C CNN
F 2 "Resistor_THT:R_Array_SIP9" V 6625 7450 50  0001 C CNN
F 3 "http://www.vishay.com/docs/31509/csc.pdf" H 6150 7450 50  0001 C CNN
	1    6150 7450
	0    1    1    0   
$EndComp
$Comp
L Device:R_Network08_US RN2
U 1 1 5FA03E7C
P 6150 8650
F 0 "RN2" V 5533 8650 50  0000 C CNN
F 1 "R_Network08_US" V 5624 8650 50  0000 C CNN
F 2 "Resistor_THT:R_Array_SIP9" V 6625 8650 50  0001 C CNN
F 3 "http://www.vishay.com/docs/31509/csc.pdf" H 6150 8650 50  0001 C CNN
	1    6150 8650
	0    1    1    0   
$EndComp
$Comp
L Connector:Conn_01x18_Female J2
U 1 1 5FA0675E
P 14850 4500
F 0 "J2" V 14900 3550 50  0000 L CNN
F 1 "RES_AEQB_CRYBRW_OUT" V 14900 4450 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x18_P2.54mm_Horizontal" H 14850 4500 50  0001 C CNN
F 3 "~" H 14850 4500 50  0001 C CNN
	1    14850 4500
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
P 9900 7950
F 0 "#PWR01" H 9900 7800 50  0001 C CNN
F 1 "VCC" H 9917 8123 50  0000 C CNN
F 2 "" H 9900 7950 50  0001 C CNN
F 3 "" H 9900 7950 50  0001 C CNN
	1    9900 7950
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR02
U 1 1 5FA1038F
P 9900 8300
F 0 "#PWR02" H 9900 8050 50  0001 C CNN
F 1 "GND" H 9905 8127 50  0000 C CNN
F 2 "" H 9900 8300 50  0001 C CNN
F 3 "" H 9900 8300 50  0001 C CNN
	1    9900 8300
	1    0    0    -1  
$EndComp
$Comp
L power:PWR_FLAG #FLG01
U 1 1 5FA12019
P 9900 7950
F 0 "#FLG01" H 9900 8025 50  0001 C CNN
F 1 "PWR_FLAG" V 9900 8078 50  0000 L CNN
F 2 "" H 9900 7950 50  0001 C CNN
F 3 "~" H 9900 7950 50  0001 C CNN
	1    9900 7950
	0    1    1    0   
$EndComp
$Comp
L power:PWR_FLAG #FLG02
U 1 1 5FA13D2F
P 9900 8300
F 0 "#FLG02" H 9900 8375 50  0001 C CNN
F 1 "PWR_FLAG" V 9900 8428 50  0000 L CNN
F 2 "" H 9900 8300 50  0001 C CNN
F 3 "~" H 9900 8300 50  0001 C CNN
	1    9900 8300
	0    1    1    0   
$EndComp
Text Label 9850 7950 2    50   ~ 0
VCC
Text Label 9850 8300 2    50   ~ 0
GND
Connection ~ 9900 7950
Connection ~ 9900 8300
Text Label 12600 6800 0    50   ~ 0
BUS_00
Text Label 12600 6900 0    50   ~ 0
BUS_01
Text Label 12600 7000 0    50   ~ 0
BUS_02
Text Label 12600 7100 0    50   ~ 0
BUS_03
Text Label 12600 7200 0    50   ~ 0
BUS_04
Text Label 12600 7300 0    50   ~ 0
BUS_05
Text Label 12600 7400 0    50   ~ 0
BUS_06
Text Label 12600 7500 0    50   ~ 0
BUS_07
Text Label 12600 7600 0    50   ~ 0
BUS_08
Text Label 12600 7700 0    50   ~ 0
BUS_09
Text Label 12600 7800 0    50   ~ 0
BUS_10
Text Label 12600 7900 0    50   ~ 0
BUS_11
Text Label 12600 8000 0    50   ~ 0
BUS_12
Text Label 12600 8100 0    50   ~ 0
BUS_13
Text Label 12600 8200 0    50   ~ 0
BUS_14
Text Label 12600 8300 0    50   ~ 0
BUS_15
Text Label 13800 7250 0    50   ~ 0
VCC
Wire Wire Line
	13800 7350 13800 7250
Wire Wire Line
	13800 7550 13800 7450
Text Label 13800 7450 0    50   ~ 0
GND
NoConn ~ 13800 7750
NoConn ~ 13800 7950
NoConn ~ 13800 8150
Text Label 2250 1600 2    50   ~ 0
BUS_00
Text Label 2250 1700 2    50   ~ 0
BUS_01
Text Label 2250 1800 2    50   ~ 0
BUS_02
Text Label 2250 1900 2    50   ~ 0
BUS_03
Text Label 4500 1600 2    50   ~ 0
BUS_04
Text Label 4500 1700 2    50   ~ 0
BUS_05
Text Label 4500 1800 2    50   ~ 0
BUS_06
Text Label 4500 1900 2    50   ~ 0
BUS_07
Text Label 6750 1600 2    50   ~ 0
BUS_08
Text Label 6750 1700 2    50   ~ 0
BUS_09
Text Label 6750 1800 2    50   ~ 0
BUS_10
Text Label 6750 1900 2    50   ~ 0
BUS_11
Text Label 9050 1600 2    50   ~ 0
BUS_12
Text Label 9050 1700 2    50   ~ 0
BUS_13
Text Label 9050 1800 2    50   ~ 0
BUS_14
Text Label 9050 1900 2    50   ~ 0
BUS_15
Text Label 15200 6900 0    50   ~ 0
S0
Text Label 15200 7000 0    50   ~ 0
S1
Text Label 15200 7100 0    50   ~ 0
S2
Text Label 15200 7200 0    50   ~ 0
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
Text Label 13350 4700 3    50   ~ 0
ACC_00
Text Label 13250 4700 3    50   ~ 0
ACC_01
Text Label 13150 4700 3    50   ~ 0
ACC_02
Text Label 13050 4700 3    50   ~ 0
ACC_03
Text Label 12950 4700 3    50   ~ 0
ACC_04
Text Label 12750 4700 3    50   ~ 0
ACC_06
Text Label 12850 4700 3    50   ~ 0
ACC_05
Text Label 12650 4700 3    50   ~ 0
ACC_07
Text Label 12550 4700 3    50   ~ 0
ACC_08
Text Label 12450 4700 3    50   ~ 0
ACC_09
Text Label 12350 4700 3    50   ~ 0
ACC_10
Text Label 12250 4700 3    50   ~ 0
ACC_11
Text Label 12150 4700 3    50   ~ 0
ACC_12
Text Label 12050 4700 3    50   ~ 0
ACC_13
Text Label 11950 4700 3    50   ~ 0
ACC_14
Text Label 11850 4700 3    50   ~ 0
ACC_15
Text Label 15650 4700 3    50   ~ 0
RES_00
Text Label 15550 4700 3    50   ~ 0
RES_01
Text Label 15450 4700 3    50   ~ 0
RES_02
Text Label 15350 4700 3    50   ~ 0
RES_03
Text Label 15250 4700 3    50   ~ 0
RES_04
Text Label 15150 4700 3    50   ~ 0
RES_05
Text Label 15050 4700 3    50   ~ 0
RES_06
Text Label 14950 4700 3    50   ~ 0
RES_07
Text Label 14850 4700 3    50   ~ 0
RES_08
Text Label 14750 4700 3    50   ~ 0
RES_09
Text Label 14650 4700 3    50   ~ 0
RES_10
Text Label 14550 4700 3    50   ~ 0
RES_11
Text Label 14450 4700 3    50   ~ 0
RES_12
Text Label 14350 4700 3    50   ~ 0
RES_13
Text Label 14250 4700 3    50   ~ 0
RES_14
Text Label 14150 4700 3    50   ~ 0
RES_15
Text Label 2200 9900 2    50   ~ 0
RES_00
Text Label 2200 9800 2    50   ~ 0
RES_01
Text Label 2200 9700 2    50   ~ 0
RES_02
Text Label 2200 9600 2    50   ~ 0
RES_03
Text Label 2200 9500 2    50   ~ 0
RES_04
Text Label 2200 9400 2    50   ~ 0
RES_05
Text Label 2200 9300 2    50   ~ 0
RES_06
Text Label 2200 9200 2    50   ~ 0
RES_07
Text Label 2200 7750 2    50   ~ 0
RES_08
Text Label 2200 7650 2    50   ~ 0
RES_09
Text Label 2200 7550 2    50   ~ 0
RES_10
Text Label 2200 7450 2    50   ~ 0
RES_11
Text Label 2200 7350 2    50   ~ 0
RES_12
Text Label 2200 7250 2    50   ~ 0
RES_13
Text Label 2200 7150 2    50   ~ 0
RES_14
Text Label 2200 7050 2    50   ~ 0
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
Text Label 2300 4850 2    50   ~ 0
BUS_00
Text Label 2300 4950 2    50   ~ 0
BUS_01
Text Label 2300 5050 2    50   ~ 0
BUS_02
Text Label 2300 5150 2    50   ~ 0
BUS_03
Text Label 4750 4850 2    50   ~ 0
BUS_04
Text Label 4750 4950 2    50   ~ 0
BUS_05
Text Label 4750 5050 2    50   ~ 0
BUS_06
Text Label 4750 5150 2    50   ~ 0
BUS_07
Text Label 7050 4850 2    50   ~ 0
BUS_08
Text Label 7050 4950 2    50   ~ 0
BUS_09
Text Label 7050 5050 2    50   ~ 0
BUS_10
Text Label 7050 5150 2    50   ~ 0
BUS_11
Text Label 9300 4850 2    50   ~ 0
BUS_12
Text Label 9300 4950 2    50   ~ 0
BUS_13
Text Label 9300 5050 2    50   ~ 0
BUS_14
Text Label 9300 5150 2    50   ~ 0
BUS_15
Text Label 15200 6800 0    50   ~ 0
A_IS_BUS
Text Label 15200 7300 0    50   ~ 0
M
Text Label 15200 7400 0    50   ~ 0
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
	11400 2850 11400 2100
Wire Wire Line
	11400 2100 10250 2100
Text Label 11600 2850 0    50   ~ 0
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
	11400 2850 11600 2850
Text Label 9650 900  1    50   ~ 0
VCC
Text Label 7350 900  1    50   ~ 0
VCC
Text Label 5100 900  1    50   ~ 0
VCC
Text Label 2850 900  1    50   ~ 0
VCC
Wire Wire Line
	3950 1700 3950 900 
Wire Wire Line
	3950 900  2850 900 
Wire Wire Line
	3950 2000 3950 2900
Wire Wire Line
	3950 2900 2850 2900
Wire Wire Line
	6150 1700 6150 900 
Wire Wire Line
	6150 900  5100 900 
Wire Wire Line
	6150 2000 6150 2900
Wire Wire Line
	6150 2900 5100 2900
Wire Wire Line
	8450 1700 8450 900 
Wire Wire Line
	8450 900  7350 900 
Wire Wire Line
	8450 2000 8450 2900
Wire Wire Line
	8450 2900 7350 2900
Wire Wire Line
	10800 1700 10800 900 
Wire Wire Line
	10800 900  9650 900 
Wire Wire Line
	10800 2000 10800 2900
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
	3800 4050 3800 4700
Wire Wire Line
	3800 5000 3800 5750
Wire Wire Line
	3800 5750 2800 5750
Connection ~ 2800 5750
Wire Wire Line
	5250 4050 6250 4050
Wire Wire Line
	6250 4050 6250 4750
Wire Wire Line
	6250 5050 6250 5750
Wire Wire Line
	6250 5750 5250 5750
Connection ~ 5250 5750
Wire Wire Line
	7550 4050 8550 4050
Wire Wire Line
	8550 4050 8550 4700
Wire Wire Line
	8550 5000 8550 5750
Wire Wire Line
	6650 5750 7550 5750
Connection ~ 7550 5750
Wire Wire Line
	7550 5750 8550 5750
Wire Wire Line
	9800 4050 10800 4050
Wire Wire Line
	10800 4050 10800 4750
Wire Wire Line
	10800 5050 10800 5750
Wire Wire Line
	10800 5750 9800 5750
Connection ~ 9800 5750
Text Label 3300 9900 0    50   ~ 0
RES_BUF_00
Text Label 3300 9800 0    50   ~ 0
RES_BUF_01
Text Label 3300 9700 0    50   ~ 0
RES_BUF_02
Text Label 3300 9600 0    50   ~ 0
RES_BUF_03
Text Label 3300 9500 0    50   ~ 0
RES_BUF_04
Text Label 3300 9400 0    50   ~ 0
RES_BUF_05
Text Label 3300 9300 0    50   ~ 0
RES_BUF_06
Text Label 3300 9200 0    50   ~ 0
RES_BUF_07
Text Label 3300 7750 0    50   ~ 0
RES_BUF_08
Text Label 3300 7650 0    50   ~ 0
RES_BUF_09
Text Label 3300 7550 0    50   ~ 0
RES_BUF_10
Text Label 3300 7450 0    50   ~ 0
RES_BUF_11
Text Label 3300 7350 0    50   ~ 0
RES_BUF_12
Text Label 3300 7250 0    50   ~ 0
RES_BUF_13
Text Label 3300 7150 0    50   ~ 0
RES_BUF_14
Text Label 3300 7050 0    50   ~ 0
RES_BUF_15
Wire Wire Line
	2200 9050 1950 9050
Wire Wire Line
	1950 9050 1950 8500
Wire Wire Line
	1950 8500 2750 8500
Wire Wire Line
	2200 8900 1750 8900
Wire Wire Line
	1750 8900 1750 10250
Wire Wire Line
	1750 10250 2750 10250
Text Label 2750 10250 3    50   ~ 0
GND
Text Label 2750 8100 3    50   ~ 0
GND
Text Label 2750 6350 1    50   ~ 0
VCC
Text Label 2750 8500 1    50   ~ 0
VCC
Wire Wire Line
	2200 6900 1950 6900
Wire Wire Line
	1950 6900 1950 6350
Wire Wire Line
	1950 6350 2750 6350
Wire Wire Line
	2200 6750 1750 6750
Wire Wire Line
	1750 6750 1750 8100
Wire Wire Line
	1750 8100 2750 8100
Wire Wire Line
	2750 6350 3950 6350
Wire Wire Line
	3950 6350 3950 7200
Connection ~ 2750 6350
Wire Wire Line
	3950 7500 3950 8100
Wire Wire Line
	3950 8100 2750 8100
Connection ~ 2750 8100
Wire Wire Line
	2750 8500 3900 8500
Wire Wire Line
	3900 8500 3900 9350
Connection ~ 2750 8500
Wire Wire Line
	3900 9650 3900 10250
Wire Wire Line
	3900 10250 2750 10250
Connection ~ 2750 10250
Text Label 4850 8100 2    50   ~ 0
RES_BUF_08
Text Label 4850 7950 2    50   ~ 0
RES_BUF_09
Text Label 4850 7800 2    50   ~ 0
RES_BUF_10
Text Label 4850 7650 2    50   ~ 0
RES_BUF_11
Text Label 4850 7500 2    50   ~ 0
RES_BUF_12
Text Label 4850 7350 2    50   ~ 0
RES_BUF_13
Text Label 4850 7200 2    50   ~ 0
RES_BUF_14
Text Label 4850 7050 2    50   ~ 0
RES_BUF_15
Text Label 4850 9300 2    50   ~ 0
RES_BUF_00
Text Label 4850 9150 2    50   ~ 0
RES_BUF_01
Text Label 4850 9000 2    50   ~ 0
RES_BUF_02
Text Label 4850 8850 2    50   ~ 0
RES_BUF_03
Text Label 4850 8700 2    50   ~ 0
RES_BUF_04
Text Label 4850 8550 2    50   ~ 0
RES_BUF_05
Text Label 4850 8400 2    50   ~ 0
RES_BUF_06
Text Label 4850 8250 2    50   ~ 0
RES_BUF_07
Wire Wire Line
	5150 7050 5950 7050
Wire Wire Line
	5150 7200 5550 7200
Wire Wire Line
	5550 7200 5550 7150
Wire Wire Line
	5550 7150 5950 7150
Wire Wire Line
	5150 7350 5600 7350
Wire Wire Line
	5600 7350 5600 7250
Wire Wire Line
	5600 7250 5950 7250
Wire Wire Line
	5150 7500 5650 7500
Wire Wire Line
	5650 7500 5650 7350
Wire Wire Line
	5650 7350 5950 7350
Wire Wire Line
	5150 7650 5700 7650
Wire Wire Line
	5700 7650 5700 7450
Wire Wire Line
	5700 7450 5950 7450
Wire Wire Line
	5150 7800 5750 7800
Wire Wire Line
	5750 7800 5750 7550
Wire Wire Line
	5750 7550 5950 7550
Wire Wire Line
	5950 7650 5800 7650
Wire Wire Line
	5800 7650 5800 7950
Wire Wire Line
	5800 7950 5150 7950
Wire Wire Line
	5150 8100 5850 8100
Wire Wire Line
	5850 8100 5850 7750
Wire Wire Line
	5850 7750 5950 7750
Wire Wire Line
	5150 8250 5950 8250
Wire Wire Line
	5150 8400 5550 8400
Wire Wire Line
	5550 8400 5550 8350
Wire Wire Line
	5550 8350 5950 8350
Wire Wire Line
	5150 8550 5600 8550
Wire Wire Line
	5600 8550 5600 8450
Wire Wire Line
	5600 8450 5950 8450
Wire Wire Line
	5150 8700 5650 8700
Wire Wire Line
	5650 8700 5650 8550
Wire Wire Line
	5650 8550 5950 8550
Wire Wire Line
	5150 8850 5700 8850
Wire Wire Line
	5700 8850 5700 8650
Wire Wire Line
	5700 8650 5950 8650
Wire Wire Line
	5150 9000 5750 9000
Wire Wire Line
	5750 9000 5750 8750
Wire Wire Line
	5750 8750 5950 8750
Wire Wire Line
	5950 8850 5800 8850
Wire Wire Line
	5800 8850 5800 9150
Wire Wire Line
	5800 9150 5150 9150
Wire Wire Line
	5150 9300 5850 9300
Wire Wire Line
	5850 9300 5850 8950
Wire Wire Line
	5850 8950 5950 8950
Text Label 6350 7050 0    50   ~ 0
GND
Text Label 6350 8250 0    50   ~ 0
GND
Text Label 13050 800  1    50   ~ 0
VCC
Text Label 13050 1800 3    50   ~ 0
GND
Wire Wire Line
	13050 800  13850 800 
Wire Wire Line
	13850 800  13850 1100
Wire Wire Line
	13850 1400 13850 1800
Wire Wire Line
	13850 1800 13050 1800
Wire Wire Line
	13850 1800 14250 1800
Connection ~ 13850 1800
Wire Wire Line
	14250 1200 14250 1700
Connection ~ 14250 1700
Wire Wire Line
	14250 1700 14250 1800
Connection ~ 14250 1800
Wire Wire Line
	14250 1800 14250 2200
Connection ~ 14250 2200
Wire Wire Line
	14250 2200 14250 2700
Connection ~ 14250 2700
Wire Wire Line
	14250 2700 14250 3250
NoConn ~ 14850 1200
NoConn ~ 14850 1700
NoConn ~ 14850 2200
NoConn ~ 14850 2700
NoConn ~ 14850 3250
NoConn ~ 15200 5700
NoConn ~ 15200 5800
NoConn ~ 15200 5900
NoConn ~ 15200 6000
NoConn ~ 15200 6100
NoConn ~ 15200 6200
NoConn ~ 15200 6300
NoConn ~ 15200 6400
NoConn ~ 15200 6500
NoConn ~ 15200 6600
NoConn ~ 15200 6700
NoConn ~ 15200 7500
NoConn ~ 15200 7600
NoConn ~ 15200 7700
NoConn ~ 15200 7800
NoConn ~ 15200 7900
NoConn ~ 15200 8000
NoConn ~ 15200 8100
NoConn ~ 15200 8300
NoConn ~ 15200 8200
NoConn ~ 15200 8400
NoConn ~ 15200 8500
NoConn ~ 15200 8600
NoConn ~ 15200 8700
NoConn ~ 15200 8800
Text Label 14050 4700 3    50   ~ 0
CARRY_BORROW_OUT
Text Label 13950 4700 3    50   ~ 0
A_EQ_B
Wire Wire Line
	8850 2600 9050 2600
Wire Wire Line
	8850 2100 8850 2600
$Comp
L eight-bit-computer:74LS181 U2
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
L eight-bit-computer:74LS181 U3
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
L eight-bit-computer:74LS181 U5
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
L eight-bit-computer:74LS181 U7
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
P 9250 8100
F 0 "C12" H 9368 8146 50  0000 L CNN
F 1 "33uF" H 9368 8055 50  0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D6.3mm_P2.50mm" H 9288 7950 50  0001 C CNN
F 3 "~" H 9250 8100 50  0001 C CNN
	1    9250 8100
	1    0    0    -1  
$EndComp
Wire Wire Line
	9250 7950 9900 7950
Wire Wire Line
	9250 8250 9250 8300
Wire Wire Line
	9250 8300 9900 8300
$Comp
L Device:CP C14
U 1 1 5FC812BA
P 8800 8100
F 0 "C14" H 8918 8146 50  0000 L CNN
F 1 "33uF" H 8918 8055 50  0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D6.3mm_P2.50mm" H 8838 7950 50  0001 C CNN
F 3 "~" H 8800 8100 50  0001 C CNN
	1    8800 8100
	1    0    0    -1  
$EndComp
$Comp
L Device:CP C13
U 1 1 5FC81852
P 8350 8100
F 0 "C13" H 8468 8146 50  0000 L CNN
F 1 "33uF" H 8468 8055 50  0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D6.3mm_P2.50mm" H 8388 7950 50  0001 C CNN
F 3 "~" H 8350 8100 50  0001 C CNN
	1    8350 8100
	1    0    0    -1  
$EndComp
Wire Wire Line
	8350 7950 8800 7950
Connection ~ 9250 7950
Connection ~ 8800 7950
Wire Wire Line
	8800 7950 9250 7950
Wire Wire Line
	9250 8300 8800 8300
Wire Wire Line
	8350 8300 8350 8250
Connection ~ 9250 8300
Wire Wire Line
	8800 8250 8800 8300
Connection ~ 8800 8300
Wire Wire Line
	8800 8300 8350 8300
$EndSCHEMATC
