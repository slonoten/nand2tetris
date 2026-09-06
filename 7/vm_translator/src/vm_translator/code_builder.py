from lark import Transformer


def _push_d() -> str:
    return """@SP
A=M 
M=D
@SP
M=M+1
"""

def _pop_d() -> str:
    return """@SP
M=M-1
A=M
D=M
"""

def segment_to_d(segment: str) -> str:
    if segment == "local":
        return """
    """
    raise NotImplemented("No code for {segment}")


class CodeBuilder                                                                                       (Transformer):
    def push(self, args):
        segment, index = args
        print(segment, index)
        return "push"

    def program(self, commands):
        return "\n".join(map(str, commands))

    