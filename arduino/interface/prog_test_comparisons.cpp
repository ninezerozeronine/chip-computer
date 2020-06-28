#include "prog_test_comparisons.h"

extern const byte num_test_comparisons_program_bytes = 76;
extern const byte test_comparisons_program_bytes[] PROGMEM = {
    0x38, // 000 SET ACC #84 (@start)
    0x54, // 001 (84)
    0x3A, // 002 SET B #32
    0x20, // 003 (32)
    0x17, // 004 JUMP_IF_EQ_ACC B @halt
    0x4B, // 005 (75)
    0x39, // 006 SET A #84
    0x54, // 007 (84)
    0x0F, // 008 JUMP_IF_EQ_ACC A @eq_zero
    0x0B, // 009 (11)
    0xB6, // 010 HALT
    0x39, // 011 SET A #-1 (@eq_zero)
    0xFF, // 012 (255)
    0xA1, // 013 JUMP_IF_EQ_ZERO A @halt
    0x4B, // 014 (75)
    0xC2, // 015 SET_ZERO B
    0xA2, // 016 JUMP_IF_EQ_ZERO B @lt_acc
    0x13, // 017 (19)
    0xB6, // 018 HALT
    0x39, // 019 SET A #100 (@lt_acc)
    0x64, // 020 (100)
    0x31, // 021 JUMP_IF_LT_ACC A @halt
    0x4B, // 022 (75)
    0x3B, // 023 SET C #52
    0x34, // 024 (52)
    0x33, // 025 JUMP_IF_LT_ACC C @lte_acc_0
    0x1C, // 026 (28)
    0xB6, // 027 HALT
    0x3A, // 028 SET B #123 (@lte_acc_0)
    0x7B, // 029 (123)
    0x16, // 030 JUMP_IF_LTE_ACC B @halt
    0x4B, // 031 (75)
    0x3C, // 032 SET SP #84
    0x54, // 033 (84)
    0x26, // 034 JUMP_IF_LTE_ACC SP @lte_acc_1
    0x25, // 035 (37)
    0xB6, // 036 HALT
    0x3B, // 037 SET C #201 (@lte_acc_1)
    0xC9, // 038 (201)
    0x1E, // 039 JUMP_IF_LTE_ACC C @halt
    0x4B, // 040 (75)
    0x39, // 041 SET A #4
    0x04, // 042 (4)
    0x0E, // 043 JUMP_IF_LTE_ACC A @gte_acc_0
    0x2E, // 044 (46)
    0xB6, // 045 HALT
    0x38, // 046 SET ACC #150 (@gte_acc_0)
    0x96, // 047 (150)
    0x3A, // 048 SET B #15
    0x0F, // 049 (15)
    0x54, // 050 JUMP_IF_GTE_ACC B @halt
    0x4B, // 051 (75)
    0x39, // 052 SET A #150
    0x96, // 053 (150)
    0x4C, // 054 JUMP_IF_GTE_ACC A @gte_acc_1
    0x39, // 055 (57)
    0xB6, // 056 HALT
    0x3B, // 057 SET C #45 (@gte_acc_1)
    0x2D, // 058 (45)
    0x5C, // 059 JUMP_IF_GTE_ACC C @halt
    0x4B, // 060 (75)
    0x3A, // 061 SET B #200
    0xC8, // 062 (200)
    0x54, // 063 JUMP_IF_GTE_ACC B @gt_acc
    0x42, // 064 (66)
    0xB6, // 065 HALT
    0x39, // 066 SET A #3 (@gt_acc)
    0x03, // 067 (3)
    0xB1, // 068 JUMP_IF_GT_ACC A @halt
    0x4B, // 069 (75)
    0x3B, // 070 SET C #255
    0xFF, // 071 (255)
    0xB3, // 072 JUMP_IF_GT_ACC C @start
    0x00, // 073 (0)
    0xB6, // 074 HALT
    0xB6  // 075 HALT (@halt)
};

extern const byte num_test_comparisons_data_bytes = 0;

// Needs to be at least 1 byte in this array
extern const byte test_comparisons_data_bytes[] PROGMEM = {
    0x00 // Placeholder.
};

// Max of seven characters
extern const char test_comparisons_program_name[] = "tstcmp";
