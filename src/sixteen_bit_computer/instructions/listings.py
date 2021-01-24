from .components import (
    A,
    ADD,
    CONST,
    LOAD,
    M_A,
    M_CONST,
    NOOP,
    STORE,
)

INSTRUCTION_SIGNATURES = frozenset([
    (ADD, A),
    (ADD, CONST),
    (ADD, M_A),
    (ADD, M_CONST),
    (LOAD, M_CONST, A),
    (NOOP,),
    (STORE, A, M_CONST),
])


def get_instruction_byte_val(signature):
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
    if signature not in _FUNC_MAPPING:
        raise
    return _FUNC_MAPPING[signature]
                    

