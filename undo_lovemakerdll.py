import sys
from pathlib import Path


def safe_delete(path: Path):
    if path.exists():
        print(f"Deleting {path}")
        path.unlink()
    else:
        print(f"Skipping (not found): {path}")


def main():
    if len(sys.argv) != 2:
        print("usage: python undo_love_rundll32_magic.py <original_game.exe>")
        sys.exit(1)

    game_exe = Path(sys.argv[1]).resolve()

    if not game_exe.exists():
        print("Original EXE not found.")
        sys.exit(1)

    work_dir = game_exe.parent
    base = game_exe.stem

    dll_file = work_dir / f"{base}.dll"
    fake_love = work_dir / f"{base}.dll,Start"
    bat_file = work_dir / f"run_{base}.bat"
    rundll_copy = work_dir / "rundll32.exe"

    print("Cleaning generated files...\n")

    safe_delete(dll_file)
    safe_delete(fake_love)
    safe_delete(bat_file)

    # only delete rundll32 if it's the copied one in the folder
    if rundll_copy.exists():
        print(f"Deleting {rundll_copy}")
        rundll_copy.unlink()
    else:
        print("Skipping rundll32.exe (not found in folder)")

    print("\nCleanup complete.")


if __name__ == "__main__":
    main()