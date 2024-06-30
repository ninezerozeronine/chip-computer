"""
Programs that can be loaded into the computer
"""

PROGRAMS = (
    {
        "name":"Dum1",
        "content": (
            (0, 0),
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
        )
    },
    {
        "name":"Dum2",
        "content": (
            (0, 5),
            (1, 4),
            (2, 3),
            (3, 2),
            (4, 1),
            (1234, 1234),
        )
    },
    {
        "name":"Fibb",
        "content": (
            (0, 113),        # Line: 0016     SET SP #1
            (1, 1),          # Line: 0016
            (2, 110),        # Line: 0017     SET A #1
            (3, 1),          # Line: 0017
            (4, 43),         # Line: 0020     COPY SP ACC
            (5, 0),          # Line: 0021     ADD A
            (6, 161),        # Line: 0022     JUMP_IF_ACC_GT #1597 &set_initial
            (7, 1597),       # Line: 0022
            (8, 0),          # Line: 0022
            (9, 29),         # Line: 0023     COPY A SP
            (10, 22),        # Line: 0024     COPY ACC A
            (11, 125),       # Line: 0025     JUMP &fib_loop
            (12, 4),         # Line: 0025
        )
    },
    {
        "name":"TEST",
        "content": (
            (0, 119),        # Line: 0008     NOOP
            (1, 109),        # Line: 0015     SET ACC #1
            (2, 1),          # Line: 0015
            (3, 110),        # Line: 0016     SET A #2
            (4, 2),          # Line: 0016
            (5, 0),          # Line: 0017     ADD A
            (6, 146),        # Line: 0018     JUMP_IF_ACC_EQ #3 &add_1
            (7, 3),          # Line: 0018
            (8, 10),         # Line: 0018
            (9, 186),        # Line: 0019     HALT
            (10, 109),       # Line: 0022     SET ACC #456
            (11, 456),       # Line: 0022
            (12, 111),       # Line: 0023     SET B #111
            (13, 111),       # Line: 0023
            (14, 1),         # Line: 0024     ADD B
            (15, 146),       # Line: 0025     JUMP_IF_ACC_EQ #567 &add_2
            (16, 567),       # Line: 0025
            (17, 19),        # Line: 0025
            (18, 186),       # Line: 0026     HALT
            (19, 109),       # Line: 0029     SET ACC #3333
            (20, 3333),      # Line: 0029
            (21, 112),       # Line: 0030     SET C #2222
            (22, 2222),      # Line: 0030
            (23, 2),         # Line: 0031     ADD C
            (24, 146),       # Line: 0032     JUMP_IF_ACC_EQ #5555 &add_3
            (25, 5555),      # Line: 0032
            (26, 28),        # Line: 0032
            (27, 186),       # Line: 0033     HALT
            (28, 109),       # Line: 0036     SET ACC #123
            (29, 123),       # Line: 0036
            (30, 3),         # Line: 0037     ADD #-23
            (31, 65513),     # Line: 0037
            (32, 146),       # Line: 0038     JUMP_IF_ACC_EQ #100 &add_4
            (33, 100),       # Line: 0038
            (34, 37),        # Line: 0038
            (35, 186),       # Line: 0039     HALT
            (36, 42),        # Line: 0041 $v_add_0 #42
            (37, 109),       # Line: 0043     SET ACC #42
            (38, 42),        # Line: 0043
            (39, 4),         # Line: 0044     ADD [$v_add_0]
            (40, 36),        # Line: 0044
            (41, 146),       # Line: 0045     JUMP_IF_ACC_EQ #84 &lshift_0
            (42, 84),        # Line: 0045
            (43, 45),        # Line: 0045
            (44, 186),       # Line: 0046     HALT
            (45, 109),       # Line: 0053     SET ACC        #0b0011_1101_0000_0001
            (46, 15617),     # Line: 0053
            (47, 10),        # Line: 0054     LSHIFT ACC
            (48, 146),       # Line: 0055     JUMP_IF_ACC_EQ #0b0111_1010_0000_0010 &lshift_1
            (49, 31234),     # Line: 0055
            (50, 52),        # Line: 0055
            (51, 186),       # Line: 0056     HALT
            (52, 110),       # Line: 0059     SET A   #0b0101_0101_0101_0101
            (53, 21845),     # Line: 0059
            (54, 109),       # Line: 0060     SET ACC #0b1010_1010_1010_1010
            (55, 43690),     # Line: 0060
            (56, 11),        # Line: 0061     LSHIFT A
            (57, 142),       # Line: 0062     JUMP_IF_ACC_EQ A &lshift_2
            (58, 60),        # Line: 0062
            (59, 186),       # Line: 0063     HALT
            (60, 111),       # Line: 0066     SET B   #0b1111_1111_1111_1111
            (61, 65535),     # Line: 0066
            (62, 109),       # Line: 0067     SET ACC #0b1111_1111_1111_1110
            (63, 65534),     # Line: 0067
            (64, 12),        # Line: 0068     LSHIFT B
            (65, 143),       # Line: 0069     JUMP_IF_ACC_EQ B &lshift_3
            (66, 68),        # Line: 0069
            (67, 186),       # Line: 0070     HALT
            (68, 112),       # Line: 0073     SET C   #0b0000_1000_1000_1000
            (69, 2184),      # Line: 0073
            (70, 109),       # Line: 0074     SET ACC #0b0001_0001_0001_0000
            (71, 4368),      # Line: 0074
            (72, 13),        # Line: 0075     LSHIFT C
            (73, 144),       # Line: 0076     JUMP_IF_ACC_EQ C &sub_0
            (74, 76),        # Line: 0076
            (75, 186),       # Line: 0077     HALT
            (76, 109),       # Line: 0084     SET ACC #1
            (77, 1),         # Line: 0084
            (78, 110),       # Line: 0085     SET A #2
            (79, 2),         # Line: 0085
            (80, 5),         # Line: 0086     SUB A
            (81, 146),       # Line: 0087     JUMP_IF_ACC_EQ #-1 &sub_1
            (82, 65535),     # Line: 0087
            (83, 85),        # Line: 0087
            (84, 186),       # Line: 0088     HALT
            (85, 109),       # Line: 0091     SET ACC #456
            (86, 456),       # Line: 0091
            (87, 111),       # Line: 0092     SET B #111
            (88, 111),       # Line: 0092
            (89, 6),         # Line: 0093     SUB B
            (90, 146),       # Line: 0094     JUMP_IF_ACC_EQ #345 &sub_2
            (91, 345),       # Line: 0094
            (92, 94),        # Line: 0094
            (93, 186),       # Line: 0095     HALT
            (94, 109),       # Line: 0098     SET ACC #3333
            (95, 3333),      # Line: 0098
            (96, 112),       # Line: 0099     SET C #2222
            (97, 2222),      # Line: 0099
            (98, 7),         # Line: 0100     SUB C
            (99, 146),       # Line: 0101     JUMP_IF_ACC_EQ #1111 &sub_3
            (100, 1111),     # Line: 0101
            (101, 103),      # Line: 0101
            (102, 186),      # Line: 0102     HALT
            (103, 114),      # Line: 0105     SET_ZERO ACC
            (104, 8),        # Line: 0106     SUB #1
            (105, 1),        # Line: 0106
            (106, 146),      # Line: 0107     JUMP_IF_ACC_EQ #0xFFFF &sub_4
            (107, 65535),    # Line: 0107
            (108, 111),      # Line: 0107
            (109, 186),      # Line: 0108     HALT
            (110, 42),       # Line: 0110 $v_sub_0 #42
            (111, 109),      # Line: 0112     SET ACC #42
            (112, 42),       # Line: 0112
            (113, 9),        # Line: 0113     SUB [$v_sub_0]
            (114, 110),      # Line: 0113
            (115, 162),      # Line: 0114     JUMP_IF_EQ_ZERO ACC &incr_0
            (116, 118),      # Line: 0114
            (117, 186),      # Line: 0115     HALT
            (118, 109),      # Line: 0123     SET ACC #32
            (119, 32),       # Line: 0123
            (120, 14),       # Line: 0124     INCR ACC 
            (121, 146),      # Line: 0125     JUMP_IF_ACC_EQ #33 &incr_1
            (122, 33),       # Line: 0125
            (123, 125),      # Line: 0125
            (124, 186),      # Line: 0126     HALT
            (125, 109),      # Line: 0129     SET ACC #-31
            (126, 65505),    # Line: 0129
            (127, 110),      # Line: 0130     SET A #-32
            (128, 65504),    # Line: 0130
            (129, 15),       # Line: 0131     INCR A
            (130, 142),      # Line: 0132     JUMP_IF_ACC_EQ A &incr_2
            (131, 133),      # Line: 0132
            (132, 186),      # Line: 0133     HALT
            (133, 109),      # Line: 0136     SET ACC #256
            (134, 256),      # Line: 0136
            (135, 111),      # Line: 0137     SET B #255
            (136, 255),      # Line: 0137
            (137, 16),       # Line: 0138     INCR B
            (138, 143),      # Line: 0139     JUMP_IF_ACC_EQ B &incr_3
            (139, 141),      # Line: 0139
            (140, 186),      # Line: 0140     HALT
            (141, 109),      # Line: 0143     SET ACC #0
            (142, 0),        # Line: 0143
            (143, 112),      # Line: 0144     SET C #0xFFFF
            (144, 65535),    # Line: 0144
            (145, 17),       # Line: 0145     INCR C
            (146, 144),      # Line: 0146     JUMP_IF_ACC_EQ C &decr_0
            (147, 149),      # Line: 0146
            (148, 186),      # Line: 0147     HALT
            (149, 109),      # Line: 0154     SET ACC #32
            (150, 32),       # Line: 0154
            (151, 18),       # Line: 0155     DECR ACC 
            (152, 146),      # Line: 0156     JUMP_IF_ACC_EQ #31 &decr_1
            (153, 31),       # Line: 0156
            (154, 156),      # Line: 0156
            (155, 186),      # Line: 0157     HALT
            (156, 109),      # Line: 0160     SET ACC #-33
            (157, 65503),    # Line: 0160
            (158, 110),      # Line: 0161     SET A #-32
            (159, 65504),    # Line: 0161
            (160, 19),       # Line: 0162     DECR A
            (161, 142),      # Line: 0163     JUMP_IF_ACC_EQ A &decr_2
            (162, 164),      # Line: 0163
            (163, 186),      # Line: 0164     HALT
            (164, 109),      # Line: 0167     SET ACC #255
            (165, 255),      # Line: 0167
            (166, 111),      # Line: 0168     SET B #256
            (167, 256),      # Line: 0168
            (168, 20),       # Line: 0169     DECR B
            (169, 143),      # Line: 0170     JUMP_IF_ACC_EQ B &decr_3
            (170, 172),      # Line: 0170
            (171, 186),      # Line: 0171     HALT
            (172, 109),      # Line: 0174     SET ACC #0xFFFF
            (173, 65535),    # Line: 0174
            (174, 112),      # Line: 0175     SET C #0
            (175, 0),        # Line: 0175
            (176, 21),       # Line: 0176     DECR C
            (177, 144),      # Line: 0177     JUMP_IF_ACC_EQ C &copy_0
            (178, 180),      # Line: 0177
            (179, 186),      # Line: 0178     HALT
            (180, 109),      # Line: 0185     SET ACC #4799
            (181, 4799),     # Line: 0185
            (182, 22),       # Line: 0186     COPY ACC A
            (183, 142),      # Line: 0187     JUMP_IF_ACC_EQ A &copy_1
            (184, 186),      # Line: 0187
            (185, 186),      # Line: 0188     HALT
            (186, 109),      # Line: 0191     SET ACC #52686
            (187, 52686),    # Line: 0191
            (188, 23),       # Line: 0192     COPY ACC B
            (189, 143),      # Line: 0193     JUMP_IF_ACC_EQ B &copy_2
            (190, 192),      # Line: 0193
            (191, 186),      # Line: 0194     HALT
            (192, 109),      # Line: 0197     SET ACC #35304
            (193, 35304),    # Line: 0197
            (194, 24),       # Line: 0198     COPY ACC C
            (195, 144),      # Line: 0199     JUMP_IF_ACC_EQ C &copy_3
            (196, 198),      # Line: 0199
            (197, 186),      # Line: 0200     HALT
            (198, 109),      # Line: 0203     SET ACC #36137
            (199, 36137),    # Line: 0203
            (200, 25),       # Line: 0204     COPY ACC SP
            (201, 145),      # Line: 0205     JUMP_IF_ACC_EQ SP &copy_4
            (202, 204),      # Line: 0205
            (203, 186),      # Line: 0206     HALT
            (204, 110),      # Line: 0209     SET A #15993
            (205, 15993),    # Line: 0209
            (206, 26),       # Line: 0210     COPY A ACC
            (207, 146),      # Line: 0211     JUMP_IF_ACC_EQ #15993 &copy_5
            (208, 15993),    # Line: 0211
            (209, 211),      # Line: 0211
            (210, 186),      # Line: 0212     HALT
            (211, 110),      # Line: 0215     SET A #28834
            (212, 28834),    # Line: 0215
            (213, 109),      # Line: 0216     SET ACC #28834
            (214, 28834),    # Line: 0216
            (215, 27),       # Line: 0217     COPY A B
            (216, 143),      # Line: 0218     JUMP_IF_ACC_EQ B &copy_6
            (217, 219),      # Line: 0218
            (218, 186),      # Line: 0219     HALT
            (219, 110),      # Line: 0222     SET A #58775
            (220, 58775),    # Line: 0222
            (221, 109),      # Line: 0223     SET ACC #58775
            (222, 58775),    # Line: 0223
            (223, 28),       # Line: 0224     COPY A C
            (224, 144),      # Line: 0225     JUMP_IF_ACC_EQ C &copy_7
            (225, 227),      # Line: 0225
            (226, 186),      # Line: 0226     HALT
            (227, 110),      # Line: 0229     SET A #60244
            (228, 60244),    # Line: 0229
            (229, 109),      # Line: 0230     SET ACC #60244
            (230, 60244),    # Line: 0230
            (231, 29),       # Line: 0231     COPY A SP
            (232, 145),      # Line: 0232     JUMP_IF_ACC_EQ SP &copy_8
            (233, 235),      # Line: 0232
            (234, 186),      # Line: 0233     HALT
            (235, 111),      # Line: 0236     SET B #17634
            (236, 17634),    # Line: 0236
            (237, 30),       # Line: 0237     COPY B ACC
            (238, 146),      # Line: 0238     JUMP_IF_ACC_EQ #17634 &copy_9
            (239, 17634),    # Line: 0238
            (240, 242),      # Line: 0238
            (241, 186),      # Line: 0239     HALT
            (242, 111),      # Line: 0242     SET B #56775
            (243, 56775),    # Line: 0242
            (244, 109),      # Line: 0243     SET ACC #56775
            (245, 56775),    # Line: 0243
            (246, 31),       # Line: 0244     COPY B A
            (247, 142),      # Line: 0245     JUMP_IF_ACC_EQ A &copy_10
            (248, 250),      # Line: 0245
            (249, 186),      # Line: 0246     HALT
            (250, 111),      # Line: 0249     SET B #59278
            (251, 59278),    # Line: 0249
            (252, 109),      # Line: 0250     SET ACC #59278
            (253, 59278),    # Line: 0250
            (254, 32),       # Line: 0251     COPY B C
            (255, 144),      # Line: 0252     JUMP_IF_ACC_EQ C &copy_11
            (256, 258),      # Line: 0252
            (257, 186),      # Line: 0253     HALT
            (258, 111),      # Line: 0256     SET B #22164
            (259, 22164),    # Line: 0256
            (260, 109),      # Line: 0257     SET ACC #22164
            (261, 22164),    # Line: 0257
            (262, 33),       # Line: 0258     COPY B SP
            (263, 145),      # Line: 0259     JUMP_IF_ACC_EQ SP &copy_12
            (264, 266),      # Line: 0259
            (265, 186),      # Line: 0260     HALT
            (266, 112),      # Line: 0263     SET C #48215
            (267, 48215),    # Line: 0263
            (268, 34),       # Line: 0264     COPY C ACC
            (269, 146),      # Line: 0265     JUMP_IF_ACC_EQ #48215 &copy_13
            (270, 48215),    # Line: 0265
            (271, 273),      # Line: 0265
            (272, 186),      # Line: 0266     HALT
            (273, 112),      # Line: 0269     SET C #10020
            (274, 10020),    # Line: 0269
            (275, 109),      # Line: 0270     SET ACC #10020
            (276, 10020),    # Line: 0270
            (277, 35),       # Line: 0271     COPY C A
            (278, 142),      # Line: 0272     JUMP_IF_ACC_EQ A &copy_14
            (279, 281),      # Line: 0272
            (280, 186),      # Line: 0273     HALT
            (281, 112),      # Line: 0276     SET C #65463
            (282, 65463),    # Line: 0276
            (283, 109),      # Line: 0277     SET ACC #65463
            (284, 65463),    # Line: 0277
            (285, 36),       # Line: 0278     COPY C B
            (286, 143),      # Line: 0279     JUMP_IF_ACC_EQ B &copy_15
            (287, 289),      # Line: 0279
            (288, 186),      # Line: 0280     HALT
            (289, 112),      # Line: 0283     SET C #38525
            (290, 38525),    # Line: 0283
            (291, 109),      # Line: 0284     SET ACC #38525
            (292, 38525),    # Line: 0284
            (293, 37),       # Line: 0285     COPY C SP
            (294, 145),      # Line: 0286     JUMP_IF_ACC_EQ SP &copy_16
            (295, 297),      # Line: 0286
            (296, 186),      # Line: 0287     HALT
            (297, 113),      # Line: 0290     SET SP #47483
            (298, 47483),    # Line: 0290
            (299, 43),       # Line: 0291     COPY SP ACC
            (300, 146),      # Line: 0292     JUMP_IF_ACC_EQ #47483 &copy_17
            (301, 47483),    # Line: 0292
            (302, 304),      # Line: 0292
            (303, 186),      # Line: 0293     HALT
            (304, 113),      # Line: 0296     SET SP #5944
            (305, 5944),     # Line: 0296
            (306, 109),      # Line: 0297     SET ACC #5944
            (307, 5944),     # Line: 0297
            (308, 44),       # Line: 0298     COPY SP A
            (309, 142),      # Line: 0299     JUMP_IF_ACC_EQ A &copy_18
            (310, 312),      # Line: 0299
            (311, 186),      # Line: 0300     HALT
            (312, 113),      # Line: 0303     SET SP #57017
            (313, 57017),    # Line: 0303
            (314, 109),      # Line: 0304     SET ACC #57017
            (315, 57017),    # Line: 0304
            (316, 45),       # Line: 0305     COPY SP B
            (317, 143),      # Line: 0306     JUMP_IF_ACC_EQ B &copy_19
            (318, 320),      # Line: 0306
            (319, 186),      # Line: 0307     HALT
            (320, 113),      # Line: 0310     SET SP #34392
            (321, 34392),    # Line: 0310
            (322, 109),      # Line: 0311     SET ACC #34392
            (323, 34392),    # Line: 0311
            (324, 46),       # Line: 0312     COPY SP C
            (325, 144),      # Line: 0313     JUMP_IF_ACC_EQ C &load_0
            (326, 329),      # Line: 0313
            (327, 186),      # Line: 0314     HALT
            (328, 24004),    # Line: 0320 $v_load_0 #24004
            (329, 109),      # Line: 0322     SET ACC $v_load_0
            (330, 328),      # Line: 0322
            (331, 47),       # Line: 0323     LOAD [ACC] ACC
            (332, 146),      # Line: 0324     JUMP_IF_ACC_EQ #24004 &load_1
            (333, 24004),    # Line: 0324
            (334, 337),      # Line: 0324
            (335, 186),      # Line: 0325     HALT
            (336, 11709),    # Line: 0327 $v_load_1 #11709
            (337, 109),      # Line: 0329     SET ACC $v_load_1
            (338, 336),      # Line: 0329
            (339, 48),       # Line: 0330     LOAD [ACC] A
            (340, 109),      # Line: 0331     SET ACC #11709
            (341, 11709),    # Line: 0331
            (342, 142),      # Line: 0332     JUMP_IF_ACC_EQ A &load_2
            (343, 346),      # Line: 0332
            (344, 186),      # Line: 0333     HALT
            (345, 59692),    # Line: 0335 $v_load_2 #59692
            (346, 109),      # Line: 0337     SET ACC $v_load_2
            (347, 345),      # Line: 0337
            (348, 49),       # Line: 0338     LOAD [ACC] B
            (349, 109),      # Line: 0339     SET ACC #59692
            (350, 59692),    # Line: 0339
            (351, 143),      # Line: 0340     JUMP_IF_ACC_EQ B &load_3
            (352, 355),      # Line: 0340
            (353, 186),      # Line: 0341     HALT
            (354, 12087),    # Line: 0343 $v_load_3 #12087
            (355, 109),      # Line: 0345     SET ACC $v_load_3
            (356, 354),      # Line: 0345
            (357, 50),       # Line: 0346     LOAD [ACC] C
            (358, 109),      # Line: 0347     SET ACC #12087
            (359, 12087),    # Line: 0347
            (360, 144),      # Line: 0348     JUMP_IF_ACC_EQ C &load_4
            (361, 364),      # Line: 0348
            (362, 186),      # Line: 0349     HALT
            (363, 20982),    # Line: 0351 $v_load_4 #20982
            (364, 110),      # Line: 0353     SET A $v_load_4
            (365, 363),      # Line: 0353
            (366, 51),       # Line: 0354     LOAD [A] ACC
            (367, 146),      # Line: 0355     JUMP_IF_ACC_EQ #20982 &load_5
            (368, 20982),    # Line: 0355
            (369, 372),      # Line: 0355
            (370, 186),      # Line: 0356     HALT
            (371, 51597),    # Line: 0358 $v_load_5 #51597
            (372, 110),      # Line: 0360     SET A $v_load_5
            (373, 371),      # Line: 0360
            (374, 52),       # Line: 0361     LOAD [A] A
            (375, 109),      # Line: 0362     SET ACC #51597
            (376, 51597),    # Line: 0362
            (377, 142),      # Line: 0363     JUMP_IF_ACC_EQ A &load_6
            (378, 381),      # Line: 0363
            (379, 186),      # Line: 0364     HALT
            (380, 22009),    # Line: 0366 $v_load_6 #22009
            (381, 110),      # Line: 0368     SET A $v_load_6
            (382, 380),      # Line: 0368
            (383, 53),       # Line: 0369     LOAD [A] B
            (384, 109),      # Line: 0370     SET ACC #22009
            (385, 22009),    # Line: 0370
            (386, 143),      # Line: 0371     JUMP_IF_ACC_EQ B &load_7
            (387, 390),      # Line: 0371
            (388, 186),      # Line: 0372     HALT
            (389, 11703),    # Line: 0374 $v_load_7 #11703
            (390, 110),      # Line: 0376     SET A $v_load_7
            (391, 389),      # Line: 0376
            (392, 54),       # Line: 0377     LOAD [A] C
            (393, 109),      # Line: 0378     SET ACC #11703
            (394, 11703),    # Line: 0378
            (395, 144),      # Line: 0379     JUMP_IF_ACC_EQ C &load_8
            (396, 399),      # Line: 0379
            (397, 186),      # Line: 0380     HALT
            (398, 57854),    # Line: 0382 $v_load_8 #57854
            (399, 111),      # Line: 0384     SET B $v_load_8
            (400, 398),      # Line: 0384
            (401, 55),       # Line: 0385     LOAD [B] ACC
            (402, 146),      # Line: 0386     JUMP_IF_ACC_EQ #57854 &load_9
            (403, 57854),    # Line: 0386
            (404, 407),      # Line: 0386
            (405, 186),      # Line: 0387     HALT
            (406, 37360),    # Line: 0389 $v_load_9 #37360
            (407, 111),      # Line: 0391     SET B $v_load_9
            (408, 406),      # Line: 0391
            (409, 56),       # Line: 0392     LOAD [B] A
            (410, 109),      # Line: 0393     SET ACC #37360
            (411, 37360),    # Line: 0393
            (412, 142),      # Line: 0394     JUMP_IF_ACC_EQ A &load_10
            (413, 416),      # Line: 0394
            (414, 186),      # Line: 0395     HALT
            (415, 57819),    # Line: 0397 $v_load_10 #57819
            (416, 111),      # Line: 0399     SET B $v_load_10
            (417, 415),      # Line: 0399
            (418, 57),       # Line: 0400     LOAD [B] B
            (419, 109),      # Line: 0401     SET ACC #57819
            (420, 57819),    # Line: 0401
            (421, 143),      # Line: 0402     JUMP_IF_ACC_EQ B &load_11
            (422, 425),      # Line: 0402
            (423, 186),      # Line: 0403     HALT
            (424, 60912),    # Line: 0405 $v_load_11 #60912
            (425, 111),      # Line: 0407     SET B $v_load_11
            (426, 424),      # Line: 0407
            (427, 58),       # Line: 0408     LOAD [B] C
            (428, 109),      # Line: 0409     SET ACC #60912
            (429, 60912),    # Line: 0409
            (430, 144),      # Line: 0410     JUMP_IF_ACC_EQ C &load_12
            (431, 434),      # Line: 0410
            (432, 186),      # Line: 0411     HALT
            (433, 38245),    # Line: 0413 $v_load_12 #38245
            (434, 112),      # Line: 0415     SET C $v_load_12
            (435, 433),      # Line: 0415
            (436, 59),       # Line: 0416     LOAD [C] ACC
            (437, 146),      # Line: 0417     JUMP_IF_ACC_EQ #38245 &load_13
            (438, 38245),    # Line: 0417
            (439, 442),      # Line: 0417
            (440, 186),      # Line: 0418     HALT
            (441, 25454),    # Line: 0420 $v_load_13 #25454
            (442, 112),      # Line: 0422     SET C $v_load_13
            (443, 441),      # Line: 0422
            (444, 60),       # Line: 0423     LOAD [C] A
            (445, 109),      # Line: 0424     SET ACC #25454
            (446, 25454),    # Line: 0424
            (447, 142),      # Line: 0425     JUMP_IF_ACC_EQ A &load_14
            (448, 451),      # Line: 0425
            (449, 186),      # Line: 0426     HALT
            (450, 25444),    # Line: 0428 $v_load_14 #25444
            (451, 112),      # Line: 0430     SET C $v_load_14
            (452, 450),      # Line: 0430
            (453, 61),       # Line: 0431     LOAD [C] B
            (454, 109),      # Line: 0432     SET ACC #25444
            (455, 25444),    # Line: 0432
            (456, 143),      # Line: 0433     JUMP_IF_ACC_EQ B &load_15
            (457, 460),      # Line: 0433
            (458, 186),      # Line: 0434     HALT
            (459, 20527),    # Line: 0436 $v_load_15 #20527
            (460, 112),      # Line: 0438     SET C $v_load_15
            (461, 459),      # Line: 0438
            (462, 62),       # Line: 0439     LOAD [C] C
            (463, 109),      # Line: 0440     SET ACC #20527
            (464, 20527),    # Line: 0440
            (465, 144),      # Line: 0441     JUMP_IF_ACC_EQ C &load_16
            (466, 469),      # Line: 0441
            (467, 186),      # Line: 0442     HALT
            (468, 60336),    # Line: 0444 $v_load_16 #60336
            (469, 113),      # Line: 0446     SET SP $v_load_16
            (470, 468),      # Line: 0446
            (471, 63),       # Line: 0447     LOAD [SP] ACC
            (472, 146),      # Line: 0448     JUMP_IF_ACC_EQ #60336 &load_17
            (473, 60336),    # Line: 0448
            (474, 477),      # Line: 0448
            (475, 186),      # Line: 0449     HALT
            (476, 56769),    # Line: 0451 $v_load_17 #56769
            (477, 113),      # Line: 0453     SET SP $v_load_17
            (478, 476),      # Line: 0453
            (479, 64),       # Line: 0454     LOAD [SP] A
            (480, 109),      # Line: 0455     SET ACC #56769
            (481, 56769),    # Line: 0455
            (482, 142),      # Line: 0456     JUMP_IF_ACC_EQ A &load_18
            (483, 486),      # Line: 0456
            (484, 186),      # Line: 0457     HALT
            (485, 49044),    # Line: 0459 $v_load_18 #49044
            (486, 113),      # Line: 0461     SET SP $v_load_18
            (487, 485),      # Line: 0461
            (488, 65),       # Line: 0462     LOAD [SP] B
            (489, 109),      # Line: 0463     SET ACC #49044
            (490, 49044),    # Line: 0463
            (491, 143),      # Line: 0464     JUMP_IF_ACC_EQ B &load_19
            (492, 495),      # Line: 0464
            (493, 186),      # Line: 0465     HALT
            (494, 34177),    # Line: 0467 $v_load_19 #34177
            (495, 113),      # Line: 0469     SET SP $v_load_19
            (496, 494),      # Line: 0469
            (497, 66),       # Line: 0470     LOAD [SP] C
            (498, 109),      # Line: 0471     SET ACC #34177
            (499, 34177),    # Line: 0471
            (500, 144),      # Line: 0472     JUMP_IF_ACC_EQ C &load_20
            (501, 504),      # Line: 0472
            (502, 186),      # Line: 0473     HALT
            (503, 56580),    # Line: 0475 $v_load_20 #56580
            (504, 67),       # Line: 0477     LOAD [$v_load_20] ACC
            (505, 503),      # Line: 0477
            (506, 146),      # Line: 0478     JUMP_IF_ACC_EQ #56580 &load_21
            (507, 56580),    # Line: 0478
            (508, 511),      # Line: 0478
            (509, 186),      # Line: 0479     HALT
            (510, 47253),    # Line: 0481 $v_load_21 #47253
            (511, 68),       # Line: 0483     LOAD [$v_load_21] A
            (512, 510),      # Line: 0483
            (513, 109),      # Line: 0484     SET ACC #47253
            (514, 47253),    # Line: 0484
            (515, 142),      # Line: 0485     JUMP_IF_ACC_EQ A &load_22
            (516, 519),      # Line: 0485
            (517, 186),      # Line: 0486     HALT
            (518, 55439),    # Line: 0488 $v_load_22 #55439
            (519, 69),       # Line: 0490     LOAD [$v_load_22] B
            (520, 518),      # Line: 0490
            (521, 109),      # Line: 0491     SET ACC #55439
            (522, 55439),    # Line: 0491
            (523, 143),      # Line: 0492     JUMP_IF_ACC_EQ B &load_23
            (524, 527),      # Line: 0492
            (525, 186),      # Line: 0493     HALT
            (526, 7661),     # Line: 0495 $v_load_23 #7661
            (527, 70),       # Line: 0497     LOAD [$v_load_23] C
            (528, 526),      # Line: 0497
            (529, 109),      # Line: 0498     SET ACC #7661
            (530, 7661),     # Line: 0498
            (531, 144),      # Line: 0499     JUMP_IF_ACC_EQ C &store_0
            (532, 535),      # Line: 0499
            (533, 186),      # Line: 0500     HALT
            (535, 109),      # Line: 0508     SET ACC $v_store_0
            (536, 534),      # Line: 0508
            (537, 71),       # Line: 0509     STORE ACC [ACC]
            (538, 47),       # Line: 0510     LOAD [ACC] ACC
            (539, 146),      # Line: 0511     JUMP_IF_ACC_EQ $v_store_0 &store_1
            (540, 534),      # Line: 0511
            (541, 544),      # Line: 0511
            (542, 186),      # Line: 0512     HALT
            (544, 109),      # Line: 0516     SET ACC #31763
            (545, 31763),    # Line: 0516
            (546, 110),      # Line: 0517     SET A $v_store_1
            (547, 543),      # Line: 0517
            (548, 72),       # Line: 0518     STORE ACC [A]
            (549, 51),       # Line: 0519     LOAD [A] ACC
            (550, 146),      # Line: 0520     JUMP_IF_ACC_EQ #31763 &store_2
            (551, 31763),    # Line: 0520
            (552, 555),      # Line: 0520
            (553, 186),      # Line: 0521     HALT
            (555, 109),      # Line: 0525     SET ACC #35606
            (556, 35606),    # Line: 0525
            (557, 111),      # Line: 0526     SET B $v_store_2
            (558, 554),      # Line: 0526
            (559, 73),       # Line: 0527     STORE ACC [B]
            (560, 55),       # Line: 0528     LOAD [B] ACC
            (561, 146),      # Line: 0529     JUMP_IF_ACC_EQ #35606 &store_3
            (562, 35606),    # Line: 0529
            (563, 566),      # Line: 0529
            (564, 186),      # Line: 0530     HALT
            (566, 109),      # Line: 0534     SET ACC #27292
            (567, 27292),    # Line: 0534
            (568, 112),      # Line: 0535     SET C $v_store_3
            (569, 565),      # Line: 0535
            (570, 74),       # Line: 0536     STORE ACC [C]
            (571, 59),       # Line: 0537     LOAD [C] ACC
            (572, 146),      # Line: 0538     JUMP_IF_ACC_EQ #27292 &store_4
            (573, 27292),    # Line: 0538
            (574, 577),      # Line: 0538
            (575, 186),      # Line: 0539     HALT
            (577, 109),      # Line: 0543     SET ACC #13156
            (578, 13156),    # Line: 0543
            (579, 113),      # Line: 0544     SET SP $v_store_4
            (580, 576),      # Line: 0544
            (581, 75),       # Line: 0545     STORE ACC [SP]
            (582, 63),       # Line: 0546     LOAD [SP] ACC
            (583, 146),      # Line: 0547     JUMP_IF_ACC_EQ #13156 &store_5
            (584, 13156),    # Line: 0547
            (585, 588),      # Line: 0547
            (586, 186),      # Line: 0548     HALT
            (588, 109),      # Line: 0552     SET ACC #36181
            (589, 36181),    # Line: 0552
            (590, 76),       # Line: 0553     STORE ACC [$v_store_5]
            (591, 587),      # Line: 0553
            (592, 67),       # Line: 0554     LOAD [$v_store_5] ACC
            (593, 587),      # Line: 0554
            (594, 146),      # Line: 0555     JUMP_IF_ACC_EQ #36181 &store_6
            (595, 36181),    # Line: 0555
            (596, 599),      # Line: 0555
            (597, 186),      # Line: 0556     HALT
            (599, 110),      # Line: 0560     SET A #11935
            (600, 11935),    # Line: 0560
            (601, 109),      # Line: 0561     SET ACC $v_store_6
            (602, 598),      # Line: 0561
            (603, 77),       # Line: 0562     STORE A [ACC]
            (604, 47),       # Line: 0563     LOAD [ACC] ACC
            (605, 146),      # Line: 0564     JUMP_IF_ACC_EQ #11935 &store_7
            (606, 11935),    # Line: 0564
            (607, 610),      # Line: 0564
            (608, 186),      # Line: 0565     HALT
            (610, 110),      # Line: 0569     SET A $v_store_7
            (611, 609),      # Line: 0569
            (612, 78),       # Line: 0570     STORE A [A]
            (613, 51),       # Line: 0571     LOAD [A] ACC
            (614, 146),      # Line: 0572     JUMP_IF_ACC_EQ $v_store_7 &store_8
            (615, 609),      # Line: 0572
            (616, 619),      # Line: 0572
            (617, 186),      # Line: 0573     HALT
            (619, 110),      # Line: 0577     SET A #27215
            (620, 27215),    # Line: 0577
            (621, 111),      # Line: 0578     SET B $v_store_8
            (622, 618),      # Line: 0578
            (623, 79),       # Line: 0579     STORE A [B]
            (624, 55),       # Line: 0580     LOAD [B] ACC
            (625, 146),      # Line: 0581     JUMP_IF_ACC_EQ #27215 &store_9
            (626, 27215),    # Line: 0581
            (627, 630),      # Line: 0581
            (628, 186),      # Line: 0582     HALT
            (630, 110),      # Line: 0586     SET A #31533
            (631, 31533),    # Line: 0586
            (632, 112),      # Line: 0587     SET C $v_store_9
            (633, 629),      # Line: 0587
            (634, 80),       # Line: 0588     STORE A [C]
            (635, 59),       # Line: 0589     LOAD [C] ACC
            (636, 146),      # Line: 0590     JUMP_IF_ACC_EQ #31533 &store_10
            (637, 31533),    # Line: 0590
            (638, 641),      # Line: 0590
            (639, 186),      # Line: 0591     HALT
            (641, 110),      # Line: 0595     SET A #65214
            (642, 65214),    # Line: 0595
            (643, 113),      # Line: 0596     SET SP $v_store_10
            (644, 640),      # Line: 0596
            (645, 81),       # Line: 0597     STORE A [SP]
            (646, 63),       # Line: 0598     LOAD [SP] ACC
            (647, 146),      # Line: 0599     JUMP_IF_ACC_EQ #65214 &store_11
            (648, 65214),    # Line: 0599
            (649, 652),      # Line: 0599
            (650, 186),      # Line: 0600     HALT
            (652, 110),      # Line: 0604     SET A #25149
            (653, 25149),    # Line: 0604
            (654, 82),       # Line: 0605     STORE A [$v_store_11]
            (655, 651),      # Line: 0605
            (656, 67),       # Line: 0606     LOAD [$v_store_11] ACC
            (657, 651),      # Line: 0606
            (658, 146),      # Line: 0607     JUMP_IF_ACC_EQ #25149 &store_12
            (659, 25149),    # Line: 0607
            (660, 663),      # Line: 0607
            (661, 186),      # Line: 0608     HALT
            (663, 111),      # Line: 0612     SET B #61844
            (664, 61844),    # Line: 0612
            (665, 109),      # Line: 0613     SET ACC $v_store_12
            (666, 662),      # Line: 0613
            (667, 83),       # Line: 0614     STORE B [ACC]
            (668, 47),       # Line: 0615     LOAD [ACC] ACC
            (669, 146),      # Line: 0616     JUMP_IF_ACC_EQ #61844 &store_13
            (670, 61844),    # Line: 0616
            (671, 674),      # Line: 0616
            (672, 186),      # Line: 0617     HALT
            (674, 111),      # Line: 0621     SET B #22749
            (675, 22749),    # Line: 0621
            (676, 110),      # Line: 0622     SET A $v_store_13
            (677, 673),      # Line: 0622
            (678, 84),       # Line: 0623     STORE B [A]
            (679, 51),       # Line: 0624     LOAD [A] ACC
            (680, 146),      # Line: 0625     JUMP_IF_ACC_EQ #22749 &store_14
            (681, 22749),    # Line: 0625
            (682, 685),      # Line: 0625
            (683, 186),      # Line: 0626     HALT
            (685, 111),      # Line: 0630     SET B $v_store_14
            (686, 684),      # Line: 0630
            (687, 85),       # Line: 0631     STORE B [B]
            (688, 55),       # Line: 0632     LOAD [B] ACC
            (689, 146),      # Line: 0633     JUMP_IF_ACC_EQ $v_store_14 &store_15
            (690, 684),      # Line: 0633
            (691, 694),      # Line: 0633
            (692, 186),      # Line: 0634     HALT
            (694, 111),      # Line: 0638     SET B #21277
            (695, 21277),    # Line: 0638
            (696, 112),      # Line: 0639     SET C $v_store_15
            (697, 693),      # Line: 0639
            (698, 86),       # Line: 0640     STORE B [C]
            (699, 59),       # Line: 0641     LOAD [C] ACC
            (700, 146),      # Line: 0642     JUMP_IF_ACC_EQ #21277 &store_16
            (701, 21277),    # Line: 0642
            (702, 705),      # Line: 0642
            (703, 186),      # Line: 0643     HALT
            (705, 111),      # Line: 0647     SET B #64660
            (706, 64660),    # Line: 0647
            (707, 113),      # Line: 0648     SET SP $v_store_16
            (708, 704),      # Line: 0648
            (709, 87),       # Line: 0649     STORE B [SP]
            (710, 63),       # Line: 0650     LOAD [SP] ACC
            (711, 146),      # Line: 0651     JUMP_IF_ACC_EQ #64660 &store_17
            (712, 64660),    # Line: 0651
            (713, 716),      # Line: 0651
            (714, 186),      # Line: 0652     HALT
            (716, 111),      # Line: 0656     SET B #54157
            (717, 54157),    # Line: 0656
            (718, 88),       # Line: 0657     STORE B [$v_store_17]
            (719, 715),      # Line: 0657
            (720, 67),       # Line: 0658     LOAD [$v_store_17] ACC
            (721, 715),      # Line: 0658
            (722, 146),      # Line: 0659     JUMP_IF_ACC_EQ #54157 &store_18
            (723, 54157),    # Line: 0659
            (724, 727),      # Line: 0659
            (725, 186),      # Line: 0660     HALT
            (727, 112),      # Line: 0664     SET C #46522
            (728, 46522),    # Line: 0664
            (729, 109),      # Line: 0665     SET ACC $v_store_18
            (730, 726),      # Line: 0665
            (731, 89),       # Line: 0666     STORE C [ACC]
            (732, 47),       # Line: 0667     LOAD [ACC] ACC
            (733, 146),      # Line: 0668     JUMP_IF_ACC_EQ #46522 &store_19
            (734, 46522),    # Line: 0668
            (735, 738),      # Line: 0668
            (736, 186),      # Line: 0669     HALT
            (738, 112),      # Line: 0673     SET C #7117
            (739, 7117),     # Line: 0673
            (740, 110),      # Line: 0674     SET A $v_store_19
            (741, 737),      # Line: 0674
            (742, 90),       # Line: 0675     STORE C [A]
            (743, 51),       # Line: 0676     LOAD [A] ACC
            (744, 146),      # Line: 0677     JUMP_IF_ACC_EQ #7117 &store_20
            (745, 7117),     # Line: 0677
            (746, 749),      # Line: 0677
            (747, 186),      # Line: 0678     HALT
            (749, 112),      # Line: 0682     SET C #49497
            (750, 49497),    # Line: 0682
            (751, 111),      # Line: 0683     SET B $v_store_20
            (752, 748),      # Line: 0683
            (753, 91),       # Line: 0684     STORE C [B]
            (754, 55),       # Line: 0685     LOAD [B] ACC
            (755, 146),      # Line: 0686     JUMP_IF_ACC_EQ #49497 &store_21
            (756, 49497),    # Line: 0686
            (757, 760),      # Line: 0686
            (758, 186),      # Line: 0687     HALT
            (760, 112),      # Line: 0691     SET C $v_store_21
            (761, 759),      # Line: 0691
            (762, 92),       # Line: 0692     STORE C [C]
            (763, 59),       # Line: 0693     LOAD [C] ACC
            (764, 146),      # Line: 0694     JUMP_IF_ACC_EQ $v_store_21 &store_22
            (765, 759),      # Line: 0694
            (766, 769),      # Line: 0694
            (767, 186),      # Line: 0695     HALT
            (769, 112),      # Line: 0699     SET C #12486
            (770, 12486),    # Line: 0699
            (771, 113),      # Line: 0700     SET SP $v_store_22
            (772, 768),      # Line: 0700
            (773, 93),       # Line: 0701     STORE C [SP]
            (774, 63),       # Line: 0702     LOAD [SP] ACC
            (775, 146),      # Line: 0703     JUMP_IF_ACC_EQ #12486 &store_23
            (776, 12486),    # Line: 0703
            (777, 780),      # Line: 0703
            (778, 186),      # Line: 0704     HALT
            (780, 112),      # Line: 0708     SET C #63220
            (781, 63220),    # Line: 0708
            (782, 94),       # Line: 0709     STORE C [$v_store_23]
            (783, 779),      # Line: 0709
            (784, 67),       # Line: 0710     LOAD [$v_store_23] ACC
            (785, 779),      # Line: 0710
            (786, 146),      # Line: 0711     JUMP_IF_ACC_EQ #63220 &store_24
            (787, 63220),    # Line: 0711
            (788, 791),      # Line: 0711
            (789, 186),      # Line: 0712     HALT
            (791, 113),      # Line: 0716     SET SP #50736
            (792, 50736),    # Line: 0716
            (793, 109),      # Line: 0717     SET ACC $v_store_24
            (794, 790),      # Line: 0717
            (795, 95),       # Line: 0718     STORE SP [ACC]
            (796, 47),       # Line: 0719     LOAD [ACC] ACC
            (797, 146),      # Line: 0720     JUMP_IF_ACC_EQ #50736 &store_25
            (798, 50736),    # Line: 0720
            (799, 802),      # Line: 0720
            (800, 186),      # Line: 0721     HALT
            (802, 113),      # Line: 0725     SET SP #44571
            (803, 44571),    # Line: 0725
            (804, 110),      # Line: 0726     SET A $v_store_25
            (805, 801),      # Line: 0726
            (806, 96),       # Line: 0727     STORE SP [A]
            (807, 51),       # Line: 0728     LOAD [A] ACC
            (808, 146),      # Line: 0729     JUMP_IF_ACC_EQ #44571 &store_26
            (809, 44571),    # Line: 0729
            (810, 813),      # Line: 0729
            (811, 186),      # Line: 0730     HALT
            (813, 113),      # Line: 0734     SET SP #28464
            (814, 28464),    # Line: 0734
            (815, 111),      # Line: 0735     SET B $v_store_26
            (816, 812),      # Line: 0735
            (817, 97),       # Line: 0736     STORE SP [B]
            (818, 55),       # Line: 0737     LOAD [B] ACC
            (819, 146),      # Line: 0738     JUMP_IF_ACC_EQ #28464 &store_27
            (820, 28464),    # Line: 0738
            (821, 824),      # Line: 0738
            (822, 186),      # Line: 0739     HALT
            (824, 113),      # Line: 0743     SET SP #34092
            (825, 34092),    # Line: 0743
            (826, 112),      # Line: 0744     SET C $v_store_27
            (827, 823),      # Line: 0744
            (828, 98),       # Line: 0745     STORE SP [C]
            (829, 59),       # Line: 0746     LOAD [C] ACC
            (830, 146),      # Line: 0747     JUMP_IF_ACC_EQ #34092 &store_28
            (831, 34092),    # Line: 0747
            (832, 835),      # Line: 0747
            (833, 186),      # Line: 0748     HALT
            (835, 113),      # Line: 0752     SET SP $v_store_28
            (836, 834),      # Line: 0752
            (837, 99),       # Line: 0753     STORE SP [SP]
            (838, 63),       # Line: 0754     LOAD [SP] ACC
            (839, 146),      # Line: 0755     JUMP_IF_ACC_EQ $v_store_28 &store_29
            (840, 834),      # Line: 0755
            (841, 844),      # Line: 0755
            (842, 186),      # Line: 0756     HALT
            (844, 113),      # Line: 0760     SET SP #30456
            (845, 30456),    # Line: 0760
            (846, 100),      # Line: 0761     STORE SP [$v_store_29]
            (847, 843),      # Line: 0761
            (848, 67),       # Line: 0762     LOAD [$v_store_29] ACC
            (849, 843),      # Line: 0762
            (850, 146),      # Line: 0763     JUMP_IF_ACC_EQ #30456 &push_0
            (851, 30456),    # Line: 0763
            (852, 854),      # Line: 0763
            (853, 186),      # Line: 0764     HALT
            (854, 119),      # Line: 0771     NOOP
            (855, 119),      # Line: 0772     NOOP
            (856, 119),      # Line: 0774     NOOP
            (857, 119),      # Line: 0775     NOOP
            (858, 119),      # Line: 0776     NOOP
            (859, 113),      # Line: 0777     SET SP &push_1    
            (860, 856),      # Line: 0777
            (861, 109),      # Line: 0779     SET ACC #567
            (862, 567),      # Line: 0779
            (863, 101),      # Line: 0780     PUSH ACC
            (864, 114),      # Line: 0781     SET_ZERO ACC
            (865, 63),       # Line: 0782     LOAD [SP] ACC
            (866, 146),      # Line: 0783     JUMP_IF_ACC_EQ #567 &push_2
            (867, 567),      # Line: 0783
            (868, 870),      # Line: 0783
            (869, 186),      # Line: 0784     HALT
            (870, 113),      # Line: 0787     SET SP &push_1 
            (871, 856),      # Line: 0787
            (872, 110),      # Line: 0788     SET A #123
            (873, 123),      # Line: 0788
            (874, 102),      # Line: 0789     PUSH A
            (875, 63),       # Line: 0790     LOAD [SP] ACC
            (876, 146),      # Line: 0791     JUMP_IF_ACC_EQ #123 &push_3
            (877, 123),      # Line: 0791
            (878, 880),      # Line: 0791
            (879, 186),      # Line: 0792     HALT
            (880, 113),      # Line: 0795     SET SP &push_1 
            (881, 856),      # Line: 0795
            (882, 111),      # Line: 0796     SET B #333
            (883, 333),      # Line: 0796
            (884, 103),      # Line: 0797     PUSH B
            (885, 63),       # Line: 0798     LOAD [SP] ACC
            (886, 146),      # Line: 0799     JUMP_IF_ACC_EQ #333 &push_4
            (887, 333),      # Line: 0799
            (888, 890),      # Line: 0799
            (889, 186),      # Line: 0800     HALT
            (890, 113),      # Line: 0803     SET SP &push_1 
            (891, 856),      # Line: 0803
            (892, 112),      # Line: 0804     SET C !zero_one
            (893, 21845),    # Line: 0804
            (894, 104),      # Line: 0805     PUSH C
            (895, 63),       # Line: 0806     LOAD [SP] ACC
            (896, 146),      # Line: 0807     JUMP_IF_ACC_EQ !zero_one &pop_0
            (897, 21845),    # Line: 0807
            (898, 900),      # Line: 0807
            (899, 186),      # Line: 0808     HALT
            (900, 119),      # Line: 0815     NOOP
            (901, 119),      # Line: 0816     NOOP
            (902, 119),      # Line: 0818     NOOP
            (903, 119),      # Line: 0819     NOOP
            (904, 119),      # Line: 0820     NOOP
            (905, 113),      # Line: 0821     SET SP &pop_1    
            (906, 902),      # Line: 0821
            (907, 109),      # Line: 0823     SET ACC !one_zero
            (908, 43690),    # Line: 0823
            (909, 101),      # Line: 0824     PUSH ACC
            (910, 114),      # Line: 0825     SET_ZERO ACC
            (911, 63),       # Line: 0826     LOAD [SP] ACC
            (912, 146),      # Line: 0827     JUMP_IF_ACC_EQ !one_zero &pop_2
            (913, 43690),    # Line: 0827
            (914, 916),      # Line: 0827
            (915, 186),      # Line: 0828     HALT
            (916, 113),      # Line: 0831     SET SP &pop_1 
            (917, 902),      # Line: 0831
            (918, 110),      # Line: 0832     SET A #5681
            (919, 5681),     # Line: 0832
            (920, 102),      # Line: 0833     PUSH A
            (921, 63),       # Line: 0834     LOAD [SP] ACC
            (922, 146),      # Line: 0835     JUMP_IF_ACC_EQ #5681 &pop_3
            (923, 5681),     # Line: 0835
            (924, 926),      # Line: 0835
            (925, 186),      # Line: 0836     HALT
            (926, 113),      # Line: 0839     SET SP &pop_1 
            (927, 902),      # Line: 0839
            (928, 111),      # Line: 0840     SET B #22222
            (929, 22222),    # Line: 0840
            (930, 103),      # Line: 0841     PUSH B
            (931, 63),       # Line: 0842     LOAD [SP] ACC
            (932, 146),      # Line: 0843     JUMP_IF_ACC_EQ #22222 &pop_4
            (933, 22222),    # Line: 0843
            (934, 936),      # Line: 0843
            (935, 186),      # Line: 0844     HALT
            (936, 113),      # Line: 0847     SET SP &pop_1 
            (937, 902),      # Line: 0847
            (938, 112),      # Line: 0848     SET C #4242
            (939, 4242),     # Line: 0848
            (940, 104),      # Line: 0849     PUSH C
            (941, 63),       # Line: 0850     LOAD [SP] ACC
            (942, 146),      # Line: 0851     JUMP_IF_ACC_EQ #4242 &set_0
            (943, 4242),     # Line: 0851
            (944, 946),      # Line: 0851
            (945, 186),      # Line: 0852     HALT
            (946, 109),      # Line: 0859     SET ACC !zero_one
            (947, 21845),    # Line: 0859
            (948, 110),      # Line: 0860     SET A !zero_one
            (949, 21845),    # Line: 0860
            (950, 147),      # Line: 0861     JUMP_IF_ACC_NEQ A &set_halt0
            (951, 972),      # Line: 0861
            (952, 109),      # Line: 0863     SET ACC !one_zero
            (953, 43690),    # Line: 0863
            (954, 111),      # Line: 0864     SET B !one_zero
            (955, 43690),    # Line: 0864
            (956, 148),      # Line: 0865     JUMP_IF_ACC_NEQ B &set_halt1
            (957, 973),      # Line: 0865
            (958, 109),      # Line: 0867     SET ACC !zero_one
            (959, 21845),    # Line: 0867
            (960, 112),      # Line: 0868     SET C !zero_one
            (961, 21845),    # Line: 0868
            (962, 149),      # Line: 0869     JUMP_IF_ACC_NEQ C &set_halt2   
            (963, 974),      # Line: 0869
            (964, 109),      # Line: 0871     SET ACC !one_zero
            (965, 43690),    # Line: 0871
            (966, 113),      # Line: 0872     SET SP !one_zero
            (967, 43690),    # Line: 0872
            (968, 150),      # Line: 0873     JUMP_IF_ACC_NEQ SP &set_halt3
            (969, 975),      # Line: 0873
            (970, 125),      # Line: 0875     JUMP &set_zero_0
            (971, 976),      # Line: 0875
            (972, 186),      # Line: 0878     HALT
            (973, 186),      # Line: 0880     HALT
            (974, 186),      # Line: 0882     HALT
            (975, 186),      # Line: 0884     HALT
            (976, 114),      # Line: 0891     SET_ZERO ACC
            (977, 167),      # Line: 0892     JUMP_IF_NEQ_ZERO ACC &set_zero_halt0
            (978, 993),      # Line: 0892
            (979, 115),      # Line: 0894     SET_ZERO A
            (980, 168),      # Line: 0895     JUMP_IF_NEQ_ZERO A &set_zero_halt1
            (981, 994),      # Line: 0895
            (982, 116),      # Line: 0897     SET_ZERO B
            (983, 169),      # Line: 0898     JUMP_IF_NEQ_ZERO B &set_zero_halt2
            (984, 995),      # Line: 0898
            (985, 117),      # Line: 0900     SET_ZERO C
            (986, 170),      # Line: 0901     JUMP_IF_NEQ_ZERO C &set_zero_halt3
            (987, 996),      # Line: 0901
            (988, 118),      # Line: 0903     SET_ZERO SP
            (989, 171),      # Line: 0904     JUMP_IF_NEQ_ZERO SP &set_zero_halt4
            (990, 997),      # Line: 0904
            (991, 125),      # Line: 0906     JUMP &noop_0
            (992, 998),      # Line: 0906
            (993, 186),      # Line: 0909     HALT
            (994, 186),      # Line: 0911     HALT
            (995, 186),      # Line: 0913     HALT
            (996, 186),      # Line: 0915     HALT
            (997, 186),      # Line: 0917     HALT
            (998, 119),      # Line: 0924     NOOP
            (999, 109),      # Line: 0931     SET ACC &jump_1
            (1000, 1003),    # Line: 0931
            (1001, 120),     # Line: 0932     JUMP ACC
            (1002, 186),     # Line: 0933     HALT
            (1003, 110),     # Line: 0936     SET A &jump_2
            (1004, 1007),    # Line: 0936
            (1005, 121),     # Line: 0937     JUMP A
            (1006, 186),     # Line: 0938     HALT
            (1007, 111),     # Line: 0941     SET B &jump_3
            (1008, 1011),    # Line: 0941
            (1009, 122),     # Line: 0942     JUMP B
            (1010, 186),     # Line: 0943     HALT
            (1011, 112),     # Line: 0946     SET C &jump_4
            (1012, 1015),    # Line: 0946
            (1013, 123),     # Line: 0947     JUMP C
            (1014, 186),     # Line: 0948     HALT
            (1015, 113),     # Line: 0951     SET SP &jump_5
            (1016, 1019),    # Line: 0951
            (1017, 124),     # Line: 0952     JUMP SP
            (1018, 186),     # Line: 0953     HALT
            (1019, 125),     # Line: 0956     JUMP &jump_6
            (1020, 1023),    # Line: 0956
            (1021, 186),     # Line: 0957     HALT
            (1022, 1028),    # Line: 0959 $v_jump_0 &jump7
            (1023, 109),     # Line: 0961     SET ACC $v_jump_0
            (1024, 1022),    # Line: 0961
            (1025, 126),     # Line: 0962     JUMP [ACC]
            (1026, 186),     # Line: 0963     HALT
            (1027, 1033),    # Line: 0965 $v_jump_1 &jump8
            (1028, 110),     # Line: 0967     SET A $v_jump_1
            (1029, 1027),    # Line: 0967
            (1030, 127),     # Line: 0968     JUMP [A]
            (1031, 186),     # Line: 0969     HALT
            (1032, 1038),    # Line: 0971 $v_jump_2 &jump9
            (1033, 111),     # Line: 0973     SET B $v_jump_2
            (1034, 1032),    # Line: 0973
            (1035, 128),     # Line: 0974     JUMP [B]
            (1036, 186),     # Line: 0975     HALT
            (1037, 1043),    # Line: 0977 $v_jump_3 &jump10
            (1038, 112),     # Line: 0979     SET C $v_jump_3
            (1039, 1037),    # Line: 0979
            (1040, 129),     # Line: 0980     JUMP [C]
            (1041, 186),     # Line: 0981     HALT
            (1042, 1048),    # Line: 0983 $v_jump_4 &jump11
            (1043, 113),     # Line: 0985     SET SP $v_jump_4
            (1044, 1042),    # Line: 0985
            (1045, 130),     # Line: 0986     JUMP [SP]
            (1046, 186),     # Line: 0987     HALT
            (1047, 1051),    # Line: 0989 $v_jump_5 &jialt_0
            (1048, 131),     # Line: 0991     JUMP [$v_jump_5]
            (1049, 1047),    # Line: 0991
            (1050, 186),     # Line: 0992     HALT
            (1051, 110),     # Line: 1000     SET A #12
            (1052, 12),      # Line: 1000
            (1053, 109),     # Line: 1001     SET ACC #2
            (1054, 2),       # Line: 1001
            (1055, 132),     # Line: 1002     JUMP_IF_ACC_LT A &jialt_1
            (1056, 1058),    # Line: 1002
            (1057, 186),     # Line: 1003     HALT
            (1058, 111),     # Line: 1006     SET B #123
            (1059, 123),     # Line: 1006
            (1060, 109),     # Line: 1007     SET ACC #0
            (1061, 0),       # Line: 1007
            (1062, 133),     # Line: 1008     JUMP_IF_ACC_LT B &jialt_2
            (1063, 1065),    # Line: 1008
            (1064, 186),     # Line: 1009     HALT
            (1065, 112),     # Line: 1012     SET C #12345
            (1066, 12345),   # Line: 1012
            (1067, 109),     # Line: 1013     SET ACC #1234
            (1068, 1234),    # Line: 1013
            (1069, 134),     # Line: 1014     JUMP_IF_ACC_LT C &jialt_3
            (1070, 1072),    # Line: 1014
            (1071, 186),     # Line: 1015     HALT
            (1072, 113),     # Line: 1018     SET SP #6000
            (1073, 6000),    # Line: 1018
            (1074, 109),     # Line: 1019     SET ACC #4242
            (1075, 4242),    # Line: 1019
            (1076, 135),     # Line: 1020     JUMP_IF_ACC_LT SP &jialt_4
            (1077, 1079),    # Line: 1020
            (1078, 186),     # Line: 1021     HALT
            (1079, 109),     # Line: 1024     SET ACC #1000
            (1080, 1000),    # Line: 1024
            (1081, 136),     # Line: 1025     JUMP_IF_ACC_LT #1001 &jialt_5
            (1082, 1001),    # Line: 1025
            (1083, 1085),    # Line: 1025
            (1084, 186),     # Line: 1026     HALT
            (1085, 110),     # Line: 1030     SET A #2
            (1086, 2),       # Line: 1030
            (1087, 109),     # Line: 1031     SET ACC #2
            (1088, 2),       # Line: 1031
            (1089, 132),     # Line: 1032     JUMP_IF_ACC_LT A &jialt_halt_0
            (1090, 1116),    # Line: 1032
            (1091, 111),     # Line: 1034     SET B #1
            (1092, 1),       # Line: 1034
            (1093, 109),     # Line: 1035     SET ACC #123
            (1094, 123),     # Line: 1035
            (1095, 133),     # Line: 1036     JUMP_IF_ACC_LT B &jialt_halt_1
            (1096, 1117),    # Line: 1036
            (1097, 112),     # Line: 1038     SET C #123
            (1098, 123),     # Line: 1038
            (1099, 109),     # Line: 1039     SET ACC #12345
            (1100, 12345),   # Line: 1039
            (1101, 134),     # Line: 1040     JUMP_IF_ACC_LT C &jialt_halt_2
            (1102, 1118),    # Line: 1040
            (1103, 113),     # Line: 1042     SET SP #3545
            (1104, 3545),    # Line: 1042
            (1105, 109),     # Line: 1043     SET ACC #3545
            (1106, 3545),    # Line: 1043
            (1107, 135),     # Line: 1044     JUMP_IF_ACC_LT SP &jialt_halt_3
            (1108, 1119),    # Line: 1044
            (1109, 109),     # Line: 1046     SET ACC #1001
            (1110, 1001),    # Line: 1046
            (1111, 136),     # Line: 1047     JUMP_IF_ACC_LT #1000 &jialt_halt_4
            (1112, 1000),    # Line: 1047
            (1113, 1120),    # Line: 1047
            (1114, 125),     # Line: 1048     JUMP &jialte_0
            (1115, 1121),    # Line: 1048
            (1116, 186),     # Line: 1051     HALT
            (1117, 186),     # Line: 1053     HALT
            (1118, 186),     # Line: 1055     HALT
            (1119, 186),     # Line: 1057     HALT
            (1120, 186),     # Line: 1059     HALT
            (1121, 110),     # Line: 1067     SET A #12
            (1122, 12),      # Line: 1067
            (1123, 109),     # Line: 1068     SET ACC #2
            (1124, 2),       # Line: 1068
            (1125, 137),     # Line: 1069     JUMP_IF_ACC_LTE A &jialte_1
            (1126, 1128),    # Line: 1069
            (1127, 186),     # Line: 1070     HALT
            (1128, 110),     # Line: 1073     SET A #123
            (1129, 123),     # Line: 1073
            (1130, 109),     # Line: 1074     SET ACC #123
            (1131, 123),     # Line: 1074
            (1132, 137),     # Line: 1075     JUMP_IF_ACC_LTE A &jialte_2
            (1133, 1135),    # Line: 1075
            (1134, 186),     # Line: 1076     HALT
            (1135, 111),     # Line: 1079     SET B #12345
            (1136, 12345),   # Line: 1079
            (1137, 109),     # Line: 1080     SET ACC #1234
            (1138, 1234),    # Line: 1080
            (1139, 138),     # Line: 1081     JUMP_IF_ACC_LTE B &jialte_3
            (1140, 1142),    # Line: 1081
            (1141, 186),     # Line: 1082     HALT
            (1142, 111),     # Line: 1085     SET B #6000
            (1143, 6000),    # Line: 1085
            (1144, 109),     # Line: 1086     SET ACC #6000
            (1145, 6000),    # Line: 1086
            (1146, 138),     # Line: 1087     JUMP_IF_ACC_LTE B &jialte_4
            (1147, 1149),    # Line: 1087
            (1148, 186),     # Line: 1088     HALT
            (1149, 112),     # Line: 1091     SET C #12345
            (1150, 12345),   # Line: 1091
            (1151, 109),     # Line: 1092     SET ACC #1234
            (1152, 1234),    # Line: 1092
            (1153, 139),     # Line: 1093     JUMP_IF_ACC_LTE C &jialte_5
            (1154, 1156),    # Line: 1093
            (1155, 186),     # Line: 1094     HALT
            (1156, 112),     # Line: 1097     SET C #4321
            (1157, 4321),    # Line: 1097
            (1158, 109),     # Line: 1098     SET ACC #4321
            (1159, 4321),    # Line: 1098
            (1160, 139),     # Line: 1099     JUMP_IF_ACC_LTE C &jialte_6
            (1161, 1163),    # Line: 1099
            (1162, 186),     # Line: 1100     HALT
            (1163, 113),     # Line: 1103     SET SP #12345
            (1164, 12345),   # Line: 1103
            (1165, 109),     # Line: 1104     SET ACC #1234
            (1166, 1234),    # Line: 1104
            (1167, 140),     # Line: 1105     JUMP_IF_ACC_LTE SP &jialte_7
            (1168, 1170),    # Line: 1105
            (1169, 186),     # Line: 1106     HALT
            (1170, 113),     # Line: 1109     SET SP #6000
            (1171, 6000),    # Line: 1109
            (1172, 109),     # Line: 1110     SET ACC #6000
            (1173, 6000),    # Line: 1110
            (1174, 140),     # Line: 1111     JUMP_IF_ACC_LTE SP &jialte_8
            (1175, 1177),    # Line: 1111
            (1176, 186),     # Line: 1112     HALT
            (1177, 109),     # Line: 1115     SET ACC #1000
            (1178, 1000),    # Line: 1115
            (1179, 141),     # Line: 1116     JUMP_IF_ACC_LTE #1001 &jialte_9
            (1180, 1001),    # Line: 1116
            (1181, 1183),    # Line: 1116
            (1182, 186),     # Line: 1117     HALT
            (1183, 109),     # Line: 1120     SET ACC #1111
            (1184, 1111),    # Line: 1120
            (1185, 141),     # Line: 1121     JUMP_IF_ACC_LTE #1111 &jialte_10
            (1186, 1111),    # Line: 1121
            (1187, 1189),    # Line: 1121
            (1188, 186),     # Line: 1122     HALT
            (1189, 110),     # Line: 1127     SET A #2
            (1190, 2),       # Line: 1127
            (1191, 109),     # Line: 1128     SET ACC #12
            (1192, 12),      # Line: 1128
            (1193, 137),     # Line: 1129     JUMP_IF_ACC_LTE A &jialte_halt_0
            (1194, 1220),    # Line: 1129
            (1195, 111),     # Line: 1131     SET B #1
            (1196, 1),       # Line: 1131
            (1197, 109),     # Line: 1132     SET ACC #123
            (1198, 123),     # Line: 1132
            (1199, 138),     # Line: 1133     JUMP_IF_ACC_LTE B &jialte_halt_1
            (1200, 1221),    # Line: 1133
            (1201, 112),     # Line: 1135     SET C #123
            (1202, 123),     # Line: 1135
            (1203, 109),     # Line: 1136     SET ACC #12345
            (1204, 12345),   # Line: 1136
            (1205, 139),     # Line: 1137     JUMP_IF_ACC_LTE C &jialte_halt_2
            (1206, 1222),    # Line: 1137
            (1207, 113),     # Line: 1139     SET SP #3545
            (1208, 3545),    # Line: 1139
            (1209, 109),     # Line: 1140     SET ACC #50000
            (1210, 50000),   # Line: 1140
            (1211, 140),     # Line: 1141     JUMP_IF_ACC_LTE SP &jialte_halt_3
            (1212, 1223),    # Line: 1141
            (1213, 109),     # Line: 1143     SET ACC #1001
            (1214, 1001),    # Line: 1143
            (1215, 141),     # Line: 1144     JUMP_IF_ACC_LTE #1000 &jialte_halt_4
            (1216, 1000),    # Line: 1144
            (1217, 1224),    # Line: 1144
            (1218, 125),     # Line: 1145     JUMP &jiae_0
            (1219, 1225),    # Line: 1145
            (1220, 186),     # Line: 1148     HALT
            (1221, 186),     # Line: 1150     HALT
            (1222, 186),     # Line: 1152     HALT
            (1223, 186),     # Line: 1154     HALT
            (1224, 186),     # Line: 1156     HALT
            (1225, 109),     # Line: 1163     SET ACC #123
            (1226, 123),     # Line: 1163
            (1227, 110),     # Line: 1164     SET A #123
            (1228, 123),     # Line: 1164
            (1229, 142),     # Line: 1165     JUMP_IF_ACC_EQ A &jiae_1
            (1230, 1232),    # Line: 1165
            (1231, 186),     # Line: 1166     HALT
            (1232, 109),     # Line: 1169     SET ACC #456
            (1233, 456),     # Line: 1169
            (1234, 111),     # Line: 1170     SET B #456
            (1235, 456),     # Line: 1170
            (1236, 143),     # Line: 1171     JUMP_IF_ACC_EQ B &jiae_2
            (1237, 1239),    # Line: 1171
            (1238, 186),     # Line: 1172     HALT
            (1239, 109),     # Line: 1175     SET ACC #789
            (1240, 789),     # Line: 1175
            (1241, 112),     # Line: 1176     SET C #789
            (1242, 789),     # Line: 1176
            (1243, 144),     # Line: 1177     JUMP_IF_ACC_EQ C &jiae_3
            (1244, 1246),    # Line: 1177
            (1245, 186),     # Line: 1178     HALT
            (1246, 109),     # Line: 1181     SET ACC #1011
            (1247, 1011),    # Line: 1181
            (1248, 113),     # Line: 1182     SET SP #1011
            (1249, 1011),    # Line: 1182
            (1250, 145),     # Line: 1183     JUMP_IF_ACC_EQ SP &jiae_4
            (1251, 1253),    # Line: 1183
            (1252, 186),     # Line: 1184     HALT
            (1253, 109),     # Line: 1187     SET ACC #60123
            (1254, 60123),   # Line: 1187
            (1255, 146),     # Line: 1188     JUMP_IF_ACC_EQ #60123 &jiane_5
            (1256, 60123),   # Line: 1188
            (1257, 1329),    # Line: 1188
            (1258, 186),     # Line: 1189     HALT
            (1259, 109),     # Line: 1192     SET ACC #123
            (1260, 123),     # Line: 1192
            (1261, 110),     # Line: 1193     SET A #345
            (1262, 345),     # Line: 1193
            (1263, 142),     # Line: 1194     JUMP_IF_ACC_EQ A &jiae_halt_0
            (1264, 1290),    # Line: 1194
            (1265, 109),     # Line: 1196     SET ACC #456
            (1266, 456),     # Line: 1196
            (1267, 111),     # Line: 1197     SET B #11111
            (1268, 11111),   # Line: 1197
            (1269, 143),     # Line: 1198     JUMP_IF_ACC_EQ B &jiae_halt_1
            (1270, 1291),    # Line: 1198
            (1271, 109),     # Line: 1200     SET ACC #789
            (1272, 789),     # Line: 1200
            (1273, 112),     # Line: 1201     SET C #477
            (1274, 477),     # Line: 1201
            (1275, 144),     # Line: 1202     JUMP_IF_ACC_EQ C &jiae_halt_2
            (1276, 1292),    # Line: 1202
            (1277, 109),     # Line: 1204     SET ACC #1011
            (1278, 1011),    # Line: 1204
            (1279, 113),     # Line: 1205     SET SP #4524
            (1280, 4524),    # Line: 1205
            (1281, 145),     # Line: 1206     JUMP_IF_ACC_EQ SP &jiae_halt_3
            (1282, 1293),    # Line: 1206
            (1283, 109),     # Line: 1208     SET ACC #60123
            (1284, 60123),   # Line: 1208
            (1285, 146),     # Line: 1209     JUMP_IF_ACC_EQ #999 &jiae_halt_4
            (1286, 999),     # Line: 1209
            (1287, 1294),    # Line: 1209
            (1288, 125),     # Line: 1211     JUMP &jiane_0
            (1289, 1295),    # Line: 1211
            (1290, 186),     # Line: 1214     HALT
            (1291, 186),     # Line: 1216     HALT
            (1292, 186),     # Line: 1218     HALT
            (1293, 186),     # Line: 1220     HALT
            (1294, 186),     # Line: 1222     HALT
            (1295, 109),     # Line: 1229     SET ACC #123
            (1296, 123),     # Line: 1229
            (1297, 110),     # Line: 1230     SET A #1234
            (1298, 1234),    # Line: 1230
            (1299, 147),     # Line: 1231     JUMP_IF_ACC_NEQ A &jiane_1
            (1300, 1302),    # Line: 1231
            (1301, 186),     # Line: 1232     HALT
            (1302, 109),     # Line: 1235     SET ACC #321
            (1303, 321),     # Line: 1235
            (1304, 111),     # Line: 1236     SET B #55555
            (1305, 55555),   # Line: 1236
            (1306, 148),     # Line: 1237     JUMP_IF_ACC_NEQ B &jiane_2
            (1307, 1309),    # Line: 1237
            (1308, 186),     # Line: 1238     HALT
            (1309, 109),     # Line: 1241     SET ACC #21454
            (1310, 21454),   # Line: 1241
            (1311, 112),     # Line: 1242     SET C #6874
            (1312, 6874),    # Line: 1242
            (1313, 149),     # Line: 1243     JUMP_IF_ACC_NEQ C &jiane_3
            (1314, 1316),    # Line: 1243
            (1315, 186),     # Line: 1244     HALT
            (1316, 109),     # Line: 1247     SET ACC #3333
            (1317, 3333),    # Line: 1247
            (1318, 113),     # Line: 1248     SET SP #4444
            (1319, 4444),    # Line: 1248
            (1320, 150),     # Line: 1249     JUMP_IF_ACC_NEQ SP &jiane_4
            (1321, 1323),    # Line: 1249
            (1322, 186),     # Line: 1250     HALT
            (1323, 109),     # Line: 1253     SET ACC !one_zero
            (1324, 43690),   # Line: 1253
            (1325, 151),     # Line: 1254     JUMP_IF_ACC_NEQ !zero_one &jiane_5
            (1326, 21845),   # Line: 1254
            (1327, 1329),    # Line: 1254
            (1328, 186),     # Line: 1255     HALT
            (1329, 109),     # Line: 1258     SET ACC #456
            (1330, 456),     # Line: 1258
            (1331, 110),     # Line: 1259     SET A #456
            (1332, 456),     # Line: 1259
            (1333, 147),     # Line: 1260     JUMP_IF_ACC_NEQ A &jiane_halt_0
            (1334, 1360),    # Line: 1260
            (1335, 109),     # Line: 1262     SET ACC #1122
            (1336, 1122),    # Line: 1262
            (1337, 111),     # Line: 1263     SET B #1122
            (1338, 1122),    # Line: 1263
            (1339, 148),     # Line: 1264     JUMP_IF_ACC_NEQ B &jiane_halt_1
            (1340, 1361),    # Line: 1264
            (1341, 109),     # Line: 1266     SET ACC #3333
            (1342, 3333),    # Line: 1266
            (1343, 112),     # Line: 1267     SET C #3333
            (1344, 3333),    # Line: 1267
            (1345, 149),     # Line: 1268     JUMP_IF_ACC_NEQ C &jiane_halt_2
            (1346, 1362),    # Line: 1268
            (1347, 109),     # Line: 1270     SET ACC #5678
            (1348, 5678),    # Line: 1270
            (1349, 113),     # Line: 1271     SET SP #5678
            (1350, 5678),    # Line: 1271
            (1351, 150),     # Line: 1272     JUMP_IF_ACC_NEQ SP &jiane_halt_3
            (1352, 1363),    # Line: 1272
            (1353, 109),     # Line: 1274     SET ACC !one_zero
            (1354, 43690),   # Line: 1274
            (1355, 151),     # Line: 1275     JUMP_IF_ACC_NEQ !one_zero &jiane_halt_4
            (1356, 43690),   # Line: 1275
            (1357, 1364),    # Line: 1275
            (1358, 125),     # Line: 1277     JUMP &jiagte_0
            (1359, 1365),    # Line: 1277
            (1360, 186),     # Line: 1280     HALT
            (1361, 186),     # Line: 1282     HALT
            (1362, 186),     # Line: 1284     HALT
            (1363, 186),     # Line: 1286     HALT
            (1364, 186),     # Line: 1288     HALT
            (1365, 110),     # Line: 1296     SET A #12
            (1366, 12),      # Line: 1296
            (1367, 109),     # Line: 1297     SET ACC #20
            (1368, 20),      # Line: 1297
            (1369, 152),     # Line: 1298     JUMP_IF_ACC_GTE A &jiagte_1
            (1370, 1372),    # Line: 1298
            (1371, 186),     # Line: 1299     HALT
            (1372, 110),     # Line: 1302     SET A #123
            (1373, 123),     # Line: 1302
            (1374, 109),     # Line: 1303     SET ACC #123
            (1375, 123),     # Line: 1303
            (1376, 152),     # Line: 1304     JUMP_IF_ACC_GTE A &jiagte_2
            (1377, 1379),    # Line: 1304
            (1378, 186),     # Line: 1305     HALT
            (1379, 111),     # Line: 1308     SET B #1234
            (1380, 1234),    # Line: 1308
            (1381, 109),     # Line: 1309     SET ACC #12341
            (1382, 12341),   # Line: 1309
            (1383, 153),     # Line: 1310     JUMP_IF_ACC_GTE B &jiagte_3
            (1384, 1386),    # Line: 1310
            (1385, 186),     # Line: 1311     HALT
            (1386, 111),     # Line: 1314     SET B #6000
            (1387, 6000),    # Line: 1314
            (1388, 109),     # Line: 1315     SET ACC #6000
            (1389, 6000),    # Line: 1315
            (1390, 153),     # Line: 1316     JUMP_IF_ACC_GTE B &jiagte_4
            (1391, 1393),    # Line: 1316
            (1392, 186),     # Line: 1317     HALT
            (1393, 112),     # Line: 1320     SET C #123
            (1394, 123),     # Line: 1320
            (1395, 109),     # Line: 1321     SET ACC #1234
            (1396, 1234),    # Line: 1321
            (1397, 154),     # Line: 1322     JUMP_IF_ACC_GTE C &jiagte_5
            (1398, 1400),    # Line: 1322
            (1399, 186),     # Line: 1323     HALT
            (1400, 112),     # Line: 1326     SET C #555
            (1401, 555),     # Line: 1326
            (1402, 109),     # Line: 1327     SET ACC #555
            (1403, 555),     # Line: 1327
            (1404, 154),     # Line: 1328     JUMP_IF_ACC_GTE C &jiagte_6
            (1405, 1407),    # Line: 1328
            (1406, 186),     # Line: 1329     HALT
            (1407, 113),     # Line: 1332     SET SP #500
            (1408, 500),     # Line: 1332
            (1409, 109),     # Line: 1333     SET ACC #1000
            (1410, 1000),    # Line: 1333
            (1411, 155),     # Line: 1334     JUMP_IF_ACC_GTE SP &jiagte_7
            (1412, 1414),    # Line: 1334
            (1413, 186),     # Line: 1335     HALT
            (1414, 113),     # Line: 1338     SET SP #999
            (1415, 999),     # Line: 1338
            (1416, 109),     # Line: 1339     SET ACC #999
            (1417, 999),     # Line: 1339
            (1418, 155),     # Line: 1340     JUMP_IF_ACC_GTE SP &jiagte_8
            (1419, 1421),    # Line: 1340
            (1420, 186),     # Line: 1341     HALT
            (1421, 109),     # Line: 1344     SET ACC #1000
            (1422, 1000),    # Line: 1344
            (1423, 156),     # Line: 1345     JUMP_IF_ACC_GTE #3 &jiagte_9
            (1424, 3),       # Line: 1345
            (1425, 1427),    # Line: 1345
            (1426, 186),     # Line: 1346     HALT
            (1427, 109),     # Line: 1349     SET ACC #1111
            (1428, 1111),    # Line: 1349
            (1429, 156),     # Line: 1350     JUMP_IF_ACC_GTE #1111 &jiagte_10
            (1430, 1111),    # Line: 1350
            (1431, 1433),    # Line: 1350
            (1432, 186),     # Line: 1351     HALT
            (1433, 110),     # Line: 1356     SET A #24
            (1434, 24),      # Line: 1356
            (1435, 109),     # Line: 1357     SET ACC #12
            (1436, 12),      # Line: 1357
            (1437, 152),     # Line: 1358     JUMP_IF_ACC_GTE A &jiagte_halt_0
            (1438, 1464),    # Line: 1358
            (1439, 111),     # Line: 1360     SET B #1
            (1440, 1),       # Line: 1360
            (1441, 109),     # Line: 1361     SET ACC #0
            (1442, 0),       # Line: 1361
            (1443, 153),     # Line: 1362     JUMP_IF_ACC_GTE B &jiagte_halt_1
            (1444, 1465),    # Line: 1362
            (1445, 112),     # Line: 1364     SET C #987
            (1446, 987),     # Line: 1364
            (1447, 109),     # Line: 1365     SET ACC #654
            (1448, 654),     # Line: 1365
            (1449, 154),     # Line: 1366     JUMP_IF_ACC_GTE C &jiagte_halt_2
            (1450, 1466),    # Line: 1366
            (1451, 113),     # Line: 1368     SET SP #50000
            (1452, 50000),   # Line: 1368
            (1453, 109),     # Line: 1369     SET ACC #352
            (1454, 352),     # Line: 1369
            (1455, 155),     # Line: 1370     JUMP_IF_ACC_GTE SP &jiagte_halt_3
            (1456, 1467),    # Line: 1370
            (1457, 109),     # Line: 1372     SET ACC #10001
            (1458, 10001),   # Line: 1372
            (1459, 156),     # Line: 1373     JUMP_IF_ACC_GTE #12000 &jiagte_halt_4
            (1460, 12000),   # Line: 1373
            (1461, 1468),    # Line: 1373
            (1462, 125),     # Line: 1374     JUMP &jiagt_0
            (1463, 1469),    # Line: 1374
            (1464, 186),     # Line: 1377     HALT
            (1465, 186),     # Line: 1379     HALT
            (1466, 186),     # Line: 1381     HALT
            (1467, 186),     # Line: 1383     HALT
            (1468, 186),     # Line: 1385     HALT
            (1469, 110),     # Line: 1393     SET A #12
            (1470, 12),      # Line: 1393
            (1471, 109),     # Line: 1394     SET ACC #200
            (1472, 200),     # Line: 1394
            (1473, 157),     # Line: 1395     JUMP_IF_ACC_GT A &jiagt_1
            (1474, 1476),    # Line: 1395
            (1475, 186),     # Line: 1396     HALT
            (1476, 111),     # Line: 1399     SET B #123
            (1477, 123),     # Line: 1399
            (1478, 109),     # Line: 1400     SET ACC #9999
            (1479, 9999),    # Line: 1400
            (1480, 158),     # Line: 1401     JUMP_IF_ACC_GT B &jiagt_2
            (1481, 1483),    # Line: 1401
            (1482, 186),     # Line: 1402     HALT
            (1483, 112),     # Line: 1405     SET C #100
            (1484, 100),     # Line: 1405
            (1485, 109),     # Line: 1406     SET ACC #10000
            (1486, 10000),   # Line: 1406
            (1487, 159),     # Line: 1407     JUMP_IF_ACC_GT C &jiagt_3
            (1488, 1490),    # Line: 1407
            (1489, 186),     # Line: 1408     HALT
            (1490, 113),     # Line: 1411     SET SP #6000
            (1491, 6000),    # Line: 1411
            (1492, 109),     # Line: 1412     SET ACC #7000
            (1493, 7000),    # Line: 1412
            (1494, 160),     # Line: 1413     JUMP_IF_ACC_GT SP &jiagt_4
            (1495, 1497),    # Line: 1413
            (1496, 186),     # Line: 1414     HALT
            (1497, 109),     # Line: 1417     SET ACC #1111
            (1498, 1111),    # Line: 1417
            (1499, 161),     # Line: 1418     JUMP_IF_ACC_GT #1110 &jiagt_5
            (1500, 1110),    # Line: 1418
            (1501, 1503),    # Line: 1418
            (1502, 186),     # Line: 1419     HALT
            (1503, 110),     # Line: 1423     SET A #2
            (1504, 2),       # Line: 1423
            (1505, 109),     # Line: 1424     SET ACC #2
            (1506, 2),       # Line: 1424
            (1507, 157),     # Line: 1425     JUMP_IF_ACC_GT A &jiagt_halt_0
            (1508, 1534),    # Line: 1425
            (1509, 111),     # Line: 1427     SET B #1112
            (1510, 1112),    # Line: 1427
            (1511, 109),     # Line: 1428     SET ACC #12
            (1512, 12),      # Line: 1428
            (1513, 158),     # Line: 1429     JUMP_IF_ACC_GT B &jiagt_halt_1
            (1514, 1535),    # Line: 1429
            (1515, 112),     # Line: 1431     SET C #9987
            (1516, 9987),    # Line: 1431
            (1517, 109),     # Line: 1432     SET ACC #345
            (1518, 345),     # Line: 1432
            (1519, 159),     # Line: 1433     JUMP_IF_ACC_GT C &jiagt_halt_2
            (1520, 1536),    # Line: 1433
            (1521, 113),     # Line: 1435     SET SP #748
            (1522, 748),     # Line: 1435
            (1523, 109),     # Line: 1436     SET ACC #333
            (1524, 333),     # Line: 1436
            (1525, 160),     # Line: 1437     JUMP_IF_ACC_GT SP &jiagt_halt_3
            (1526, 1537),    # Line: 1437
            (1527, 109),     # Line: 1439     SET ACC #10
            (1528, 10),      # Line: 1439
            (1529, 161),     # Line: 1440     JUMP_IF_ACC_GT #15 &jiagt_halt_4
            (1530, 15),      # Line: 1440
            (1531, 1538),    # Line: 1440
            (1532, 125),     # Line: 1441     JUMP &jiez_0
            (1533, 1539),    # Line: 1441
            (1534, 186),     # Line: 1444     HALT
            (1535, 186),     # Line: 1446     HALT
            (1536, 186),     # Line: 1448     HALT
            (1537, 186),     # Line: 1450     HALT
            (1538, 186),     # Line: 1452     HALT
            (1539, 114),     # Line: 1459     SET_ZERO ACC
            (1540, 162),     # Line: 1460     JUMP_IF_EQ_ZERO ACC &jiez_1
            (1541, 1543),    # Line: 1460
            (1542, 186),     # Line: 1461     HALT
            (1543, 115),     # Line: 1464     SET_ZERO A
            (1544, 163),     # Line: 1465     JUMP_IF_EQ_ZERO A &jiez_2
            (1545, 1547),    # Line: 1465
            (1546, 186),     # Line: 1466     HALT
            (1547, 116),     # Line: 1469     SET_ZERO B
            (1548, 164),     # Line: 1470     JUMP_IF_EQ_ZERO B &jiez_3
            (1549, 1551),    # Line: 1470
            (1550, 186),     # Line: 1471     HALT
            (1551, 117),     # Line: 1474     SET_ZERO C
            (1552, 165),     # Line: 1475     JUMP_IF_EQ_ZERO C &jiez_4
            (1553, 1555),    # Line: 1475
            (1554, 186),     # Line: 1476     HALT
            (1555, 118),     # Line: 1479     SET_ZERO SP
            (1556, 166),     # Line: 1480     JUMP_IF_EQ_ZERO SP &jiez_5
            (1557, 1559),    # Line: 1480
            (1558, 186),     # Line: 1481     HALT
            (1559, 109),     # Line: 1484     SET ACC #1
            (1560, 1),       # Line: 1484
            (1561, 162),     # Line: 1485     JUMP_IF_EQ_ZERO ACC &jiez_halt_0
            (1562, 1581),    # Line: 1485
            (1563, 110),     # Line: 1487     SET A #58767
            (1564, 58767),   # Line: 1487
            (1565, 163),     # Line: 1488     JUMP_IF_EQ_ZERO A &jiez_halt_1
            (1566, 1582),    # Line: 1488
            (1567, 111),     # Line: 1490     SET B #443
            (1568, 443),     # Line: 1490
            (1569, 164),     # Line: 1491     JUMP_IF_EQ_ZERO B &jiez_halt_2
            (1570, 1583),    # Line: 1491
            (1571, 112),     # Line: 1493     SET C #7687
            (1572, 7687),    # Line: 1493
            (1573, 165),     # Line: 1494     JUMP_IF_EQ_ZERO C &jiez_halt_3
            (1574, 1584),    # Line: 1494
            (1575, 113),     # Line: 1496     SET SP #1536
            (1576, 1536),    # Line: 1496
            (1577, 166),     # Line: 1497     JUMP_IF_EQ_ZERO SP &jiez_halt_4
            (1578, 1585),    # Line: 1497
            (1579, 125),     # Line: 1499     JUMP &jinez_0
            (1580, 1586),    # Line: 1499
            (1581, 186),     # Line: 1502     HALT
            (1582, 186),     # Line: 1504     HALT
            (1583, 186),     # Line: 1506     HALT
            (1584, 186),     # Line: 1508     HALT
            (1585, 186),     # Line: 1510     HALT
            (1586, 109),     # Line: 1517     SET ACC #1
            (1587, 1),       # Line: 1517
            (1588, 167),     # Line: 1518     JUMP_IF_NEQ_ZERO ACC &jinez_1
            (1589, 1591),    # Line: 1518
            (1590, 186),     # Line: 1519     HALT
            (1591, 110),     # Line: 1522     SET A #1
            (1592, 1),       # Line: 1522
            (1593, 168),     # Line: 1523     JUMP_IF_NEQ_ZERO A &jinez_2
            (1594, 1596),    # Line: 1523
            (1595, 186),     # Line: 1524     HALT
            (1596, 111),     # Line: 1527     SET B #1
            (1597, 1),       # Line: 1527
            (1598, 169),     # Line: 1528     JUMP_IF_NEQ_ZERO B &jinez_3
            (1599, 1601),    # Line: 1528
            (1600, 186),     # Line: 1529     HALT
            (1601, 112),     # Line: 1532     SET C #1
            (1602, 1),       # Line: 1532
            (1603, 170),     # Line: 1533     JUMP_IF_NEQ_ZERO C &jinez_4
            (1604, 1606),    # Line: 1533
            (1605, 186),     # Line: 1534     HALT
            (1606, 113),     # Line: 1537     SET SP #1
            (1607, 1),       # Line: 1537
            (1608, 171),     # Line: 1538     JUMP_IF_NEQ_ZERO SP &jinez_5
            (1609, 1611),    # Line: 1538
            (1610, 186),     # Line: 1539     HALT
            (1611, 114),     # Line: 1542     SET_ZERO ACC
            (1612, 167),     # Line: 1543     JUMP_IF_NEQ_ZERO ACC &jinez_halt_0
            (1613, 1628),    # Line: 1543
            (1614, 115),     # Line: 1545     SET_ZERO A
            (1615, 168),     # Line: 1546     JUMP_IF_NEQ_ZERO A &jinez_halt_1
            (1616, 1629),    # Line: 1546
            (1617, 116),     # Line: 1548     SET_ZERO B
            (1618, 169),     # Line: 1549     JUMP_IF_NEQ_ZERO B &jinez_halt_2
            (1619, 1630),    # Line: 1549
            (1620, 117),     # Line: 1551     SET_ZERO C
            (1621, 170),     # Line: 1552     JUMP_IF_NEQ_ZERO C &jinez_halt_3
            (1622, 1631),    # Line: 1552
            (1623, 118),     # Line: 1554     SET_ZERO SP
            (1624, 171),     # Line: 1555     JUMP_IF_NEQ_ZERO SP &jinez_halt_4
            (1625, 1632),    # Line: 1555
            (1626, 125),     # Line: 1557     JUMP &jinf_0
            (1627, 1633),    # Line: 1557
            (1628, 186),     # Line: 1560     HALT
            (1629, 186),     # Line: 1562     HALT
            (1630, 186),     # Line: 1564     HALT
            (1631, 186),     # Line: 1566     HALT
            (1632, 186),     # Line: 1568     HALT
            (1633, 109),     # Line: 1575     SET ACC #10
            (1634, 10),      # Line: 1575
            (1635, 8),       # Line: 1576     SUB #20
            (1636, 20),      # Line: 1576
            (1637, 172),     # Line: 1577     JUMP_IF_NEGATIVE_FLAG &jinf_1
            (1638, 1640),    # Line: 1577
            (1639, 186),     # Line: 1578     HALT
            (1640, 109),     # Line: 1581     SET ACC #222
            (1641, 222),     # Line: 1581
            (1642, 8),       # Line: 1582     SUB #5
            (1643, 5),       # Line: 1582
            (1644, 172),     # Line: 1583     JUMP_IF_NEGATIVE_FLAG &jinf_halt_0
            (1645, 1648),    # Line: 1583
            (1646, 125),     # Line: 1584     JUMP &jinnf_0
            (1647, 1649),    # Line: 1584
            (1648, 186),     # Line: 1587     HALT
            (1649, 109),     # Line: 1594     SET ACC #10
            (1650, 10),      # Line: 1594
            (1651, 8),       # Line: 1595     SUB #5
            (1652, 5),       # Line: 1595
            (1653, 173),     # Line: 1596     JUMP_IF_NOT_NEGATIVE_FLAG &jinnf_1
            (1654, 1656),    # Line: 1596
            (1655, 186),     # Line: 1597     HALT
            (1656, 109),     # Line: 1600     SET ACC #5
            (1657, 5),       # Line: 1600
            (1658, 8),       # Line: 1601     SUB #10
            (1659, 10),      # Line: 1601
            (1660, 173),     # Line: 1602     JUMP_IF_NOT_NEGATIVE_FLAG &jinnf_halt_0
            (1661, 1664),    # Line: 1602
            (1662, 125),     # Line: 1603     JUMP &jicbf_0
            (1663, 1665),    # Line: 1603
            (1664, 186),     # Line: 1606     HALT
            (1665, 109),     # Line: 1613     SET ACC #0xFFFF
            (1666, 65535),   # Line: 1613
            (1667, 3),       # Line: 1614     ADD #1
            (1668, 1),       # Line: 1614
            (1669, 174),     # Line: 1615     JUMP_IF_CARRYBORROW_FLAG &jicbf_1
            (1670, 1672),    # Line: 1615
            (1671, 186),     # Line: 1616     HALT
            (1672, 109),     # Line: 1619     SET ACC #5
            (1673, 5),       # Line: 1619
            (1674, 3),       # Line: 1620     ADD #10
            (1675, 10),      # Line: 1620
            (1676, 174),     # Line: 1621     JUMP_IF_CARRYBORROW_FLAG &jicbf_halt_0
            (1677, 1680),    # Line: 1621
            (1678, 125),     # Line: 1622     JUMP &jincbf_0
            (1679, 1681),    # Line: 1622
            (1680, 186),     # Line: 1625     HALT
            (1681, 109),     # Line: 1632     SET ACC #18
            (1682, 18),      # Line: 1632
            (1683, 3),       # Line: 1633     ADD #5
            (1684, 5),       # Line: 1633
            (1685, 175),     # Line: 1634     JUMP_IF_NOT_CARRYBORROW_FLAG &jincbf_1
            (1686, 1688),    # Line: 1634
            (1687, 186),     # Line: 1635     HALT
            (1688, 109),     # Line: 1638     SET ACC #0xFFFF
            (1689, 65535),   # Line: 1638
            (1690, 3),       # Line: 1639     ADD #55
            (1691, 55),      # Line: 1639
            (1692, 175),     # Line: 1640     JUMP_IF_NOT_CARRYBORROW_FLAG &jincbf_halt_0
            (1693, 1696),    # Line: 1640
            (1694, 125),     # Line: 1641     JUMP &jief_0
            (1695, 1697),    # Line: 1641
            (1696, 186),     # Line: 1644     HALT
            (1697, 109),     # Line: 1652     SET ACC #1
            (1698, 1),       # Line: 1652
            (1699, 8),       # Line: 1653     SUB #2
            (1700, 2),       # Line: 1653
            (1701, 176),     # Line: 1654     JUMP_IF_EQUAL_FLAG &jief_1
            (1702, 1704),    # Line: 1654
            (1703, 186),     # Line: 1655     HALT
            (1704, 109),     # Line: 1658     SET ACC #5
            (1705, 5),       # Line: 1658
            (1706, 3),       # Line: 1659     ADD #10
            (1707, 10),      # Line: 1659
            (1708, 176),     # Line: 1660     JUMP_IF_EQUAL_FLAG &jief_halt_0
            (1709, 1712),    # Line: 1660
            (1710, 125),     # Line: 1661     JUMP &jinef_0
            (1711, 1713),    # Line: 1661
            (1712, 186),     # Line: 1664     HALT
            (1713, 109),     # Line: 1671     SET ACC #34
            (1714, 34),      # Line: 1671
            (1715, 3),       # Line: 1672     ADD #5
            (1716, 5),       # Line: 1672
            (1717, 177),     # Line: 1673     JUMP_IF_NOT_EQUAL_FLAG &jinef_1
            (1718, 1720),    # Line: 1673
            (1719, 186),     # Line: 1674     HALT
            (1720, 109),     # Line: 1678     SET ACC #1
            (1721, 1),       # Line: 1678
            (1722, 8),       # Line: 1679     SUB #2
            (1723, 2),       # Line: 1679
            (1724, 177),     # Line: 1680     JUMP_IF_NOT_EQUAL_FLAG &jinef_halt_0
            (1725, 1728),    # Line: 1680
            (1726, 125),     # Line: 1681     JUMP &jizf_0
            (1727, 1729),    # Line: 1681
            (1728, 186),     # Line: 1684     HALT
            (1729, 109),     # Line: 1691     SET ACC #0
            (1730, 0),       # Line: 1691
            (1731, 3),       # Line: 1692     ADD #0
            (1732, 0),       # Line: 1692
            (1733, 178),     # Line: 1693     JUMP_IF_ZERO_FLAG &jizf_1
            (1734, 1736),    # Line: 1693
            (1735, 186),     # Line: 1694     HALT
            (1736, 109),     # Line: 1697     SET ACC #1
            (1737, 1),       # Line: 1697
            (1738, 3),       # Line: 1698     ADD #1
            (1739, 1),       # Line: 1698
            (1740, 178),     # Line: 1699     JUMP_IF_ZERO_FLAG &jizf_halt_0
            (1741, 1744),    # Line: 1699
            (1742, 125),     # Line: 1700     JUMP &jinzf_0
            (1743, 1745),    # Line: 1700
            (1744, 186),     # Line: 1703     HALT
            (1745, 109),     # Line: 1710     SET ACC #1
            (1746, 1),       # Line: 1710
            (1747, 3),       # Line: 1711     ADD #1
            (1748, 1),       # Line: 1711
            (1749, 179),     # Line: 1712     JUMP_IF_NOT_ZERO_FLAG &jinzf_1
            (1750, 1752),    # Line: 1712
            (1751, 186),     # Line: 1713     HALT
            (1752, 109),     # Line: 1716     SET ACC #0
            (1753, 0),       # Line: 1716
            (1754, 3),       # Line: 1717     ADD #0
            (1755, 0),       # Line: 1717
            (1756, 179),     # Line: 1718     JUMP_IF_NOT_ZERO_FLAG &jinzf_halt_0
            (1757, 1760),    # Line: 1718
            (1758, 125),     # Line: 1719     JUMP &call_0
            (1759, 1782),    # Line: 1719
            (1760, 186),     # Line: 1722     HALT
            (1761, 119),     # Line: 1730     NOOP
            (1762, 119),     # Line: 1731     NOOP
            (1763, 119),     # Line: 1732     NOOP
            (1764, 119),     # Line: 1733     NOOP
            (1765, 119),     # Line: 1734     NOOP
            (1766, 119),     # Line: 1735     NOOP
            (1767, 119),     # Line: 1736     NOOP
            (1768, 119),     # Line: 1737     NOOP
            (1769, 119),     # Line: 1739     NOOP
            (1770, 119),     # Line: 1740     NOOP
            (1771, 119),     # Line: 1741     NOOP
            (1772, 119),     # Line: 1742     NOOP
            (1773, 119),     # Line: 1743     NOOP
            (1774, 119),     # Line: 1744     NOOP
            (1775, 119),     # Line: 1745     NOOP
            (1776, 14),      # Line: 1749     INCR ACC
            (1777, 185),     # Line: 1750     RETURN
            (1778, 186),     # Line: 1751     HALT
            (1779, 15),      # Line: 1754     INCR A
            (1780, 185),     # Line: 1755     RETURN
            (1781, 186),     # Line: 1756     HALT
            (1782, 113),     # Line: 1759     SET SP &safe_sp
            (1783, 1769),    # Line: 1759
            (1784, 110),     # Line: 1760     SET A #0
            (1785, 0),       # Line: 1760
            (1786, 109),     # Line: 1761     SET ACC &increment_a
            (1787, 1779),    # Line: 1761
            (1788, 180),     # Line: 1762     CALL ACC
            (1789, 109),     # Line: 1763     SET ACC #1
            (1790, 1),       # Line: 1763
            (1791, 142),     # Line: 1764     JUMP_IF_ACC_EQ A &call_1
            (1792, 1794),    # Line: 1764
            (1793, 186),     # Line: 1765     HALT
            (1794, 109),     # Line: 1768     SET ACC #0
            (1795, 0),       # Line: 1768
            (1796, 110),     # Line: 1769     SET A &increment_acc
            (1797, 1776),    # Line: 1769
            (1798, 181),     # Line: 1770     CALL A
            (1799, 146),     # Line: 1771     JUMP_IF_ACC_EQ #1 &call_2
            (1800, 1),       # Line: 1771
            (1801, 1803),    # Line: 1771
            (1802, 186),     # Line: 1772     HALT
            (1803, 109),     # Line: 1775     SET ACC #0
            (1804, 0),       # Line: 1775
            (1805, 111),     # Line: 1776     SET B &increment_acc
            (1806, 1776),    # Line: 1776
            (1807, 182),     # Line: 1777     CALL B
            (1808, 146),     # Line: 1778     JUMP_IF_ACC_EQ #1 &call_3
            (1809, 1),       # Line: 1778
            (1810, 1812),    # Line: 1778
            (1811, 186),     # Line: 1779     HALT
            (1812, 109),     # Line: 1782     SET ACC #0
            (1813, 0),       # Line: 1782
            (1814, 112),     # Line: 1783     SET C &increment_acc
            (1815, 1776),    # Line: 1783
            (1816, 183),     # Line: 1784     CALL C
            (1817, 146),     # Line: 1785     JUMP_IF_ACC_EQ #1 &call_4
            (1818, 1),       # Line: 1785
            (1819, 1821),    # Line: 1785
            (1820, 186),     # Line: 1786     HALT
            (1821, 109),     # Line: 1789     SET ACC #0
            (1822, 0),       # Line: 1789
            (1823, 184),     # Line: 1790     CALL &increment_acc
            (1824, 1776),    # Line: 1790
            (1825, 146),     # Line: 1791     JUMP_IF_ACC_EQ #1 &not_0
            (1826, 1),       # Line: 1791
            (1827, 1829),    # Line: 1791
            (1828, 186),     # Line: 1792     HALT
            (1829, 109),     # Line: 1799     SET ACC        #0b1001_0100_0011_1111
            (1830, 37951),   # Line: 1799
            (1831, 187),     # Line: 1800     NOT ACC
            (1832, 146),     # Line: 1801     JUMP_IF_ACC_EQ #0b0110_1011_1100_0000 &not_1
            (1833, 27584),   # Line: 1801
            (1834, 1836),    # Line: 1801
            (1835, 186),     # Line: 1802     HALT
            (1836, 110),     # Line: 1805     SET A   #0b1010_1010_0101_0101
            (1837, 43605),   # Line: 1805
            (1838, 109),     # Line: 1806     SET ACC #0b0101_0101_1010_1010
            (1839, 21930),   # Line: 1806
            (1840, 188),     # Line: 1807     NOT A
            (1841, 142),     # Line: 1808     JUMP_IF_ACC_EQ A &not_2
            (1842, 1844),    # Line: 1808
            (1843, 186),     # Line: 1809     HALT
            (1844, 111),     # Line: 1812     SET B   #0b1111_1111_1111_1111
            (1845, 65535),   # Line: 1812
            (1846, 109),     # Line: 1813     SET ACC #0b0000_0000_0000_0000
            (1847, 0),       # Line: 1813
            (1848, 189),     # Line: 1814     NOT B
            (1849, 143),     # Line: 1815     JUMP_IF_ACC_EQ B &not_3
            (1850, 1852),    # Line: 1815
            (1851, 186),     # Line: 1816     HALT
            (1852, 112),     # Line: 1819     SET C   #0b0000_0000_0000_0000
            (1853, 0),       # Line: 1819
            (1854, 109),     # Line: 1820     SET ACC #0b1111_1111_1111_1111
            (1855, 65535),   # Line: 1820
            (1856, 190),     # Line: 1821     NOT C
            (1857, 144),     # Line: 1822     JUMP_IF_ACC_EQ C &and_0
            (1858, 1860),    # Line: 1822
            (1859, 186),     # Line: 1823     HALT
            (1860, 109),     # Line: 1830     SET ACC        #0b1111
            (1861, 15),      # Line: 1830
            (1862, 110),     # Line: 1831     SET A          #0b0101
            (1863, 5),       # Line: 1831
            (1864, 191),     # Line: 1832     AND A
            (1865, 146),     # Line: 1833     JUMP_IF_ACC_EQ #0b0101 &and_1
            (1866, 5),       # Line: 1833
            (1867, 1869),    # Line: 1833
            (1868, 186),     # Line: 1834     HALT
            (1869, 109),     # Line: 1837     SET ACC        #0b1111_0000_1111_0000
            (1870, 61680),   # Line: 1837
            (1871, 111),     # Line: 1838     SET B          #0b1111_1111_1111_1111
            (1872, 65535),   # Line: 1838
            (1873, 192),     # Line: 1839     AND B
            (1874, 146),     # Line: 1840     JUMP_IF_ACC_EQ #0b1111_0000_1111_0000 &and_2
            (1875, 61680),   # Line: 1840
            (1876, 1878),    # Line: 1840
            (1877, 186),     # Line: 1841     HALT
            (1878, 109),     # Line: 1844     SET ACC        #0b1100_1111
            (1879, 207),     # Line: 1844
            (1880, 112),     # Line: 1845     SET C          #0b0000_0000
            (1881, 0),       # Line: 1845
            (1882, 193),     # Line: 1846     AND C
            (1883, 146),     # Line: 1847     JUMP_IF_ACC_EQ #0b0000_0000 &and_3
            (1884, 0),       # Line: 1847
            (1885, 1887),    # Line: 1847
            (1886, 186),     # Line: 1848     HALT
            (1887, 109),     # Line: 1851     SET ACC        #0b0011_1100_1111_0000
            (1888, 15600),   # Line: 1851
            (1889, 194),     # Line: 1852     AND            #0b1111_1111_0000_1111
            (1890, 65295),   # Line: 1852
            (1891, 146),     # Line: 1853     JUMP_IF_ACC_EQ #0b0011_1100_0000_0000 &and_4
            (1892, 15360),   # Line: 1853
            (1893, 1896),    # Line: 1853
            (1894, 186),     # Line: 1854     HALT
            (1895, 1),       # Line: 1856 $v_and_0           #0b1
            (1896, 109),     # Line: 1858     SET ACC        #0b1
            (1897, 1),       # Line: 1858
            (1898, 195),     # Line: 1859     AND [$v_and_0]
            (1899, 1895),    # Line: 1859
            (1900, 146),     # Line: 1860     JUMP_IF_ACC_EQ #0b1 &nand_0
            (1901, 1),       # Line: 1860
            (1902, 1904),    # Line: 1860
            (1903, 186),     # Line: 1861     HALT
            (1904, 109),     # Line: 1868     SET ACC        #0b0000_0000_0000_1111
            (1905, 15),      # Line: 1868
            (1906, 110),     # Line: 1869     SET A          #0b1111_1111_1111_0101
            (1907, 65525),   # Line: 1869
            (1908, 196),     # Line: 1870     NAND A
            (1909, 146),     # Line: 1871     JUMP_IF_ACC_EQ #0b1111_1111_1111_1010 &nand_1
            (1910, 65530),   # Line: 1871
            (1911, 1913),    # Line: 1871
            (1912, 186),     # Line: 1872     HALT
            (1913, 109),     # Line: 1875     SET ACC        #0b1111_0000_1111_0000
            (1914, 61680),   # Line: 1875
            (1915, 111),     # Line: 1876     SET B          #0b1111_1111_1111_1111
            (1916, 65535),   # Line: 1876
            (1917, 197),     # Line: 1877     NAND B
            (1918, 146),     # Line: 1878     JUMP_IF_ACC_EQ #0b0000_1111_0000_1111 &nand_2
            (1919, 3855),    # Line: 1878
            (1920, 1922),    # Line: 1878
            (1921, 186),     # Line: 1879     HALT
            (1922, 109),     # Line: 1882     SET ACC        #0b1111_1111_1100_1111
            (1923, 65487),   # Line: 1882
            (1924, 112),     # Line: 1883     SET C          #0b1111_1111_0000_0000
            (1925, 65280),   # Line: 1883
            (1926, 198),     # Line: 1884     NAND C
            (1927, 146),     # Line: 1885     JUMP_IF_ACC_EQ #0b0000_0000_1111_1111 &nand_3
            (1928, 255),     # Line: 1885
            (1929, 1931),    # Line: 1885
            (1930, 186),     # Line: 1886     HALT
            (1931, 109),     # Line: 1889     SET ACC        #0b0011_1100_1111_0000
            (1932, 15600),   # Line: 1889
            (1933, 199),     # Line: 1890     NAND           #0b1111_1111_0000_1111
            (1934, 65295),   # Line: 1890
            (1935, 146),     # Line: 1891     JUMP_IF_ACC_EQ #0b1100_0011_1111_1111 &nand_4
            (1936, 50175),   # Line: 1891
            (1937, 1940),    # Line: 1891
            (1938, 186),     # Line: 1892     HALT
            (1939, 1),       # Line: 1894 $v_nand_0          #0b0000_0000_0000_0001
            (1940, 109),     # Line: 1896     SET ACC        #0b0000_0000_0000_0001
            (1941, 1),       # Line: 1896
            (1942, 200),     # Line: 1897     NAND [$v_nand_0]
            (1943, 1939),    # Line: 1897
            (1944, 146),     # Line: 1898     JUMP_IF_ACC_EQ #0b1111_1111_1111_1110 &or_0
            (1945, 65534),   # Line: 1898
            (1946, 1948),    # Line: 1898
            (1947, 186),     # Line: 1899     HALT
            (1948, 109),     # Line: 1906     SET ACC        #0b1111
            (1949, 15),      # Line: 1906
            (1950, 110),     # Line: 1907     SET A          #0b0101
            (1951, 5),       # Line: 1907
            (1952, 201),     # Line: 1908     OR A
            (1953, 146),     # Line: 1909     JUMP_IF_ACC_EQ #0b1111 &or_1
            (1954, 15),      # Line: 1909
            (1955, 1957),    # Line: 1909
            (1956, 186),     # Line: 1910     HALT
            (1957, 109),     # Line: 1913     SET ACC        #0b1111_0000_1111_0000
            (1958, 61680),   # Line: 1913
            (1959, 111),     # Line: 1914     SET B          #0b1111_1111_1111_1111
            (1960, 65535),   # Line: 1914
            (1961, 202),     # Line: 1915     OR B
            (1962, 146),     # Line: 1916     JUMP_IF_ACC_EQ #0b1111_1111_1111_1111 &or_2
            (1963, 65535),   # Line: 1916
            (1964, 1966),    # Line: 1916
            (1965, 186),     # Line: 1917     HALT
            (1966, 109),     # Line: 1920     SET ACC        #0b1100_1111
            (1967, 207),     # Line: 1920
            (1968, 112),     # Line: 1921     SET C          #0b0000_0000
            (1969, 0),       # Line: 1921
            (1970, 203),     # Line: 1922     OR C
            (1971, 146),     # Line: 1923     JUMP_IF_ACC_EQ #0b1100_1111 &or_3
            (1972, 207),     # Line: 1923
            (1973, 1975),    # Line: 1923
            (1974, 186),     # Line: 1924     HALT
            (1975, 109),     # Line: 1927     SET ACC        #0b0011_1100_1111_0000
            (1976, 15600),   # Line: 1927
            (1977, 204),     # Line: 1928     OR             #0b1111_1111_0000_1111
            (1978, 65295),   # Line: 1928
            (1979, 146),     # Line: 1929     JUMP_IF_ACC_EQ #0b1111_1111_1111_1111 &or_4
            (1980, 65535),   # Line: 1929
            (1981, 1984),    # Line: 1929
            (1982, 186),     # Line: 1930     HALT
            (1983, 1),       # Line: 1932 $v_or_0            #0b1
            (1984, 109),     # Line: 1934     SET ACC        #0b1
            (1985, 1),       # Line: 1934
            (1986, 205),     # Line: 1935     OR [$v_or_0]
            (1987, 1983),    # Line: 1935
            (1988, 146),     # Line: 1936     JUMP_IF_ACC_EQ #0b1 &nor_0
            (1989, 1),       # Line: 1936
            (1990, 1992),    # Line: 1936
            (1991, 186),     # Line: 1937     HALT
            (1992, 109),     # Line: 1944     SET ACC        #0b1111_0101_0000_1111
            (1993, 62735),   # Line: 1944
            (1994, 110),     # Line: 1945     SET A          #0b0010_0010_1111_0101
            (1995, 8949),    # Line: 1945
            (1996, 206),     # Line: 1946     NOR A
            (1997, 146),     # Line: 1947     JUMP_IF_ACC_EQ #0b0000_1000_0000_0000 &nor_1
            (1998, 2048),    # Line: 1947
            (1999, 2001),    # Line: 1947
            (2000, 186),     # Line: 1948     HALT
            (2001, 109),     # Line: 1951     SET ACC        #0b1111_0000_1111_0000
            (2002, 61680),   # Line: 1951
            (2003, 111),     # Line: 1952     SET B          #0b1111_1111_1111_1111
            (2004, 65535),   # Line: 1952
            (2005, 207),     # Line: 1953     NOR B
            (2006, 146),     # Line: 1954     JUMP_IF_ACC_EQ #0b0000_0000_0000_0000 &nor_2
            (2007, 0),       # Line: 1954
            (2008, 2010),    # Line: 1954
            (2009, 186),     # Line: 1955     HALT
            (2010, 109),     # Line: 1958     SET ACC        #0b0000_0000_1100_1111
            (2011, 207),     # Line: 1958
            (2012, 112),     # Line: 1959     SET C          #0b0000_1111_0000_0000
            (2013, 3840),    # Line: 1959
            (2014, 208),     # Line: 1960     NOR C
            (2015, 146),     # Line: 1961     JUMP_IF_ACC_EQ #0b1111_0000_0011_0000 &nor_3
            (2016, 61488),   # Line: 1961
            (2017, 2019),    # Line: 1961
            (2018, 186),     # Line: 1962     HALT
            (2019, 109),     # Line: 1965     SET ACC        #0b0011_1100_1111_0000
            (2020, 15600),   # Line: 1965
            (2021, 209),     # Line: 1966     NOR            #0b0111_1110_0000_1110
            (2022, 32270),   # Line: 1966
            (2023, 146),     # Line: 1967     JUMP_IF_ACC_EQ #0b1000_0001_0000_0001 &nor_4
            (2024, 33025),   # Line: 1967
            (2025, 2028),    # Line: 1967
            (2026, 186),     # Line: 1968     HALT
            (2027, 16385),   # Line: 1970 $v_nor_0           #0b0100_0000_0000_0001
            (2028, 109),     # Line: 1972     SET ACC        #0b0000_0010_0000_0001
            (2029, 513),     # Line: 1972
            (2030, 210),     # Line: 1973     NOR [$v_nor_0]
            (2031, 2027),    # Line: 1973
            (2032, 146),     # Line: 1974     JUMP_IF_ACC_EQ #0b1011_1101_1111_1110 &xor_0
            (2033, 48638),   # Line: 1974
            (2034, 2036),    # Line: 1974
            (2035, 186),     # Line: 1975     HALT
            (2036, 109),     # Line: 1982     SET ACC        #0b1111
            (2037, 15),      # Line: 1982
            (2038, 110),     # Line: 1983     SET A          #0b0101
            (2039, 5),       # Line: 1983
            (2040, 211),     # Line: 1984     XOR A
            (2041, 146),     # Line: 1985     JUMP_IF_ACC_EQ #0b1010 &xor_1
            (2042, 10),      # Line: 1985
            (2043, 2045),    # Line: 1985
            (2044, 186),     # Line: 1986     HALT
            (2045, 109),     # Line: 1989     SET ACC        #0b0011
            (2046, 3),       # Line: 1989
            (2047, 111),     # Line: 1990     SET B          #0b0101
            (2048, 5),       # Line: 1990
            (2049, 212),     # Line: 1991     XOR B
            (2050, 146),     # Line: 1992     JUMP_IF_ACC_EQ #0b0110 &xor_2
            (2051, 6),       # Line: 1992
            (2052, 2054),    # Line: 1992
            (2053, 186),     # Line: 1993     HALT
            (2054, 109),     # Line: 1996     SET ACC        #0b1100_1111
            (2055, 207),     # Line: 1996
            (2056, 112),     # Line: 1997     SET C          #0b0000_0000
            (2057, 0),       # Line: 1997
            (2058, 213),     # Line: 1998     XOR C
            (2059, 146),     # Line: 1999     JUMP_IF_ACC_EQ #0b1100_1111 &xor_3
            (2060, 207),     # Line: 1999
            (2061, 2063),    # Line: 1999
            (2062, 186),     # Line: 2000     HALT
            (2063, 109),     # Line: 2003     SET ACC        #0b0011_1100_1011_0001
            (2064, 15537),   # Line: 2003
            (2065, 214),     # Line: 2004     XOR            #0b1111_1111_0000_1111
            (2066, 65295),   # Line: 2004
            (2067, 146),     # Line: 2005     JUMP_IF_ACC_EQ #0b1100_0011_1011_1110 &xor_4
            (2068, 50110),   # Line: 2005
            (2069, 2072),    # Line: 2005
            (2070, 186),     # Line: 2006     HALT
            (2071, 1),       # Line: 2008 $v_xor_0           #0b1
            (2072, 109),     # Line: 2010     SET ACC        #0b1
            (2073, 1),       # Line: 2010
            (2074, 215),     # Line: 2011     XOR [$v_xor_0]
            (2075, 2071),    # Line: 2011
            (2076, 146),     # Line: 2012     JUMP_IF_ACC_EQ #0b0 &nxor_0
            (2077, 0),       # Line: 2012
            (2078, 2080),    # Line: 2012
            (2079, 186),     # Line: 2013     HALT
            (2080, 109),     # Line: 2020     SET ACC        #0b1111_1111_1111_1111
            (2081, 65535),   # Line: 2020
            (2082, 110),     # Line: 2021     SET A          #0b0000_0000_0000_0101
            (2083, 5),       # Line: 2021
            (2084, 216),     # Line: 2022     NXOR A
            (2085, 146),     # Line: 2023     JUMP_IF_ACC_EQ #0b0000_0000_0000_0101 &nxor_1
            (2086, 5),       # Line: 2023
            (2087, 2089),    # Line: 2023
            (2088, 186),     # Line: 2024     HALT
            (2089, 109),     # Line: 2027     SET ACC        #0b1111_1111_1111_0011
            (2090, 65523),   # Line: 2027
            (2091, 111),     # Line: 2028     SET B          #0b1111_1111_1111_0101
            (2092, 65525),   # Line: 2028
            (2093, 217),     # Line: 2029     NXOR B
            (2094, 146),     # Line: 2030     JUMP_IF_ACC_EQ #0b1111_1111_1111_1001 &nxor_2
            (2095, 65529),   # Line: 2030
            (2096, 2098),    # Line: 2030
            (2097, 186),     # Line: 2031     HALT
            (2098, 109),     # Line: 2034     SET ACC        #0b0111_1100_1100_1111
            (2099, 31951),   # Line: 2034
            (2100, 112),     # Line: 2035     SET C          #0b1011_0000_0000_0000
            (2101, 45056),   # Line: 2035
            (2102, 218),     # Line: 2036     NXOR C
            (2103, 146),     # Line: 2037     JUMP_IF_ACC_EQ #0b0011_0011_0011_0000 &nxor_3
            (2104, 13104),   # Line: 2037
            (2105, 2107),    # Line: 2037
            (2106, 186),     # Line: 2038     HALT
            (2107, 109),     # Line: 2041     SET ACC        #0b0011_1100_1011_0001
            (2108, 15537),   # Line: 2041
            (2109, 219),     # Line: 2042     NXOR           #0b1111_1111_0000_1111
            (2110, 65295),   # Line: 2042
            (2111, 146),     # Line: 2043     JUMP_IF_ACC_EQ #0b0011_1100_0100_0001 &nxor_4
            (2112, 15425),   # Line: 2043
            (2113, 2116),    # Line: 2043
            (2114, 186),     # Line: 2044     HALT
            (2115, 61423),   # Line: 2046 $v_nxor_0          #0b1110_1111_1110_1111
            (2116, 109),     # Line: 2048     SET ACC        #0b1111_1110_1110_1111
            (2117, 65263),   # Line: 2048
            (2118, 220),     # Line: 2049     NXOR [$v_nxor_0]
            (2119, 2115),    # Line: 2049
            (2120, 146),     # Line: 2050     JUMP_IF_ACC_EQ #0b1110_1110_1111_1111 &rot_left_0
            (2121, 61183),   # Line: 2050
            (2122, 2124),    # Line: 2050
            (2123, 186),     # Line: 2051     HALT
            (2124, 109),     # Line: 2058     SET ACC        #0b0100_0001_1111_0000
            (2125, 16880),   # Line: 2058
            (2126, 221),     # Line: 2059     ROT_LEFT ACC
            (2127, 146),     # Line: 2060     JUMP_IF_ACC_EQ #0b1000_0011_1110_0000 &rot_left_1
            (2128, 33760),   # Line: 2060
            (2129, 2130),    # Line: 2060
            (2130, 110),     # Line: 2063     SET A   #0b1000_1000_1000_1000
            (2131, 34952),   # Line: 2063
            (2132, 109),     # Line: 2064     SET ACC #0b0001_0001_0001_0001
            (2133, 4369),    # Line: 2064
            (2134, 142),     # Line: 2065     JUMP_IF_ACC_EQ A &rot_left_2
            (2135, 2136),    # Line: 2065
            (2136, 111),     # Line: 2068     SET B   #0b1001_1001_1001_1001
            (2137, 39321),   # Line: 2068
            (2138, 109),     # Line: 2069     SET ACC #0b0011_0011_0011_0011
            (2139, 13107),   # Line: 2069
            (2140, 143),     # Line: 2070     JUMP_IF_ACC_EQ B &rot_left_2
            (2141, 2136),    # Line: 2070
            (2142, 112),     # Line: 2073     SET C   #0b0000_1111_0000_1111
            (2143, 3855),    # Line: 2073
            (2144, 109),     # Line: 2074     SET ACC #0b0001_1110_0001_1110
            (2145, 7710),    # Line: 2074
            (2146, 144),     # Line: 2075     JUMP_IF_ACC_EQ C &placeholder
            (2147, 2148),    # Line: 2075
            (2148, 125),     # Line: 2079     JUMP &start
            (2149, 0),       # Line: 2079
        )
    }
)
