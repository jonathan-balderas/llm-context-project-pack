from datetime import timedelta

from scripts import bump_headers


def test_parse_lastupdated_accepts_date_only():
    dt = bump_headers._parse_lastupdated("2026-03-14")

    assert dt is not None
    assert dt.year == 2026
    assert dt.month == 3
    assert dt.day == 14
    assert dt.tzinfo is None


def test_parse_lastupdated_accepts_iso_z():
    dt = bump_headers._parse_lastupdated("2026-03-14T10:20:30Z")

    assert dt is not None
    assert dt.utcoffset() == timedelta(0)


def test_insertion_index_for_missing_headers_respects_canonical_marker():
    lines = [
        "\n",
        "CHATGPT_CONTEXT_INDEX_CANONICAL\n",
        "\n",
        "Body starts here\n",
    ]

    idx = bump_headers._insertion_index_for_missing_headers(lines)

    assert idx == 3


def test_iter_context_markdown_returns_only_markdown_files(tmp_path):
    context = tmp_path / "Context"
    context.mkdir()
    (context / "a.md").write_text("x", encoding="utf-8")
    (context / "b.txt").write_text("x", encoding="utf-8")
    (context / "nested").mkdir()
    (context / "nested" / "c.md").write_text("x", encoding="utf-8")

    found = list(bump_headers._iter_context_markdown(tmp_path))

    assert found == sorted([context / "a.md", context / "nested" / "c.md"])


def test_bump_file_skips_when_timestamp_is_recent(tmp_path):
    md = tmp_path / "doc.md"
    text = (
        "Version: 3\n"
        "LastUpdated: 2999-01-01T00:00:00+00:00\n"
        "\n"
        "Body\n"
    )
    md.write_text(text, encoding="utf-8")

    changed, message = bump_headers.bump_file(
        path=md,
        date_only=False,
        margin_seconds=2,
        force=False,
        sync_mtime=False,
        dry_run=False,
    )

    assert changed is False
    assert message.startswith("OK (no bump):")


def test_bump_file_dry_run_does_not_modify_file(tmp_path):
    md = tmp_path / "doc.md"
    original = (
        "Version: 1\n"
        "LastUpdated: 2000-01-01T00:00:00+00:00\n"
        "\n"
        "Body\n"
    )
    md.write_text(original, encoding="utf-8")

    changed, message = bump_headers.bump_file(
        path=md,
        date_only=False,
        margin_seconds=0,
        force=False,
        sync_mtime=False,
        dry_run=True,
    )

    assert changed is True
    assert message.startswith("DRY-RUN bump:")
    assert md.read_text(encoding="utf-8") == original


def test_bump_file_updates_existing_headers(tmp_path):
    md = tmp_path / "doc.md"
    md.write_text(
        "Version: 1\n"
        "LastUpdated: 2000-01-01T00:00:00+00:00\n"
        "\n"
        "Body\n",
        encoding="utf-8",
    )

    changed, message = bump_headers.bump_file(
        path=md,
        date_only=False,
        margin_seconds=0,
        force=False,
        sync_mtime=False,
        dry_run=False,
    )

    updated = md.read_text(encoding="utf-8")

    assert changed is True
    assert message.startswith("BUMPED:")
    assert "Version: 2\n" in updated
    assert "LastUpdated:" in updated


def test_bump_file_inserts_missing_headers_and_keeps_version_1(tmp_path):
    md = tmp_path / "doc.md"
    md.write_text("Body only\n", encoding="utf-8", newline="\n")

    changed, message = bump_headers.bump_file(
        path=md,
        date_only=False,
        margin_seconds=0,
        force=False,
        sync_mtime=False,
        dry_run=False,
    )

    updated = md.read_text(encoding="utf-8")

    assert changed is True
    assert message.startswith("BUMPED:")
    assert "Version: 1\n" in updated
    assert "LastUpdated:" in updated
    assert "Body only\n" in updated


def test_bump_file_inserts_after_canonical_marker(tmp_path):
    md = tmp_path / "Context_Index.md"
    md.write_text(
        "CHATGPT_CONTEXT_INDEX_CANONICAL\n"
        "\n"
        "Index body\n",
        encoding="utf-8",
        newline="\n",
    )

    changed, _ = bump_headers.bump_file(
        path=md,
        date_only=False,
        margin_seconds=0,
        force=False,
        sync_mtime=False,
        dry_run=False,
    )

    updated = md.read_text(encoding="utf-8").splitlines()

    assert changed is True
    assert updated[0] == "CHATGPT_CONTEXT_INDEX_CANONICAL"
    assert updated[1] == ""
    assert updated[2].startswith("Version:")
    assert updated[3].startswith("LastUpdated:")