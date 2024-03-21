from pathlib import Path

import scanline_wrapper


class Test__get_scanline_cmd:

    def test_default_value(self, monkeypatch):
        monkeypatch.delenv("SCANLINE_CMD", raising=False)
        assert scanline_wrapper._get_scanline_cmd() == "scanline"

    def test_env_overide(self, monkeypatch):
        monkeypatch.setenv("SCANLINE_CMD", "foobar")
        assert scanline_wrapper._get_scanline_cmd() == "foobar"


class Test_list_scanner:

    def test_list_scanner_with_2_scanners(self, monkeypatch):
        monkeypatch.setenv(
            "SCANLINE_CMD",
            (Path(__file__).parent / "mock" / "scanline-list-2-scanners.sh").as_posix(),
        )
        scanners = scanline_wrapper.list_scanners()
        assert len(scanners) == 2
        assert scanners[0] == "HP LaserJet MFP M130fw (XXXXXX)"
        assert scanners[1] == "My Other Scanner"

    def test_list_scanner_with_no_scanners(self, monkeypatch):
        monkeypatch.setenv(
            "SCANLINE_CMD",
            (Path(__file__).parent / "mock" / "scanline-list-0-scanners.sh").as_posix(),
        )
        scanners = scanline_wrapper.list_scanners()
        assert len(scanners) == 0
