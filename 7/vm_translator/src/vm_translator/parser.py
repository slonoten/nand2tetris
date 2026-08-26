from lark import Lark

vm_grammar = r"""
    ?program: command+
    ?command: push
          | pop
          | "add"              -> add
          | "sub"              -> sub
          | "neg"              -> neg
          | "eq"               -> eq
          | "lt"               -> lt
          | "gt"               -> gt
          | "and"              -> and
          | "or"               -> or
          | "not"               -> not

    push : "push" segment index
    pop : "pop" segment index

    segment : SEGMENT
    index : NUMBER

    SEGMENT : /argument|local|static|this|that|pointer/

    %import common.NUMBER
    %import common.WS
    %ignore WS
    """

parser = Lark(vm_grammar, start="program", lexer="basic")
