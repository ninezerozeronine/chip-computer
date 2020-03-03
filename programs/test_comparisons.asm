// Tests that the comparison operators work

@start
    SET ACC #84
    SET A #84
    JUMP_IF_EQ_ACC A @eq_zero
    HALT

@eq_zero
    SET_ZERO B
    JUMP_IF_EQ_ZERO B @lt_acc
    HALT

@lt_acc
    SET C #52
    JUMP_IF_LT_ACC C @lte_acc_0
    HALT

@lte_acc_0
    SET SP #84
    JUMP_IF_LTE_ACC SP @lte_acc_1
    HALT

@lte_acc_1
    SET A #4
    JUMP_IF_LTE_ACC A @gte_acc_0
    HALT

@gte_acc_0
    SET ACC #150
    SET A #150
    JUMP_IF_GTE_ACC A @gte_acc_1
    HALT

@gte_acc_1
    SET B #200
    JUMP_IF_GTE_ACC B @gt_acc
    HALT

@gt_acc
    SET C #255
    JUMP_IF_GT_ACC C @start
    HALT