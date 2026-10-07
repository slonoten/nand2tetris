import sys
from pathlib import Path

from vm_translator.code_builder import CodeBuilder
from vm_translator.parser import parser

def translate(src_path: Path) -> str:
    print(f"Translating \"{src_path.name}\"...")
    tree = parser.parse(src_path.read_text())
    return CodeBuilder(src_path.stem).transform(tree) 


def main(src_path: str):
    src_path = Path(src_path)
    if src_path.is_dir():
        vm_paths = [*src_path.glob("*.vm")]
        if "Sys.vm" not in [path.name for path in vm_paths]:
            raise RuntimeError("Sys.vm not found")
        asm_sources = [translate(vm_path) for vm_path in src_path.glob("*.vm")]            
        (src_path / src_path.name).with_suffix(".asm").write_text("\n".join(asm_sources))
    else:
        src_path.with_suffix(".asm").write_text(translate(src_path))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Source file name requered", file=sys.stderr)
    main(sys.argv[1])
