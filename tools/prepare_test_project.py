"""Make an isolated Ren'Py project; --savedir alone also writes game/saves."""
from pathlib import Path
import os
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
destination = Path(sys.argv[1]).resolve()
assert destination.is_relative_to(ROOT / "tests/rebuild"), destination
assert not destination.exists(), "Use a fresh runner directory"
for source in (ROOT / "game").rglob("*"):
    relative = source.relative_to(ROOT / "game")
    if not source.is_file() or any(part in ("cache", "saves") for part in relative.parts):
        continue
    if source.suffix == ".rpyc" or source.name in ("log.txt", "traceback.txt", "errors.txt"):
        continue
    target = destination / "game" / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    if relative.parts[0] in ("images", "audio"):
        os.link(source, target)
    else:
        shutil.copy2(source, target)
override = destination / "game/test_save_namespace.rpy"
override.write_text('init 100 python:\n    config.save_directory = "FPTCommitRebuildTests"\n', encoding="utf-8")
print(destination)
