import sys
import zipfile

import pytest
from scripts import build_project_pack


def test_main_builds_zip_from_context(tmp_path, monkeypatch, capsys):
    context_dir = tmp_path / "Context" / "System"
    context_dir.mkdir(parents=True)
    sample_file = context_dir / "sample.md"
    sample_file.write_text("hello\n", encoding="utf-8", newline="\n")

    out_zip = tmp_path / "Project_Pack.zip"

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_project_pack.py",
            "--root",
            "Context",
            "--out",
            str(out_zip),
        ],
    )

    rc = build_project_pack.main()

    assert rc == 0
    assert out_zip.exists()

    with zipfile.ZipFile(out_zip) as zf:
        assert zf.namelist() == ["Context/System/sample.md"]
        assert zf.read("Context/System/sample.md").decode("utf-8") == "hello\n"

    out = capsys.readouterr().out
    assert "Built:" in out
    assert "Project_Pack.zip" in out


def test_main_exits_when_context_root_is_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["build_project_pack.py"])

    with pytest.raises(SystemExit, match="Context root not found: Context"):
        build_project_pack.main()