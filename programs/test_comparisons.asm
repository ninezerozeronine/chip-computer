// Tests that the comparison operators work

@start
    SET ACC #84
    SET B #32
    JUMP_IF_EQ_ACC B @halt
    SET A #84
    JUMP_IF_EQ_ACC A @eq_zero
    HALT

@eq_zero
    SET A #-1
    JUMP_IF_EQ_ZERO A @halt
    SET_ZERO B
    JUMP_IF_EQ_ZERO B @lt_acc
    HALT

@lt_acc
    SET A #100
    JUMP_IF_LT_ACC A @halt
    SET C #52
    JUMP_IF_LT_ACC C @lte_acc_0
    HALT

@lte_acc_0
    SET B #123
    JUMP_IF_LTE_ACC B @halt
    SET SP #84
    JUMP_IF_LTE_ACC SP @lte_acc_1
    HALT

@lte_acc_1
    SET C #201
    JUMP_IF_LTE_ACC C @halt
    SET A #4
    JUMP_IF_LTE_ACC A @gte_acc_0
    HALT

@gte_acc_0
    SET ACC #150
    SET B #15
    JUMP_IF_GTE_ACC B @halt
    SET A #150
    JUMP_IF_GTE_ACC A @gte_acc_1
    HALT

@gte_acc_1
    SET C #45
    JUMP_IF_GTE_ACC C @halt
    SET B #200
    JUMP_IF_GTE_ACC B @gt_acc
    HALT

@gt_acc
    SET A #3
    JUMP_IF_GT_ACC A @halt
    SET C #255
    JUMP_IF_GT_ACC C @start
    HALT

@halt
    HALT