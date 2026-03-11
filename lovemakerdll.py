import sys
import subprocess
import shutil
from pathlib import Path


def extract_love(exe_path: Path, output_path: Path):
    data = exe_path.read_bytes()
    idx = data.find(b"PK\x03\x04")
    if idx == -1:
        raise RuntimeError("ZIP header not found. Not a packaged LÖVE game?")
    output_path.write_bytes(data[idx:])


def main():
    if len(sys.argv) != 2:
        print("usage: python love_rundll32_magic.py <game.exe>")
        sys.exit(1)

    game_exe = Path(sys.argv[1]).resolve()
    if not game_exe.exists():
        print("input exe not found")
        sys.exit(1)

    script_dir = Path(__file__).parent.resolve()
    exe_to_dll = script_dir / "exe_to_dll.exe"

    if not exe_to_dll.exists():
        print("exe_to_dll.exe not found next to this script")
        sys.exit(1)

    work_dir = game_exe.parent
    base = game_exe.stem

    dll_output = work_dir / f"{base}.dll"
    love_output = work_dir / f"{base}.love"
    renamed_love = work_dir / f"{base}.dll,Start"
    bat_file = work_dir / f"run_{base}.bat"

    print("Converting EXE to DLL...")
    subprocess.run([str(exe_to_dll), str(game_exe), str(dll_output)], check=True)

    print("Extracting .love archive...")
    extract_love(game_exe, love_output)

    print("Renaming .love to DLL trick name...")
    if renamed_love.exists():
        renamed_love.unlink()
    love_output.rename(renamed_love)

    print("Copying rundll32.exe...")
    rundll_src = Path(r"C:\Windows\System32\rundll32.exe")
    rundll_dst = work_dir / "rundll32.exe"
    shutil.copy2(rundll_src, rundll_dst)

    print("Creating launcher bat...")
    bat_file.write_text(f".\\rundll32.exe {base}.dll,Start\n")

    print("\nDone.")
    print("Files created:")
    print(dll_output)
    print(renamed_love)
    print(rundll_dst)
    print(bat_file)


if __name__ == "__main__":
    main()