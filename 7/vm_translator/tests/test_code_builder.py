from vm_translator.code_builder import CodeBuilder
from vm_translator.parser import parser

def test_push():
    tree = parser.parse("push constant 1")
    print(CodeBuilder().transform(tree))
    assert False


def test_code_pop():
    tree = parser.parse("pop local 10")
    print(CodeBuilder().transform(tree))
    assert False