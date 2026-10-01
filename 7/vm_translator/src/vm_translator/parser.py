from lark import Lark

vm_grammar = r"""
    ?program: command (_NL command)* _NL*
    ?command: comment 
          | push
          | pop
          | function
          | "add"              -> add
          | "sub"              -> sub
          | "neg"              -> neg
          | "eq"               -> eq
          | "lt"               -> lt
          | "gt"               -> gt
          | "and"              -> and_
          | "or"               -> or_
          | "not"              -> not_
          | "return"           -> return_ 

    function: "function" func_name vars_num
    push : "push" segment index
    pop : "pop" segment index

    comment : COMMENT
    ?segment : SEGMENT
    ?index : NUMBER
    ?vars_num: NUMBER
    ?func_name: IDENTIFIER

    IDENTIFIER : /[\w\d]+\.[\w\d]+/
    SEGMENT : /argument|local|static|this|that|pointer|constant|temp/
    COMMENT : /\/\/.*/
 
    %import common.NUMBER
    %import common.WS_INLINE
    %import common.NEWLINE -> _NL
    %ignore WS_INLINE
    """

parser = Lark(vm_grammar, start="program", lexer="basic")
