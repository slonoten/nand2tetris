from lark import Lark

vm_grammar = r"""
    ?program: line (_NL line)* _NL*
    ?line : command comment? | comment?
    ?command: push
          | pop
          | function
          | call
          | label
          | goto
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

    push : "push" segment index
    pop : "pop" segment index
    function: "function" func_name vars_num
    call: "call" func_name args_num
    label: "label" label_name
    goto: "goto" label_name

    comment : COMMENT
    ?segment : SEGMENT
    ?index : NUMBER
    ?vars_num: NUMBER
    ?args_num: NUMBER
    ?func_name: IDENTIFIER
    ?label_name: IDENTIFIER

    IDENTIFIER : /[A-Za-z][\w\d\$_\.]*/
    SEGMENT.1 : /argument|local|static|this|that|pointer|constant|temp/
    COMMENT : /\/\/.*/
 
    %import common.NUMBER
    %import common.WS_INLINE
    %import common.NEWLINE -> _NL
    %ignore WS_INLINE
    """

parser = Lark(vm_grammar, start="program", lexer="basic")
