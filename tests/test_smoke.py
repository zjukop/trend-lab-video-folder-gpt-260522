from pathlib import Path

from video_folder_gpt.main import answer, index_folder


def test_index_and_answer(tmp_path: Path) -> None:
    videos = tmp_path / "videos"
    videos.mkdir()
    (videos / "zoom-demo.mp4").write_bytes(b"fake video")
    db = tmp_path / "index.sqlite3"

    assert index_folder(videos, db) == 1
    result = answer("zoom", db)

    assert "zoom demo" in result
    assert "00:00" in result
