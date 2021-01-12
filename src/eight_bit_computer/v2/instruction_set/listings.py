from .instruction_components import (
    NOOP,
    LOAD,
    STORE,
    A,
    M_A,
    M_CONST
)

INSTRUCTION_SIGNATURES = set(
    (NOOP,),
    (LOAD, M_CONST, A),
    (STORE, A, M_CONST),
    (ADD, M_A),
    (ADD, A)
)


def get_instruction_byte_val(instruction):
    pass



_FUNC_MAPPING = None
# Need a unit test to make sure these template functions don't double up
def get_template_function(signature):
    global _FUNC_MAPPING
    if _FUNC_MAPPING is None:
        for operation in all_operations:
            template_func = operation.get_template_function(signature)
            if template_func is not None:
                _FUNC_MAPPING[signature] = template_func
                break
    return _FUNC_MAPPING[signature]
                    

