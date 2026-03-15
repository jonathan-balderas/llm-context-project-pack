from scripts import validate_context


def test_check_headers_passes_when_headers_exist(tmp_path):
    md = tmp_path / "file.md"
    md.write_text(
        "Version: 1\n"
        "LastUpdated: 2026-03-14\n"
        "\n"
        "# Title\n",
        encoding="utf-8",
    )

    assert validate_context.check_headers(md) == []


def test_check_headers_reports_missing_headers(tmp_path):
    md = tmp_path / "file.md"
    md.write_text("# Title\n", encoding="utf-8")

    errs = validate_context.check_headers(md)

    assert len(errs) == 2
    assert "missing Version header" in errs[0]
    assert "missing LastUpdated header" in errs[1]


def test_check_index_passes_for_valid_index(tmp_path):
    index = tmp_path / "Context_Index.md"
    index.write_text(
        "- DocID: SYS-1\n"
        "  FilePath: Context/System/A.md\n"
        "  Owns: A doc\n"
        "\n"
        "- DocID: SYS-2\n"
        "  FilePath: Context/System/B.md\n"
        "  Owns: B doc\n",
        encoding="utf-8",
    )

    assert validate_context.check_index(index) == []


def test_check_index_reports_duplicate_docid_duplicate_path_and_missing_fields(tmp_path):
    index = tmp_path / "Context_Index.md"
    index.write_text(
        "- DocID: SYS-1\n"
        "  FilePath: Context/System/A.md\n"
        "  Owns: A doc\n"
        "\n"
        "- DocID: SYS-1\n"
        "  FilePath: Context/System/B.md\n"
        "\n"
        "- DocID: SYS-2\n"
        "  FilePath: Context/System/A.md\n"
        "  Owns: Duplicate path\n"
        "\n"
        "- DocID: SYS-3\n"
        "  Owns: Missing filepath\n",
        encoding="utf-8",
    )

    errs = validate_context.check_index(index)

    assert any("duplicate DocID SYS-1" in e for e in errs)
    assert any("DocID SYS-1 missing Owns:" in e for e in errs)
    assert any("duplicate FilePath Context/System/A.md" in e for e in errs)
    assert any("DocID SYS-3 missing FilePath" in e for e in errs)


def test_main_returns_2_when_context_folder_is_missing(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    rc = validate_context.main()

    assert rc == 2
    out = capsys.readouterr().out
    assert "ERROR: Context/ not found" in out


def test_main_returns_0_for_valid_context(tmp_path, monkeypatch, capsys):
    context_dir = tmp_path / "Context" / "System"
    context_dir.mkdir(parents=True)

    index = context_dir / "Context_Index.md"
    index.write_text(
        "Version: 1\n"
        "LastUpdated: 2026-03-14\n"
        "\n"
        "- DocID: SYS-1\n"
        "  FilePath: Context/System/Context_Index.md\n"
        "  Owns: Canonical index\n",
        encoding="utf-8",
    )

    other_md = tmp_path / "Context" / "Guide.md"
    other_md.write_text(
        "Version: 1\n"
        "LastUpdated: 2026-03-14\n"
        "\n"
        "Guide body\n",
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)

    rc = validate_context.main()

    assert rc == 0
    out = capsys.readouterr().out
    assert "Validation OK." in out


def test_main_returns_1_when_validation_fails(tmp_path, monkeypatch, capsys):
    context_dir = tmp_path / "Context" / "System"
    context_dir.mkdir(parents=True)

    bad_index = context_dir / "Context_Index.md"
    bad_index.write_text(
        "- DocID: SYS-1\n"
        "  FilePath: Context/System/Context_Index.md\n",
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)

    rc = validate_context.main()

    assert rc == 1
    out = capsys.readouterr().out
    assert "Validation failed:" in out