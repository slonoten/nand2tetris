import sys
from pathlib import Path

from vm_translator.code_builder import CodeBuilder
from vm_translator.parser import parser

def main(src_path: str):
    src_path = Path(src_path)
    tree = parser.parse(src_path.read_text())
    tgt_path = src_path.with_suffix(".asm")
    tgt_path.write_text(CodeBuilder(src_path.stem).transform(tree))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Source file name requered", file=sys.stderr)
    main(sys.argv[1])
