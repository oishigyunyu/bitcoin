from helper import hash160, hash256


def op_dup(stack) -> bool:
    if len(stack) < 1:
        return False
    stack.append(stack[-1])
    return True


def op_hash256(stack) -> bool:
    if len(stack) < 1:
        return False
    element = stack.pop()
    stack.append(hash256(element))
    return True


def op_hash160(stack) -> bool:
    if len(stack) < 1:
        return False
    element = stack.pop()
    stack.append(hash160(element))
    return True


OP_CODE_FUNCTIONS: dict = {
    118: op_dup,  # 118=0x78
    170: op_hash256
}
